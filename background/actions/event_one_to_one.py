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


def event_one_to_one(start: datetime, end: datetime):
    """
    Событие типа '1:1'
    Запускать: 0 23 * * * | Каждый день в 23:00 (проверять за сегодня)
    :param start: Начальная дата поиска
    :param end: Конечная дата поиска
    :return: None
    """
    logger.info(f"Начался поиск события '1:1' с {start} по {end}")

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()
    event_type: EventTypesModel = EventTypesModel.objects.get(title="1:1")

    for product in products:
        manager: EmployeesModel = product.manager
        developers: [EmployeesModel] = product.developers.all()
        all_namespaces = ",".join([product.base_namespace.title] + [item.title for item in product.namespaces.all()])
        for developer in developers:
            query = (
                f"resolutiondate >= {start.strftime('%Y-%m-%d')} AND resolutiondate <= \"{end.strftime('%Y-%m-%d')} 23:59\" "
                f"AND (summary ~ '1-1' OR summary ~ 'Совещание: 1 на 1' OR summary ~ 'Совещание: 1-1') "
                f"AND project in ({all_namespaces}) "
                f"AND type in ('Совещание (подзадача)', 'Совещание (бот) (подзадача)') AND assignee = {developer.login} "
                f"AND status IN (Closed, Done, Resolved)"
            )
            issues: List[JiraIssue] = Jira.get_issue_on_jql(query)

            for issue in issues:
                # if issue.fields.aggregatetimespent != 0:
                date = issue.fields.resolutiondate.date()
                url = f"{settings.JIRA_URL}/browse/{issue.key}"
                # TODO: Протокол где искать?
                comment = (Jira.get_comments_on_issue(issue.key)).get_comment_protocol_on_employee()
                description = comment.body if comment is not None else None

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
