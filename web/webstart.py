# -*- coding: utf-8 -*-
# Create Date 2015/12/9

from web import create_app, web_listen_ip, web_port, env
from flask.ext.bootstrap import Bootstrap
app = create_app()
bootstrap = Bootstrap(app)
if env != "Production" and env != "Test":
    if __name__ == '__main__':
        # from werkzeug.contrib.fixers import ProxyFix
        # app.wsgi app = ProxyFix(app.wsgi_app)
        app.run(host="127.0.0.1", threaded=True, debug=True, port=int(web_port))

    

