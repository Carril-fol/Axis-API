import os
import time
import logging

from flask import request, g

from .extensions import app

app.logger.setLevel(logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO)


@app.before_request
def start_timer():
    """Runs before every request to record the start time."""
    g.start_time = time.time()


@app.after_request
def log_request_info(response):
    start_time = g.pop("start_time", None)
    duration_ms = round((time.time() - start_time) * 1000, 2) if start_time else 0.0

    app.logger.info(
        f"Method: {request.method} | Path: {request.path} | "
        f"Status: {response.status_code} | Duration: {duration_ms}ms"
    )

    return response
