import logging.config
from datetime import datetime

logger = logging.getLogger("work")


def set_close_task_on_product_manager():
    """
    Создает задачи на закрытие своих задач за неделю на всех сотрудников Продукта
    Запускать: 00 9 * * * | Каждый день в 09:00
    :return: None
    """
    date = datetime.now().date()
    last_day_in_month = calendar.monthrange(date.year, date.month)[1]

    logging.debug("Start set close task on product manager")

    global new_issue

    for product in products:
        if Utils.is_close_task_created(product, date):
            continue

        manager: Employee = product.get_product_manager()

        request_data = {
            "fields": {
                "project": {"key": product.base_namespace.title},
                "priority": {"id": "4"},
                "summary": f"Еженедельное закрытие задач",
                "assignee": {"name": manager.login},
                "issuetype": {"name": "Задача"},
                "description": Directory.DESCRIPTION_CLOSE_TASK_ON_MANAGER,
                "duedate": date.strftime("%Y-%m-%d"),
                "customfield_10021": date.strftime("%Y-%m-%d"),
            }
        }
        # на понедельник можно ставить
        if (date + timedelta(3)).month == date.month:
            request_data["fields"]["duedate"] = (date + timedelta(3)).strftime("%Y-%m-%d")
        else:
            request_data["fields"]["duedate"] = datetime.strptime(
                f"{date.year}-{date.month}-{last_day_in_month}", "%Y-%m-%d"
            ).strftime("%Y-%m-%d")

        try:
            if (date.weekday() == 2 or date.day == last_day_in_month) and product.product_name == "Фабрика игр":
                new_issue = jira_services.create_issue(request_data)
                jira_services.update_reporter_issue(new_issue["self"], manager.login)
            elif (date.weekday() == 4 or date.day == last_day_in_month) and product.product_name != "Фабрика игр":
                new_issue = jira_services.create_issue(request_data)
                jira_services.update_reporter_issue(new_issue["self"], manager.login)
            else:
                continue
        except Exception:
            logging.error(f"Не смог создать задачу на {manager.login}")
            exit(1)

        for employee in product.developers:
            if employee.isLeader and not employee.isWorker:
                continue

            subissue_request_data = {
                "fields": {
                    "parent": {"id": new_issue["id"]},
                    "project": {"key": product.base_namespace.title},
                    "priority": {"id": "4"},
                    "summary": "Закрытие задач",
                    "assignee": {"name": employee.login},
                    "issuetype": {"name": "Подзадача"},
                    "duedate": date.strftime("%Y-%m-%d"),
                    "customfield_10021": date.strftime("%Y-%m-%d"),
                    "timetracking": {"originalEstimate": "30m"},
                }
            }

            try:
                if (date.weekday() == 2 or date.day == last_day_in_month) and product.product_name == "Фабрика игр":
                    new_subissue = jira_services.create_issue(subissue_request_data)
                    jira_services.update_reporter_issue(new_subissue["self"], manager.login)
                elif (date.weekday() == 4 or date.day == last_day_in_month) and product.product_name != "Фабрика игр":
                    new_subissue = jira_services.create_issue(subissue_request_data)
                    jira_services.update_reporter_issue(new_subissue["self"], manager.login)
            except Exception:
                logging.warning(f"Не смог создать подзадачу на {employee.login}")

        for chatId in product.chatid_telegram:
            if date.weekday() == 2 and product.product_name == "Фабрика игр":
                Telegram.send_message(
                    "Еженедельное закрытие задач ⏰💸\n" f"{JiraServices.BASE_URL}/browse/{new_issue['key']}",
                    chatId,
                )
            elif (date.weekday() == 4 or date.day == last_day_in_month) and product.product_name != "Фабрика игр":
                Telegram.send_message(
                    "Еженедельное закрытие задач ⏰💸\n" f"{JiraServices.BASE_URL}/browse/{new_issue['key']}",
                    chatId,
                )
