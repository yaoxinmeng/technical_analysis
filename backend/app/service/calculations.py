from scipy.optimize import curve_fit
import numpy as np
from loguru import logger


def _predict_y_value(x: int | float, m: float, c: float) -> float:
    """
    Predict the y value for a given x using the exponential regression parameters.

    :param x: The x value.
    :param m: Slope parameter.
    :param c: Intercept parameter.
    :return: Predicted y value.
    """
    return c + m * x
    

def _regression(x_data: list[int | float], y_data: list[int | float]) -> tuple[float, float]:
    """
    Perform exponential regression on the given data.

    :param x_data: List of x values.
    :param y_data: List of y values.
    :return: Tuple containing the parameters (gr, v0) of the fitted curve.
    """
    # Perform curve fitting
    params, _ = curve_fit(_predict_y_value, x_data, y_data)

    return params.tolist()  # m, c


def predict_values(y_data: list[float]) -> tuple[float, float]:
    """
    Calculate the average growth rate and the predicted average income.

    :param data: List of y values.
    :return: tuple containing the average growth rate and the predicted average income.
    """
    logger.debug(f"Input data for prediction: {y_data}")
    assert len(y_data) >= 2, "Data must contain at least two points for regression."
    x_data = range(len(y_data))

    # calculate factor to divide y_data to avoid overflow
    min_y = min(y_data)
    factor = 1
    while min_y > 1:
        factor *= 10
        min_y /= 10
    m, c = _regression(x_data, [y / factor for y in y_data])

    predicted_ys = [_predict_y_value(x, m, c) * factor for x in x_data]
    avg_income = sum(predicted_ys) / len(predicted_ys)
    gr = predicted_ys[-1] / predicted_ys[0] if predicted_ys[0] != 0 else 0
    cagr = gr ** (1 / (len(predicted_ys) - 1))  # convert to growth rate
    logger.debug(f"Predicted values: {predicted_ys}, Growth Rate: {cagr}, Average Income: {avg_income}")
    return cagr-1, avg_income


def fallback_predict_average_income(data: list[float]) -> tuple[float, float]:
    """
    Fallback method to calculate average growth rate and predicted average income using CAGR.

    :param data: List of y values.
    :return: tuple containing the average growth rate and the predicted average income.
    """
    n = len(data)
    if n < 2:
        raise ValueError("Insufficient valid data points for CAGR calculation.")
    
    if data[-1] <= 0 or data[0] <= 0:
        cagr = 0.0
    else:
        cagr = (data[-1] / data[0]) ** (1 / (n - 1)) - 1
    avg_income = sum(data) / n
    logger.debug(f"Fallback CAGR: {cagr}, Average Income: {avg_income}")
    return cagr, avg_income
