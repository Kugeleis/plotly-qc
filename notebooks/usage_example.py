import marimo

__generated_with = "0.17.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    mo.md("# Welcome to a marimo notebook to explain the package usage! 🌊🍃")
    return (mo,)


@app.cell
def _():
    import numpy as np
    import pandas as pd
    from plotly_qc.plotting import plot_engineering_data
    return np, pd, plot_engineering_data


@app.cell
def _(mo):
    mo.md("""
    # Plotly QC Package Usage Example
    """)
    return


@app.cell
def _(mo):
    mo.md("## 1. Introduction")
    mo.md(
        "This notebook demonstrates how to use the `plot_engineering_data` function "
        "from the `plotly-qc` package. This function allows you to create "
        "engineering plots like box plots and ECDF plots with specification limits."
    )
    return


@app.cell
def _(mo, np, pd):
    mo.md("## 2. Sample Data Preparation")
    mo.md(
        "First, let's create some sample data and specification limits as pandas "
        "DataFrames."
    )

    # Create a realistic dataset
    np.random.seed(42)
    data = {
        "value": np.concatenate(
            [
                np.random.normal(15, 1.5, 50),  # Batch A around target
                np.random.normal(16, 1.0, 50),  # Batch B slightly higher
                np.random.normal(14, 2.0, 50),  # Batch C with more variance
            ]
        ),
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50,
    }
    df_data = pd.DataFrame(data)

    # Create specification limits
    specs = {"value": {"LSL": 12, "USL": 18, "Target": 15}}
    df_specs = pd.DataFrame(specs)
    return df_data, df_specs


@app.cell
def _(df_data, mo):
    mo.md("### Sample Data (`df_data`)")
    mo.ui.table(df_data.head())
    return


@app.cell
def _(df_specs, mo):
    mo.md("### Specification Limits (`df_specs`)")
    mo.ui.table(df_specs)
    return


@app.cell
def _(df_data, df_specs, mo, plot_engineering_data):
    mo.md("## 3. Creating a Box Plot")
    mo.md(
        "Here is a simple box plot of the `value` column with the specification "
        "limits drawn."
    )
    plot_engineering_data(df_data, df_specs, "value", plot_type="box")
    return


@app.cell
def _(df_data, df_specs, mo, plot_engineering_data):
    mo.md("## 4. Creating an ECDF Plot")
    mo.md(
        "Here is an ECDF plot of the `value` column with the specification "
        "limits drawn."
    )
    fig_ecdf = plot_engineering_data(df_data, df_specs, "value", plot_type="ecdf",group_by="group")
    mo.md(f"""
    {mo.as_html(fig_ecdf)}

    - `refs: {mo.refs()}`
    - `defs: {mo.defs()}`
    """)
    return


@app.cell
def _(df_data, df_specs, mo, plot_engineering_data):
    mo.md("## 5. Creating a Grouped Box Plot")
    mo.md(
        "The function also supports grouping by a specific column. Here, we group "
        "the data by the `group` column."
    )
    fig_grouped_box = plot_engineering_data(
        df_data, df_specs, "value", plot_type="box", group_by="group"
    )
    mo.md(f"""
    {mo.as_html(fig_grouped_box)}
    - `refs: {mo.refs()}`
    - `defs: {mo.defs()}`
    """)
    return


if __name__ == "__main__":
    app.run()
