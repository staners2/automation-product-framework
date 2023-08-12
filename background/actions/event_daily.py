import logging.config
from datetime import datetime

from background.models.JiraIssue import JiraIssue
from background.service import Jira
from web.models.EmployeesModel import EmployeesModel
from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel
from web.serializers.events.CreateEventsSerializer import CreateEventsSerializer
from web import settings

logger = logging.getLogger("work")


def event_daily(start: datetime, end: datetime):
    """
    Событие типа 'Дейли'
    :param start: Начальная даты поиска
    :param end: Конечная дата поиска
    :return: None
    """
    logger.info(f"Начался поиск события 'Дейли' с {start} по {end}")

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()
    event_type: EventTypesModel = EventTypesModel.objects.get(title="Дейли")

    for product in products:
        jql_issue = (
            f"project = '{product.base_namespace.title}' AND "
            f"summary ~ 'Совещание: Daily-митинг. {start.strftime('%d')}.{start.strftime('%m')} - "
            f"{end.strftime('%d')}.{end.strftime('%m')}' "
            "AND type = Совещание"
        )
        try:
            header_issue: JiraIssue = Jira.get_issue_on_jql(jql_issue)[0]
        except IndexError:
            logger.error(f"Не смог найти главную задачу по продукту {product.title}")
            continue

        keys = [item.key for item in header_issue.fields.subtasks]
        # Список дат за которые дейли исполнялись
        date_execute_daily = {}
        for key in keys:
            issue: JiraIssue = Jira.get_info_issue(key)
            if issue.fields.timespent is not None:
                if (
                    issue.fields.timespent != 0
                    and issue.fields.status.name == "Исполнена"
                    and issue.fields.summary.__contains__(f"Daily-митинг")
                ):
                    # logger.debug(
                    #     f"{issue.fields.resolutiondate.date()} | {issue.key} "
                    # )
                    date_execute_daily[issue.fields.customfield_10021] = True
        # Исполнителем выбираем менеджера проекта
        manager: EmployeesModel = product.manager
        description = f"Ежедневный дейли проведен"
        for key in date_execute_daily:
            date = datetime.strptime(key, "%Y-%m-%d").date()
            url = f"{settings.JIRA_URL}/browse/{header_issue.key}"

            data = {
                "date": date,
                "type": event_type.id,
                "product": product.id,
                "assignee": manager.id if manager is not None else None,
                "url": url,
                "description": description,
            }
            event = CreateEventsSerializer(data=data)
            if event.is_valid():
                event.save()
                logger.info(f"Событие добавлено: {event.data}")
            else:
                logger.error(f"Событие не добавлено: {event.data} | {event.errors}")
