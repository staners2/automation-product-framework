from dataclasses import dataclass

from dataclasses_json import dataclass_json

from product_app.samples.JiraIssueField import JiraIssueField


@dataclass_json
@dataclass
class JiraIssue:
    key: str
    id: int
    self: str
    fields: JiraIssueField
