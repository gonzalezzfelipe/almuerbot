from flask import Flask
from flask_restful import Api

from almuerbot.app.resources import (
    UsersResource, RatingsResource, VenuesResource, GroupsResource,
    CategoryResource)
from almuerbot.config import constants
from almuerbot.app.new import new  #, new_almuerbot, new_autocohort, new_user


def create_app(debug=constants.WEBAPP_DEBUG,
               host=constants.WEBAPP_HOST,
               port=constants.WEBAPP_PORT):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = constants.SECRET_KEY

    # RestAPI for objects.
    api = Api(app)
    for resource in [
            UsersResource,
            RatingsResource,
            VenuesResource,
            GroupsResource,
            CategoryResource]:
        api.add_resource(resource, resource._endpoint)

    # Adding new objects through UI.
    app.add_url_rule(rule='/', endpoint='home', view_func=new)
    app.add_url_rule(rule='/new', endpoint='new', view_func=new)
    app.add_url_rule(
        rule='/new/user',
        endpoint='new_user',
        view_func=new,
        # view_func=new_user,
        methods=['GET', 'POST'])
    app.add_url_rule(
        rule='/new/venue',
        endpoint='new_venue',
        view_func=new,
        # view_func=new_autocohort,
        methods=['GET', 'POST'])
    app.add_url_rule(
        rule='/new/rating',
        endpoint='new_rating',
        view_func=new,
        # view_func=new_rating,
        methods=['GET', 'POST'])
    return app


if __name__ == '__main__':
    from almuerbot.data.models import Base
    from almuerbot.data.manager import UserManager

    Base.metadata.create_all(UserManager().engine)

    app = create_app()
    app.run(debug=True, host=constants.WEBAPP_HOST, port=constants.WEBAPP_PORT)
