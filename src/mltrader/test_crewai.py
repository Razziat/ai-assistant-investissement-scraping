import os
import glob
import pandas as pd
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

os.environ["OTEL_SDK_DISABLED"] = "true"

# Initialisation du modèle Ollama
llm = Ollama(model="llama2")

# Configuration de l'agent
financial_analyst = Agent(
    llm=llm,
    role="Financial Analyst",
    goal="Analyze the financial and sentiment data of Airbus SE and Thales to predict their stock performance.",
    backstory="You are a seasoned financial analyst specializing in the French stock market. Your task is to evaluate Airbus SE, Thales and Lvmh based on historical financial data and sentiment analysis provided in the CSV files to identify promising investment opportunities.",
    allow_delegation=False,
    tools=[],
    verbose=True,
)

# Function to load and prepare data
def prepare_data():
    # Paths can be adjusted as necessary
    stock_paths = {
        'Airbus': 'datas/actions_price_datas/all_categories/AIR.PA_full_monthly_data.csv',
        'Thales': 'datas/actions_price_datas/all_categories/HO.PA_full_monthly_data.csv',
        'Lvmh': 'datas/actions_price_datas/all_categories/MC.PA_full_monthly_data.csv'
    }
    sentiment_paths = {
        'Airbus': 'datas/resultats_analyse_sentiment_consolidés.csv',
        'Thales': 'datas/resultats_analyse_sentiment_consolidés_thales.csv',
        'Lvmh': 'datas/resultats_analyse_sentiment_consolidés_lvmh.csv'
    }

    data = {}
    for key, stock_file in stock_paths.items():
        stock_data = pd.read_csv(stock_file)
        stock_data['Month'] = pd.to_datetime(stock_data['Month'])
        stock_data = stock_data[stock_data['Month'] >= '2010-01-01']
        sentiment_data = pd.read_csv(sentiment_paths[key])

        data[key] = {
            'stock': stock_data,
            'sentiment': sentiment_data
        }
    return data

# Function to calculate statistics
def calculate_statistics(data):
    stats = {}
    for key, values in data.items():
        stock_data = values['stock']
        sentiment_data = values['sentiment']

        # Calculating stock statistics
        average_monthly_change = stock_data['Percent Change'].mean()
        max_price = stock_data['High'].max()
        min_price = stock_data['Low'].min()
        pe_ratio_avg = stock_data['PE Ratio'].mean()

        # Calculating sentiment statistics
        average_sentiment = sentiment_data['Moyenne_Sentiment'].mean()
        confidence_mean = sentiment_data['Moyenne_Score_Confiance'].mean()

        stats[key] = {
            "Average Monthly Percent Change": average_monthly_change,
            "Max Price": max_price,
            "Min Price": min_price,
            "Average Sentiment": average_sentiment,
            "Average Confidence Score": confidence_mean,
            "Average PE Ratio": pe_ratio_avg
        }
    return stats

# Load and prepare data
data = prepare_data()
stats = calculate_statistics(data)

# Creating the task
task_description = f"""
Analyze the provided CSV data specifically for Airbus SE and Thales. The data includes monthly stock prices and sentiment analysis of related articles.
Generate predictions for future stock performance of both Airbus SE, Thales and Lvmh and evaluate their potential as investment opportunities based on this data.

Key Statistics for Airbus SE:
- Average Monthly Percent Change: {stats['Airbus']['Average Monthly Percent Change']:.2f}%
- Max Price: {stats['Airbus']['Max Price']}
- Min Price: {stats['Airbus']['Min Price']}
- Average Sentiment: {stats['Airbus']['Average Sentiment']:.2f}
- Average Confidence Score: {stats['Airbus']['Average Confidence Score']:.2f}
- Average PE Ratio: {stats['Airbus']['Average PE Ratio']:.2f}

Key Statistics for Thales:
- Average Monthly Percent Change: {stats['Thales']['Average Monthly Percent Change']:.2f}%
- Max Price: {stats['Thales']['Max Price']}
- Min Price: {stats['Thales']['Min Price']}
- Average Sentiment: {stats['Thales']['Average Sentiment']:.2f}
- Average Confidence Score: {stats['Thales']['Average Confidence Score']:.2f}
- Average PE Ratio: {stats['Thales']['Average PE Ratio']:.2f}

Key Statistics for Thales:
- Average Monthly Percent Change: {stats['Lvmh']['Average Monthly Percent Change']:.2f}%
- Max Price: {stats['Lvmh']['Max Price']}
- Min Price: {stats['Lvmh']['Min Price']}
- Average Sentiment: {stats['Lvmh']['Average Sentiment']:.2f}
- Average Confidence Score: {stats['Lvmh']['Average Confidence Score']:.2f}
- Average PE Ratio: {stats['Lvmh']['Average PE Ratio']:.2f}
"""

task = Task(
    description=task_description,
    expected_output="A detailed comparative analysis of Airbus SE, Thales and Lvmh stocks based on predicted future performance using the specific csv data provided. The analysis will conclude with investment recommendations.",
    agent=financial_analyst,
)

# Configure the crew
crew = Crew(agents=[financial_analyst], tasks=[task], verbose=2)

# Execute the task
task_output = crew.kickoff()
print(task_output)

output_filename = 'src/mltrader/output_analysis.txt'
with open(output_filename, 'w') as file:
    file.write(task_output)

print(f"Analysis output saved to {output_filename}")
