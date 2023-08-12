import logging.config
from datetime import datetime


from background.models.NotifyDaily import NotifyDaily
from background.service import Jira, Utils
from web.models.EmployeesModel import EmployeesModel
from web.models.ProductsModel import ProductsModel

from web import settings

logger = logging.getLogger("work")


def create_subissue_daily(start: datetime, end: datetime, target: datetime):
    """
    Создать подзадачи на дейли
    Запускать: 55 8 * * 1-6 | С понедельника по субботу в 8:55
    :param start: дата первого рабочего дня
    :param end: дата последнего рабочего дня
    :param target: дата на которую создаются подзадачи
    :return: None
    """
    global subissue

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()

    for product in products:
        manager: EmployeesModel = product.manager
        developers: [EmployeesModel] = product.developers.all()
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
            issue_jql = (
                f"project = '{product.base_namespace.title}' AND "
                f"summary ~ 'Совещание: Daily-митинг. {start.strftime('%d')}.{start.strftime('%m')} - "
                f"{end.strftime('%d')}.{end.strftime('%m')} / {product.title}' "
                "AND type = Совещание"
            )
            try:
                header_issue = Jira.get_issue_on_jql(issue_jql)[0]
            except Exception as ex:
                logger.error(f"Не смог найти главную задачу по продукту: {product.title} | {ex}")
                continue

            notify_list: [NotifyDaily] = []
            for developer in developers:

                request_data = {
                    "fields": {
                        "project": {"key": product.base_namespace.title},
                        "priority": {"id": "4"},
                        "summary": f"Daily-митинг {target.strftime('%d')}.{target.strftime('%m')} / {developer.login}",
                        "assignee": {"name": developer.login},
                        "issuetype": {"name": "Совещание (Подзадача)"},
                        "description": "",
                        "duedate": target.strftime("%Y-%m-%d"),
                        "customfield_10021": target.strftime("%Y-%m-%d"),
                        "timetracking": {"remainingEstimate": "1h"},
                        "parent": {"key": header_issue.key},
                    }
                }

                try:
                    subissue = Jira.create_issue(request_data)
                    Jira.update_reporter_issue(subissue["self"], manager.login)
                    notify_list.append(
                        NotifyDaily(
                            login=developer.login,
                            message=f'<a href="{settings.JIRA_URL}/browse/{subissue["key"]}"> ➤➤➤ Задача ➤➤➤ </a>\n',
                        )
                    )
                except Exception as ex:
                    logger.error(f"Не смог создать подзадачу по продукту: {product.title} на {developer.login} | {ex}")
                    notify_list.append(
                        NotifyDaily(
                            login=developer.login,
                            message="не удалось создать подзадачу :(",
                        )
                    )

            Utils.send_message_created_subissue_daily(product, notify_list, target)
