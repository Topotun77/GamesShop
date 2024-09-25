from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
# from rest_framework import generics
from .forms import UserRegister
from .models import *
from .crud_func import *

# Create your views here.


def start(request: HttpRequest):
    check_team(request)
    context = add_field_in_context()
    return render(request, template_name='start_template.html', context=context)


def shop(request: HttpRequest):
    check_team(request)
    if request.method == 'POST':
        product = request.POST.get('product')
        chk_inc_product_in_basket(product)
    global cnt_choice
    cnt = request.GET.get('cnt', cnt_choice)
    if int(cnt) == 0:
        cnt = cnt_choice
    cnt_choice = cnt
    games = Game.objects.all().order_by('cost')
    paginator = Paginator(games, cnt)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = add_field_in_context()
    context = {
        **context,
        'items': games,
        'page_obj': page_obj,
    }
    return render(request, template_name='shop.html', context=context)


def basket(request: HttpRequest):
    check_team(request)
    # user_login = get_user_login()
    bsk_list = get_bsk_list()
    context = add_field_in_context()
    user_login = context['user']
    bsk_sum = basket_sum(bsk_list)

    if request.method == 'POST':
        bay_list: list[BasketItem] = []
        for item in bsk_list:
            item.checked = ''
            game = request.POST.get(str(item))
            if game:
                item.checked = 'checked'
                bay_list.append(item)
        bsk_sum = basket_sum(bay_list)
        act = request.POST.get('act')
        if act == 'del':
            del_basket(bay_list)
            bsk_list_ = get_bsk_list()
            # bsk_sum = basket_sum(bsk_list_)
        elif act == 'bay':
            if user_login:
                if user_login.balance - bsk_sum > 0:
                    balance, err = bay_basket(bay_list)
                    context.update(err)
                    user_login.balance = user_login.balance - balance
                    Buyer.objects.filter(id=user_login.id).update(balance=user_login.balance)
                    context['balance'] = user_login.balance
                else:
                    context = {**context, 'message': "У вас нет денег!!! Пополните баланс!"}
            else:
                context = {**context, 'message': "Для оплаты покупки, пожалуйста, войдите в свой аккаунт"}
        else:
            pass
    bsk_sum = basket_sum(get_bsk_list())
    context['basket_'] = bsk_list
    context['basket_sum'] = bsk_sum
    context['basket_len'] = get_basket_count(bsk_list)
    # get_user_login()
    return render(request, template_name='basket.html', context=context)


def login(request: HttpRequest):
    check_team(request)
    info = read_field_login(request, request.method)  # Считываем поля по методу POST
    status = 400 if 'error' in info else 200
    info.update(add_field_in_context())
    return render(request, template_name='login.html', context=info, status=status)


def sign_up_by_html(request: HttpRequest):
    check_team(request)
    info = read_field(request, request.method)  # Считываем поля по методу POST
    status = 400 if 'error' in info else 200
    info.update(add_field_in_context())
    return render(request, template_name='registration_page.html', context=info, status=status)


def sign_up_by_django(request: HttpRequest):
    check_team(request)
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
    }
    info.update(add_field_in_context())
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
