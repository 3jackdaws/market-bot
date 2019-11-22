from discord import Client
import sys
import logging
from . import config

logging.getLogger('discord').setLevel(logging.ERROR)

logger= logging.getLogger()

def print_error(*args, **kwargs):
    logger.error(*args, **kwargs)

class Bot(Client):
    __slots__ = [
        'handlers',
        'logger'
    ]

    def __init__(self):
        super(Bot, self).__init__()
        self.handlers = {}
        self.logger = logging.getLogger("BOT")

    def add_handler(self, event:str, handler):
        event_name = "on_" + event
        if not hasattr(self, event_name):
            async def delegate_events(*args, **kwargs):
                for handler in self.handlers.get(event, []):
                    try:
                        await handler(self, *args, **kwargs)
                    except StopEvent:
                        logger.error(f"[{handler.__module__}.{handler.__name__}] has prevented event propagation")
                        return
                    except Exception as e:
                        print_error(f"[{type(e)}] in [{handler.__module__}.{handler.__name__}]: {e}")
            setattr(self, event_name, delegate_events)
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)



class StopEvent(Exception): pass




