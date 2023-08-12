import logging.config
import os
import shutil
from datetime import date
from pathlib import Path

from background.service import Telegram
from background.service.Sauron import Sauron
from web.models.EmployeesModel import EmployeesModel
from web.models.ProductsModel import ProductsModel


logger = logging.getLogger("work")


def sending_plan_and_fact(start: date, end: date):
    """
    Отправка ежедневного отчета ПЛАН/ФАКТ с картинками в чат с РП
    Запускать: 05 12 * * 1-5 | с ПН по ПТ в 12:05
    :param start: дата первого рабочего дня
    :param end: дата последнего рабочего дня
    :return:
    """

    Path("images").mkdir(parents=True, exist_ok=True)
    products: [ProductsModel] = ProductsModel.objects.filter(deleted=None).all()

    for product in products:
        manager: EmployeesModel = product.manager
        developers: [EmployeesModel] = product.developers.all()
        logins = [x.login for x in developers]
        if len(logins) == 0:
            logger.error(f"У продукта: {product.title} нет сотрудников")
        product_key = "devops"
        logger.info(f"\n==> {product.title} <==\n{manager}\n{logins}")
        Sauron.get_images_on_department(product_key, product.title, manager.full_name, logins, start, end)

    for filename in os.listdir("images"):
        path = os.path.join("images", filename)
        Telegram.send_photo(path, "-770738525")  # Чат ID=План/факт продуктов | -1001544521489
    shutil.rmtree(Path("images").absolute())
