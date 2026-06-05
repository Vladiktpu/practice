"""Тесты модуля транспортной задачи."""
import pytest
from src.transport_task import (
    is_balanced,
    balance_task,
    northwest_corner,
    calculate_cost,
    get_basis,
    calculate_potentials,
    calculate_deltas,
    solve_transport_task,
)
from src.exceptions import InvalidMatrixError, BalanceError


class TestIsBalanced:
    def test_balanced(self):
        assert is_balanced([100, 200], [150, 150]) is True

    def test_unbalanced(self):
        assert is_balanced([100, 200], [100, 100]) is False


class TestBalanceTask:
    def test_already_balanced(self):
        costs = [[1, 2], [3, 4]]
        c, s, d = balance_task(costs, [100, 100], [50, 150])
        assert s == [100, 100]
        assert d == [50, 150]

    def test_add_dummy_consumer(self):
        costs = [[1, 2], [3, 4]]
        c, s, d = balance_task(costs, [200, 100], [50, 150])
        assert len(d) == 3
        assert d[-1] == 100

    def test_add_dummy_supplier(self):
        costs = [[1, 2], [3, 4]]
        c, s, d = balance_task(costs, [50, 50], [150, 150])
        assert len(s) == 3
        assert s[-1] == 200


class TestNorthwestCorner:
    def test_simple(self):
        plan = northwest_corner([20, 30], [25, 25])
        assert plan[0][0] == 20
        assert plan[0][1] is None or plan[0][1] == 0  # может быть None или 0
        assert plan[1][0] == 5
        assert plan[1][1] == 25

    def test_3x4(self):
        plan = northwest_corner([300, 400, 500], [250, 350, 400, 200])
        assert plan[0][0] == 250
        assert plan[2][3] == 200


class TestCalculateCost:
    def test_basic(self):
        costs = [[3, 1], [2, 6]]
        plan = [[10, 5], [0, 15]]
        assert calculate_cost(costs, plan) == 3*10 + 1*5 + 6*15


class TestPotentialsAndDeltas:
    def test_calculate_potentials(self):
        costs = [[3, 1, 7], [2, 6, 5]]
        basis = [(0, 0), (0, 1), (1, 1), (1, 2)]
        u, v = calculate_potentials(costs, basis, 2, 3)
        assert u[0] == 0
        assert v[0] == 3
        assert v[1] == 1
        assert u[1] == 5
        assert v[2] == 0

    def test_calculate_deltas(self):
        costs = [[3, 1, 7], [2, 6, 5]]
        basis = [(0, 0), (0, 1), (1, 1), (1, 2)]
        u, v = calculate_potentials(costs, basis, 2, 3)
        deltas = calculate_deltas(costs, u, v, 2, 3, basis)
        assert deltas[0][2] is not None


class TestSolveTransportTask:
    def test_3x4(self):
        costs = [
            [3, 1, 7, 4],
            [2, 6, 5, 9],
            [8, 3, 3, 2],
        ]
        supply = [300, 400, 500]
        demand = [250, 350, 400, 200]
        plan, initial, final = solve_transport_task(costs, supply, demand)
        assert initial > 0
        assert final > 0
        assert final <= initial + 1  # допуск на округление

    def test_unbalanced_auto(self):
        costs = [[1, 2], [3, 4]]
        plan, initial, final = solve_transport_task(costs, [100, 100], [50, 100])
        assert final > 0

    def test_invalid_matrix_empty(self):
        with pytest.raises(InvalidMatrixError):
            solve_transport_task([], [100], [100])

    def test_negative_value(self):
        with pytest.raises(InvalidMatrixError):
            solve_transport_task([[-1, 2], [3, 4]], [100, 100], [100, 100])

    def test_mismatched_dimensions(self):
        with pytest.raises(InvalidMatrixError):
            solve_transport_task([[1, 2], [3, 4]], [100], [50, 50, 100])


class TestParametrized:
    @pytest.mark.parametrize("supply,demand", [
        ([10, 20], [15, 15]),
        ([100, 200, 300], [150, 150, 150, 150]),
        ([5, 5, 5, 5], [10, 10]),
    ])
    def test_various_sizes(self, supply, demand):
        import random
        random.seed(42)
        m = len(supply)
        n = len(demand)
        costs = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        plan, initial, final = solve_transport_task(costs, supply, demand)
        assert final > 0
        assert initial > 0
