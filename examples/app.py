# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


r"""Minimal Flask application example for development.

Run example development server:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ export FLASK_APP=app.py
   $ flask run

Load the list of records:

.. code-block:: console

   $ curl -v -XGET http://0.0.0.0:5000/records/?q=title:Test
   $ curl -v -XGET http://0.0.0.0:5000/records/?q=title:Test \
       Accept:application/xml
"""

from __future__ import absolute_import, print_function

import os
import xmlrpclib

from flask import Blueprint, Flask, jsonify, make_response

from invenio_rest import ContentNegotiatedMethodView, InvenioREST


def json_v1_search(search_result):
    """Serialize records."""
    return make_response(jsonify(search_result))


def xml_v1_search(search_result):
    """Serialize records as text."""
    return make_response(xmlrpclib.dumps((search_result,), allow_none=True))


class RecordsListResource(ContentNegotiatedMethodView):
    """Example Record List."""

    def __init__(self, **kwargs):
        """Init."""
        super(RecordsListResource, self).__init__(
            method_serializers={
                'GET': {
                    'application/json': json_v1_search,
                    'application/xml': xml_v1_search,
                },
            },
            default_method_media_type={
                'GET': 'application/json',
            },
            default_media_type='application/json',
            **kwargs)

    def get(self, **kwargs):
        """Implement the GET /records."""
        return {"title": "Test"}

# Create Flask application
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI',
                                           'sqlite:///app.db'),
)

InvenioREST(app)

blueprint = Blueprint(
    'mymodule',
    __name__,
    url_prefix='/records',
    template_folder='templates',
    static_folder='static',
)

records_view = RecordsListResource.as_view('records')
blueprint.add_url_rule('/', view_func=records_view)

app.register_blueprint(blueprint)
