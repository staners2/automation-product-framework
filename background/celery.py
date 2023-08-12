from background.actions.sending_plan_and_fact import sending_plan_and_fact
from background.actions.try_closed_header_issue_daily import try_closed_header_issue_daily
from background.actions.create_subissue_daily import create_subissue_daily
from background.actions.create_header_issue_daily import create_header_issue_daily
from background.actions.generate_plan_products import generate_plan_products
from background.actions.event_individual_plan import event_individual_plan
from background.actions.event_one_to_one import event_one_to_one
from background.actions.event_review_code import event_review_code
from background.actions.event_daily import event_daily
from background.actions.event_close_task import event_close_task
from celery import Celery
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
import calendar
import logging.config

from background.service import Utils


# from background.actions.set_close_task_on_product_manager import set_close_task_on_product_manager
# from background.actions.notify_week_result import sending_notify_week_result

celery_app = Celery("web")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

logging.config.fileConfig("logging.conf")
logger = get_task_logger("work")


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_daily(params, today=datetime.now().date(), **kwargs):
    dates = Utils.get_start_and_end_week(today)
    if dates:
        start, end = dates[0], dates[-1]
        event_daily(start, end)


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_close_task(params, today=datetime.now().date(), **kwargs):
    # today = datetime.strptime("2022-11-21", "%Y-%m-%d").date()
    dates = Utils.get_start_and_end_week(today)
    if dates:
        start, end = dates[0], dates[-1]
        event_close_task(start, end)


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_review_code(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день месяца
    start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
    end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")
    event_review_code(start, end)


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_one_to_one(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день месяца
    # start = datetime.strptime(f"{today.year}-10-1", "%Y-%m-%d")
    # end = datetime.strptime(f"{today.year}-10-{calendar.monthrange(today.year, 10)[1]}", "%Y-%m-%d")
    start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
    end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")
    event_one_to_one(start, end)


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_individual_plan(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день месяца
    start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
    end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")
    # start = datetime.strptime(f"{today.year}-11-1", "%Y-%m-%d")
    # end = datetime.strptime(f"{today.year}-11-{calendar.monthrange(today.year, 11)[1]}", "%Y-%m-%d")
    event_individual_plan(start, end)


# TODO: Реализовать


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_set_close_task_on_product(params, today=datetime.now().date(), **kwargs):
    pass
    # Взяты первый и последний день месяца
    # start = datetime.strptime(f"{today.year}-11-1", "%Y-%m-%d")
    # end = datetime.strptime(f"{today.year}-11-{calendar.monthrange(today.year, 11)[1]}", "%Y-%m-%d")
    # set_close_task_on_product_manager()


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_generate_plan_products(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день месяца
    start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
    end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")
    # start = datetime.strptime(f"{today.year}-11-1", "%Y-%m-%d")
    # end = datetime.strptime(f"{today.year}-11-{calendar.monthrange(today.year, 11)[1]}", "%Y-%m-%d")
    generate_plan_products(start, end)


# TODO: Реализовать
@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_sending_notify_week_result(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день недели
    # start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
    # end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")
    dates = Utils.get_start_and_end_week(today)
    if dates is not None:
        # Первый рабочий день на неделе
        if today == dates[0]:
            start = datetime.strptime(f"{today.year}-11-1", "%Y-%m-%d")
            end = datetime.strptime(f"{today.year}-11-{calendar.monthrange(today.year, 11)[1]}", "%Y-%m-%d")
            # sending_notify_week_result(start, end)


# TODO: Реализовать
@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_sending_notify_month_result(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день недели
    # start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
    # end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")
    dates = Utils.get_start_and_end_week(today)
    if dates is not None:
        # Первый рабочий день на неделе
        if today == dates[0]:
            start = datetime.strptime(f"{today.year}-11-1", "%Y-%m-%d")
            end = datetime.strptime(f"{today.year}-11-{calendar.monthrange(today.year, 11)[1]}", "%Y-%m-%d")
            # sending_notify_month_result(start, end)


# TODO: Проверить


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_create_header_issue_daily(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день недели
    dates = Utils.get_start_and_end_week(today)
    if dates:
        # Первый рабочий день недели
        start = dates[0]
        # Последний рабочий день недели
        end = dates[-1]

        # Для отладки
        # start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
        # end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")

        if today == start:
            create_header_issue_daily(start, end)


# TODO: Проверить


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_create_subissue_daily(params, today=datetime.now(), **kwargs):
    # Взяты первый и последний день месяца
    dates = Utils.get_start_and_end_week(today.date())
    if today in dates:
        # Первый рабочий день недели
        start = dates[0]
        # Последний рабочий день недели
        end = dates[-1]
        # Сегодняшняя дата
        target = today

        # Для отладки
        # start = datetime.strptime(f"{today.year}-{today.month}-1", "%Y-%m-%d")
        # end = datetime.strptime(f"{today.year}-{today.month}-{calendar.monthrange(today.year, today.month)[1]}", "%Y-%m-%d")

        create_subissue_daily(start, end, target)


# TODO: Проверить, параметры которые принимает метод?
# Запускать утром 1 числа и ночью в воскресенье


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_try_closed_header_issue_daily(params, today=datetime.now(), **kwargs):
    # Взяты первый и последний день месяца
    dates = Utils.get_start_and_end_week(today.date())
    if today.weekday() == 6 and today.day == 1:
        # start = today - timedelta(abs(0 - today.weekday()))
        # end = today - timedelta(1)
        dates = Utils.get_start_and_end_week(today - timedelta(1))
        start = dates[0]
        end = dates[-1]
        try_closed_header_issue_daily(start, end)
    elif today.weekday() == 6:
        start = dates[0]
        end = dates[-1]
        try_closed_header_issue_daily(start, end)
    elif today.day == 1:
        dates = Utils.get_start_and_end_week(today - timedelta(1))
        start = dates[0]
        end = dates[-1]
        try_closed_header_issue_daily(start, end)


@celery_app.task(bind=True, max_retries=3, name="add every 10")
def task_sending_plan_and_fact(params, today=datetime.now().date(), **kwargs):
    # Взяты первый и последний день недели
    dates = Utils.get_start_and_end_week(today)
    logger.info("sdfsdfdsf")
    if today in dates:
        if datetime.isoweekday(today) == 1:
            start = today - timedelta(abs(0 - today.weekday()))
            end = today - timedelta(1)
        else:
            start = today - timedelta(datetime.isoweekday(today)) + timedelta(1)
            end = today

        sending_plan_and_fact(start, end)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
    # sender.add_periodic_task(2.0, task_daily.s())
    # sender.add_periodic_task(2.0, task_close_task.s())
    # sender.add_periodic_task(2.0, task_review_code.s())
    # sender.add_periodic_task(2.0, task_one_to_one.s())
    # sender.add_periodic_task(2.0, task_individual_plan.s())
    # sender.add_periodic_task(2.0, task_set_close_task_on_product.s())
    # sender.add_periodic_task(2.0, task_generate_plan_products.s())
    # sender.add_periodic_task(2.0, task_sending_notify_week_result.s())
    sender.add_periodic_task(2.0, task_sending_notify_week_result.s())
    # sender.add_periodic_task(2.0, task_create_header_issue_daily.s())
    # sender.add_periodic_task(2.0, task_create_subissue_daily.s())
    # sender.add_periodic_task(2.0, task_try_closed_header_issue_daily.s())
    # sender.add_periodic_task(2.0, task_sending_plan_and_fact.s())

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(5.0, debug_task.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )
