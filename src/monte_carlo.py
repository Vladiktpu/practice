"""Модуль статистического моделирования методом Монте-Карло."""
import random
import logging
from typing import List, Dict, Tuple
from collections import Counter

from .exceptions import SimulationError

logger = logging.getLogger(__name__)


def roll_dices(count: int = 5, sides: int = 6) -> List[int]:
    """Бросок заданного количества кубиков."""
    return [random.randint(1, sides) for _ in range(count)]


def monte_carlo_simulation(
    iterations: int = 100_000,
    dice_count: int = 5,
    dice_sides: int = 6,
) -> Tuple[Dict[int, int], Dict[int, float], float, int, int]:
    """Статистическое моделирование бросков кубиков.

    Returns:
        frequencies: частоты сумм
        probabilities: вероятности сумм
        mean: среднее значение
        min_sum: минимальная сумма
        max_sum: максимальная сумма
    """
    if iterations <= 0:
        raise SimulationError("Количество итераций должно быть положительным")
    if not isinstance(iterations, int):
        raise SimulationError("Количество итераций должно быть целым числом")

    logger.info(f"Запуск симуляции: {iterations} итераций, {dice_count}d{dice_sides}")

    results = []
    min_sum = dice_count * 1
    max_sum = dice_count * dice_sides

    for _ in range(iterations):
        roll = roll_dices(dice_count, dice_sides)
        results.append(sum(roll))

    frequencies = Counter(results)
    probabilities = {
        s: frequencies.get(s, 0) / iterations
        for s in range(min_sum, max_sum + 1)
    }

    mean = sum(results) / iterations
    actual_min = min(results)
    actual_max = max(results)

    logger.info(f"Симуляция завершена: среднее={mean:.2f}, min={actual_min}, max={actual_max}")

    return frequencies, probabilities, mean, actual_min, actual_max


def calculate_distribution(
    probabilities: Dict[int, float],
) -> Dict[int, float]:
    """Форматирование распределения вероятностей."""
    return {k: round(v * 100, 4) for k, v in sorted(probabilities.items())}
