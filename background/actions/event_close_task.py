import logging.config
from datetime import datetime

from background.service import Jira
from web.models.EmployeesModel import EmployeesModel
from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel
from web.serializers.events.CreateEventsSerializer import CreateEventsSerializer
from web import settings

logger = logging.getLogger("work")


def event_close_task(start: datetime, end: datetime):
    """
    Событие типа 'Закрытие задач'
    Запускать: 20 23 * * * | Каждый день
    :param start: Начальная дата поиска
    :param end: Конечная дата поиска
    :return: None
    """
    logger.info(f"Начался поиск события 'Закрытие задач' с {start} по {end}")

    summary = f"Еженедельное закрытие задач"  # summary не может искать с испол. символа '!'
    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()
    event_type: EventTypesModel = EventTypesModel.objects.get(title="Закрытие задач")

    description = f"Еженедельное закрытие задач"
    for product in products:
        manager: EmployeesModel = product.manager
        if manager is None:
            logger.error(f"Менеджер по продукту: {product.title} не найден!")
            continue
        query = (
            f"assignee in ({manager.login}) "
            f"AND resolutiondate >= {start.strftime('%Y-%m-%d')} AND resolutiondate <= \"{end.strftime('%Y-%m-%d')} 23:59\" AND summary ~ '{summary}' "
            f"AND project='{product.base_namespace.title}'"
        )
        issues = Jira.get_issue_on_jql(query)

        for issue in issues:
            if issue.fields.aggregatetimespent:
                date = issue.fields.resolutiondate.date()
                url = f"{settings.JIRA_URL}/browse/{issue.key}"

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
                    logger.error(f"Событие не добавлено: {event.data} | {event.errors}")
