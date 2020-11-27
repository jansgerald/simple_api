from flask import Flask, request 
import pandas as pd 
import sqlite3
app = Flask(__name__) 

#home root
@app.route('/')
def homepage():
    return '<h1>#Hello World this is my project to build a simple API#</h1>'

# mendapatkan buku
@app.route('/ambil_buku')
def ambilbuku():
    data = pd.read_csv('data/books_c.csv')
    return (data.to_json()) #atau integer atau string

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
    condition = data['average_rating'] == float(rating)
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
    rbd = revenue.groupby('DayName').agg({'Total':'sum'}).sort_values(by='Total', ascending=False).loc['Wednesday'][0]
    return (f'''<h1>Wednesday is the day with highest revenue: {rbd}</h1>
                ''')

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
        LIMIT 5
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
            LIMIT 5
        )
        GROUP BY genres.Name, artists.Name
        ORDER BY Total DESC
        ''',
            conn
        )
    artists = data.drop_duplicates(subset='Name').set_index('Name')
    return (artists.to_json())

# mendapatkan keseluruhan data dari <data_name>
@app.route('/data/get/<data_name>', methods=['GET']) 
def get_data(data_name): 
    data = pd.read_csv('data/' + str(data_name))
    return (data.to_json())
 

# mendapatkan data dengan filter nilai <value> pada kolom <column>
@app.route('/data/get/equal/<data_name>/<column>/<value>', methods=['GET']) 
def get_data_equal(data_name, column, value): 
    data = pd.read_csv('data/' + str(data_name))
    mask = data[column] == value
    data = data[mask]
    return (data.to_json())


if __name__ == '__main__':
    app.run(debug=True, port=5000) 