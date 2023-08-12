from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from background.models.JiraSubtaskIssueField import JiraSubtaskIssueField


@dataclass_json
@dataclass
class JiraSubtaskIssue:
    key: str
    self: str
    fields: Optional[JiraSubtaskIssueField]
