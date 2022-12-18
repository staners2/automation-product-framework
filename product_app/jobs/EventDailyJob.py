import logging
from datetime import datetime

from django_cron import CronJobBase, Schedule


class EventDailyJob(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Сбор информации по событию "Дейли"'  # a unique code

    def do(self):
        """
        Событие типа 'Дейли'
        :param event: событие
        :param products: список продуктов
        :return: None
        """
        logging.debug("Start event 'Daily'")

        date = datetime.now().date()
        print(date)

        print(f"Search 'daily' in day: {date}")
        # date_range = Utils.get_start_and_end_week(date)
        # Неделя рабочая
        # if date_range is not None:
        #     # Первый рабочий день
        #     first_date = date_range[0]
        #     # Последний рабочий день на неделе
        #     last_date = date_range[-1]
        #
        #     for product in products:
        #         # пока только на Запись к врачу
        #         # if (
        #         #     product.product_name == "Запись к врачу"
        #         #     or product.product_name == "Сервисы самообслуживания Goodline"
        #         #     or product.product_name == "CRM ULA"
        #         # ):
        #         jql_issue = (
        #             f"project = '{product.base_workspace}' AND "
        #             f"summary ~ 'Совещание: Daily-митинг. {first_date.strftime('%d')}.{first_date.strftime('%m')} - "
        #             f"{last_date.strftime('%d')}.{last_date.strftime('%m')}' "
        #             "AND type = Совещание"
        #         )
        #         try:
        #             header_issue: JiraIssue = jira_services.get_issue_on_jql(jql_issue)[
        #                 0
        #             ]
        #         except Exception as er:
        #             logging.debug(
        #                 f"Не смог найти главную задачу по продукту {product.product_name} | {er}"
        #             )
        #             continue
        #
        #         keys = [item.key for item in header_issue.fields.subtasks]
        #         # Список дат за которые дейли исполнялись
        #         date_execute_daily = {}
        #         for key in keys:
        #             issue: JiraIssue = jira_services.get_info_issue(key)
        #             if issue.fields.timespent is not None:
        #                 if (
        #                         issue.fields.timespent != 0
        #                         and issue.fields.status.name == "Исполнена"
        #                         and issue.fields.summary.__contains__(
        #                     f"Daily-митинг {datetime.today().strftime('%d.%m')}")
        #                 ):
        #                     print(
        #                         f"{issue.fields.resolutiondate.date()} | {issue.key} "
        #                     )
        #                     date_execute_daily[issue.fields.customfield_10021] = True
        #
        #         for key in date_execute_daily:
        #             date_event = datetime.strptime(key, "%Y-%m-%d").strftime("%d.%m.%Y")
        #             task_url = f"{JiraServices.BASE_URL}/browse/{header_issue.key}"
        #             message = f"Ежедневный дейли проведен за {date_event}"
        #             google_services.added_new_event(
        #                 product.product_name, event, date_event, task_url, message
        #             )
