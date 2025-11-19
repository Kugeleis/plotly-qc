from typing import Any, Dict, Literal, Protocol

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Define a protocol for plotters
class Plotter(Protocol):
    """Protocol for creating a plot."""

    def create_plot(
        self, df_data: pd.DataFrame, column_name: str, group_by: str | None
    ) -> tuple[go.Figure, Literal["h", "v"]]:
        """Creates a plot and returns the figure and line orientation."""
        ...


# Concrete implementation for Box Plot
class BoxPlotter:
    """A plotter for creating box plots."""

    def create_plot(
        self, df_data: pd.DataFrame, column_name: str, group_by: str | None
    ) -> tuple[go.Figure, Literal["h", "v"]]:
        fig = px.box(
            df_data,
            y=column_name,
            x=group_by,
            color=group_by,
            title=f"Boxplot: {column_name}",
        )
        return fig, "h"


# Concrete implementation for ECDF Plot
class EcdfPlotter:
    """A plotter for creating ECDF plots."""

    def create_plot(
        self, df_data: pd.DataFrame, column_name: str, group_by: str | None
    ) -> tuple[go.Figure, Literal["h", "v"]]:
        fig = px.ecdf(
            df_data,
            x=column_name,
            color=group_by,
            title=f"Cumulative Frequency: {column_name}",
        )
        return fig, "v"


# Factory to get the plotter
def get_plotter(plot_type: str) -> Plotter:
    """Factory function to get the appropriate plotter."""
    if plot_type == "box":
        return BoxPlotter()
    elif plot_type == "ecdf":
        return EcdfPlotter()
    else:
        raise ValueError("plot_type must be 'box' or 'ecdf'.")


def _add_spec_lines(
    fig: go.Figure,
    df_specs: pd.DataFrame,
    column_name: str,
    orientation: Literal["h", "v"],
):
    """Adds specification lines to a plot."""
    specs_to_draw: Dict[str, Dict[str, Any]] = {
        "LSL": {"color": "red", "dash": "dash"},
        "Target": {"color": "green", "dash": "dot"},
        "USL": {"color": "red", "dash": "dash"},
    }

    if column_name in df_specs.columns:
        for spec_name, style in specs_to_draw.items():
            try:
                if spec_name in df_specs.index:
                    val = df_specs.loc[spec_name, column_name]
                    if pd.notna(val):
                        annotation = f"{spec_name}: {val}"
                        if orientation == "h":
                            fig.add_hline(
                                y=val,
                                line_dash=style["dash"],
                                line_color=style["color"],
                                annotation_text=annotation,
                            )
                        else:
                            fig.add_vline(
                                x=val,
                                line_dash=style["dash"],
                                line_color=style["color"],
                                annotation_text=annotation,
                                annotation_position="top right",
                            )
            except Exception as e:
                print(f"Could not draw {spec_name}: {e}")


def plot_engineering_data(
    df_data: pd.DataFrame,
    df_specs: pd.DataFrame,
    column_name: str,
    plot_type: str = "box",
    group_by: str | None = None,
) -> go.Figure:
    """
    Creates a plot (Boxplot or ECDF) with automatically drawn specification limits.

    Args:
        df_data (pd.DataFrame): Table with the measurement values.
        df_specs (pd.DataFrame): Table with limits. Must have indices like 'LSL', 'USL', 'Target'.
                                 Column names must match df_data.
        column_name (str): The name of the column to be analyzed.
        plot_type (str): 'box' or 'ecdf'.
        group_by (str, optional): Column for grouping (e.g., 'Charge' or 'Machine').

    Returns:
        plotly.graph_objects.Figure
    """
    plotter = get_plotter(plot_type)
    fig, orientation = plotter.create_plot(df_data, column_name, group_by)
    _add_spec_lines(fig, df_specs, column_name, orientation)
    return fig
