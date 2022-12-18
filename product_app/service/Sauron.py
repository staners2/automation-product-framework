import logging
import os
import time
from copy import copy
from datetime import datetime
from pathlib import Path

import requests


class Sauron:
    BASE_URL = "https://api.sauron.eltc.ru"
    count_error = 0
    MAX_ERROR = 4

    @classmethod
    def get_token(cls) -> str:
        body = {
            "client_secret": f"{os.environ['SAURON_CLIENT_SECRET']}",
            "grant_type": "client_credentials",
            "client_id": 1,
        }
        response = requests.post(cls.BASE_URL + "/oauth/token", data=body, verify=False)

        if response.status_code != 200:
            logging.error(f"Failed get token: {response.content} | Error: {cls.count_error}/{cls.MAX_ERROR}")
            time.sleep(21)
            cls.count_error += 1
            if cls.count_error == cls.MAX_ERROR:
                raise Exception(f"Failed get token")
            cls.get_token()
        else:
            cls.count_error = 0
            return response.json()["access_token"]

    @classmethod
    def get_images_on_department(
        cls,
        key: str,
        title: str,
        description: str,
        employees_login: [str],
        date_start: datetime,
        date_end: datetime,
    ):

        date_start = copy(date_start.strftime("%Y-%m-%d"))

        date_end = copy(date_end.strftime("%Y-%m-%d"))

        logins = ",".join(employees_login)
        response = requests.get(
            cls.BASE_URL + f"/api/external/plan-image/{key}?date_from={date_start}&date_to={date_end}"
            f"&title={title}&description={description}&employees={logins}",
            headers={"Authorization": f"Bearer {cls.get_token()}"},
            verify=False,
        )

        if response.status_code != 200:
            logging.error(
                f"Failed get images on department: {response.content} | Error: {cls.count_error}/{cls.MAX_ERROR}"
            )
            time.sleep(21)
            cls.count_error += 1
            if cls.count_error == cls.MAX_ERROR:
                raise Exception(f"Failed get images on department")
            cls.get_images_on_department(key, title, description, employees_login, date_start, date_end)
        else:
            cls.count_error = 0
            Path(f"./images/{title}.jpg").write_bytes(response.content)

    @classmethod
    def get_worked_employees(cls, login: str, date_start, date_end) -> str:
        """
        Получить рабочие дни сотрудника по его календарю в Гите
        :param login: логин сотрудника
        :param month: номер месяца
        :param year: номер года
        :return:
        """

        params = {
            "start": str(date_start),
            "end": str(date_end),
            "login": login,
        }

        response = requests.get("https://api.sauron.eltc.ru/api/календарь", params=params)
        response.encoding = "utf-8"
        return response.json()


sauron = Sauron()
