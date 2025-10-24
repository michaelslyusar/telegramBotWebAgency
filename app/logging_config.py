"""
WWWizards Telegram Bot - Logging Configuration
"""
import sys
from pathlib import Path
from typing import Any, Dict

from loguru import logger

from app.config import settings


def setup_logging() -> None:
    """Configure application logging."""
    # Remove default logger
    logger.remove()
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Console logging
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )
    
    # File logging - General logs
    logger.add(
        logs_dir / "bot.log",
        format=log_format,
        level=settings.LOG_LEVEL,
        rotation="1 day",
        retention="30 days",
        compression="zip",
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )
    
    # File logging - Error logs
    logger.add(
        logs_dir / "errors.log",
        format=log_format,
        level="ERROR",
        rotation="1 week",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    # File logging - Access logs (for webhooks if needed)
    logger.add(
        logs_dir / "access.log",
        format=log_format,
        level="INFO",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        filter=lambda record: record["extra"].get("type") == "access",
    )
    
    logger.info("Logging configured successfully")


def get_logger(name: str) -> Any:
    """Get a logger instance with a specific name."""
    return logger.bind(name=name)


def log_user_action(user_id: int, action: str, **kwargs: Any) -> None:
    """Log user actions for analytics."""
    logger.info(
        f"User action: {action}",
        user_id=user_id,
        action=action,
        **kwargs,
    )


def log_bot_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """Log bot errors with context."""
    logger.error(
        f"Bot error: {error}",
        error=str(error),
        error_type=type(error).__name__,
        context=context or {},
    )


def log_storage_operation(operation: str, success: bool, **kwargs: Any) -> None:
    """Log storage operations."""
    level = "INFO" if success else "ERROR"
    logger.log(
        level,
        f"Storage operation: {operation}",
        operation=operation,
        success=success,
        **kwargs,
    )

