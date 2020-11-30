from flask import Flask, request 
import pandas as pd 
import sqlite3
from datetime import date
from pandas_datareader import data
app = Flask(__name__) 


#home root
@app.route('/')
def homepage():
    return (f'''
    <br>
    <center><h1>Hello World this is my project to build a simple API</h1></center>
    <center><h2>ENJOY!!!</h2></center>
    <center><img src="https://miro.medium.com/max/625/1*ZU1EQ7tYeQNQlhOhyonHFA.png" width="872" height="403"></center>
    ''')

# mendapatkan keseluruhan data csv <data_name> 
@app.route('/data/get/<data_name>', methods=['GET']) 
def get_data(data_name): 
    data = pd.read_csv('data/' + str(data_name))
    return (data.to_json())

# mendapatkan keseluruhan database <data_name> 
@app.route('/data2/get/<data_name>/<table_name>')
def get_data2(data_name, table_name):
    conn = sqlite3.connect('data/' + str(data_name))
    data = pd.read_sql_query('SELECT * FROM ' + str(table_name), conn)
    return (data.to_json())

# toplanguage
@app.route('/toplanguage')
def language():
    data = pd.read_csv('data/books_c.csv')
    data['language_code'] = data['language_code'].astype('category')
    top = pd.crosstab(
            index=data['language_code'],
            columns='Frequency'
        ).sort_values(by='Frequency',ascending=False).head(5)
    return (top.to_json())

# toprating
@app.route('/toprating/<rating>', methods=['GET'])
def toprating(rating):
    data = pd.read_csv('data/books_c.csv')
    condition = data['average_rating'] >= float(rating)
    books = data[condition]
    return books.to_json()

# revenuebyday
@app.route('/revenuebyday')
def revenue():
    conn = sqlite3.connect('data/chinook.db')
    revenue = pd.read_sql_query(
        '''
        SELECT InvoiceDate, Total
        FROM invoices
        ''',
            conn,
            parse_dates='InvoiceDate'
        )
    revenue['DayName'] = revenue['InvoiceDate'].dt.day_name()
    rbd = revenue.groupby('DayName').agg({'Total':'sum'}).sort_values(by='Total', ascending=False)
    highest_day = rbd.index[0]
    highest_value = rbd.values[0][0]
    return (rbd.to_json() +
    f'''
    <h4>So,{highest_day} is the day with highest revenue with {highest_value}.</h4>
    ''')

# BBRI vs BBCA
@app.route('/stock')
def stock():
    symbol = ['BBRI.JK', 'BBCA.JK']
    source = 'yahoo'
    start_date = '2019-11-30'
    end_date = date.today().strftime('%Y-%m-%d')
    stock = data.DataReader(symbol, source, start_date, end_date)
    vs = stock.stack().reset_index().groupby('Symbols').mean()
    return (vs.to_json())

# bestgenremusicbytotalsell
@app.route('/bestgenres')
def genres():
    conn = sqlite3.connect('data/chinook.db')
    genres = pd.read_sql_query(
        '''
        SELECT genres.Name, SUM(invoices.Total) as Total
        FROM invoices
        LEFT JOIN invoice_items
        ON invoice_items.InvoiceId = invoices.InvoiceId
        LEFT JOIN tracks
        ON tracks.TrackId = invoice_items.TrackId
        LEFT JOIN genres
        ON genres.GenreId = tracks.GenreId
        GROUP BY genres.Name
        ORDER BY Total DESC
        LIMIT 10
        ''',
            conn,
            index_col='Name'
        )
    return (genres.to_json())

# artistpergenres
@app.route('/artists')
def artist():
    conn = sqlite3.connect('data/chinook.db')
    data = pd.read_sql_query(
        '''
        SELECT genres.Name, SUM(invoices.Total) as Total, artists.Name AS ArtistName
        FROM invoices
        LEFT JOIN invoice_items
        ON invoice_items.InvoiceId = invoices.InvoiceId
        LEFT JOIN tracks
        ON tracks.TrackId = invoice_items.TrackId
        LEFT JOIN genres
        ON genres.GenreId = tracks.GenreId
        LEFT JOIN albums
        ON albums.AlbumId = tracks.AlbumId
        LEFT JOIN artists
        ON artists.ArtistId = albums.ArtistId
        WHERE genres.Name IN (
            SELECT genres.Name
            FROM invoices
            LEFT JOIN invoice_items
            ON invoice_items.InvoiceId = invoices.InvoiceId
            LEFT JOIN tracks
            ON tracks.TrackId = invoice_items.TrackId
            LEFT JOIN genres
            ON genres.GenreId = tracks.GenreId
            GROUP BY genres.Name
            ORDER BY SUM(invoices.Total) DESC
            LIMIT 10
        )
        GROUP BY genres.Name, artists.Name
        ORDER BY Total DESC
        ''',
            conn
        )
    artists = data.drop_duplicates(subset='Name').set_index('Name')
    return (artists.to_json())

 

if __name__ == '__main__':
    app.run(debug=True, port=5000) 