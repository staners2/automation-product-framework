import logging
import os
from io import BytesIO
from pathlib import Path

import requests
from dotenv import load_dotenv

from product_app import Config

load_dotenv()


def send_message(message: str, chat_id: str):
    """
    Отправка сообщений
    :param message: текст сообщения
    :param chat_id: id чата
    :return: None
    """

    send_text = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={message}&disable_notification=true"

    response = requests.post(send_text)

    if response.status_code != 200:
        logging.error(f"Failed send message: {response.text}")


def send_doc(path_file: str, chat_id: str):
    """
    Отправка документа
    :param path_file: путь до файла
    :param chat_id: id чата
    :return: None
    """

    name = Path(path_file).name
    query = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendDocument?chat_id={chat_id}&caption={name}&disable_notification=true"

    file = BytesIO(Path(path_file).read_bytes())
    file.name = name
    response = requests.post(query, files={"document": file})

    if response.status_code != 200:
        logging.error(f"Failed send doc: {response.text}")


def send_photo(path_image: str, chat_id: str):
    """
    Отправка фотографии
    :param path_image: путь до изображения
    :param chat_id: id чата
    :return: None
    """

    name = Path(path_image).name
    query = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendPhoto?chat_id={chat_id}&caption={name}&disable_notification=true"

    file = BytesIO(Path(path_image).read_bytes())
    file.name = name
    response = requests.post(query, files={"photo": file})

    if response.status_code != 200:
        logging.error(f"Failed send photo: {response.text}")
