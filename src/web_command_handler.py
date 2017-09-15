"""
    web_api_handler
    ~~~~~~~~~~~~~~~~

    This is web api handler object.

"""
import inspect
import cherrypy
import os
import traceback
import sys
from auth import check_auth
from utils import error, create_response


class WebApiHandler(object):
    """
    Handles all the /api path requests
    """

    def __init__(self, ip, port, index_file):
        print "starting web api handler"
        self.exposed = True
        self.listening_port = port
        self.listening_ip = ip
        self.cherrypy_conf = {}
        self.logs_path = 'logs'
        self.index_file = index_file
        self.api_list = []
        self.function_list = []
        self.get_all_apis()

        self.setup_cherrypy()

    def start_handler(self):
        pass

    def stop_handler(self):
        pass

    def setup_cherrypy(self):
        self.cherrypy_conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd()),
                'tools.staticdir.dir': './public'
            },

            '/api': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './../public'
            },
        }
        cherrypy.engine.autoreload.match = r'^(?!settings).+'
        cherrypy.engine.timeout_monitor.unsubscribe()
        cherrypy.engine.subscribe('start', self.start_handler)
        cherrypy.engine.subscribe('stop', self.stop_handler)

    def CORS(self):
        """Allow AngularJS apps not on the same server to use our API
        """
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    def start(self):
        try:
            webapp = self
            webapp.api = self

            cherrypy.tools.cors = cherrypy.Tool('before_handler', self.CORS)

            cherrypy.config.update({'server.socket_host': self.listening_ip,
                                    'server.socket_port': int(os.environ.get('PORT', '5000')),
                                    'engine.autoreload_on': False,
                                    'tools.sessions.on': True,
                                    'log.screen': True,
                                    'log.access_file': os.path.join(self.logs_path, 'server_access_logs'),
                                    'log.error_file': os.path.join(self.logs_path, 'server_error_logs'),
                                    })

            # start the cherrypy and block
            cherrypy.quickstart(webapp, "/", self.cherrypy_conf)

        except Exception as ex:
            # no matter what we have to cancel the background thread
            # and exit gracefully
            print("error from cherrypy.quickstart()")
            traceback.format_exception_only(type(ex), ex)
            error_string = traceback.format_exc()
            print("error:" + error_string)
        print("program exited.")

    @cherrypy.expose
    def index(self):
        if os.path.isfile(self.index_file):
            webpage = open(self.index_file).read()
            return webpage
        else:
            return self.index_file

    @cherrypy.expose
    def GET(self, api=None, _=None, **kwargs):
        if not check_auth():
            return error(400, 'Bad Request')
        return self.execute(api, _, **kwargs)

    @cherrypy.expose
    def POST(self, api=None,  _=None, **kwargs):
        if not check_auth():
            return error(400, 'Bad Request')
        return self.execute(api, _, **kwargs)

    def execute(self, api=None, _=None, **kwargs):
        try:
            args = kwargs

            # make sure that api is exists
            if not self.is_api_exists(api):
                response = error(1002, "error:api received doesnt exists")
            else:
                func = self.get_api_func(api)
                response = func(args)

            cherrypy.response.headers['Access-Control-Allow-Origin'] = "*"

        except Exception as ex:
            # print out the error
            print(traceback.format_exc())
            print(sys.exc_info()[0])
            traceback.format_exception_only(type(ex), ex)
            response = error(1002, "from:RobotCmdWebService::execute()\nerror:" + str(ex))

        return response

    def get_api_func(self, api_name):
        apis = [a[1] for a in self.function_list if (a[0].startswith('api_' + api_name))]
        return apis[0]

    def api_get_all_apis(self, *args):
        return self.get_all_apis()

    def get_all_apis(self):
        all_functions = inspect.getmembers(self, inspect.ismethod)
        self.api_list = [a[0][4:] for a in all_functions if (a[0].startswith('api_'))]
        self.function_list = inspect.getmembers(self, inspect.ismethod)

    def is_api_exists(self, api_name):
        return api_name in self.api_list
