# services/socamas/project/api/schemas/__init__.py
from project.api.exceptions.customs import InvalidAPIRequest


class OneOf:
    def __init__(self, choices, desc=''):
        self.choices = choices
        self.desc = desc

    def __call__(self, value):
        if value not in self.choices:
            raise InvalidAPIRequest(self.desc)


def length_validator(length):
    if length < 0 or length > 100:
        raise InvalidAPIRequest('长度应在0-100之间')
