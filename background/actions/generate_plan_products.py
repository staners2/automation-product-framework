import logging.config
from datetime import datetime

from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel
from web.serializers.plans.CreatePlansSerializer import CreatePlansSerializer
from workalendar.europe import Russia

logger = logging.getLogger("work")


def generate_plan_products(start: datetime, end: datetime):
    """
    Подсчет баллов плана по продуктам
    :param start: Первый день месяца
    :param end: Последний день месяца
    :return: None
    """
    worked_calendar = Russia()
    worked_days = worked_calendar.get_working_days_delta(start, end, True)
    worked_month = worked_days // 5  # 5 - кол-во дней в неделе, TODO: придумать как считать?

    daily: EventTypesModel = EventTypesModel.objects.get(title="Дейли")
    close_task: EventTypesModel = EventTypesModel.objects.get(title="Закрытие задач")
    review_code: EventTypesModel = EventTypesModel.objects.get(title="Работа в двойках")
    one_to_one: EventTypesModel = EventTypesModel.objects.get(title="1:1")
    individual_plan: EventTypesModel = EventTypesModel.objects.get(title="ПИР")
    meeting_on_product: EventTypesModel = EventTypesModel.objects.get(title="Встреча по продукту")

    plan_daily = worked_days * daily.point
    plan_close_task = worked_month * close_task.point
    plan_review_code = worked_month * review_code.point

    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()
    for product in products:
        plan_one_to_one = product.developers.filter(is_developer=True).count() * one_to_one.point
        plan_individual_plan = product.developers.filter(is_developer=True).count() * individual_plan.point
        plan_meeting_on_product = 1 * meeting_on_product.point

        data = {
            "date": start.date(),
            "product": product.id,
            "daily": plan_daily,
            "review_code": plan_review_code,
            "one_to_one": plan_one_to_one,
            "individual_plan": plan_individual_plan,
            "meeting_on_product": plan_meeting_on_product,
            "close_task": plan_close_task,
        }

        plan = CreatePlansSerializer(data=data)
        if plan.is_valid():
            plan.save()
            logger.info(f"План для {product.title.upper()} составлен {plan.data}")
        else:
            logger.error(f"План для {product.title.upper()} не составлен: {plan.data} | {plan.errors}")
