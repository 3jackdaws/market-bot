from discord import Message
import os
import sys
from .bot import Bot

def event(type:str, handler):
    handler.__event__ = type
    return handler


