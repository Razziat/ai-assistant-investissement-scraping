from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment
from lumibot.entities import Asset
import pandas as pd
import pandas_ta as ta

API_KEY = "YOUR_ALPACA_API_KEY"
API_SECRET = "YOUR_ALPACA_API_SECRET"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

class MLTrader(Strategy): 
    def initialize(self, symbol:str="GOOG", cash_at_risk:float=.25): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=7)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today) 
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        sentiments = [estimate_sentiment(headline) for headline in news]
        sentiment_df = pd.DataFrame(sentiments, columns=['probability', 'sentiment'])
        return sentiment_df 

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        sentiment_df = self.get_sentiment()

        # Calcul de la moyenne mobile des scores de sentiment
        sentiment_df['sentiment_score'] = sentiment_df['probability'] * sentiment_df['sentiment'].apply(lambda x: 1 if x == 'positive' else -1)
        sentiment_df['moving_average'] = sentiment_df['sentiment_score'].rolling(window=30).mean()

        current_sentiment = sentiment_df['moving_average'].iloc[-1]

        # Obtention des données historiques pour le calcul du RSI
        historical_prices = self.get_historical_prices(self.symbol, 30, "day")
        if historical_prices is not None:
            df = historical_prices.df

            # Appliquer pandas_ta pour activer les méthodes TA directement sur le DataFrame
            df.ta.rsi(close='close', length=14, append=True)  # Assurez-vous d'utiliser append=True pour ajouter le RSI au DataFrame existant

            current_rsi = df.iloc[-1]['RSI_14']  # Accès à la colonne RSI correctement ajoutée

            if cash > last_price:
                if current_sentiment > 0 and current_rsi < 70:
                    if self.last_trade == "sell":
                        self.sell_all() 
                    order = self.create_order(
                        self.symbol, 
                        quantity, 
                        "buy", 
                        type="bracket", 
                        take_profit_price=last_price*1.05, 
                        stop_loss_price=last_price*.95
                    )
                    self.submit_order(order) 
                    self.last_trade = "buy"
                elif current_sentiment < 0 and current_rsi > 30:
                    if self.last_trade == "buy": 
                        self.sell_all() 
                    order = self.create_order(
                        self.symbol, 
                        quantity, 
                        "sell", 
                        type="bracket", 
                        take_profit_price=last_price*.95, 
                        stop_loss_price=last_price*1.05
                    )
                    self.submit_order(order) 
                    self.last_trade = "sell"

start_date = datetime(2023,1,1)
end_date = datetime(2023,12,31) 
broker = Alpaca(ALPACA_CREDS)   
strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol":"GOOG", "cash_at_risk":.5})
strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    benchmark_asset="GOOG",
    parameters={"symbol":"GOOG", "cash_at_risk":.5}
)