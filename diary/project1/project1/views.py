import datetime
from project1.calendar_help import (
    months,
    years
)

from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config

from sqlalchemy.exc import DBAPIError
from pyramid.renderers import render_to_response

import transaction

from .models import (
    DBSession,
    MyModel,
    User,
    Articles,
    ArticlesTypes,
    CurrentDate
    )

from pyramid.security import (
    remember,
    forget,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    if 'commit' in request.params:
        try:
            user_login = request.params['login']
            user_password = request.params['password']
            user = DBSession.query(User).filter(User.login == user_login).all()
            if user:
                if user[0].password == user_password:
                    headers = remember(request, user[0].id)
                    return HTTPFound(location='/home', headers = headers)
        except:
            return {}
    return {}

@view_config(route_name='logout')
def logout(request):
    DBSession.query(CurrentDate).delete()
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)

@view_config(route_name='createAccount', renderer='templates/CreateAccount.jinja2')
def createAccount(request):
    if 'commit' in request.params and 'login' in request.params and 'password' in request.params:
        user_login = request.params['login']
        user_password = request.params['password']
        if user_login != '' and user_password != '':
            users = DBSession.query(User).filter(User.login == user_login).all()
            if users:
                return {}
            else:
                user = User(login=user_login, password=user_password)
                DBSession.add(user)
                return HTTPFound(location='/')
    return {}

@view_config(route_name='home', renderer='templates/Calendar.jinja2', permission='view')
def my_view(request):
    if 'year_num' in request.params and 'month_num' in request.params and 'day_num' in request.params:
        year = request.params['year_num']
        month = request.params['month_num']
        day = request.params['day_num']
        try:
            current_date = CurrentDate(date = datetime.date(years[int(year)],int(month),int(day)))
            DBSession.add(current_date)
            return HTTPFound(location='/day')
        except:
            return {'login':DBSession.query(User).filter(User.id == request.authenticated_userid).first().login}
    else:
        return {'login':DBSession.query(User).filter(User.id == request.authenticated_userid).first().login}

@view_config(route_name='openday', renderer='templates/Day.jinja2', permission='view')
def open_day(request):
    current_day = DBSession.query(CurrentDate).filter().all()[-1]
    user = DBSession.query(User).filter(User.id == request.authenticated_userid).first()
    return {'login':user.login, 'day':current_day.date.day,
            'month': months[current_day.date.month], 'year': current_day.date.year}

def get_text_view(article_type_name, request):
    current_date = DBSession.query(CurrentDate).filter().all()[-1]
    user = DBSession.query(User).filter(User.id == request.authenticated_userid).first()
    article_type = DBSession.query(ArticlesTypes).filter(ArticlesTypes.name == article_type_name).first()
    articles = DBSession.query(Articles).filter(Articles.date == current_date.date)\
        .filter(Articles.user_id == request.authenticated_userid)\
        .filter(Articles.type_id == article_type.id)
    try:
        return {'text': articles[-1].text, 'login':user.login, 'day':current_date.date.day,
                'month': months[current_date.date.month],
                'year': current_date.date.year}
    except:
        return {'text': '', 'login':user.login, 'day': current_date.date.day,
                'month': months[current_date.date.month],
                'year': current_date.date.year}


@view_config(route_name='feeling', renderer='templates/Feeling.jinja2', permission='view')
def feeling_view(request):
    return get_text_view('Самочувствие', request)

@view_config(route_name='mood', renderer='templates/Mood.jinja2', permission='view')
def mood_view(request):
    return get_text_view('Настроение', request)

@view_config(route_name='today', renderer='templates/Today.jinja2', permission='view')
def today_view(request):
    return get_text_view('Сегодня', request)

@view_config(route_name='good', renderer='templates/Good.jinja2', permission='view')
def good_view(request):
    return get_text_view('Хорошее', request)

@view_config(route_name='bad', renderer='templates/Bad.jinja2', permission='view')
def bad_view(request):
    return get_text_view('Плохое', request)

@view_config(route_name='save', permission='view')
def save(request):
    if 'text' in request.params and 'articleType' in request.params:
        text = request.params['text']
        articleType = DBSession.query(ArticlesTypes).filter(ArticlesTypes.name == request.params['articleType']).first()
        current_date = DBSession.query(CurrentDate).filter().all()[-1]
        user_id = request.authenticated_userid
        DBSession.query(Articles).filter(Articles.date == current_date.date)\
            .filter(Articles.user_id == request.authenticated_userid)\
            .filter(Articles.type_id == articleType.id).delete()
        if articleType:
            article = Articles(text = text, date = current_date.date, user_id = user_id, type_id = articleType.id)
            DBSession.add(article)
            return HTTPFound(location='/day')
        else:
            return HTTPFound(location='/')
    else:
        return HTTPFound(location='/')

@view_config(route_name='like', renderer='templates/Like.jinja2', permission='view')
def like_view(request):
    return get_text_view('Нравится', request)

@view_config(route_name='hate', renderer='templates/Hate.jinja2', permission='view')
def hate_view(request):
    return get_text_view('Ненавижу', request)

@view_config(route_name='time', renderer='templates/Time.jinja2', permission='view')
def time_view(request):
    return get_text_view('Куда ушло время', request)

@view_config(route_name='moneyPlus', renderer='templates/MoneyPlus.jinja2', permission='view')
def moneyPlus_view(request):
    return get_text_view('Деньги +', request)

@view_config(route_name='moneyMinus', renderer='templates/MoneyMinus.jinja2', permission='view')
def moneyMinus_view(request):
    return get_text_view('Деньги -', request)

@view_config(route_name='quote', renderer='templates/Quote.jinja2', permission='view')
def quote_view(request):
    return get_text_view('Цитата дня', request)

@view_config(route_name='dream', renderer='templates/Dream.jinja2', permission='view')
def dream_view(request):
    return get_text_view('Сон', request)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_project1_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

