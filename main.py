import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

twilio_sid = "INSERT ID"
auth_token = "INSERT KEY"

stock_api_key = "INSERT KEY"
stock_owm = "https://www.alphavantage.co/query"

news_api_key = "INSERT KEY"
news_owm = "https://newsapi.org/v2/everything"



## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {"function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": STOCK,
                "apikey": stock_api_key}
stock_response = requests.get("https://www.alphavantage.co/query", params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

yesterday_closing_price = data_list[0]["4. close"]
day_before_yesterday_closing_price = data_list[1]["4. close"]

percent_change = abs((float(yesterday_closing_price)/float(day_before_yesterday_closing_price))/100)
percent_change = round(percent_change, 3)


get_news = False
if percent_change >= 5:
    print("Get News")
    get_news = True



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# if get_news:

news_params = {"q": "Google",
               "apikey":news_api_key}

news_response = requests.get(news_owm, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
news_article = news_data["articles"][:3]



## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

formatted_articles = [f"Headline: {article['title']}\n\nBrief: {article['description']}\n\n" for article in news_article]

client = Client(twilio_sid, auth_token)
for article in formatted_articles:
    message = client.messages \
        .create(
        body=article,
        from_='7262042176',
        to='2406189060'
                )

