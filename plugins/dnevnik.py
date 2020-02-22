from io import BytesIO, StringIO

import dateutil
from kutana import Plugin, Message, Context
from netschoolapi import NetSchoolAPI
from pandas.plotting import table
from tinydb import Query
import matplotlib.pyplot as plt
import convertapi

from db import db

import pandas as pd

plugin = Plugin(name="Login")

def get_img(df):
    ax = plt.subplot(111, frame_on=False)  # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, df)  # where df is your data frame

    plt.savefig('mytable.png')

weektorus = {
    5: "субботу",
    4: "пятницу",
    3: "четверг",
    2: "среду",
    1: "вторник",
    0: "понедельник"
}

@plugin.on_commands(commands=["dnevnik"])
async def dnevnik(msg: Message, ctx: Context):
    api = NetSchoolAPI("http://sgo.cit73.ru")
    q = Query()
    user = db.table("login_data").search(q.user_id == ctx.user_uid)[0]
    await api.login(
        user["login"].split(":")[0],
        user["login"].split(":")[1],
        user["school"],
        city=user["city"],
        oo=user["oo"],
    )
    data = await api.get_diary()
    df = pd.DataFrame(data={})

    await ctx.reply("Ваш класс: ")
    for day in data["weekDays"]:
        date = dateutil.parser.parse(day["date"]).weekday()
        for lesson in day["lessons"]:
            try:
                hw = lesson["assignments"][0]["assignmentName"]
                mark = lesson["assignments"][0]["mark"]
            except KeyError:
                hw = None
                mark = None
            subject = lesson["subjectName"]
            print(lesson["room"])
            room = [int(s) for s in lesson["room"].split("/") if s.isdigit()][0]
            df = df.append({"Date": date, "Homework": hw, "Subject": subject, "Mark": mark, "Room": room}, ignore_index=True)
    df = df.set_index("Date")
    for name, group in df.groupby("Date"):
        msg_ = "Уроки на {}\n".format(weektorus[name])
        for row in group.iterrows():
            data = row[1]
            msg_ += "{} / {} - {}\n".format(data["Subject"], int(data["Room"]), data["Homework"])
        await ctx.reply(msg_)
