"""Тесты модуля Монте-Карло."""
import pytest
from src.monte_carlo import roll_dices, monte_carlo_simulation, calculate_distribution
from src.exceptions import SimulationError


class TestRollDices:
    def test_count(self):
        result = roll_dices(5)
        assert len(result) == 5

    def test_range(self):
        result = roll_dices(100)
        assert all(1 <= x <= 6 for x in result)

    def test_sides(self):
        result = roll_dices(10, sides=4)
        assert all(1 <= x <= 4 for x in result)


class TestMonteCarloSimulation:
    def test_basic(self):
        freq, prob, mean, mn, mx = monte_carlo_simulation(1000)
        assert len(freq) > 0
        assert 5 <= mn <= mx <= 30
        assert 10 <= mean <= 20

    def test_iterations_10000(self):
        freq, prob, mean, mn, mx = monte_carlo_simulation(10_000)
        assert sum(freq.values()) == 10_000

    def test_negative_iterations(self):
        with pytest.raises(SimulationError):
            monte_carlo_simulation(-1)

    def test_zero_iterations(self):
        with pytest.raises(SimulationError):
            monte_carlo_simulation(0)

    def test_large_simulation(self):
        freq, prob, mean, mn, mx = monte_carlo_simulation(50_000)
        assert sum(freq.values()) == 50_000

    @pytest.mark.parametrize("iters", [100, 1000, 5000, 10000])
    def test_various_iterations(self, iters):
        freq, prob, mean, mn, mx = monte_carlo_simulation(iters)
        assert sum(freq.values()) == iters
        assert 5 <= mean <= 30


class TestCalculateDistribution:
    def test_distribution(self):
        prob = {5: 0.001, 6: 0.005, 17: 0.1, 30: 0.0001}
        dist = calculate_distribution(prob)
        assert dist[5] == 0.1
        assert dist[17] == 10.0
