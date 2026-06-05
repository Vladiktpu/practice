"""Модуль интеграции компонентов."""
import logging
from pathlib import Path
from typing import Dict, Any

from . import config
from .transport_task import solve_transport_task
from .monte_carlo import monte_carlo_simulation, calculate_distribution
from .utils import save_json, print_matrix

logger = logging.getLogger(__name__)


def run_transport_example() -> Dict[str, Any]:
    """Запуск примера транспортной задачи."""
    costs = [
        [3, 1, 7, 4],
        [2, 6, 5, 9],
        [8, 3, 3, 2],
    ]
    supply = [300, 400, 500]
    demand = [250, 350, 400, 200]

    plan, initial, final = solve_transport_task(costs, supply, demand)

    result = {
        "task": "transport",
        "costs": costs,
        "supply": supply,
        "demand": demand,
        "plan": plan,
        "initial_cost": initial,
        "final_cost": final,
        "savings": initial - final,
        "savings_percent": round((initial - final) / initial * 100, 2) if initial else 0,
    }

    logger.info(f"Транспортная задача: {initial} -> {final} (экономия {result['savings_percent']}%)")
    return result


def run_monte_carlo_example() -> Dict[str, Any]:
    """Запуск примера Монте-Карло."""
    frequencies, probabilities, mean, mn, mx = monte_carlo_simulation(
        iterations=100_000,
        dice_count=5,
        dice_sides=6,
    )

    distribution = calculate_distribution(probabilities)

    result = {
        "task": "monte_carlo",
        "iterations": 100_000,
        "dice_count": 5,
        "dice_sides": 6,
        "mean": round(mean, 4),
        "min_sum": mn,
        "max_sum": mx,
        "distribution": distribution,
    }

    logger.info(f"Монте-Карло: среднее={mean:.2f}")
    return result


def run_full_pipeline(output_dir: Path = None) -> Dict[str, Any]:
    """Полный запуск всех модулей."""
    if output_dir is None:
        output_dir = config.REPORTS_DIR

    logger.info("=== Запуск полного конвейера ===")

    transport_result = run_transport_example()
    monte_result = run_monte_carlo_example()

    full_result = {
        "transport_task": transport_result,
        "monte_carlo": monte_result,
    }

    # Сохранение результатов
    save_json(full_result, output_dir / "results.json")
    logger.info(f"Результаты сохранены в {output_dir / 'results.json'}")

    return full_result
