from kutana import Plugin, Context

from state_logic import StartUpMachine

plugin = Plugin(name="Login")

@plugin.on_any_unprocessed_message()
async def asd(msg, ctx: Context):
    m = StartUpMachine.from_user_id(ctx.user_uid)
    if m.current_state == StartUpMachine.not_started:
        return
    if m.current_state == StartUpMachine.entering_school:
        m.reset()
        await ctx.reply("Done")
    else:
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
