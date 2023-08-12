import logging.config
from datetime import datetime
from typing import List

from background.models.JiraIssue import JiraIssue
from background.service import Jira
from web.models.EmployeesModel import EmployeesModel
from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel
from web.serializers.events.CreateEventsSerializer import CreateEventsSerializer
from web import settings

logger = logging.getLogger("work")


def event_review_code(start: datetime, end: datetime):
    """
    Событие типа 'Работа в двойках'
    Запускать: 0 23 * * * | Каждый день в 23:00 (проверять за сегодня)
    :param start: Начальная дата поиска
    :param end: Конечная дата поиска
    :return: None
    """
    logger.info(f"Начался поиск события 'Работа в двойках' с {start} по {end}")

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()
    event_type: EventTypesModel = EventTypesModel.objects.get(title="Работа в двойках")

    for product in products:
        developers: [EmployeesModel] = product.developers.all()
        all_namespaces = ",".join([product.base_namespace.title] + [item.title for item in product.namespaces.all()])
        for developer in developers:
            query = (
                f"project in ({all_namespaces}) AND (summary ~ 'Работа в двойках' OR summary ~ 'Ревью') "
                f"AND resolutiondate >= {start.strftime('%Y-%m-%d')} AND resolutiondate <= \"{end.strftime('%Y-%m-%d')} 23:59\" AND assignee = {developer.login} "
                f"AND resolution != Отменено"
            )
            issues: List[JiraIssue] = Jira.get_issue_on_jql(query)

            for issue in issues:
                date = issue.fields.resolutiondate.date()
                url = f"{settings.JIRA_URL}/browse/{issue.key}"
                description = f"{issue.fields.summary}"

                data = {
                    "date": date,
                    "type": event_type.id,
                    "product": product.id,
                    "assignee": developer.id,
                    "url": url,
                    "description": description,
                }
                event = CreateEventsSerializer(data=data)
                if event.is_valid():
                    event.save()
                    logger.info(f"Событие добавлено: {event.data}")
                else:
                    logger.error(f"Событие не добавлено: {event.data} | {event.errors}")
