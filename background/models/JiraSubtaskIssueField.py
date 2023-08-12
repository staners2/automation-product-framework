from dataclasses import dataclass

from dataclasses_json import dataclass_json

from background.models.JiraIssueType import JiraIssueType


@dataclass_json
@dataclass
class JiraSubtaskIssueField:
    summary: str
    issuetype: JiraIssueType
