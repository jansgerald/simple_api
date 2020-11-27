from flask import Flask, request 
import pandas as pd 
import sqlite3
app = Flask(__name__) 


#home root
@app.route('/')
def homepage():
    return 'Hello World 2020'

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

# bestgenremusicbytotalsell
@app.route('/bestgenres')
def genres():
    conn = sqlite3.connect('data/chinook.db')
    genres = pd.read_sql_query(
        '''
        SELECT genres.*, SUM(invoices.Total) as Total
        FROM genres
        LEFT JOIN tracks
        ON tracks.GenreId = genres.GenreId
        LEFT JOIN invoice_items
        ON invoice_items.TrackId = tracks.TrackId
        LEFT JOIN invoices
        ON invoices.InvoiceId = invoice_items.InvoiceId
        GROUP BY genres.Name
        ORDER BY Total DESC
        LIMIT 5
        ''',
            conn,
            index_col='GenreId'
        )
    return (genres.to_json()) 

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