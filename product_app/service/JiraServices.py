import json
import logging

import requests
from dotenv import load_dotenv
from requests import RequestException
from typing import Dict, List, Union

from product_app import Config
from product_app.samples.JiraCommentsList import JiraCommentsList
from product_app.samples.JiraIssue import JiraIssue
from product_app.samples.JiraIssueList import JiraIssueList

BASE_URL = "https://jira.eltc.ru"

load_dotenv()


def create_issue(request_data: Dict) -> Dict:
    """
    Создание задачи
    :param request_data: тело запроса
    :return: ответ в формате json
    """
    logging.info(f"REQUEST = {request_data}")
    jira_response = requests.post(
        BASE_URL + "/rest/api/2/issue",
        json=request_data,
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )

    jira_json = json.loads(jira_response.text)

    if "errors" in jira_json:
        raise RequestException(jira_json["errors"])

    logging.debug("Successful created task")

    return jira_json


def get_issue_on_jql(query: str) -> List[JiraIssue]:
    """
    Получение списрка задач по jql запосу
    :param query: jql запрос
    :return: Список задач
    """
    logging.info(f"JQL = {query}")
    request_data = {"jql": f"{query}", "maxResults": 500}

    jira_response = requests.post(
        BASE_URL + "/rest/api/2/search",
        json=request_data,
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )
    items = JiraIssueList.from_dict(jira_response.json())

    logging.debug(f"Get issues count: {len(items.issues)}")
    logging.debug(f"Get issues request: {request_data}")
    return items.issues


def update_reporter_issue(issue_url: str, login: str):
    """
    Обновление автора у задачи
    :param issue_url: url задачи
    :param login: логин сотрудника
    :return: None
    """

    request_data = {"fields": {"reporter": {"name": f"{login}"}}}

    jira_response = requests.put(
        f"{issue_url}",
        json=request_data,
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )

    if jira_response.status_code != 204:
        logging.error(f"Failed update reporter {login}: {jira_response.content}")
    else:
        logging.debug(f"Successful update reporter: {login}")


def get_comments_on_issue(issue_key: str) -> Union[JiraCommentsList, None]:
    """
    Получение всех комментариев по задаче
    :param issue_key: ключ задачи
    :return: Список комментариев
    """

    jira_response = requests.get(
        BASE_URL + f"/rest/api/2/issue/{issue_key}/comment",
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )

    if jira_response.status_code != 200:
        logging.error(f"Failed get comment on {issue_key}: {jira_response.content}")
        return None

    items = JiraCommentsList.from_dict(jira_response.json())

    logging.debug(f"Get comments count: {len(items.comments)}")
    return items


def get_info_issue(issue_key):
    jira_response = requests.get(
        BASE_URL + f"/rest/api/2/issue/{issue_key}",
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )

    if jira_response.status_code != 200:
        logging.error(f"Failed get comment on {issue_key}: {jira_response.content}")
        return

    return JiraIssue.from_dict(jira_response.json())


def transition_issue(issue: JiraIssue, id_status: int):
    """
    Доводит задачу до заданного статуса
    :param issue: задача
    :param id_status: id статуса
    :return: список доступных
    """
    url = BASE_URL + f"/rest/api/2/issue/{issue.id}/transitions"
    data = {"transition": {"id": f"{id_status}"}}

    jira_response = requests.post(
        f"{url}",
        json=data,
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )

    if jira_response.status_code != 200:
        logging.error(f"Failed update transition status on {issue.key}")


def update_assignee(issue: JiraIssue, login: str):
    url = BASE_URL + f"/rest/api/2/issue/{issue.key}/assignee"
    data = {"name": f"{login}"}

    jira_response = requests.put(
        f"{url}",
        json=data,
        auth=(Config.JIRA_USER, Config.JIRA_PASSWORD),
    )

    if jira_response.status_code != 204:
        logging.error(f"Failed update assignee on {issue.key} | New assignee: {login}")
