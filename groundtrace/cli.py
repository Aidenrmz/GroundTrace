"""Command-line interface for GroundTrace."""
from __future__ import annotations

import argparse
import logging
import signal
import threading

import groundtrace
from groundtrace.branding import PRODUCT_NAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _wait_for_stop_signal() -> None:
    """Block portably until Ctrl+C or SIGTERM is received."""
    stop_requested = threading.Event()

    def request_stop(signum: int, frame: object) -> None:
        stop_requested.set()

    signal.signal(signal.SIGINT, request_stop)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, request_stop)

    while not stop_requested.wait(0.5):
        pass


def main() -> None:
    """Run the GroundTrace CLI."""
    parser = argparse.ArgumentParser(
        prog="groundtrace",
        description=f"{PRODUCT_NAME} - local RAG tracing and grounding dashboard",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    serve_parser = subparsers.add_parser(
        "serve",
        help=f"Start the {PRODUCT_NAME} dashboard server",
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=7756,
        help="Server port (default: 7756)",
    )
    serve_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open browser automatically",
    )
    serve_parser.add_argument(
        "--no-intercept",
        action="store_true",
        help="Do not auto-install interceptors",
    )

    args = parser.parse_args()

    if args.command != "serve":
        parser.print_help()
        return

    try:
        url = groundtrace.serve(
            host=args.host,
            port=args.port,
            open_browser=not args.no_browser,
            auto_intercept=not args.no_intercept,
        )
        logger.info("Server started at %s", url)
        logger.info("Press Ctrl+C to stop")
        _wait_for_stop_signal()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down...")
        groundtrace.stop()


if __name__ == "__main__":
    main()
