from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import UserRegister
from .models import *

# Create your views here.

basket_: dict = {}


def get_basket_count():
    return len(basket_)


def shop(request: HttpRequest):
    if request.method == 'POST':
        product = request.POST.get('product')
        if product in basket_.keys():
            basket_[product] += 1
        else:
            basket_[product] = 1
    print(basket_, len(basket_))

    games = Game.objects.all()
    context = {
        'items': games,
        'basket_len': get_basket_count(),
    }
    return render(request, template_name='shop.html', context=context)


def basket(request: HttpRequest):
    global basket_
    if request.method == 'POST':
        basket_ = {}
    print(basket_, get_basket_count())
    context = {
        'basket_len': get_basket_count(),
        'basket_': basket_,
    }
    return render(request, template_name='basket.html', context=context)


# class User():
#     def __init__(self, username, password, age, subscribe):
#         self.username = username
#         self.password = password
#         self.age = age
#         self.subscribe = subscribe
#
#
# users = [
#     User('Alex', '12345678', 22, False),
#     User('Pasha', 'Da$f8k@a8n!Rx~54Bzs*3}a', 39, False),
#     User('Rosa', '111', 51, True),
# ]


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
        Buyer.objects.create(name=username, balance=10, age=age)
        # users.append(User(username, password, age, subscribe))
    info = {'message': f'Приветствуем, {username}'}
    print(users)
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
    password = req.get('password', None)
    repeat_password = req.get('repeat_password', None)
    age = req.get('age', 18)
    subscribe = req.get('subscribe') == 'on'
    info = check_field(username, password, repeat_password, age, subscribe)
    return info


def sign_up_by_html(request: HttpRequest):
    info = read_field(request, request.method)  # Считываем поля по методу POST
    status = 400 if 'error' in info else 200
    info = {
        **info,
        'basket_len': get_basket_count(),
    }
    return render(request, template_name='registration_page.html', context=info, status=status)


def sign_up_by_django(request: HttpRequest):
    info: dict = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            subscribe = form.cleaned_data['subscribe']
            info = check_field(username, password, repeat_password, age, subscribe)
    else:
        form = UserRegister()
    info['form'] = form
    info = {
        **info,
        'basket_len': get_basket_count(),
    }
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
