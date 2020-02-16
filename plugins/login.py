from kutana import Plugin, Context, Message
from netschoolapi import NetSchoolAPI
from tinydb import Query
from tinydb.operations import set as set_

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
        db.table("login_data").update(
            set_("school", msg.text), q.user_id == ctx.user_uid
        )
        await ctx.reply("Done")
        m.reset()
    elif m.current_state == StartUpMachine.entering_login:
        q = Query()
        db.table("login_data").update(
            set_("login", msg.text), q.user_id == ctx.user_uid
        )
        await ctx.reply("Введите Город:")
        await ctx.reply(
            "Все возможные города:\n"
            + "\n".join(
                await NetSchoolAPI("http://sgo.cit73.ru").get_form_data("cities")
            )
        )
        m.cycle()
    elif m.current_state == StartUpMachine.entering_city:
        q = Query()
        db.table("login_data").update(set_("city", msg.text), q.user_id == ctx.user_uid)
        await ctx.reply("Введите ОО:")
        await ctx.reply(
            "Все возможные ОО:\n"
            + "\n".join(
                await NetSchoolAPI("http://sgo.cit73.ru").get_form_data("funcs")
            )
        )
        m.cycle()
    elif m.current_state == StartUpMachine.entering_oo:
        q = Query()
        db.table("login_data").update(set_("oo", msg.text), q.user_id == ctx.user_uid)
        await ctx.reply("Введите Школу:")
        await ctx.reply(
            "Все возможные школы:\n"
            + "\n".join(
                await NetSchoolAPI("http://sgo.cit73.ru").get_form_data("schools")
            )
        )
        m.cycle()
    await ctx.reply(m.model.state)
    q = Query()
    await ctx.reply(str(db.table("login_data").search(q.user_id == ctx.user_uid)))
    m.save()


@plugin.on_commands(["start", "login"])
async def _(msg, ctx: Context):
    m = StartUpMachine.from_user_id(ctx.user_uid)
    m.reset()
    m.sent_start()
    q = Query()
    db.table("login_data").upsert({"user_id": ctx.user_uid}, q.user_id == ctx.user_uid)
    await ctx.reply(
        """Введите логин и пароль от Сетевого города.

Формат: <Логин>:<Пароль>"""
    )
    m.save()
