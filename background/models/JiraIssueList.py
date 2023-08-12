from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json

from background.models.JiraIssue import JiraIssue


@dataclass_json
@dataclass
class JiraIssueList:
    issues: List[JiraIssue] = field(default_factory=list)
