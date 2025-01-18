
import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
import sqlite3

def parse_time(time):
    """convert the string time into datetime 
        like 2 hours ago will convert it into 18 january 2025
    """
    try:
        if "ago" in time:
            num,unit=time.split()[:2]
            num=int(num)
            if "min" in unit:
                return datetime.now()-timedelta(minutes=num)
            elif "hrs" in unit:
                return datetime.now()-timedelta(hours=num)
            elif "days" in unit:
                return datetime.now()-timedelta(days=num)
        else:
            return datetime.strptime(time, "%d %B %Y")
    except Exception as e:
        return None



def scrape_news():
    url = "https://www.bbc.com"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to fetch the website {url} with status code {response.status_code}")
        return None
    else:
        print("Website fetched successfully")
        print("Response Content Preview:", response.text[:500])
    soup=BeautifulSoup(response.text,'html.parser')
    article=soup.find('article')
    sections=article.find_all('a')
    conn = sqlite3.connect('news_data.db')
    c = conn.cursor()
    for i in sections:
        h=i.find('h2')
        title=h.text.strip() if h else "no title"
        link=f"{url}{i['href']}" if i['href'].startswith("/") else i['href']
        p=i.find('p')
        content=p.text.strip() if p else "no content"
        t = i.find('span', attrs={'data-testid': 'card-metadata-lastupdated'})
        time=t.text.strip() if t else None
        parsed_time = parse_time(time) if time else "no time"
        cat=i.find('span',attrs={'data-testid':'card-metadata-tag'})
        category = ' '.join(cat.text.split()) if cat else "not specified"
        c.execute("SELECT COUNT(*) FROM news_table WHERE url=?", (link,))
        if c.fetchone()[0] == 0:
            c.execute('''
            INSERT INTO news_table(title, url, summary, category, publication_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (title, link, content, category, parsed_time))

    conn.commit()
    conn.close()

    
scrape_news()