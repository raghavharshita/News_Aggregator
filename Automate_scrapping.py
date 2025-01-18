
import schedule
import time
from scraper import scrape_news
schedule.every().day.at("10:00").do(scrape_news)
while True:
    schedule.run_pending()
    time.sleep(1)