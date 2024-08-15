"""Functions that supports plotting."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from plot_page.control.data_operations import split_data


#####################################################################################################################################################
def plot_data(data_table: dict[str, list[dict]], plot_setting: list[dict], title: str, x_axis: str, y_axis: str) -> dcc.Graph:
    """Plot the selected tables ans settings.

    Args:
        data_table (dict[str, list[dict]]): All table data.
        plot_setting (list[dict]): The selected plot settings.
        x_axis (str): The selected x_axis attribute.
        y_axis (str): The selected y_axis attribute.

    Returns:
        dcc.Graph: The dcc.Graph that should be plotted.
    """
    fig = go.Figure()
    fig.update_layout(title=title, xaxis_title=x_axis, yaxis_title=y_axis)
    for val in plot_setting:
        if val["type"] == "Line":
            splitted_data = split_data(data_table, val["group_attributes"])
            plot_line(fig, splitted_data, x_axis, y_axis, val)
        if val["type"] == "Bar":
            splitted_data = split_data(data_table, val["group_attributes"])
            plot_bar(fig, splitted_data, x_axis, y_axis, val)

    return dcc.Graph(figure=fig)


#####################################################################################################################################################
def plot_line(fig: go.Figure, splitted_data: dict[str, pd.DataFrame], x_axis: str, y_axis: str, settings: dict) -> None:
    """Add the line to the figure.

    Args:
        fig (go.Figure): The existing figure.
        splitted_data (dict[str, pd.DataFrame]): Dictionary of key and dataframe pair.
        x_axis (str): The selected attribute for the x_axis.
        y_axis (str): The selected attribute for the y_axis.
        settings (dict): The configuration of the line.
    """
    if settings["value"] == "History":
        for key, val in splitted_data.items():
            fig.add_trace(go.Scatter(x=val[x_axis], y=val[y_axis], mode=settings["mode"], name=f"trace_{key}"))

    if settings["value"] == "Min":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].min()
            fig.add_trace(go.Scatter(x=plot_data.index.values, y=plot_data, mode=settings["mode"], name=f"min_{key}"))

    if settings["value"] == "Max":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].max()
            fig.add_trace(go.Scatter(x=plot_data.index.values, y=plot_data, mode=settings["mode"], name=f"max_{key}"))

    if settings["value"] == "Median":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].median()
            fig.add_trace(go.Scatter(x=plot_data.index.values, y=plot_data, mode=settings["mode"], name=f"median_{key}"))

    if settings["value"] == "Mean":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].mean()
            fig.add_trace(go.Scatter(x=plot_data.index.values, y=plot_data, mode=settings["mode"], name=f"mean_{key}"))


#####################################################################################################################################################
def plot_bar(fig: go.Figure, splitted_data: dict[str, pd.DataFrame], x_axis: str, y_axis: str, settings: dict) -> None:
    """Add the line to the figure.

    Args:
        fig (go.Figure): The existing figure.
        splitted_data (dict[str, pd.DataFrame]): Dictionary of key and dataframe pair.
        x_axis (str): The selected attribute for the x_axis.
        y_axis (str): The selected attribute for the y_axis.
        settings (dict): The configuration of the line.
    """
    if settings["value"] == "History":
        for key, val in splitted_data.items():
            fig.add_trace(go.Bar(x=val[x_axis], y=val[y_axis], name=f"trace_{key}"))

    if settings["value"] == "Min":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].min()
            fig.add_trace(go.Bar(x=plot_data.index.values, y=plot_data, name=f"min_{key}"))

    if settings["value"] == "Max":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].max()
            fig.add_trace(go.Bar(x=plot_data.index.values, y=plot_data, name=f"max_{key}"))

    if settings["value"] == "Median":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].median()
            fig.add_trace(go.Bar(x=plot_data.index.values, y=plot_data, name=f"median_{key}"))

    if settings["value"] == "Mean":
        for key, val in splitted_data.items():
            plot_data = val.groupby(by=x_axis)[y_axis].mean()
            fig.add_trace(go.Bar(x=plot_data.index.values, y=plot_data, name=f"mean{key}"))


def plot_correlation_coefficient(loaded_data: pd.DataFrame, main_attribute: str, key: str, factor: float) -> list[dcc.Graph]:
    normalized_factor = (factor - (-1)) / (1 - (-1))

    x_value = loaded_data[key]
    y_value = loaded_data[main_attribute]

    y_min = y_value.min()
    y_max = y_value.max()
    figure = go.Figure()
    figure.update_layout(title=f"Correlation Coefficient {main_attribute} {key} - factor {factor} ", xaxis_title=key, yaxis_title=main_attribute)
    figure.add_trace(go.Scatter(x=x_value, y=y_value, mode="markers", name="Datapoints"))
    # figure.add_trace(
    #     go.Line(
    #         y=[y_max - ((y_max - y_min) * normalized_factor), y_min + ((y_max - y_min) * normalized_factor)],
    #         x=[x_value.min(), x_value.max()],
    #         name="Correlation coefficient",
    #     )
    # )
    figure.add_trace(
        go.Scatter(
            y=[y_max - ((y_max - y_min) * normalized_factor), y_min + ((y_max - y_min) * normalized_factor)],
            x=[x_value.min(), x_value.max()],
            mode="lines",
            name="Linear Regression",
            line=dict(color="red"),  # Initial style
        )
    )

    return dcc.Graph(figure=figure)


def plot_notlinear_regression(
    loaded_data: pd.DataFrame, main_attribute: str, second_attribute, popt, pcov, res_string, model_func
) -> list[dcc.Graph]:
    function_string = res_string.format(*popt)

    x_value = loaded_data[second_attribute]
    y_value = loaded_data[main_attribute]

    function_x = np.linspace(x_value.min(), x_value.max(), 300)
    # y_values = [model_func(x, *popt) for x in function_x]
    test = {"x_value": function_x, "y_value": [model_func(x, *popt) for x in function_x]}
    figure = go.Figure()
    figure.update_layout(
        title=f"Notlinear Regression {main_attribute} {second_attribute} - function {function_string} ",
        xaxis_title=second_attribute,
        yaxis_title=main_attribute,
    )

    figure.add_trace(go.Scatter(x=x_value, y=y_value, mode="markers", name="Datapoints"))
    figure.add_trace(
        go.Scatter(
            x=test["x_value"],
            y=test["y_value"],
            mode="lines+markers",
            name="Linear Regression",
            line=dict(color="red"),  # Initial style
        )
    )
    return [dcc.Graph(figure=figure)]
