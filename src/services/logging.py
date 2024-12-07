import sys

from loguru import logger


def configure_logger() -> None:
    log_format_all = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <9}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n{exception}"
    log_format_update = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <9}</level> | {extra[update_type]} | {message}\n{exception}"

    def log_format(record: "Record") -> str:  # type: ignore
        if record["level"].name == "UPDATE":
            return log_format_update
        return log_format_all

    logger.remove()
    logger.add(sys.stdout, colorize=True, format=log_format, diagnose=True, backtrace=True)
    logger.level("DEBUG", color="<fg #7f7f7f>")
    logger.level("INFO", color="<white>")
    logger.level("SUCCESS", color="<green>")
    logger.level("WARNING", color="<yellow>")
    logger.level("ERROR", color="<red>")
    logger.level("CRITICAL", color="<bold><white><RED>")
    logger.level("UPDATE", no=38, color="<magenta>")
