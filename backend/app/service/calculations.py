from scipy.optimize import curve_fit


def _predict_exponential_value(x: int | float, gr: float, v0: float) -> float:
    """
    Predict the y value for a given x using the exponential regression parameters.

    :param x: The x value.
    :param gr: Growth rate parameter.
    :param v0: Initial value parameter.
    :return: Predicted y value.
    """
    return v0 * gr ** x
    

def _exponential_regression(x_data: list[int | float], y_data: list[int | float]) -> tuple[float, float, float]:
    """
    Perform exponential regression on the given data.

    :param x_data: List of x values.
    :param y_data: List of y values.
    :return: Tuple containing the parameters (gr, v0) of the fitted curve.
    """
    # Perform curve fitting
    params, _ = curve_fit(_predict_exponential_value, x_data, y_data)

    return params.tolist()  # gr, v0


def predict_values(data: list[float]) -> tuple[float, float]:
    """
    Calculate the average growth rate and the predicted average income.

    :param data: List of y values.
    :return: tuple containing the average growth rate and the predicted average income.
    """
    assert len(data) >= 2, "Data must contain at least two points for regression."

    x_data = list(range(len(data)))
    gr, v0 = _exponential_regression(x_data, data)

    return gr, _predict_exponential_value(x_data[-1], gr, v0)
