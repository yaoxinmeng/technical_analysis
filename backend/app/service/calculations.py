from scipy.optimize import curve_fit
import numpy as np
from loguru import logger


def _predict_exponential_value(x: int | float, m: float, c: float) -> float:
    """
    Predict the y value for a given x using the exponential regression parameters.

    :param x: The x value.
    :param gr: Growth rate parameter.
    :param v0: Initial value parameter.
    :return: Predicted y value.
    """
    return c + m * x
    

def _exponential_regression(x_data: list[int | float], y_data: list[int | float]) -> tuple[float, float, float]:
    """
    Perform exponential regression on the given data.

    :param x_data: List of x values.
    :param y_data: List of y values.
    :return: Tuple containing the parameters (gr, v0) of the fitted curve.
    """
    # Perform curve fitting
    params, _ = curve_fit(_predict_exponential_value, x_data, y_data)

    return params.tolist()  # m, c


def predict_values(data: list[float]) -> tuple[float, float]:
    """
    Calculate the average growth rate and the predicted average income.

    :param data: List of y values.
    :return: tuple containing the average growth rate and the predicted average income.
    """
    assert len(data) >= 2, "Data must contain at least two points for regression."

    x_data = list(range(len(data)))
    m, c = _exponential_regression(x_data, [_safe_log(y) for y in data])

    predicted_ys = np.exp([_predict_exponential_value(x, m, c) for x in x_data])
    avg_income = sum(predicted_ys) / len(predicted_ys)
    gr = np.exp(m)
    logger.debug(f"Predicted values: {predicted_ys}, Growth Rate: {gr}, Average Income: {avg_income}")
    return gr-1, avg_income


def _safe_log(value: float) -> float:
    """
    Safely compute the logarithm of a value, returning 0 for non-positive inputs.

    :param value: The input value.
    :return: The logarithm of the value or 0 if the value is non-positive.
    """
    if value <= 0:
        return 0.0
    return np.log(value)