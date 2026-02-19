"""GroundTrace public API.

Usage:
    import groundtrace
    groundtrace.serve()          # start dashboard + install interceptors
    groundtrace.new_session()    # start a fresh tracing session
    groundtrace.stop()           # stop dashboard
"""
from __future__ import annotations

import logging
import threading
import time
import webbrowser

import uvicorn

from groundtrace.branding import PRODUCT_NAME
from groundtrace.interceptors import install_all, uninstall_all
from groundtrace.pipeline import setup_auto_attribution
from groundtrace.server.app import app
from groundtrace.session_bus import bus

logger = logging.getLogger(__name__)

__version__ = "0.1.0"

# Global server state
_server_thread: threading.Thread | None = None
_server_instance: uvicorn.Server | None = None
_server_lock = threading.Lock()
_server_url = "http://127.0.0.1:7756"


def serve(
    host: str = "127.0.0.1",
    port: int = 7756,
    open_browser: bool = True,
    auto_intercept: bool = True,
) -> str:
    """
    Start the GroundTrace dashboard server in a background thread.
    Install all interceptors and optionally open the dashboard URL.

    Args:
        host: Server host (default: 127.0.0.1).
        port: Server port (default: 7756).
        open_browser: Whether to open browser automatically.
        auto_intercept: Whether to auto-install interceptors.

    Returns:
        The dashboard URL.
    """
    global _server_thread, _server_instance, _server_url

    with _server_lock:
        if _server_thread is not None and _server_thread.is_alive():
            logger.warning("%s server is already running", PRODUCT_NAME)
            return get_session_url(None)

        if auto_intercept:
            installed = install_all()
            logger.info("Installed interceptors: %s", installed)

        setup_auto_attribution()

        config = uvicorn.Config(
            app=app,
            host=host,
            port=port,
            log_level="info",
            access_log=False,
        )
        _server_instance = uvicorn.Server(config)

        def run_server() -> None:
            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_server_instance.serve())

        _server_thread = threading.Thread(target=run_server, daemon=True)
        _server_thread.start()

        time.sleep(0.5)

        dashboard_url = f"http://{host}:{port}"
        _server_url = dashboard_url
        if open_browser:
            threading.Thread(
                target=lambda: webbrowser.open(dashboard_url),
                daemon=True,
            ).start()

        logger.info("%s server running at %s", PRODUCT_NAME, dashboard_url)
        return dashboard_url


def stop() -> None:
    """Stop the dashboard server and uninstall interceptors."""
    global _server_thread, _server_instance

    with _server_lock:
        if _server_instance is not None:
            logger.info("Stopping %s server...", PRODUCT_NAME)
            _server_instance.should_exit = True

            if _server_thread is not None:
                _server_thread.join(timeout=5)
            _server_thread = None
            _server_instance = None

        uninstall_all()
        logger.info("Uninstalled interceptors")


def new_session() -> str:
    """
    Start a fresh tracing session.

    Returns:
        Session ID.
    """
    session = bus.new_session()
    logger.info("Created new session: %s", session.id)
    return session.id


def get_session_url(session_id: str | None = None) -> str:
    """
    Return the dashboard URL for a specific session.

    Args:
        session_id: Session ID. If omitted, returns the dashboard root URL.

    Returns:
        Dashboard URL for the session.
    """
    if session_id:
        return f"{_server_url}/sessions/{session_id}"
    return _server_url


__all__ = [
    "serve",
    "stop",
    "new_session",
    "get_session_url",
    "__version__",
]
