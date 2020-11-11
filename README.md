# Datadog APM for Python thread bug demo

To run this demo, first ensure that you have a Datadog agent with APM
enabled running locally. Or, if not locally, modify `DDTRACE_HOST` in
`main.py` to point to your Datadog agent.

Next, run:

```bash
virtualenv -p "$(which python3)" venv
. venv/bin/activate
pip install -r requirements.txt
```

Finally, start the demo server:

```bash
FLASK_APP=main.py flask run
```

Then, in a separate window, run:

```
curl http://localhost:5000/
```

You will notice two kinds of traces appear:

* Most traces appear with the `ddtrace-thread-demo` service name, as
  configured in the application.
* Traces for `main.wait()` appear with the service name
  `unnamed-python-service` because their span does not have a parent
  with the service name -- when running in a separate thread, that
  span has no parent at all AFAICT.
