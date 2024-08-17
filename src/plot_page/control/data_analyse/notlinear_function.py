import math


def linear_model(x, a, c) -> float:
    return a * x + c


def quadratic_model(x, a, b, c) -> float:
    return a * x**2 + b * x + c


def exponential_model(x, a, b, c) -> float:
    return a * math.e ** (b * x) + c


def logarithmic_model(x, a, b, c) -> float:
    return a * math.log(b * x) + c


def power_model(x, a, b, c) -> float:
    return a * x**b + c


def sinus_model(x, a, b, c) -> float:
    return a * math.sin(b * x + c)


def gaussian_model(x, a, b, c, d) -> float:
    return a * math.e ** (-((x - b) ** 2) / (2 * c**2)) + d


def polynomial3_model(x, a, b, c, d) -> float:
    return a * x**3 + b * x**2 + c * x + d


def polynomial4_model(x, a, b, c, d, e) -> float:
    return a * x**4 + b * x**3 + c * x**2 + d * x + e


def polynomial5_model(x, a, b, c, d, e, f) -> float:
    return a * x**5 + b * x**4 + c * x**3 + d * x**2 + e * x + f
