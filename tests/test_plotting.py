import pandas as pd
import pytest
import plotly.graph_objects as go
from plotly_qc.plotting import plot_engineering_data


@pytest.fixture
def sample_data():
    """Fixture for creating sample data for tests."""
    data = {
        "value": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "group": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B", "B"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_specs():
    """Fixture for creating sample specifications for tests."""
    specs = {"value": {"LSL": 12, "USL": 18, "Target": 15}}
    return pd.DataFrame(specs)


def test_plot_engineering_data_returns_figure(sample_data, sample_specs):
    """Test if plot_engineering_data returns a plotly Figure object."""
    fig = plot_engineering_data(sample_data, sample_specs, "value")
    assert isinstance(fig, go.Figure)


def test_plot_engineering_data_box_plot(sample_data, sample_specs):
    """Test if a box plot is created correctly."""
    fig = plot_engineering_data(sample_data, sample_specs, "value", plot_type="box")
    assert len(fig.data) > 0
    assert isinstance(fig.data[0], go.Box)


def test_plot_engineering_data_ecdf_plot(sample_data, sample_specs):
    """Test if an ECDF plot is created correctly."""
    fig = plot_engineering_data(sample_data, sample_specs, "value", plot_type="ecdf")
    assert len(fig.data) > 0
    # ECDF plots in plotly express are scatter plots
    assert isinstance(fig.data[0], go.Scatter)


def test_plot_engineering_data_with_group_by(sample_data, sample_specs):
    """Test if grouping works correctly."""
    fig = plot_engineering_data(
        sample_data, sample_specs, "value", plot_type="box", group_by="group"
    )
    assert len(fig.data) == 2  # One box for each group 'A' and 'B'


def test_plot_engineering_data_spec_lines(sample_data, sample_specs):
    """Test if specification lines are added to the plot."""
    fig = plot_engineering_data(sample_data, sample_specs, "value", plot_type="box")
    # Check for 3 horizontal lines (LSL, USL, Target)
    assert len(fig.layout.shapes) == 3


def test_plot_engineering_data_spec_lines_ecdf(sample_data, sample_specs):
    """Test if specification lines are added to the ecdf plot."""
    fig = plot_engineering_data(sample_data, sample_specs, "value", plot_type="ecdf")
    # Check for 3 vertical lines (LSL, USL, Target)
    assert len(fig.layout.shapes) == 3


def test_plot_engineering_data_missing_specs(sample_data):
    """Test that no lines are drawn if specs are missing."""
    empty_specs = pd.DataFrame()
    fig = plot_engineering_data(sample_data, empty_specs, "value")
    assert len(fig.layout.shapes) == 0


def test_plot_engineering_data_partial_specs(sample_data):
    """Test that only available spec lines are drawn."""
    partial_specs = pd.DataFrame({"value": {"LSL": 12}})
    fig = plot_engineering_data(sample_data, partial_specs, "value")
    assert len(fig.layout.shapes) == 1


def test_plot_engineering_data_invalid_plot_type(sample_data, sample_specs):
    """Test if a ValueError is raised for an invalid plot_type."""
    with pytest.raises(ValueError):
        plot_engineering_data(sample_data, sample_specs, "value", plot_type="invalid")


def test_add_spec_lines_exception(sample_data, capsys):
    """Test the exception handling in _add_spec_lines."""
    invalid_specs = pd.DataFrame({"value": {"LSL": "not-a-number"}})
    plot_engineering_data(sample_data, invalid_specs, "value")
    captured = capsys.readouterr()
    assert "Could not draw LSL" in captured.out
