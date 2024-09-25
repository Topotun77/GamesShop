from .models import *
from hashlib import sha1
from django.http import HttpRequest


bsk_list: list[BasketItem] = []
cnt_choice = 5
day_team = True
user_login = None


def get_day_team():
    global day_team
    return day_team


def set_day_team(team=None):
    global day_team
    if team is None:
        day_team = not day_team
    else:
        day_team = team


def check_team(request: HttpRequest):
    if request.method == 'GET':
        day = request.GET.get('day')
        if not (day is None):
            set_day_team()


def get_basket_count(lst: list[BasketItem]):
    return len(lst)


def get_user_login():
    if user_login:
        user_login.balance = Buyer.objects.get(name=user_login.name).balance
    return user_login


def get_bsk_list():
    return bsk_list


def add_field_in_context() -> dict:
    global bsk_list
    get_user_login()
    res: dict = {'basket_len': get_basket_count(bsk_list),
                 'day_team': get_day_team(),
                 'user': user_login,
                 }
    if user_login:
        res = {**res,
               'user_login': user_login.name,
               'balance': user_login.balance,
               }

    return res


def basket_sum(lst: list[BasketItem]) -> float:
    """
    Сумма всех товаров в корзине lst
    """
    sum = 0
    for item in lst:
        # if item.checked == 'checked':
        sum += item.sum
    return sum


def del_basket(lst: list[BasketItem]) -> int:
    """
    Удалить из глобальной корзины bsk_list позиции из списка lst
    :return: Количество удаленных позиций
    """
    global bsk_list
    count = 0
    for item in lst:
        try:
            bsk_list.remove(item)
            count += 1
        except:
            pass
    print(bsk_list)  # TODO delete its
    return count


def bay_basket(lst: list[BasketItem]):
    """
    Производит покупку, очищает корзину, меняет баланс клиента и
    сопоставляет игру и клиента в базе
    :param lst: список выбранных покупок
    :return: остаток на счете клиента и ошибку
    """
    global bsk_list, user_login
    sum_, err = 0, {}
    for item in lst:
        if not item.age_limited or user_login.age > 17:
            sum_ += item.cost * item.count
            buyers = Game.objects.get(title=str(item)).buyer.filter()
            buyer_lst = []
            for buyer in buyers:
                buyer_lst.append(buyer.id)
            buyer_lst.append(user_login.id)
            Game.objects.get(title=str(item)).buyer.set(tuple(buyer_lst))
            # buyers.set(tuple(buyer_lst))
            bsk_list.remove(item)
        else:
            err = {'message': "Некоторые товары вы не можете купить, т.к. они 18+"}
    return sum_, err


def chk_inc_product_in_basket(product: str, inc: int = 1) -> bool:
    """
    Проверить товар в корзине и увеличить количество на inc
    :param product: Наименование товара (title)
    :param inc: На сколько увеличим кол-во товара (м.б. 0, тогда просто проверка наличия товара в корзине)
    :return: bool Наличие товара - True - товар есть в корзине False - в противном случае
    """
    global bsk_list
    for item in bsk_list:
        if product == str(item):
            item.count += inc
            return True
    game = Game.objects.get(title=product)
    bsk_list.append(BasketItem(product, cost=game.cost, age_limited=game.age_limited))
    return False


def check_field(username, password, repeat_password, age, subscribe) -> dict:
    """
    Проверяет на ошибки ввод данных и добавляет нового пользователя в случае отсутствия ошибок
    :return: dict - словарь ошибок и ответных сообщений
    """
    users = Buyer.objects.all()
    print(username, password, repeat_password, age, subscribe, users)  # TODO delete print
    info: dict = {}
    if username != 'Anonymous':
        for usr in users:
            if usr.name == username:
                info = {**info, 'error': 'The user already exists',
                        'error_rus': 'Пользователь уже существует'}
                return info
        if password != repeat_password:
            info = {**info, 'error': "Passwords don't match",
                    'error_rus': 'Пароли не совпадают'}
            return info
        try:
            int(age)
        except ValueError:
            info = {**info, 'error': 'The age must be an integer',
                    'error_rus': 'Возраст должен быть целым числом'}
            return info
        Buyer.objects.create(name=username, balance=10, age=age, password=password)
        # users.append(User(username, password, age, subscribe))
        usr = Buyer.objects.get(name=username)
        global user_login
        user_login = usr
        info = {**info,
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
                info = {**info, 'error': 'Invalid username and password',
                        'error_rus': 'Неверные имя пользователя и пароль'}
                return info
            user_login = usr
            info = {**info, 'user_login': user_login.name,
                    'message': f'Приветствуем, {username}'}
            return info
    info = {**info, 'error': 'Invalid username and password',
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
