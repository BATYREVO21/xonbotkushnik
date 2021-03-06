﻿from Settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage
from app import Session, Users, Settings
from datetime import datetime
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

bot_configuration = BotConfiguration(
    name='XON',
    avatar='http://viber.com/avatar.jpg',
    auth_token=TOKEN
)
viber = Api(bot_configuration)

KEYBOARD3 = {
"Type": "keyboard",
"Buttons": [
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#e6f5ff",
            "ActionBody": "Давай начнём!",
            "Text": "Давай начнём!"
        },
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#e6f5ff",
            "ActionBody": "Отложить",
            "Text": "Отложить"
        }
    ]
}


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    session = Session()
    all_users = session.query(Users.viber_id, Users.dt_last_answer)
    session.close()

    session = Session()
    settings = session.query(Settings.remind_time).filter(Settings.id_set == 1).one()
    session.close()

    for user in all_users:
        delta = datetime.utcnow() - user[1]
        print(f'delta time = {delta.seconds}')
        if delta.seconds > settings[0]:
            try:
                bot_response = TextMessage(text='Пройдите тест заново', keyboard=KEYBOARD3, tracking_data='tracking_data')
                viber.send_messages(user[0], bot_response)
            except:
                print("Пользователь отписался")


@sched.scheduled_job('interval', minutes=1)
def awake_bot():
    r = requests.get("https://kushnikbot.herokuapp.com/")
    if r.status_code == 200:
        print("Bot is awake")


sched.start()
