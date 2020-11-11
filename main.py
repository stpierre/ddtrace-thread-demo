import threading
import time

import ddtrace
import flask

app = flask.Flask(__name__)

DDTRACE_HOST = 'localhost'


@app.before_first_request
def _start_tracing():
    ddtrace.tracer.configure(hostname=DDTRACE_HOST, port=8126)
    ddtrace.patch_all()
    ddtrace.config.analytics_enabled = True
    ddtrace.Pin.override(
        flask.Flask, service='ddtrace-thread-demo', app_type='web')


@ddtrace.tracer.wrap()
def wait():
    time.sleep(5)


@app.route('/')
@ddtrace.tracer.wrap(service='ddtrace-thread-demo')
def hello_world():
    thread = threading.Thread(target=wait)
    thread.start()
    return get_message()


@ddtrace.tracer.wrap()
def get_message():
    return 'Hello, World!'
