"""Модуль транспортной задачи методом потенциалов."""
import logging
from typing import List, Tuple, Optional

from .exceptions import InvalidMatrixError, BalanceError
from .utils import validate_matrix

logger = logging.getLogger(__name__)


def is_balanced(supply: List[int], demand: List[int]) -> bool:
    """Проверка баланса задачи."""
    return sum(supply) == sum(demand)


def balance_task(
    costs: List[List[int]],
    supply: List[int],
    demand: List[int],
) -> Tuple[List[List[int]], List[int], List[int]]:
    """Добавление фиктивного поставщика или потребителя при дисбалансе."""
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply == total_demand:
        return costs, supply, demand

    costs = [row[:] for row in costs]
    supply = supply[:]
    demand = demand[:]

    if total_supply > total_demand:
        # Фиктивный потребитель
        diff = total_supply - total_demand
        for row in costs:
            row.append(0)
        demand.append(diff)
        logger.info(f"Добавлен фиктивный потребитель: {diff}")
    else:
        # Фиктивный поставщик
        diff = total_demand - total_supply
        costs.append([0] * len(demand))
        supply.append(diff)
        logger.info(f"Добавлен фиктивный поставщик: {diff}")

    return costs, supply, demand


def northwest_corner(
    supply: List[int],
    demand: List[int],
) -> List[List[Optional[int]]]:
    """Метод северо-западного угла для построения опорного плана."""
    m = len(supply)
    n = len(demand)
    plan = [[None] * n for _ in range(m)]

    i = j = 0
    supply_copy = supply[:]
    demand_copy = demand[:]

    while i < m and j < n:
        amount = min(supply_copy[i], demand_copy[j])
        plan[i][j] = amount
        supply_copy[i] -= amount
        demand_copy[j] -= amount

        if supply_copy[i] == 0 and i < m - 1:
            i += 1
        elif demand_copy[j] == 0 and j < n - 1:
            j += 1
        elif supply_copy[i] == 0 and demand_copy[j] == 0:
            if i < m - 1 and j < n - 1:
                # Вырожденный случай — фиктивный ноль
                plan[i][j + 1] = 0
            i += 1
            j += 1

    logger.info(f"Опорный план построен: {m}x{n}")
    return plan


def calculate_cost(
    costs: List[List[int]],
    plan: List[List[Optional[int]]],
) -> int:
    """Подсчёт стоимости перевозок."""
    total = 0
    for i in range(len(costs)):
        for j in range(len(costs[0])):
            if plan[i][j] is not None:
                total += costs[i][j] * plan[i][j]
    return total


def get_basis(plan: List[List[Optional[int]]]) -> List[Tuple[int, int]]:
    """Получение списка базисных клеток."""
    basis = []
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] is not None:
                basis.append((i, j))
    return basis


def calculate_potentials(
    costs: List[List[int]],
    basis: List[Tuple[int, int]],
    m: int,
    n: int,
) -> Tuple[List[Optional[int]], List[Optional[int]]]:
    """Вычисление потенциалов u_i и v_j."""
    u = [None] * m
    v = [None] * n
    u[0] = 0

    changed = True
    iterations = 0
    while changed and iterations < m * n:
        changed = False
        iterations += 1
        for i, j in basis:
            if u[i] is not None and v[j] is None:
                v[j] = costs[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = costs[i][j] - v[j]
                changed = True

    return u, v


def calculate_deltas(
    costs: List[List[int]],
    u: List[Optional[int]],
    v: List[Optional[int]],
    m: int,
    n: int,
    basis: List[Tuple[int, int]],
) -> List[List[Optional[int]]]:
    """Вычисление оценок свободных клеток."""
    deltas = [[None] * n for _ in range(m)]
    basis_set = set(basis)

    for i in range(m):
        for j in range(n):
            if (i, j) not in basis_set and u[i] is not None and v[j] is not None:
                deltas[i][j] = costs[i][j] - (u[i] + v[j])

    return deltas


def find_cycle(
    basis: List[Tuple[int, int]],
    entering: Tuple[int, int],
    m: int,
    n: int,
) -> Optional[List[Tuple[int, int]]]:
    """Поиск цикла пересчёта."""
    from collections import deque

    basis_set = set(basis)
    basis_set.add(entering)

    def neighbors(cell):
        """Соседи по строке или столбцу."""
        i, j = cell
        result = []
        for bi, bj in basis_set:
            if bi == i and bj != j:
                result.append((bi, bj))
            elif bj == j and bi != i:
                result.append((bi, bj))
        return result

    # BFS для поиска цикла
    start = entering
    queue = deque([(start, [start], 0)])  # (cell, path, direction)
    visited = set()

    while queue:
        cell, path, direction = queue.popleft()

        for next_cell in neighbors(cell):
            if next_cell == start and len(path) >= 4:
                return path

            # Чередование направлений
            same_row = (cell[0] == next_cell[0])
            if direction == 1 and same_row:
                continue
            if direction == 0 and not same_row:
                continue

            if next_cell not in visited or next_cell == start:
                new_path = path + [next_cell]
                queue.append((next_cell, new_path, 1 - direction))

        visited.add(cell)

    return None


def recalculate_plan(
    plan: List[List[Optional[int]]],
    cycle: List[Tuple[int, int]],
) -> List[List[Optional[int]]]:
    """Пересчёт плана по циклу."""
    plan = [row[:] for row in plan]

    # Чередование знаков: + - + -
    minus_cells = [cycle[i] for i in range(1, len(cycle), 2)]

    # Минимальное значение в клетках со знаком минус
    theta = min(plan[i][j] for i, j in minus_cells if plan[i][j] is not None)

    for idx, (i, j) in enumerate(cycle):
        if plan[i][j] is None:
            plan[i][j] = 0
        if idx % 2 == 0:
            plan[i][j] += theta
        else:
            plan[i][j] -= theta

    # Удаление нулевых клеток (кроме одной)
    zero_basis = None
    for i, j in minus_cells:
        if plan[i][j] == 0:
            if zero_basis is None:
                zero_basis = (i, j)
            else:
                plan[i][j] = None

    return plan


def solve_transport_task(
    costs: List[List[int]],
    supply: List[int],
    demand: List[int],
    max_iter: int = 1000,
) -> Tuple[List[List[Optional[int]]], int, int]:
    """Решение транспортной задачи методом потенциалов."""
    validate_matrix(costs)

    if len(costs) != len(supply) or len(costs[0]) != len(demand):
        raise InvalidMatrixError("Размеры матрицы не совпадают с supply/demand")

    # Балансировка
    costs, supply, demand = balance_task(costs, supply, demand)
    m, n = len(supply), len(demand)

    if not is_balanced(supply, demand):
        raise BalanceError("Задача не сбалансирована после коррекции")

    # Опорный план
    plan = northwest_corner(supply, demand)
    initial_cost = calculate_cost(costs, plan)
    logger.info(f"Начальная стоимость: {initial_cost}")

    # Оптимизация
    for iteration in range(max_iter):
        basis = get_basis(plan)

        # Добавление фиктивных нулей при вырожденности
        while len(basis) < m + n - 1:
            for i in range(m):
                for j in range(n):
                    if plan[i][j] is None:
                        plan[i][j] = 0
                        basis = get_basis(plan)
                        break
                if len(basis) >= m + n - 1:
                    break

        u, v = calculate_potentials(costs, basis, m, n)
        deltas = calculate_deltas(costs, u, v, m, n, basis)

        # Поиск отрицательной оценки
        min_delta = 0
        entering = None
        for i in range(m):
            for j in range(n):
                if deltas[i][j] is not None and deltas[i][j] < min_delta:
                    min_delta = deltas[i][j]
                    entering = (i, j)

        if entering is None:
            logger.info(f"Оптимум достигнут за {iteration} итераций")
            break

        # Поиск цикла
        cycle = find_cycle(basis, entering, m, n)
        if cycle is None:
            logger.warning("Цикл не найден")
            break

        plan = recalculate_plan(plan, cycle)
        logger.info(f"Итерация {iteration + 1}: стоимость = {calculate_cost(costs, plan)}")

    final_cost = calculate_cost(costs, plan)
    return plan, initial_cost, final_cost
