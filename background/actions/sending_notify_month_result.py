import logging.config
from datetime import datetime

from background.models.JiraIssue import JiraIssue
from background.service import Jira
from web.models.ProductsModel import ProductsModel


logger = logging.getLogger("work")

def sending_notify_month_result(start: datetime, end: datetime):
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