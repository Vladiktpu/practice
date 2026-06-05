"""Конфигурация проекта."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
DOCS_DIR = BASE_DIR / "docs"

for d in [DATA_DIR, LOGS_DIR, REPORTS_DIR, DOCS_DIR]:
    d.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "app.log"
REPORT_FILE = REPORTS_DIR / "report.txt"
TEST_LOG = REPORTS_DIR / "report_tests.log"

# Настройки транспортной задачи
DEFAULT_MATRIX_SIZE = (3, 4)
MAX_ITERATIONS = 1000

# Настройки Монте-Карло
DEFAULT_ITERATIONS = 100_000
DICE_COUNT = 5
DICE_SIDES = 6
