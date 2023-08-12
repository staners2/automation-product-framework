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


def event_individual_plan(start: datetime, end: datetime):
    """
    Событие типа 'ПИР'
    Запускать: 0 23 * * * | Каждый день в 23:00 (проверять за сегодня)
    :param start: Начальная дата поиска
    :param end: Конечная дата поиска
    :return: None
    """
    logger.info(f"Начался поиск события 'ПИР' с {start} по {end}")

    products: [ProductsModel] = ProductsModel.objects.filter(
        deleted=None).all()
    event_type: EventTypesModel = EventTypesModel.objects.get(title="ПИР")

    for product in products:
        manager: EmployeesModel = product.manager
        query = (
            f"assignee in ({manager.login}) AND resolutiondate >= {start.strftime('%Y-%m-%d')} AND resolutiondate <= \"{end.strftime('%Y-%m-%d')} 23:59\" "
            f"AND type=Задача AND project = TEACHSIT AND status IN (Closed, Done, Resolved)"
        )
        issues: List[JiraIssue] = Jira.get_issue_on_jql(query)

        for issue in issues:
            date = issue.fields.resolutiondate.date()
            url = f"{settings.JIRA_URL}/browse/{issue.key}"
            description = issue.fields.summary
            # TODO: Исполнителем считается менеджер. Попробовать сделать сотрудника?
            # employee: EmployeesModel = product.developers.get(login=issue.fields.assignee.name)
            manager: EmployeesModel = product.manager
            data = {
                "date": date,
                "type": event_type.id,
                "product": product.id,
                "assignee": manager.id,
                "url": url,
                "description": description,
            }
            event = CreateEventsSerializer(data=data)
            if event.is_valid():
                event.save()
                logger.info(f"Событие добавлено: {event.data}")
            else:
                logger.error(
                    f"Событие не добавлено: {event.data} | {event.errors}")
