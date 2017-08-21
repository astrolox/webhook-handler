#!/usr/bin/env python
"""
Webhook Handler
Lightweight but comprehensive application which receives and handles webhooks.

Written for Python 3.

"""
import argparse
import importlib
import os
import subprocess
import tempfile

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask_accept import accept


class ImproperlyConfigured(Exception):
    """Application is somehow improperly configured"""
    pass


app = Flask(__name__, instance_relative_config=True)
app.config.from_json(os.getenv('CONFIG', 'config.json'))


@app.route('/')
@accept('text/html')
def index_html():
    return app.send_static_file('index.html')


@app.route('/<slug>', methods=['POST'])
def webhook_receive(slug):
    """
    Receive a HTTP POST and behave as instructed by the configuration.

    :param slug:
    :return:
    """

    if 'WEBHOOKS' not in app.config:
        raise ImproperlyConfigured('WEBHOOKS configuration not provided')

    if slug not in app.config['WEBHOOKS']:
        abort(404)

    webhook_config = app.config['WEBHOOKS'][slug]

    if 'token' not in webhook_config or 'behaviour' not in webhook_config:
        raise ImproperlyConfigured(
            'Required key(s) missing from webhook configuration'
        )

    if request.args.get('token', None) != webhook_config['token']:
        abort(401)

    if webhook_config['behaviour'] == 'shell':

        if 'cmd' not in webhook_config:
            raise ImproperlyConfigured(
                'Shell cmd not defined in webhook configuration'
            )

        with tempfile.NamedTemporaryFile() as request_file:
            os.environ['REQUEST_DATA'] = request_file.name
            request_file.write(request.data)
            subprocess.call(webhook_config['cmd'])

    elif webhook_config['behaviour'] == 'module':

        if 'module' not in webhook_config:
            raise ImproperlyConfigured(
                'Python module not defined in webhook configuration'
            )

        python_module = importlib.import_module(name=webhook_config['module'])
        python_module.webhook_receive(webhook_config, request)

    else:
        raise ImproperlyConfigured('Unknown behaviour configured')

    return jsonify(success=True), 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Webhook Handler'
    )
    parser.add_argument(
        '--config',
        default=os.getenv('CONFIG', 'config.json'),
        help='Location of the configuration file'
    )
    parser.add_argument(
        '--host',
        default=os.getenv('HOST', '0.0.0.0'),
        help='IP address to listen for connections'
    )
    parser.add_argument(
        '--port',
        default=os.getenv('PORT', '8080'),
        help='Port number on which to list for connections'
    )
    args = parser.parse_args()
    app.config.from_json(args.config)
    app.run(host=args.host, port=int(args.port))
