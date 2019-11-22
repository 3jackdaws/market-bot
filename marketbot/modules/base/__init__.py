from marketbot import event, Bot
from .ticker import manage_stock_object
import logging
logger = logging.getLogger(__name__)

async def log_on_ready(client:Bot):
    client.logger.info(f"Logged in as {client.user}")

handlers = [
    event("ready", log_on_ready),
    event("message", manage_stock_object)
]
