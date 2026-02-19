# Databricks CLI
# Copyright 2017 Databricks, Inc.

from __future__ import absolute_import

import click

from databricks_cli.virtual_engineers.web import run_server


@click.group()
def virtual_engineers_group():
    """Manage the AI Virtual Engineer web platform."""


@virtual_engineers_group.command('serve')
@click.option('--host', default='127.0.0.1', show_default=True, help='Host to bind the web app to.')
@click.option('--port', default=8000, show_default=True, help='Port to bind the web app to.')
def serve(host, port):
    """Start the Virtual Engineer web platform."""
    server = run_server(host, port)
    click.echo('Virtual Engineer platform is running at http://{0}:{1}'.format(host, port))
    click.echo('Press Ctrl+C to stop the service.')
    server.serve_forever()
