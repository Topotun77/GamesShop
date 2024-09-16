from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import UserRegister
from .models import *
from hashlib import sha1

# Create your views here.

basket_: dict = {}
cnt_choice = 5
user_login = None


def get_basket_count():
    return len(basket_)


def bay_basket(bay_list: dict):
    """
    Производит покупку, очищает корзину, меняет баланс клиента и
    сопоставляет игру и клиента в базе
    :param bay_list: список выбранных покупок
    :return: остаток на счете клиента и ошибку
    """
    global basket_, user_login
    sum_, err = 0, {}
    for k, v in bay_list.items():
        game = Game.objects.get(title=k)
        if not game.age_limited or user_login.age > 17:
            sum_ += game.cost * v
            buyers = Game.objects.get(id=game.id).buyer.filter()
            buyer_lst = []
            for buyer in buyers:
                buyer_lst.append(buyer.id)
            buyer_lst.append(user_login.id)
            Game.objects.get(id=game.id).buyer.set(tuple(buyer_lst))
            del basket_[k]
        else:
            err = {'message': "Некоторые товары вы не можете купить, т.к. они 18+"}
    return sum_, err


def del_basket(del_list: dict):
    for k, v in del_list.items():
        del basket_[k]


def shop(request: HttpRequest):
    if request.method == 'POST':
        product = request.POST.get('product')
        if product in basket_.keys():
            basket_[product] += 1
        else:
            basket_[product] = 1

    global cnt_choice
    cnt = request.GET.get('cnt', cnt_choice)
    if int(cnt) == 0:
        cnt = cnt_choice
    cnt_choice = cnt
    games = Game.objects.all().order_by('cost')
    paginator = Paginator(games, cnt)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'items': games,
        'basket_len': get_basket_count(),
        'page_obj': page_obj,
    }
    global user_login
    if user_login:
        context = {
            **context,
            'user_login': user_login.name,
            'balance': user_login.balance}
    return render(request, template_name='shop.html', context=context)


def basket(request: HttpRequest):
    global basket_, user_login
    context: dict = {}

    if request.method == 'POST':
        bay_list: dict = {}
        for k, v in basket_.items():
            game = request.POST.get(k)
            if game:
                bay_list[k] = v
        act = request.POST.get('act')
        if act == 'del':
            del_basket(bay_list)
        else:
            if user_login:
                if user_login.balance > 0:
                    balance, context = bay_basket(bay_list)
                    balance = user_login.balance - balance
                    Buyer.objects.filter(id=user_login.id).update(balance=balance)
                    user_login.balance = balance
                else:
                    context = {'message': "У вас нет денег!!! Пополните баланс!"}
            else:
                context = {'message': "Для оплаты покупки, пожалуйста, войдите в свой аккаунт"}
    print(context)
    context['basket_len'] = get_basket_count()
    context['basket_'] = basket_
    if user_login:
        context = {
            **context,
            'user_login': user_login.name,
            'balance': user_login.balance}
    return render(request, template_name='basket.html', context=context)


def check_field(username, password, repeat_password, age, subscribe) -> dict:
    """
    Проверяет на ошибки ввод данных и добавляет нового пользователя в случае отсутствия ошибок
    :return: dict - словарь ошибок и ответных сообщений
    """
    users = Buyer.objects.all()
    print(username, password, repeat_password, age, subscribe, users)
    info: dict = {}
    if username != 'Anonymous':
        for usr in users:
            if usr.name == username:
                info = {'error': 'The user already exists',
                        'error_rus': 'Пользователь уже существует'}
                return info
        if password != repeat_password:
            info = {'error': "Passwords don't match",
                    'error_rus': 'Пароли не совпадают'}
            return info
        try:
            int(age)
        except ValueError:
            info = {'error': 'The age must be an integer',
                    'error_rus': 'Возраст должен быть целым числом'}
            return info
        Buyer.objects.create(name=username, balance=10, age=age, password=password)
        # users.append(User(username, password, age, subscribe))
        usr = Buyer.objects.get(name=username)
        global user_login
        user_login = usr
        info = {**info,
                'user_login': user_login.name,
                'message': f'Приветствуем, {username}'}
    return info


def read_field_login(request: HttpRequest, method='POST') -> dict:
    """
    Чтение полей из POST-запроса
    :param request: Запрос
    :param method: Метод передачи данных 'GET' или 'POST'
    :return: dict - словарь ошибок и ответных сообщений
    """
    info: dict = {}
    global user_login
    if method == 'GET':
        info = {'error': 'Login was denied',
                'error_rus': 'Введите корректно имя пользователя и пароль'}
        return info
    req = request.POST
    username = req.get('username', 'Anonymous')
    logout = req.get('logout', 'NO')
    password = sha1(str(req.get('password', None)).encode()).hexdigest()
    if logout == 'OK':
        info = {'message': f'Пользователь {user_login.name} вышел из системы.'}
        user_login = None
        return info
    if username == 'Anonymous':
        info = {'error': 'Anonymous access is denied',
                'error_rus': 'Невозможно войти в систему анонимным пользователем.'}
        return info
    users = Buyer.objects.all()
    for usr in users:
        if usr.name == username:
            if usr.password != str(password):
                print(usr.password, password, usr)
                info = {'error': 'Invalid username and password',
                        'error_rus': 'Неверные имя пользователя и пароль'}
                return info
            user_login = usr
            info = {**info, 'user_login': user_login.name,
                    'message': f'Приветствуем, {username}'}
            return info
    info = {'error': 'Invalid username and password',
            'error_rus': 'Неверные имя пользователя и пароль'}
    return info


def read_field(request: HttpRequest, method='GET') -> dict:
    """
    Чтение полей из GET-запроса или HTML-формы (POST-запроса)
    :param request: Запрос
    :param method: Метод передачи данных 'GET' или 'POST'
    :return: dict - словарь ошибок и ответных сообщений
    """
    if method == 'GET':
        req = request.GET
    else:
        req = request.POST
    username = req.get('username', 'Anonymous')
    password = sha1(str(req.get('password', None)).encode()).hexdigest()
    repeat_password = sha1(str(req.get('repeat_password', None)).encode()).hexdigest()
    age = req.get('age', 18)
    subscribe = req.get('subscribe') == 'on'
    info = check_field(username, password, repeat_password, age, subscribe)
    return info


def login(request: HttpRequest):
    info = read_field_login(request, request.method)  # Считываем поля по методу POST
    status = 400 if 'error' in info else 200
    info = {
        **info,
        'basket_len': get_basket_count(),
    }
    global user_login
    if user_login:
        info['user_login'] = user_login.name
        info['balance'] = user_login.balance
    return render(request, template_name='login.html', context=info, status=status)


def sign_up_by_html(request: HttpRequest):
    info = read_field(request, request.method)  # Считываем поля по методу POST
    status = 400 if 'error' in info else 200
    info = {
        **info,
        'basket_len': get_basket_count(),
    }
    global user_login
    if user_login:
        info['user_login'] = user_login.name
        info['balance'] = user_login.balance
    return render(request, template_name='registration_page.html', context=info, status=status)


def sign_up_by_django(request: HttpRequest):
    info: dict = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = sha1(str(form.cleaned_data['password']).encode()).hexdigest()
            repeat_password = sha1(str(form.cleaned_data['repeat_password']).encode()).hexdigest()
            age = form.cleaned_data['age']
            subscribe = form.cleaned_data['subscribe']
            info = check_field(username, password, repeat_password, age, subscribe)
        else:
            info = {'error': 'Form is invalid',
                    'error_rus': 'Форма заполнена с ошибками'}
    else:
        form = UserRegister()
    info = {
        **info,
        'form': form,
        'basket_len': get_basket_count(),
    }
    global user_login
    if user_login:
        info['user_login'] = user_login.name
        info['balance'] = user_login.balance
    status = 400 if 'error' in info else 200
    return render(request, template_name='registration_page.html', context=info, status=status)


def sign_up_url(request: HttpRequest):
    info = read_field(request, request.method)  # Считываем поля по методу GET
    if 'error' in info:
        status = 400
        reason = info['error']
    else:
        status = 200
        reason = None
    return HttpResponse(str(info), status=status, reason=reason)
