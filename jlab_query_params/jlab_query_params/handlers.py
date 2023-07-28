import json
import os
import logging
from urllib.parse import parse_qsl

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

class RouteHandler(APIHandler):
    @tornado.web.authenticated
    def post(self):
        body = self.request.body.decode('utf-8')
        jl_vars = {env_var[6:]: value for (env_var, value) in parse_qsl(body) if env_var.startswith('jlvar_')}
        for jl_var, value in jl_vars.items():
            os.environ[jl_var] = value
            logging.info(f'Setting ENV VAR {jl_var} to {value}')

        self.finish()


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jlab-query-params", "set-env-vars")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
