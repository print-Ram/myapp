import datetime as dt
import sqlite3
import pandas as pd
from flask import Flask, request, render_template

def get_stock_data(stockdata, start_date, end_date, interval, events):
    ts1 = str(int(start_date.timestamp()))
    ts2 = str(int(end_date.timestamp()))
    
    Stock_downurl = f'https://query1.finance.yahoo.com/v7/finance/download/{stockdata}?period1={ts1}&period2={ts2}&interval={interval}&events={events}'
    company_data = pd.read_csv(Stock_downurl)
    return company_data, Stock_downurl

def save_to_database(company_data, stockdata):
    conn = sqlite3.connect('stocks.db')
    company_data.to_sql(stockdata, conn, if_exists='replace')
    conn.close()

def load_from_database(stockdata):
    conn = sqlite3.connect('stocks.db')
    query = f'SELECT * FROM {stockdata}'
    company_data = pd.read_sql_query(query, conn)
    conn.close()
    return company_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data_route():
    stockdata = request.form['stockdata']
    start_date = dt.datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = dt.datetime.strptime(request.form['end_date'], '%Y-%m-%d')

    interval = request.form['interval']
    events = request.form['events']
    company_data, stock_url = get_stock_data(stockdata, start_date, end_date, interval, events)
    save_to_database(company_data, stockdata)
    return render_template('result.html', table=company_data.to_html(), stockdata=stockdata, stock_url=stock_url)


if __name__ == '__main__':
    app.run(debug=True)
