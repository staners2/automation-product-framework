import logging.config
from datetime import datetime

from background.models.JiraIssue import JiraIssue
from background.service import Jira
from web.models.ProductsModel import ProductsModel


logger = logging.getLogger("work")


def try_closed_header_issue_daily(start: datetime, end: datetime):
    """
    Закрыть главную задачу на событие 'Дейли'
    :param start: дата первого рабочего дня
    :param end: дата последнего рабочего дня
    :return: None
    """

    def transition_issue(issue: JiraIssue):
        """
        Сдвиг статуса задачи до статуса 'Исполнено'
            - 111 - В работу
            - 121 - Решено
            - 131 - Отменено
        :param issue: задача
        :return:
        """
        old_assignee = issue.fields.assignee.name
        logger.debug(f"Old assignee: {old_assignee}")
        Jira.update_assignee(issue, "jenkins.ci")
        Jira.transition_issue(issue, 121)
        Jira.update_assignee(issue, old_assignee)

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()

    for product in products:
        # пока только на Запись к врачу
        # TODO: Убрать хардкод?
        if product.product_name == "Запись к врачу":
            jql_issue = (
                f"project = '{product.base_namespace.title}' AND "
                f"summary ~ 'Совещание: Daily-митинг. {start.strftime('%d')}.{start.strftime('%m')} - "
                f"{end.strftime('%d')}.{end.strftime('%m')} / {product.title}' "
                "AND type = Совещание"
            )
            try:
                header_issue: JiraIssue = Jira.get_issue_on_jql(jql_issue)[0]
            except Exception as ex:
                logger.error(f"Не смог найти главную задачу по продукту: {product.title} | {ex}")
                continue

            keys = [item.key for item in header_issue.fields.subtasks]
            if Jira.task_is_closed(keys):
                transition_issue(header_issue)
