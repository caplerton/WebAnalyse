"""Functions that supports plotting."""

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
