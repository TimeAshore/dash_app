import json
import traceback
from functools import singledispatch

from flask import jsonify, Response, current_app
from sqlalchemy.exc import DBAPIError
from webargs import ValidationError
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed, HTTPException

from project.api.exceptions.customs import CustomException, RecordNotFound, \
    InvalidAPIRequest, DatabaseError, ServerError


@singledispatch
def to_serializable(rv):
    """
    Define a generic serializable function.
    """
    pass


@to_serializable.register(dict)
def ts_dict(rv):
    """Register the `dict` type
    for the generic serializable function.
    :param rv: object to be serialized
    :type rv: dict
    :returns: flask Response object
    """
    return jsonify(rv)


@to_serializable.register(list)
def ts_list(rv):
    """Register the `list` type
    for the generic serializable function.
    :param rv: objects to be serialized
    :type rv: list
    :returns: flask Response object
    """
    return Response(json.dumps(rv, indent=4, sort_keys=True))


class JSONResponse(Response):
    """
    Custom `Response` class that will be
    used as the default one for the application.
    All responses will be of type
    `application-json`.
    """

    # @classmethod
    # def force_type(cls, rv, environ=None):
    #     if rv.status_code not in (301, 302, 303, 305, 307):
    #         return super(JSONResponse, cls).force_type(to_serializable(rv), environ)
    #     return rv


def app_error_handler(app):
    @app.errorhandler(CustomException)
    def handle_invalid_usage(error):
        """
        Custom `Exception` class that will be used as the default one for the application.
        Returns pretty formatted JSON error with detailed information.
        """

        tb = traceback.format_exc()
        current_app.logger.error(
            "{}:{}\n{}".format(CustomException.__name__, error.message, tb))
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        """
        Custom error handler for 400 http exception.
        Returns a JSON object with a message of bad request.
        """

        tb = traceback.format_exc()
        message = "HTTP请求异常(参数解析错误)"
        current_app.logger.error(
            "{}:{}\n{}".format(BadRequest.__name__, error.description, tb))
        response = jsonify(InvalidAPIRequest(message=message).to_dict())
        response.status_code = BadRequest.code
        return response

    @app.errorhandler(NotFound)
    def resource_not_found(error):
        """
        Custom error handler for 404 http exception.
        Returns a JSON object with a message that accessed URL was not found.
        """

        tb = traceback.format_exc()
        message = "HTTP请求异常(找不到请求地址)"
        current_app.logger.error(
            "{}:{}\n{}".format(NotFound.__name__, error.description, tb))
        response = jsonify(RecordNotFound(message=message).to_dict())
        response.status_code = NotFound.code
        return response

    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        """
        Custom error handler for 405 http exception.
        Returns a JSON object with a message that accessed URL was not found.
        """

        tb = traceback.format_exc()
        message = "HTTP请求异常(不允许的请求方法)"
        current_app.logger.error(
            "{}:{}\n{}".format(MethodNotAllowed.__name__, error.description, tb))
        response = jsonify(InvalidAPIRequest(
            message=message, status_code=MethodNotAllowed.code).to_dict())
        response.status_code = MethodNotAllowed.code
        return response

    @app.errorhandler(DBAPIError)
    def sqlalchemy_db_error(error):
        """
        Custom error handler for DB error.
        Returns a JSON object with an error message.
        """

        tb = traceback.format_exc()
        message = "未知的数据库操作错误"
        current_app.logger.error(
            "{}:{}\n{}".format(DatabaseError.__name__, error.code, tb))
        response = jsonify(DatabaseError(message=message).to_dict())
        response.status_code = DatabaseError.status_code
        return response

    @app.errorhandler(422)
    def webargs_422_error(error):
        """
        Custom error handler for Webargs 422 error.
        Returns a JSON object with an error message.
        """

        current_app.logger.error(
            "{}:{}\n{}".format(ValidationError.__name__, "请求参数解析错误", error.data))
        response = jsonify({
            "status": False,
            "error": {
                "message": "请求参数解析错误",
                "type": ValidationError.__name__,
            }
        })
        response.status_code = InvalidAPIRequest.status_code
        return response

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Custom error handler for 500 pages.
        Returns a JSON object with a message that accessed URL was not found.
        """

        tb = traceback.format_exc()
        message = "服务器操作错误"
        current_app.logger.error("{}:{}\n{}".format(ServerError.__name__, message, tb))
        response = jsonify(ServerError(message=message).to_dict())
        response.status_code = ServerError.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """
        Custom error handler for other common http exceptions.
        Returns a JSON object with a message of bad request.
        """

        tb = traceback.format_exc()
        current_app.logger.error(
            "{}:{}\n{}".format(HTTPException.__name__, error.description, tb))
        response = jsonify({
            "status": False,
            "error": {
                "message": "HTTP请求异常",
                "type": HTTPException.__name__,
            }
        })
        response.status_code = error.code
        return response
