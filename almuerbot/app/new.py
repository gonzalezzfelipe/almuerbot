import json
import os

import requests
from flask import Flask, jsonify, render_template, request, url_for
from flask_restful import Api

from almuerbot.app.resources import (
    UsersResource, RatingsResource, VenuesResource, GroupsResource,
    CategoryResource)
from almuerbot.config import constants


def new(entity=None):
    """Endpoint to redirect to new user, autopivot or autocohort."""
    if entity is None:
        return render_template('new.html.j2', url_for=url_for)
    else:
        if request.method == 'GET':
            return render_template('new_users.html.j2', constants=constants)
        else:
            response = requests.post(
                url_for(f'{entity}resource', _external=True),
                data=request.form)
            return render_template('submit.html.j2', response=response)
