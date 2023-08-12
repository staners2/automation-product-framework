from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class JiraIssueTransition:
    id: str
    name: str


@dataclass_json
@dataclass
class Head:
    transitions: Optional[list[JiraIssueTransition]]
