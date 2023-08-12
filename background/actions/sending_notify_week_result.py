import logging.config
from datetime import datetime

from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel
from web.serializers.plans.CreatePlansSerializer import CreatePlansSerializer
from workalendar.europe import Russia

logger = logging.getLogger("work")


def sending_notify_week_result(start: datetime, end: datetime):
    """
    Отправка сообщений в чат о результатх продуктового фреймворка
    Запускать: 50 09 * * 1 | Каждый понедельник в 09:50
    Запускать: 55 09 1 * * | Каждое 1 число в 09:55
       Отчет формирует итог выполнения плана с 1 числа, по текущую дату формирования отчета,
       с подсчетом выполнения месячного плана
       Первого дня нового месяца - отправляет отчет в чат о выполнении плана за прошедший месяц
    :param products: список продуктов
    :param event_types: список всех событий
    :return: None
    """
    if date.timetuple().tm_min >= 55:
        # Отправка месячного отчета
        if date.day == 1:
            date_start = datetime.strptime(f"{date.year}-{date.month - 1}-1", "%Y-%m-%d")
            Utils.sending_notify_month_result(products, date_start.date())
            date_end = date - timedelta(1)
            Utils.sending_notify_week(products, event_types, date_start.date(), date_end.date())
    else:
        # TODO Подумать над возможными вариантами
        # Отправка месячного отчета в продукты
        if date.day == 1:
            date_start = datetime.strptime(f"{date.year}-{date.month - 1}-1", "%Y-%m-%d")
            date_end = date - timedelta(1)
            Utils.sending_notify_week(products, event_types, date_start.date(), date_end.date())
        elif date.weekday() == 0:
            if date.day - 7 <= 0:
                date_start = datetime.strptime(f"{date.year}-{date.month}-1", "%Y-%m-%d")
            else:
                date_start = date - timedelta(7)
            date_end = date - timedelta(1)
            Utils.sending_notify_week(products, event_types, date_start.date(), date_end.date())
