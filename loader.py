from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.maria_db import Database
import logging
from logging.handlers import TimedRotatingFileHandler
import os

from data import config

logger = logging.getLogger('Bot')
if not os.path.isdir("Logs"):
    os.mkdir("Logs")
logger_handler = TimedRotatingFileHandler(
    'Logs/Bot.log', encoding='utf-8', when='midnight', backupCount=30)
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)
logger.info("\n****************************************************\n")
logger_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s]:  %(message)s'))
logger.info('Запуск приложения "Bot"')

if not os.path.isdir("docs"):
    os.mkdir("docs")

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
