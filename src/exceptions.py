"""Пользовательские исключения."""


class InvalidMatrixError(ValueError):
    """Ошибка: некорректная матрица."""
    pass


class BalanceError(ValueError):
    """Ошибка: задача несбалансирована."""
    pass


class SimulationError(ValueError):
    """Ошибка: некорректные параметры симуляции."""
    pass
