from marshmallow.exceptions import MarshmallowError
from werkzeug.exceptions import BadRequest


class ParamException(MarshmallowError):
    """Raised when validation fails on a field. Validators and custom fields should
    raise this exception.

    :param message: An error message, list of error messages, or dict of
        error messages.
    :param list field_names: Field names to store the error on.
        If `None`, the error is stored in its default location.
    :param list fields: `Field` objects to which the error applies.
    """

    status_code = BadRequest.code
    messages = ""

    def __init__(self, message, status_code=None, field_names=None,
                 fields=None, data=None, **kwargs):

        self.message = message

        #: List of field objects which failed validation.
        self.fields = fields
        self.field_names = field_names or []
        # Store nested data
        self.data = data
        self.kwargs = kwargs
        if status_code is not None:
            self.status_code = status_code
        MarshmallowError.__init__(self, message)

    def normalized_messages(self, no_field_name="_schema"):
        if isinstance(self.messages, dict):
            return self.messages
        if len(self.field_names) == 0:
            return {no_field_name: self.messages}
        return dict((name, self.messages) for name in self.field_names)

    def to_dict(self):
        return {
            'status': False,
            'error': {
                'message': self.message,
                'type': str(self.__class__.__name__),
            }
        }


class ParamError(ParamException):
    status_code = ParamException.status_code

