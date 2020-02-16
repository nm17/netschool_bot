from kutana import Plugin, Context, Message
from tinydb import Query
from tinydb.operations import add

from db import db
from state_logic import StartUpMachine

plugin = Plugin(name="Login")

@plugin.on_any_unprocessed_message()
async def asd(msg: Message, ctx: Context):
    m = StartUpMachine.from_user_id(ctx.user_uid)
    if m.current_state == StartUpMachine.not_started:
        return
    elif m.current_state == StartUpMachine.entering_school:
        q = Query()
        db.table("login_data").update(add("school", msg.text), q.user_id == ctx.user_uid)
        m.reset()
        await ctx.reply("Done")
    elif m.current_state == StartUpMachine.entering_login:
        q = Query()
        db.table("login_data").update(add("login", msg.text), q.user_id == ctx.user_uid)
        await ctx.reply("Введите Город:")
    elif m.current_state == StartUpMachine.entering_city:
        q = Query()
        db.table("login_data").update(add("login", msg.text), q.user_id == ctx.user_uid)
        await ctx.reply("Введите ОО:")
    elif m.current_state == StartUpMachine.entering_oo:
        q = Query()
        db.table("login_data").update(add("login", msg.text), q.user_id == ctx.user_uid)
        await ctx.reply("Введите Школу:")
    m.cycle()
    await ctx.reply(m.model.state)
    m.save()


@plugin.on_commands(["start", "login"])
async def _(msg, ctx: Context):
    m = StartUpMachine.from_user_id(ctx.user_uid)
    m.reset()
    m.sent_start()

    await ctx.reply("""Введите логин и пароль от Сетевого города.

Формат: <Логин>:<Пароль>""")
    m.save()
