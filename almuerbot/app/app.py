from functools import partial

from flask import Flask
from flask_restful import Api

from almuerbot.app.resources import (
    UsersResource, RatingsResource, VenuesResource, GroupsResource,
    CategoryResource)
from almuerbot.config import constants
from almuerbot.app.new import new


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
    for entity in ['users', 'groups', 'categories', 'venues']:
        app.add_url_rule(
            rule=f'/new/{entity}',
            endpoint=f'new_{entity}',
            view_func=partial(new, entity=entity),
            methods=['GET', 'POST'])
    return app


if __name__ == '__main__':
    from almuerbot.data.models import Base
    from almuerbot.data.manager import UserManager

    Base.metadata.create_all(UserManager().engine)

    app = create_app()
    app.run(debug=True, host=constants.WEBAPP_HOST, port=constants.WEBAPP_PORT)
