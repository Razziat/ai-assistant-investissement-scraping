import yfinance as yf
import pandas as pd

import yfinance as yf
import pandas as pd

def get_full_monthly_price_data(ticker_symbol):
    """
    Fetches the complete historical market data for the specified ticker,
    including trading volume, dividend payments, and other financial metrics,
    calculates the monthly percentage change, highest and lowest prices, and the dates of those extremes.
    """
    # Fetch historical market data
    stock = yf.Ticker(ticker_symbol)
    historical_data = stock.history(period="max", interval="1d")

    # Get additional info from yfinance
    info = stock.info
    pe_ratio = info.get('trailingPE', None)
    beta = info.get('beta', None)

    # Include dividends and stock splits
    dividends = stock.dividends.resample('ME').sum()
    splits = stock.splits.resample('ME').sum()

    # Resample to monthly data for open, close, high, low, and volume
    monthly_data = historical_data.resample('ME').agg({
        'Open': 'first',
        'Close': 'last',
        'High': 'max',
        'Low': 'min',
        'Volume': 'sum'
    })

    # Determine the dates of the highest and lowest prices using a lambda that captures the original index
    monthly_data['Date of High'] = historical_data['High'].resample('ME').apply(lambda x: x.idxmax())
    monthly_data['Date of Low'] = historical_data['Low'].resample('ME').apply(lambda x: x.idxmin())

    # Calculate monthly percentage change
    monthly_data['Percent Change'] = monthly_data['Close'].pct_change() * 100

    # Prepare DataFrame for CSV
    monthly_data.reset_index(inplace=True)
    monthly_data['Month'] = monthly_data['Date'].dt.strftime('%Y-%m')
    monthly_data['Asset Name'] = stock.info.get('shortName', ticker_symbol)
    monthly_data['PE Ratio'] = pe_ratio
    monthly_data['Beta'] = beta
    monthly_data.drop(columns=['Date'], inplace=True)

    # Adding dividends and splits
    monthly_data['Dividends'] = dividends
    monthly_data['Splits'] = splits

    # Define column order
    column_order = ['Month', 'Asset Name', 'Open', 'Close', 'High', 'Low', 'Volume', 'Dividends', 'Splits', 'Date of High', 'Date of Low', 'Percent Change', 'PE Ratio', 'Beta']
    monthly_data = monthly_data[column_order]

    return monthly_data

# This function now returns a more comprehensive DataFrame suitable for in-depth financial analysis and forecasting.


def run_for_ticker(ticker_symbol):
    monthly_data = get_full_monthly_price_data(ticker_symbol)
    # Définir le chemin du fichier CSV en fonction de la catégorie de l'actif
    # Cette fonction ne crée plus le fichier CSV mais retourne les données
    return monthly_data

if __name__ == "__main__":
    ticker = input("Enter the ticker symbol (e.g., AAPL for Apple): ")
    monthly_data = get_full_monthly_price_data(ticker)
    
    # Define the CSV file name
    csv_file_name = f"datas/actions_price_datas/all_categories/{ticker}_full_monthly_data.csv"
    monthly_data.to_csv(csv_file_name, index=False)
    
    print(f"Full monthly data has been saved to {csv_file_name}")

