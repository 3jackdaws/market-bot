from marketbot import event, Bot
from .ticker import manage_stock_object

async def log_on_ready(client:Bot):
    print(f"Logged in as {client.user}")

handlers = [
    event("ready", log_on_ready),
    event("message", manage_stock_object)
]
