# scrapping-assistant-investissement

This repo is a only a test version for a scrapping and investment assistant using AI.
You can freely read the code and use it for you own projects.
We will continue to add new versions of the project in the futur. if you have any questions don't hesitate.
First we manage to get all the tickers available on yahoo finance. Then we created scipts that will get news hitory about a tickers or a compagny.
Those scripts can be found in src/get_data folder.
The results of the news history and sentiment analysis can be found in datas folder.
Then in mlfinder folder you will find many scripts that are using IA. Some of then are used to make sentiment analysis of the news collected.
Some of them use differents type of IA predictions models to calculate the price evolution.
There are also test script for tradingbot. And a script test for crewia.

The most advanced script in mltrader folder, is test_crewia.py, and analyse_sentiment.py. All the other scripts of the folder are just alpha versions of what we want to do.

We strongly advise to use a python virtual environments to run the scripts because some of the import needs a specific version of python (python 3.10 and python 3.12 are working well for this project).