import logging
import sys

_CONFIGURED = False


def configure_logging(debug: bool = True) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    level = logging.DEBUG if debug else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
    )
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]

    # Giảm nhiễu từ thư viện bên thứ ba ngay cả khi debug.
    for noisy in ("httpcore", "httpx", "prisma.engine._http", "prisma.engine._query"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
