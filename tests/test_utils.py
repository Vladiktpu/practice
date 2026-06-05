"""Тесты вспомогательных функций."""
import pytest
import json
from pathlib import Path
from src.utils import validate_matrix, print_matrix, save_json, load_json
from src.exceptions import InvalidMatrixError


class TestValidateMatrix:
    def test_valid(self):
        validate_matrix([[1, 2], [3, 4]])

    def test_empty(self):
        with pytest.raises(InvalidMatrixError):
            validate_matrix([])

    def test_empty_row(self):
        with pytest.raises(InvalidMatrixError):
            validate_matrix([[]])

    def test_negative(self):
        with pytest.raises(InvalidMatrixError):
            validate_matrix([[1, -2], [3, 4]])

    def test_not_rectangular(self):
        with pytest.raises(InvalidMatrixError):
            validate_matrix([[1, 2, 3], [4, 5]])


class TestPrintMatrix:
    def test_basic(self):
        result = print_matrix([[1, 2], [3, 4]])
        assert "1" in result
        assert "4" in result

    def test_with_title(self):
        result = print_matrix([[1]], "Title")
        assert "Title" in result

    def test_empty(self):
        result = print_matrix([])
        assert "пустая" in result


class TestSaveLoadJson:
    def test_roundtrip(self, tmp_path):
        data = {"key": "value", "num": 42}
        path = tmp_path / "test.json"
        save_json(data, path)
        loaded = load_json(path)
        assert loaded == data
