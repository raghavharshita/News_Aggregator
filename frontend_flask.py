
from flask import Flask, render_template, request
import sqlite3

app=Flask(__name__)
@app.route('/')
def home():
    conn=sqlite3.connect('news_data.db')
    cursor=conn.cursor()
    search_query=request.args.get('search','')
    if search_query=='':
        search_query='TikTok'
    cursor.execute('''
    SELECT TITLE,URL,SUMMARY,CATEGORY,PUBLICATION_DATE
    FROM news_table
    WHERE TITLE LIKE ? 
    ORDER BY PUBLICATION_DATE DESC
''',(f'%{search_query}%',))
    news_table=cursor.fetchall()
    conn.close()
    return render_template('index.html', news=news_table, search_query=search_query)

if __name__=="__main__":
    app.run(debug=True)