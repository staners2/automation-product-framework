from dataclasses import dataclass

from dataclasses_json import dataclass_json

from background.models.JiraIssueField import JiraIssueField


@dataclass_json
@dataclass
class JiraIssue:
    key: str
    id: int
    self: str
    fields: JiraIssueField
