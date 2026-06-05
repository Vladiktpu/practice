#!/usr/bin/env python3
"""Главный файл проекта — точка входа."""
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import LOG_FILE, REPORTS_DIR
from src.utils import setup_logging
from src.integration import run_full_pipeline


def main():
    """Главная функция."""
    setup_logging(LOG_FILE)

    print("=" * 50)
    print("УЧЕБНАЯ ПРАКТИКА: ПМ.02 Интеграция модулей")
    print("Крестьянов Владислав Игоревич, ДИС-301")
    print("=" * 50)

    results = run_full_pipeline(REPORTS_DIR)

    # Вывод результатов
    print("\n--- РЕЗУЛЬТАТЫ ---")

    tr = results["transport_task"]
    print(f"\n[Транспортная задача]")
    print(f"  Начальная стоимость: {tr['initial_cost']}")
    print(f"  Конечная стоимость:   {tr['final_cost']}")
    print(f"  Экономия:             {tr['savings']} ({tr['savings_percent']}%)")

    mc = results["monte_carlo"]
    print(f"\n[Метод Монте-Карло]")
    print(f"  Итераций:    {mc['iterations']}")
    print(f"  Среднее:       {mc['mean']}")
    print(f"  Диапазон:      {mc['min_sum']} - {mc['max_sum']}")
    print(f"  Результаты сохранены в reports/")

    print("\n" + "=" * 50)
    print("Работа завершена успешно!")
    print("=" * 50)


if __name__ == "__main__":
    main()
