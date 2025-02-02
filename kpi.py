import pandas as pd
import plotly.express as px

df = pd.read_csv("logs/logs.csv", sep=";")

timeline = px.histogram(
    df, x="date", color="ai", title="Nombre de potions générées par jour",
    labels={"date": "Date", "ai": "Type", "count": "Nombre de potions"},
    nbins=500
)

timeline.update_layout(
    xaxis_title="Date",
    yaxis_title="Nombre de potions",
    title="Nombre de potions générées par jour",
    legend_title="Type",
    legend_orientation="h",
    legend_x=0.5,
    legend_xanchor="center"
)

timeline.show()