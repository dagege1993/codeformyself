#!/usr/bin/env python

from tornado import httpserver, ioloop
from tornado import options as tnd_options
from tornado.options import options, define
from tornado.web import Application as tornadoApp

from api.settings import configs

define("addr", default='0.0.0.0', help="run on the given ip address", type=str)
define("port", default=4030, help="run on the given port", type=int)


class Application(tornadoApp):
    """ 定制 Tornado Application 集成日志、sqlalchemy 等功能 """

    def __init__(self, handlers=None, default_host="", transforms=None, **settings):
        tnd_options.parse_command_line()
        if configs.can_import:
            configs.import_dict(**settings)
        super(Application, self).__init__(handlers, default_host, transforms, **configs)
        http_server = httpserver.HTTPServer(self)
        http_server.listen(options.port, address=options.addr)
        self.io_loop = ioloop.IOLoop.instance()

    def start_server(self):
        """
        启动 tornado 服务
        :return:
        """
        try:
            self.io_loop.start()
        except KeyboardInterrupt:
            self.io_loop.stop()
        except:
            import traceback


if __name__ == '__main__':
    pass
