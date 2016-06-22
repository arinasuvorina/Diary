import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    MyModel,
    Base,
    ArticlesTypes,
    User,
    Articles
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = MyModel(name='one', value=1)
        DBSession.add(model)

        type_bad = ArticlesTypes(name='Плохое')
        DBSession.add(type_bad)
        type_good = ArticlesTypes(name='Хорошее')
        DBSession.add(type_good)
        type_today = ArticlesTypes(name='Сегодня')
        DBSession.add(type_today)
        type_feeling = ArticlesTypes(name='Самочувствие')
        DBSession.add(type_feeling)
        type_mood = ArticlesTypes(name='Настроение')
        DBSession.add(type_mood)
        type_like= ArticlesTypes(name='Нравится')
        DBSession.add(type_like)
        type_hate = ArticlesTypes(name='Ненавижу')
        DBSession.add(type_hate)
        type_time = ArticlesTypes(name='Куда ушло время')
        DBSession.add(type_time)
        type_moneyPlus = ArticlesTypes(name='Деньги +')
        DBSession.add(type_moneyPlus)
        type_moneyMinus = ArticlesTypes(name='Деньги -')
        DBSession.add(type_moneyMinus)
        type_quote = ArticlesTypes(name='Цитата дня')
        DBSession.add(type_quote)
        type_dream = ArticlesTypes(name='Сон')
        DBSession.add(type_dream)

        user1 = User(login='user1', password='1')
        DBSession.add(user1)
        user2 = User(login='user2', password='2')
        DBSession.add(user2)

        article_today_user1 = Articles(text='Сегодня у меня День Рождения',
                                       date=datetime.date(2016, 3, 15),
                                       user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                       type_id=DBSession.query(ArticlesTypes)
                                       .filter(ArticlesTypes.name == 'Сегодня').first().id)
        DBSession.add(article_today_user1)

        article_good_user1 = Articles(text='Много подарков',
                                      date=datetime.date(2016, 3, 15),
                                      user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                      type_id=DBSession.query(ArticlesTypes)
                                      .filter(ArticlesTypes.name == 'Хорошее').first().id)
        DBSession.add(article_good_user1)

        article_bad_user1 = Articles(text='На улице очень холодно',
                                     date=datetime.date(2016, 3, 15),
                                     user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                     type_id=DBSession.query(ArticlesTypes)
                                     .filter(ArticlesTypes.name == 'Плохое').first().id)
        DBSession.add(article_bad_user1)

        article_feeling_user1 = Articles(
            text='Горло не болит, и насморк исчез. Наконец-то выздоровел.',
            date=datetime.date(2016, 3, 15),
            user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
            type_id=DBSession.query(ArticlesTypes)
                .filter(ArticlesTypes.name == 'Самочувствие').first().id)
        DBSession.add(article_feeling_user1)

        article_mood_user1 = Articles(text='Радостное',
                                      date=datetime.date(2016, 3, 15),
                                      user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                      type_id=DBSession.query(ArticlesTypes)
                                      .filter(ArticlesTypes.name == 'Настроение').first().id)
        DBSession.add(article_mood_user1)

        article_like_user1 = Articles(text='Когда близкие люди рядом',
                                      date=datetime.date(2016, 3, 15),
                                      user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                      type_id=DBSession.query(ArticlesTypes)
                                      .filter(ArticlesTypes.name == 'Нравится').first().id)
        DBSession.add(article_like_user1)

        article_time_user1 = Articles(text='Весь день готовлю угощения для друзей',
                                      date=datetime.date(2016, 3, 15),
                                      user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                      type_id=DBSession.query(ArticlesTypes)
                                      .filter(ArticlesTypes.name == 'Куда ушло время').first().id)
        DBSession.add(article_time_user1)

        article_dream_user1 = Articles(text='Мне приснился прыжок с парашютом. Было страшно D:',
                                       date=datetime.date(2016, 3, 15),
                                       user_id=DBSession.query(User).filter(User.login == 'user1').first().id,
                                       type_id=DBSession.query(ArticlesTypes)
                                       .filter(ArticlesTypes.name == 'Сон').first().id)
        DBSession.add(article_dream_user1)
