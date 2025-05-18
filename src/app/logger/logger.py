import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, ClassVar
from datetime import datetime
from colorama import Fore, Style, init
import threading
from core.config import settings
# Initialize colorama for Windows support
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    # Map level names to colors
    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }
    
    # Map level numbers to level names for lookup
    LEVEL_NAMES = {
        logging.DEBUG: 'DEBUG',
        logging.INFO: 'INFO',
        logging.WARNING: 'WARNING',
        logging.ERROR: 'ERROR',
        logging.CRITICAL: 'CRITICAL'
    }

    def format(self, record):
        # Color the level name
        if record.levelno in self.LEVEL_COLORS:
            levelname = self.LEVEL_NAMES.get(record.levelno, 'UNKNOWN')
            record.levelname = f"{self.LEVEL_COLORS[record.levelno]}{levelname}{Style.RESET_ALL}"
        
        # Color the message with the same color as the level
        if record.levelno in self.LEVEL_COLORS:
            record.msg = f"{self.LEVEL_COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}"
        
        return super().format(record)

class Logger:
    _instance: ClassVar[Optional['Logger']] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._logger = logging.getLogger(settings.PROJECT_NAME)
        self._logger.setLevel(logging.DEBUG)

        # Prevent adding handlers multiple times
        if self._logger.handlers:
            self._initialized = True
            return

        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)

        # File Handler - use current date in filename
        file_handler = RotatingFileHandler(
            filename=log_dir / f'{settings.PROJECT_NAME.lower()}.log',  # Remove date from filename
            maxBytes=10*1024*1024,  # 10MB
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
        
        self._initialized = True

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        return cls().logger

logger = Logger.get_logger()