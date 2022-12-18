import calendar
import json
import logging
import re

from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Optional

import pystache
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from Months import Months
from core import JiraServices, Telegram
from core.GoogleSheetsServices import GoogleSheetsServices, google_services
from core.Sauron import sauron
from models.Employee import Employee
from models.Event import Event
from models.EventType import EventType
from models.JiraIssue import JiraIssue
from models.NotifyDaily import NotifyDaily
from models.Product import Product

load_dotenv()


def get_event_type_by_title(events: List[EventType], title: str) -> Optional[EventType]:
    """
    Получение объекта 'событие' по его наименованию
    :param events: Список всех событий
    :param title: Название события
    :return: Объект события
    """
    for event in events:
        if event.title == title:
            return event
    return None


def calculation_point_on_event(
    products: List[Product],
    event_types: List[EventType],
    date_start: date,
    date_end: date,
):
    """
    Расчитывание баллов по событиям в диапазоне дат.
    (В столбце дата событий должны присутствовать только даты)
    :param products: Список продуктов
    :param event_types: Список всех типов событий
    :param date_start: Дата старта
    :param date_end: Дата завершения
    :return: None
    """
    for product in products:
        logging.debug(f"Start calculation point on product: {product.product_name}")
        events: List[Event] = []
        sheet = google_services.open_sheet(product.product_name)
        rows = sheet.get_all_values()
        for event_title in EventType.TYPES.get_list_items():

            start_index_row, col = google_services.get_first_cell_event(
                sheet, rows, event_title, Months[date_end.month]
            )
            for row_index in range(start_index_row, len(rows)):
                if not re.fullmatch("\d{1,2}[.,-]\d{1,2}[.,-]\d\d\d\d", rows[row_index][col]):
                    break
                date_event = datetime.strptime(rows[row_index][col], "%d.%m.%Y").date()
                logging.debug(f"Date event: {date_event} | cell[{row_index}][{col}]")
                if date_start <= date_event <= date_end:
                    description = rows[row_index][col + 2]
                    event_type: EventType = get_event_type_by_title(event_types, event_title)
                    events.append(
                        Event(
                            date_field=date_event,
                            event_type=event_type,
                            description=description,
                        )
                    )

        for event in events:
            if event.event_type.title == EventType.TYPES.EVENT_DAILY_TITLE.value:
                product.fact_event_daily += float(event.event_type.point)

            elif event.event_type.title == EventType.TYPES.EVENT_CLOSE_TASK_TITLE.value:
                product.fact_event_close_task += int(event.event_type.point)

            elif event.event_type.title == EventType.TYPES.EVENT_REVIEW_CODE_TITLE.value:
                product.fact_event_review_code += int(event.event_type.point)

            elif event.event_type.title == EventType.TYPES.EVENT_ONE_TO_ONE_TITLE.value:
                product.fact_event_one_to_one += int(event.event_type.point)

            elif event.event_type.title == EventType.TYPES.EVENT_INDIVIDUAL_PLAN_TITLE.value:
                product.fact_event_individual_plan += int(event.event_type.point)

            elif event.event_type.title == EventType.TYPES.EVENT_MEETING_ON_PRODUCT_TITLE.value:
                product.fact_event_meeting_on_product += int(event.event_type.point)

            logging.debug(
                f"\n{event.date_field.strftime('%d.%m.%Y')} | {event.event_type.title} | +{event.event_type.point} point\n"
                f"{event.description[0:75]}"
            )

        logging.debug(
            f"""
            <==== {product.product_name} ====>
            {EventType.TYPES.EVENT_DAILY_TITLE.value}: {product.fact_event_daily}
            {EventType.TYPES.EVENT_REVIEW_CODE_TITLE.value}: {product.fact_event_review_code}
            {EventType.TYPES.EVENT_ONE_TO_ONE_TITLE.value}: {product.fact_event_one_to_one}
            {EventType.TYPES.EVENT_INDIVIDUAL_PLAN_TITLE.value}: {product.fact_event_individual_plan}
            {EventType.TYPES.EVENT_MEETING_ON_PRODUCT_TITLE.value}: {product.fact_event_meeting_on_product}
            {EventType.TYPES.EVENT_CLOSE_TASK_TITLE.value}: {product.fact_event_close_task}
        """
        )


def calculation_plan_point_all_product(products: List[Product], event_types: List[EventType], first_day_month: date):
    """
    Подсчет баллов плана по продуктам
    :param first_day_month: первый день месяца
    :param products: список продуктов
    :param event_types: список типов событий
    :return: None
    """
    for product in products:
        product.calculation_plan_point(first_day_month, event_types)


def get_count_all_worked_days(month: int, year: int) -> int:
    """
    Получить по календарю кол-во рабочих дней за месяц
    :param month: номер месяца
    :param year: номер года
    :return: кол-во рабочих дней
    """
    file = Path(f"{year}.json")
    data = json.loads(file.read_text())
    date_start = datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d")
    date_end = date_start + relativedelta(months=1)

    worked_days = 0
    while date_start <= date_end:
        if data[f"{date_start.strftime('%Y-%m-%d')}"] != 0:
            worked_days += 1
        date_start += timedelta(days=1)

    return worked_days


def sending_notify_week(
    products: List[Product],
    event_types: List[EventType],
    date_start: date,
    date_end: date,
):
    """
    Отправка еженедельного отчета об итогах за неделю
    :param products: список продуктов
    :param event_types: список событий
    :param date_start: первый день недели
    :param date_end: последний день недели
    :return:
    """
    logging.debug("Sending notify week")

    date_start_s = date_start.strftime("%d-%m")
    date_end_s = date_end.strftime("%d-%m")

    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")

    # TODO Переделать чтобы брал данные из нарисованной таблицы, а не заново считал ???
    calculation_point_on_event(products, event_types, date_start, date_end)
    google_services.get_plan_on_products(products, GoogleSheetsServices.SHEETS_TITLE.PLAN.value, date_end)

    for product in products:
        logging.debug(f"{product.product_name} | prepare data")
        fact = product.get_all_fact_point()
        plan = product.get_all_plan_point()
        try:
            percent = float(fact / plan * 100).__format__(".2f")
        except ZeroDivisionError:
            logging.debug(f"{fact} / {plan} => ZeroDivisionError")
            percent = 0
        data = {
            "product": {"product_name": product.product_name},
            "date_start": date_start_s,
            "date_end": date_end_s,
            "point": {
                "total_plan_point": product.get_all_plan_point().__format__(".2f"),
                "percent": percent,
                "total_fact_point": product.get_all_fact_point().__format__(".2f"),
                "result": "✅" if product.get_all_plan_point() <= product.get_all_fact_point() else "🧐",
            },
            "daily": {
                "result": "✅" if product.plan_event_daily <= product.fact_event_daily else "",
                "plan": product.plan_event_daily.__format__(".2f"),
                "fact": product.fact_event_daily.__format__(".2f"),
            },
            "review_code": {
                "result": "✅" if product.plan_event_review_code <= product.fact_event_review_code else "",
                "plan": product.plan_event_review_code.__format__(".2f"),
                "fact": product.fact_event_review_code.__format__(".2f"),
            },
            "one_to_one": {
                "result": "✅" if product.plan_event_one_to_one <= product.fact_event_one_to_one else "",
                "plan": product.plan_event_one_to_one.__format__(".2f"),
                "fact": product.fact_event_one_to_one.__format__(".2f"),
            },
            "close_task": {
                "result": "✅" if product.plan_event_close_task <= product.fact_event_close_task else "",
                "plan": product.plan_event_close_task.__format__(".2f"),
                "fact": product.fact_event_close_task.__format__(".2f"),
            },
            "individual_plan": {
                "result": "✅" if product.plan_event_individual_plan <= product.fact_event_individual_plan else "",
                "plan": product.plan_event_individual_plan.__format__(".2f"),
                "fact": product.fact_event_individual_plan.__format__(".2f"),
            },
            "meeting_product": {
                "result": "✅" if product.plan_event_meeting_on_product <= product.fact_event_meeting_on_product else "",
                "plan": product.plan_event_meeting_on_product.__format__(".2f"),
                "fact": product.fact_event_meeting_on_product.__format__(".2f"),
            },
        }

        reader = Path("./Template/week_report.mustache").read_text("utf-8")
        render = pystache.render(reader, data)
        logging.info(f"Sending message in {product.product_name} chat | {product.chatid_telegram}")
        for chatId in product.chatid_telegram:
            Telegram.send_message(render, chatId)


def sending_notify_month(products: List[Product], date_start: date):
    """
    Отправка ежемесячного отчета, об итогах за весь месяц
    :param products: список продуктов
    :param date_start: первый день месяца
    :return: None
    """
    logging.debug("Sending notify month")

    month_title = Months[date_start.month]

    sheet = google_services.open_sheet(GoogleSheetsServices.SHEETS_TITLE.REPORT.value)
    all_column = sheet.get_row(2)
    # Получение крайней ячейки Сумма факта
    index_column = len([i for i in all_column if i != ""]) - 2
    index_row = 3

    data = {"date": month_title, "products": []}
    for product in products:
        fact_sum = float(sheet.cell((index_row, index_column)).value.replace(",", "."))
        plan_sum = float(sheet.cell((index_row, index_column + 1)).value.replace(",", "."))
        procent = float(sheet.cell((index_row, index_column + 2)).value.replace(",", "."))

        data["products"].append(
            {
                "product_name": product.product_name,
                "fact": fact_sum,
                "plan": plan_sum,
                "procent": f"{procent}",
                "result": "✅" if float(procent) >= 100 else "🚫",
            }
        )

        index_row += 1

    reader = Path("./Template/month_report.mustache").read_text("utf-8")
    render = pystache.render(reader, data)
    print(data)
    Telegram.send_message(render, "623018988")  # id чата Елизаветы Полетаевой с Tixon
    print(render)


def get_count_week(date_end: date) -> int:
    """
    Получить кол-во недель в месяце
    :param date_end: дата последнего дня в месяце
    :return: кол-во недель
    """
    date_start = datetime.strptime(f"{date_end.year}-{date_end.month}-1", "%Y-%m-%d")
    count = 0
    while date_start.month == date_end.month:
        if date_start.weekday() == 6:
            count += 1
        date_start += timedelta(1)
    if (date_start - timedelta(1)).weekday() != 6:
        count += 1

    return count


def get_count_friday(date_first_day_month: date) -> int:
    """
    Получение кол-ва пятниц в месяце
    :param date_first_day_month: дата первого дня месяца
    :return:
    """
    date = datetime.strptime(f"{date_first_day_month.year}-{date_first_day_month.month}-1", "%Y-%m-%d")
    count = 0
    while date.month == date_first_day_month.month:
        if date.weekday() == 4:  # пятница
            count += 1
        date += timedelta(1)

    return count


def get_count_week_for_review_code(date_first_day: date) -> int:
    """
    Получить кол-во недель при условии (>= 4 рабочих дня)
    :param date_first_day: дата первого дня месяца
    :return: кол-во недель
    """
    date_start = date_first_day
    date_start += timedelta(1)
    count_week = 0
    temp_day = 0
    while date_start.month == date_first_day.month:
        if date_start.weekday() != 5 | 6:
            if date_start.weekday() == 0:
                temp_day = 1
            if temp_day == 4:
                count_week += 1
            temp_day += 1

        date_start += timedelta(1)

    return count_week


def is_close_task_created(product: Product, date: date) -> bool:
    """
    Была ли создана задача 'Закрытие задач' на этой неделе
    :param product: Продукт
    :param date: Дата сегодняшнего дня
    :return: Создана или нет
    """

    date_range = get_start_and_end_week(date)
    # Вся неделя выходных
    if date_range is None:
        return True

    a = date_range[0].strftime("%Y-%m-%d")  # первый день недели
    b = date_range[-1].strftime("%Y-%m-%d")  # последний день недели
    query = (
        f"project = {product.base_workspace} AND assignee in ('{product.get_product_manager().login}') "
        r"AND summary ~ 'Еженедельное закрытие задач' "
        f"AND created >= {a}"
    )

    issues: List[JiraIssue] = JiraServices.get_issue_on_jql(query)

    if len(issues) > 0:
        logging.info(f"Задача уже создана для {product.product_name}")
        return True
    logging.info(f"Задача не обнаружена для {product.product_name}")
    return False


def get_start_and_end_week(date: date) -> [datetime]:
    """
    Получение списка рабочих дней
    :return:
    - Если вся неделя выходных, то возврат None
    - Список дат
    """
    a = date - timedelta(date.weekday())  # первый день недели
    b = date + timedelta(6 - date.weekday())  # последний день недели

    # оно работает и хорошо, нужно до 1 числа и после разделять
    if a.month != b.month:
        # к левой границе ближе
        if date.month == a.month:
            b = datetime.strptime(
                f"{b.year}-{a.month}-{calendar.monthrange(a.year, a.month)[1]}",
                "%Y-%m-%d",
            ).date()
        # к левой границе ближе
        else:
            a += timedelta(datetime.strptime(f"{b.year}-{b.month}-1", "%Y-%m-%d").weekday() - a.weekday())

    a -= timedelta(1)
    res = []
    while a < b:
        a = a + timedelta(1)
        year = a.year
        worked_calendar = json.loads(Path(f"{year}.json").read_text())
        if worked_calendar[f"{year}-{a.strftime('%m-%d')}"] != 0:
            res.append(a)

    if len(res) == 0:
        return None

    return res


def close_header_issue_daily(products: [Product]):
    """
    Закрыть главную задачу на событие 'Дейли'
    :param products: Список продуктов
    :return:
    """

    def task_is_closed(keys: [str]) -> bool:
        """
        Проверка закрыты ли все подзадачи
        :param keys: Список всех ключей подзадач
        :return: Все подзадачи исполнены/закрыты?
        """
        for key in keys:
            issue: JiraIssue = JiraServices.get_info_issue(key)
            if issue.fields.timespent is not None:
                if issue.fields.status.name != "Исполнена":
                    return False
        return True

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
        logging.debug(f"Old assignee: {old_assignee}")
        JiraServices.update_assignee(issue, "jenkins.ci")
        JiraServices.transition_issue(issue, 121)
        JiraServices.update_assignee(issue, old_assignee)

    date = datetime.now().date()
    date_range = get_start_and_end_week(date)
    # Неделя рабочая
    if date_range is not None:
        # Первый рабочий день
        first_date = date_range[0]
        # Последний рабочий день на неделе
        last_date = date_range[-1]

        for product in products:
            # пока только на Запись к врачу
            if product.product_name == "Запись к врачу":
                jql_issue = (
                    f"project = '{product.base_workspace}' AND "
                    f"summary ~ 'Совещание: Daily-митинг. {first_date.strftime('%d')}.{first_date.strftime('%m')} - "
                    f"{last_date.strftime('%d')}.{last_date.strftime('%m')} / {product.product_name}' "
                    "AND type = Совещание"
                )
                try:
                    header_issue: JiraIssue = JiraServices.get_issue_on_jql(jql_issue)[0]
                except Exception as er:
                    logging.debug(f"Не смог найти главную задачу по продукту {product.product_name} | {er}")
                    continue

                keys = [item.key for item in header_issue.fields.subtasks]
                if task_is_closed(keys):
                    transition_issue(header_issue)


def send_message_created_issue_daily(product: Product, key: str, date_start: date, date_end: date):
    """
    Отправка уведомления о созданной главной задачи
    :param product: продукт
    :param key: ключ созданной задачи
    :param date_start: дата первого рабочего дня
    :param date_end: дата последнего рабочего дня
    :return:
    """
    message = (
        f"<b>Продукт:</b> {product.product_name}\n<b>Руководитель:</b> {product.get_product_manager().name}\n\n"
        f"Создана задача для проведения дейли с {date_start.strftime('%Y-%m-%d')} по {date_end.strftime('%Y-%m-%d')}!\n\n"
        f'<b><a href="{JiraServices.BASE_URL}/browse/{key}"> ➤➤➤ Задача ➤➤➤ </a></b>'
    )
    for chat_id in product.chatid_telegram:
        Telegram.send_message(message, chat_id)


def send_message_created_subissue_daily(product: Product, notify_list: [NotifyDaily], date: date):
    """
    Отправка уведомления о созданных подзадачах
    :param product: продукт
    :param notify_list: список созданных задач
    :param date: дата сегодняшнего дня
    :return:
    """
    message = f"<b>Продукт:</b> {product.product_name}\nСозданы подзадачи для проведения дейли на {date.strftime('%Y-%m-%d')}!\n\n"

    for item in notify_list:
        message += f"<b>Сотрудник:</b> {item.login} {item.message}"

    for chat_id in product.chatid_telegram:
        Telegram.send_message(message, chat_id)


def is_holiday() -> bool:
    """
    Проверка на праздник
    :return:
    """
    date = datetime.now()
    data = json.loads(Path(f"{date.strftime('%Y')}.json").read_text())

    try:
        if data[f"{date.strftime('%Y-%m-%d')}"] == 0:
            logging.debug(f"Date is holiday: {date.strftime('%Y-%m-%d')}")
            return True
    except:
        logging.debug(f"Date is not holiday: {date.strftime('%Y-%m-%d')}")
        return False


def actualization_worked_employee_on_week(employee: Employee) -> bool:
    date = datetime.now()
    date_start = date - timedelta(date.weekday())
    date_end = date_start + timedelta(6)

    if employee.isLeader:
        # Руководитель всегда работает
        logging.debug(f"> Логин: {employee.login} | Работает")
        return True
    elif not employee.isLeader:
        calendar = sauron.get_worked_employees(employee.login, date_start.date(), date_end.date())
        if sum([x["hours"] for x in calendar]) > 0:
            logging.debug(f"> Логин: {employee.login} | Работает")
            return True
        else:
            logging.debug(f"> Логин: {employee.login} | Не работает")
            return False


def actualization_worked_employees_on_week(products: List[Product]) -> List[Product]:
    """
    Актуализация состояния работает сотрудник на неделе или нет
    :param products: список продуктов
    :return: Список сотрудников с установленным параметром "Работает на неделе"
    """

    for product in products:
        logging.debug(f">>> Сотрудники продукта: {product.product_name} <<<")
        for employee in product.employees:
            employee.workedWeek = actualization_worked_employee_on_week(employee)

    return products


def get_only_worked_employees_on_week(products: List[Product]) -> List[Product]:
    """
    Фильтрует список сотрудников по параметру "Работает на неделе"
    :param products: список продуктов
    :return: Отфильтрованный список продуктов
    """
    for product in products:
        product.employees = [employee for employee in product.employees if employee.workedWeek]

    return products
