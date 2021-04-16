# from werkzeug.wsgi.middleware.dispatcher import DispatcherMiddleware
from package.login_manager import login_manager
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from dashboard_app import dashboard_app
from flask_app import app


application = DispatcherMiddleware(
    app,
    {
        "/dashboard": dashboard_app.server,
    },
)

if __name__ == "__main__":
    # app1.enable_dev_tools(debug=True)
    # app2.enable_dev_tools(debug=True)
    run_simple("localhost", 8050, application, use_debugger=True, use_reloader=True)
