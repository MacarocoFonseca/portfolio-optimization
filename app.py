from json import load
from textwrap import indent
import pandas as pd

import matplotlib.pyplot as plt

import yfinance as yf
import plotly.graph_objs as go
import streamlit as st


def load_heading():
    """The function that displays the heading.
    Provides instructions to the user
    """
    st.set_page_config(layout="wide")
    with st.container():
        st.title("Portfolio Analysis of multiple assets")
        header = st.subheader(
            "This App performs historical portfolio analysis and future analysis with Monte Carlo Simulation"
        )
        st.subheader("Please read the instructions carefully and enjoy!")
        # st.text('This is some text.')


def run():
    load_heading()

    # Sidebar
    st.sidebar.title("Ticker selection")

    # Sidebar for ticker selection
    TICKERS = ["^GSPC", "AAPL", "MSFT", "GOOGL"]
    selected_tickers = st.sidebar.multiselect(
        "Select tickers", TICKERS, default=["^GSPC"]
    )

    # Date range selector
    st.sidebar.title("Filters")
    start_date, end_date = st.sidebar.date_input(
        "Select date range",
        value=[pd.to_datetime("2000-01-01"), pd.to_datetime("today")],
    )  # type: ignore

    # Initalize Plotly figure
    fig = go.Figure()

    # Fetch and plot data for each select ticker
    for ticker in TICKERS:
        if ticker in selected_tickers:  # Ensure only selected tickers are shown
            data = yf.Ticker(ticker).history(start=start_date, end=end_date)
            fig.add_trace(
                go.Scatter(x=data.index, y=data["Close"], mode="lines", name=ticker)
            )

    # Update plot layout
    fig.update_layout(
        title="Closing Price of selected Stocks",
        xaxis_title="Date",
        yaxis_title="Closing Prices",
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
