import json
import logging.config

import requests
from requests import RequestException
from typing import Dict, List, Union

from background.models.JiraCommentsList import JiraCommentsList
from background.models.JiraIssue import JiraIssue
from background.models.JiraIssueList import JiraIssueList
from web import settings

logger = logging.getLogger("work")


def create_issue(request_data: Dict) -> Dict:
    """
    Создание задачи
    :param request_data: тело запроса
    :return: ответ в формате json
    """
    logger.info(f"REQUEST = {request_data}")
    jira_response = requests.post(
        settings.JIRA_URL + "/rest/api/2/issue",
        json=request_data,
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )

    jira_json = json.loads(jira_response.text)

    if "errors" in jira_json:
        raise RequestException(jira_json["errors"])

    return jira_json


def get_issue_on_jql(query: str) -> List[JiraIssue]:
    """
    Получение списрка задач по jql запосу
    :param query: jql запрос
    :return: Список задач
    """
    logger.info(f"JQL = {query}")
    request_data = {"jql": f"{query}", "maxResults": 500}

    jira_response = requests.post(
        settings.JIRA_URL + "/rest/api/2/search",
        json=request_data,
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )
    items = JiraIssueList.from_dict(jira_response.json())

    logger.debug(f"Get issues count: {len(items.issues)}")
    logger.debug(f"Get issues request: {request_data}")
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
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )

    if jira_response.status_code != 204:
        logger.error(f"Failed update reporter {login}: {jira_response.content}")
    else:
        logger.debug(f"Successful update reporter: {login}")


def get_comments_on_issue(issue_key: str) -> Union[JiraCommentsList, None]:
    """
    Получение всех комментариев по задаче
    :param issue_key: ключ задачи
    :return: Список комментариев
    """

    jira_response = requests.get(
        settings.JIRA_URL + f"/rest/api/2/issue/{issue_key}/comment",
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )

    if jira_response.status_code != 200:
        logger.error(f"Failed get comment on {issue_key}: {jira_response.content}")
        return None

    items = JiraCommentsList.from_dict(jira_response.json())

    logger.debug(f"Get comments count: {len(items.comments)}")
    return items


def get_info_issue(issue_key):
    jira_response = requests.get(
        settings.JIRA_URL + f"/rest/api/2/issue/{issue_key}",
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )

    if jira_response.status_code != 200:
        logger.error(f"Failed get comment on {issue_key}: {jira_response.content}")
        return

    return JiraIssue.from_dict(jira_response.json())


def transition_issue(issue: JiraIssue, id_status: int):
    """
    Доводит задачу до заданного статуса
    :param issue: задача
    :param id_status: id статуса
    :return: список доступных
    """
    url = settings.JIRA_URL + f"/rest/api/2/issue/{issue.id}/transitions"
    data = {"transition": {"id": f"{id_status}"}}

    jira_response = requests.post(
        f"{url}",
        json=data,
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )

    if jira_response.status_code != 200:
        logger.error(f"Failed update transition status on {issue.key}")


def update_assignee(issue: JiraIssue, login: str):
    url = settings.JIRA_URL + f"/rest/api/2/issue/{issue.key}/assignee"
    data = {"name": f"{login}"}

    jira_response = requests.put(
        f"{url}",
        json=data,
        auth=(settings.JIRA_USER, settings.JIRA_PASSWORD),
    )

    if jira_response.status_code != 204:
        logger.error(f"Failed update assignee on {issue.key} | New assignee: {login}")


def task_is_closed(keys: [str]) -> bool:
    """
    Проверка закрыты ли все подзадачи
    :param keys: Список всех ключей подзадач
    :return: Все подзадачи исполнены/закрыты?
    """
    for key in keys:
        issue: JiraIssue = get_info_issue(key)
        if issue.fields.timespent is not None:
            if issue.fields.status.name != "Исполнена":
                return False
    return True
