import logging.config
from datetime import datetime

from requests import RequestException

from background.service import Jira, Utils
from web.models.EmployeesModel import EmployeesModel
from web.models.ProductsModel import ProductsModel

logger = logging.getLogger("work")


def create_header_issue_daily(start: datetime, end: datetime):
    """
    Создать Главную задачу на Дейли
    Запускать: 55 8 * * 1-6 | С понедельника по субботу в 8:55
    :param start: дата первого рабочего дня
    :param end: дата последнего рабочего дня
    :return: None
    """
    global new_issue

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()

    for product in products:
        # TODO: Нужен ли здесь хардкод условия?
        if product.title in [
            "Запись к врачу",
            "Сервисы самообслуживания Goodline",
            "CRM ULA",
            "Биллинг B2C",
            "1С",
            "Фабрика игр",
            "Совхоз",
        ]:
            manager: EmployeesModel = product.manager

            request_data = {
                "fields": {
                    "project": {"key": product.base_namespace.title},
                    "priority": {"id": "4"},
                    "summary": f"Совещание: Daily-митинг. {start.strftime('%d')}.{start.strftime('%m')} - "
                    f"{end.strftime('%d')}.{end.strftime('%m')} / {product.title}",
                    "assignee": {"name": manager.login},
                    "issuetype": {"name": "Совещание"},
                    "description": "",
                    "duedate": end.strftime("%Y-%m-%d"),
                    "customfield_10021": start.strftime("%Y-%m-%d"),
                }
            }

            try:
                new_issue = Jira.create_issue(request_data)
                Jira.update_reporter_issue(new_issue["self"], manager.login)
            except RequestException as ex:
                logger.error(f"Не смог создать задачу по продукту: {product.title} на {manager.login} | {ex}")
                continue
            key = new_issue["key"]
            Utils.send_message_created_issue_daily(product, manager, key, start, end)
