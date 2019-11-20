from marketbot.bot import Bot
from marketbot.modules import modules
import sys
import os

def exit_with_error(error, code=1):
    print(error, file=sys.stderr)
    exit(code)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN") or exit_with_error("")

print("init")

bot = Bot()

for mod in modules:
    for handler in mod.handlers:
        bot.add_handler(handler.__event__, handler)

bot.run(DISCORD_TOKEN)


