from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import arrow
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from product_app.samples.JiraIssueStatus import JiraIssueStatus
from product_app.samples.JiraSubtaskIssue import JiraSubtaskIssue
from product_app.samples.JiraAssigne import JiraAssigne
from product_app.samples.JiraIssueType import JiraIssueType
from product_app.samples.JiraReporter import JiraReporter


@dataclass_json
@dataclass
class JiraIssueField:
    summary: str
    timespent: Optional[int]
    issuetype: JiraIssueType
    assignee: JiraAssigne
    reporter: JiraReporter
    resolutiondate: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=arrow.get,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    status: Optional[JiraIssueStatus]
    aggregatetimespent: Optional[int]
    subtasks: Optional[list[JiraSubtaskIssue]]
    # дата создания задачи
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=arrow.get,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    # Тоже какая-то дата
    customfield_10021: str

    description: Optional[str] = ""

    def __post_init__(self):
        if self.aggregatetimespent is None:
            self.aggregatetimespent = 0
