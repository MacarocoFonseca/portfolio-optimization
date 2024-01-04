from json import load
from textwrap import indent

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import yfinance as yf


def load_heading():
    """The function that displays the heading.
    Provides instructions to the user
    """
    st.set_page_config(layout="wide")
    with st.container():
        st.title("Portfolio Analysis")
        header = st.subheader(
            "This App performs historical portfolio analysis and future analysis with Monte Carlo Simulation"
        )
        st.subheader("Please read the instructions carefully and enjoy!")
        # st.text('This is some text.')


def run():
    load_heading()

    TICKER = "^GSPC"
    SP500 = yf.Ticker(ticker=TICKER)
    data = SP500.history(period="max")

    # Convert the index to timezone-naive datetime.date
    data.index = data.index.tz_localize(None).date

    # Date range selector
    st.sidebar.title("Filters")
    start_date, end_date = st.sidebar.date_input(
        "Select date range",
        value=[min(data.index), max(data.index)],
        min_value=min(data.index),
        max_value=max(data.index),
    )

    # Filtered data based on selection
    filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]

    # Plotly figure for closing price
    fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_data.index,
                y=filtered_data["Close"],
                mode="lines",
                name="Close",
            )
        ]
    )
    fig.update_layout(
        title="S&P 500 Closing Price",
        xaxis_title="Date",
        yaxis_title="Closing Price",
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Create two columns for the plots
    col1, col2 = st.columns(2)

    # Plot closing price
    col1.write("## Closing Price Chart")
    plt.figure(figsize=(10, 5))
    plt.plot(data["Close"])
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    col1.pyplot(fig=plt)

    if col2.checkbox("Show raw data"):
        col2.write(data)

    # Extra
    slider_val = st.slider(label="Slide me", min_value=0, max_value=100)
    st.write(f"You selected: {slider_val}")


if __name__ == "__main__":
    run()
