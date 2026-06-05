"""Вспомогательные функции."""
import json
import logging
from pathlib import Path

from .exceptions import InvalidMatrixError


def setup_logging(log_file: Path) -> None:
    """Настройка логирования."""
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


def validate_matrix(matrix: list[list]) -> None:
    """Проверка корректности матрицы."""
    if not matrix or not matrix[0]:
        raise InvalidMatrixError("Матрица пустая")
    cols = len(matrix[0])
    for row in matrix:
        if len(row) != cols:
            raise InvalidMatrixError("Непрямоугольная матрица")
        for val in row:
            if val < 0:
                raise InvalidMatrixError("Отрицательное значение в матрице")


def print_matrix(matrix: list[list], title: str = "") -> str:
    """Форматированный вывод матрицы."""
    if title:
        lines = [title]
    else:
        lines = []
    if not matrix:
        lines.append("[пустая матрица]")
        return "\n".join(lines)

    max_val = max(max(row) for row in matrix)
    width = len(str(max_val)) + 2

    for row in matrix:
        line = "".join(f"{val:>{width}d}" for val in row)
        lines.append(line)
    return "\n".join(lines)


def save_json(data, path: Path) -> None:
    """Сохранение данных в JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: Path):
    """Загрузка данных из JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
