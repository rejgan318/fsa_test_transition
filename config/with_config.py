"""
Тест на configparser
Тест на loguru
"""
import configparser
from loguru import logger

# logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')
logger.opt(ansi=True).info('Создаем <red>парсер</red> конфигов и считываем файл конфигурации')

config = configparser.ConfigParser()
config.read('config.ini')

wav_ext = config['wav']['ext']
mf = config['mp3']['max_frames']
logger.opt(ansi=True).info(f"mf = <blue>{mf}</blue>")
config['mp3']['max_frames'] = '2222'

new_config_name = 'config_new.ini'
logger.info(f'Сохраняем конфигурацию в новый файл {new_config_name}')
with open(new_config_name, 'w') as new_config_file:
    config.write(new_config_file)
