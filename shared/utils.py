import logging
from deep_translator import GoogleTranslator


# Инициализация переводчика
translator = GoogleTranslator()

# Инициализация логера
logger = logging.getLogger(__name__)