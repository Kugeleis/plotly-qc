import plotly.express as px
import pandas as pd


def plot_engineering_data(
    df_data, df_specs, column_name, plot_type="box", group_by=None
):
    """
    Erstellt einen Plot (Boxplot oder ECDF) mit automatisch eingezeichneten Spezifikationsgrenzen.

    Args:
        df_data (pd.DataFrame): Tabelle mit den Messwerten.
        df_specs (pd.DataFrame): Tabelle mit Limits. Muss Indizes wie 'LSL', 'USL', 'Target' haben. Spaltennamen müssen mit df_data übereinstimmen.
        column_name (str): Der Name der Spalte, die analysiert werden soll.
        plot_type (str): 'box' oder 'ecdf'.
        group_by (str, optional): Spalte für Gruppierung (z.B. 'Charge' oder 'Maschine').

    Returns:
        plotly.graph_objects.Figure
    """

    # 1. Basis-Plot erstellen
    if plot_type == "box":
        fig = px.box(
            df_data,
            y=column_name,
            x=group_by,
            color=group_by,
            title=f"Boxplot: {column_name}",
        )
        orientation = "h"  # Horizontal lines needed

    elif plot_type == "ecdf":
        fig = px.ecdf(
            df_data,
            x=column_name,
            color=group_by,
            title=f"Cumulative Frequency: {column_name}",
        )
        orientation = "v"  # Vertical lines needed

    else:
        raise ValueError("plot_type muss 'box' oder 'ecdf' sein.")

    # 2. Spezifikationen auslesen (Fehlertolerant)
    # Wir versuchen, die Werte aus dem Spec-Dataframe zu holen.
    # Wenn der Wert NaN ist oder die Spalte fehlt, passiert nichts.
    specs_to_draw = {
        "LSL": {"color": "red", "dash": "dash"},
        "Target": {"color": "green", "dash": "dot"},  # oder 'solid'
        "USL": {"color": "red", "dash": "dash"},
    }

    if column_name in df_specs.columns:
        for spec_name, style in specs_to_draw.items():
            try:
                # Versuchen, den Wert über den Index (z.B. "LSL") zu greifen
                if spec_name in df_specs.index:
                    val = df_specs.loc[spec_name, column_name]

                    # Nur zeichnen, wenn val eine gültige Zahl ist (kein NaN)
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
                print(f"Konnte {spec_name} nicht zeichnen: {e}")

    return fig
