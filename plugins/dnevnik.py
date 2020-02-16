import json
from pprint import pprint

from kutana import Plugin, Message, Context
from netschoolapi import NetSchoolAPI
from tinydb import Query

from db import db

plugin = Plugin(name="Login")


@plugin.on_commands(commands=["dnevnik"])
async def dnevnik(msg: Message, ctx: Context):
    api = NetSchoolAPI("http://sgo.cit73.ru")
    q = Query()
    user = db.table("login_data").search(q.user_id == ctx.user_uid)[0]
    print(user)
    await api.login(
        user["login"].split(":")[0],
        user["login"].split(":")[1],
        user["school"],
        city=user["city"],
        oo=user["oo"],
    )
    data = await api.get_diary()
    await ctx.reply("Ваш класс: " + data["weekDays"])
