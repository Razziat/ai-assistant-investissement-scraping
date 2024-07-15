import yfinance as yf
from datetime import datetime

def get_stock_price_change(ticker_symbol, start_date, end_date):
    """
    Fetches historical market data for the specified ticker between start_date and end_date,
    calculates the percentage change in closing price over that period, and returns the closing prices
    at the start and end dates along with the percentage change.

    Parameters:
    ticker_symbol (str): The stock ticker symbol.
    start_date (str): Start date in YYYY-MM-DD format.
    end_date (str): End date in YYYY-MM-DD format.

    Returns:
    tuple: A tuple containing the start price, end price, and the percentage change in closing price.
    """
    # Fetch historical market data
    stock = yf.Ticker(ticker_symbol)
    historical_data = stock.history(start=start_date, end=end_date)

    # Calculate percentage change and get start/end prices
    if not historical_data.empty:
        closing_prices = historical_data['Close']
        price_start = closing_prices.iloc[0]
        price_end = closing_prices.iloc[-1]
        percent_change = ((price_end - price_start) / price_start) * 100
        return price_start, price_end, percent_change
    else:
        return None, None, "Data not available for the given period."

if __name__ == "__main__":
    ticker = input("Enter the ticker symbol (e.g., AAPL for Apple): ")
    start = input("Enter the start date (YYYY-MM-DD): ")
    end = input("Enter the end date (YYYY-MM-DD): ")

    price_start, price_end, percent_change = get_stock_price_change(ticker, start, end)
    if price_start is not None:
        print(f"Starting price on {start}: {price_start:.2f}")
        print(f"Ending price on {end}: {price_end:.2f}")
        print(f"The percentage change in price from {start} to {end} is: {percent_change:.2f}%")
    else:
        print(percent_change)
