"""Интеграционные тесты проекта."""
import pytest
from src.integration import run_transport_example, run_monte_carlo_example, run_full_pipeline
from src.config import REPORTS_DIR


class TestIntegration:
    def test_transport_example(self):
        result = run_transport_example()
        assert result["task"] == "transport"
        assert result["initial_cost"] > result["final_cost"]
        assert result["savings"] >= 0

    def test_monte_carlo_example(self):
        result = run_monte_carlo_example()
        assert result["task"] == "monte_carlo"
        assert result["iterations"] == 100_000
        assert 5 <= result["mean"] <= 30

    def test_full_pipeline(self):
        result = run_full_pipeline(REPORTS_DIR)
        assert "transport_task" in result
        assert "monte_carlo" in result
        assert result["transport_task"]["final_cost"] > 0
        assert result["monte_carlo"]["mean"] > 0

    def test_pipeline_creates_files(self, tmp_path):
        result = run_full_pipeline(tmp_path)
        assert (tmp_path / "results.json").exists()
