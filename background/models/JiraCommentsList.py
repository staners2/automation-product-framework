from dataclasses import dataclass, field
from typing import List, Union

from dataclasses_json import dataclass_json

from background.models.JiraComment import JiraComment


@dataclass_json
@dataclass
class JiraCommentsList:
    comments: List[JiraComment] = field(default_factory=list)

    def get_comment_protocol_on_employee(self) -> Union[JiraComment, None]:
        for comment in self.comments:
            if comment.body.lower().find("протокол") != -1:
                return comment
        return None
