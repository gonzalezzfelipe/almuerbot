import json

from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort

from almuerbot.config import constants
from almuerbot.manager import UserManager, RatingManager, VenueManager
from almuerbot.utils import ignore_empty_string


class BaseResource(Resource):
    """Base API endpoint."""

    @staticmethod
    def write_exception(code, exc):
        """Write exception message."""
        abort(code, message=json.dumps({
            'exception': exc.__class__.__name__,
            'message': str(exc)}))

    def get_parser(self, method):
        """Get parser object to parse request arguments of the endpoint."""
        location = 'args' if method == 'GET' else 'form'
        try:
            return self._parser
        except AttributeError:
            self._parser = reqparse.RequestParser()
            for arg, arg_type in self.manager._model.arg_types.items():
                self._parser.add_argument(
                    arg, type=ignore_empty_string(arg_type), location=location)
        return self._parser

    def get(self):
        """Get all objects that match the filters."""
        args = self.get_parser('GET').parse_args(strict=True)
        include = args.pop('include', None)
        objects = self.manager.get(**args)
        return jsonify([a.as_dict(include=include) for a in objects])

    def post(self):
        """Add a new object."""
        args = self.get_parser('POST').parse_args(strict=True)
        args = {k: v for k, v in args.items() if v}
        try:
            obj = self.manager.add(**args)
        except Exception as exc:
            self.write_exception(400, exc)
        else:
            return make_response(jsonify({
                "message": "New object created.", "obj": obj}), 200)

    def put(self):
        """Modify an existing object."""
        args = self.get_parser('PUT').parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        id = args.pop('id', None)
        if id is None:
            self.write_exception(400, ValueError('id must be defined.'))
        try:
            obj = self.manager.update(id, **args)
        except Exception as exc:
            self.write_exception(400, exc)
        else:
            return make_response(jsonify({
                "message": "Object modified.", "obj": obj}), 200)

    def delete(self):
        """Delete an existing object."""
        args = self.get_parser('DELETE').parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        id = args.pop('id', None)
        if id is None:
            self.write_exception(400, ValueError('id must be defined.'))
        try:
            self.manager.delete(id)
        except Exception as exc:
            self.write_exception(400, exc)
        else:
            return make_response(jsonify({"message": "Object deleted."}), 200)


class UsersResource(BaseResource):

    _endpoint = '/users'

    @property
    def manager(self):
        try:
            return self._manager
        except AttributeError:
            self._manager = UserManager()
        return self._manager


class RatingsResource(BaseResource):

    _endpoint = '/ratings'

    @property
    def manager(self):
        try:
            return self._manager
        except AttributeError:
            self._manager = RatingManager()
        return self._manager


class VenuesResource(BaseResource):

    _endpoint = '/venues'

    @property
    def manager(self):
        try:
            return self._manager
        except AttributeError:
            self._manager = VenueManager()
        return self._manager
