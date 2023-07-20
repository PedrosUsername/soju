import os

from interactions import Client, ContextMenuContext, Message, listen, message_context_menu



bot = Client(
  token= os.getenv("DISCORD_SOJUBOT_TOKEN")
)

@listen()
async def on_startup():
    print("Bot is ready!")



@message_context_menu(
  name="make it real",
  scopes=[1100512333203259552]
)
async def make_it_real(ctx: ContextMenuContext):
    message: Message = ctx.target
    await ctx.send(message.content)



bot.start()








"""
import requests


get_local_comm = "https://discord.com/api/v10/applications/1100516866641891391/guilds/1100512333203259552/commands"
delete_local_comm = "https://discord.com/api/v10/applications/1100516866641891391/guilds/1100512333203259552/commands/1119884701646192660"
create_local_comm = "https://discord.com/api/v10/applications/1100516866641891391/guilds/1100512333203259552/commands"

# This is an example USER command, with a type of 2
json = {
    "name": "Make it Red",d
    "type": 3
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot MTEwMDUxNjg2NjY0MTg5MTM5MQ.G62Emz.tzG3c613Nn7H3HZuO3_h53UZvPWf-93M6myfkU"
}


r = requests.delete(delete_local_comm, headers=headers)

print(r.text)
"""