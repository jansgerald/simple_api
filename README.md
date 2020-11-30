# Capstone Project
This is Algoritma's Python for Data Analysis Capstone Project. This project aims to create a simple API to fetch data from Heroku Server. 

As a Data Scientist, we demand data to be accessible. And as a data owner, we are careful with our data. As the answer, data owner create an API for anyone who are granted access to the data to collect them. In this capstone project, we will create Flask Application as an API and deploy it to Heroku Web Hosting. 

___
## Dependencies : 
- Pandas    (pip install pandas)
- Flask     (pip install flask)
- Gunicorn  (pip install gunicorn)
___
## Goal 
- Create Flask API App
- Deploy to Heroku
- Build API Documentation of how your API works
- Implements the data analysis and wrangling behind the works

___
I have deployed this project on : https://simpleapijans.herokuapp.com
Here's the list of its endpoints: 
```
1. / , method = GET
Base Endpoint, returning welcoming string value. 

2. /data/get/<data_name> , method = GET
Return full data <data_name> in JSON format. Currently available data are:
    - books_c.csv
    - pulsar_stars.csv 

3. /data2/<data_name>/<table_name> , method = GET
Return full data <data_name> and <table_name> in JSON format. Currently available data are:
    - chinook.db
And available table are:
    - playlist_track
    - media_types
    - genres
    - playlists
    - tracks
    - artists
    - albums
    - customers
    - invoice_items
    - invoices
    - employees
    
4. /toplanguage , method = GET
Return top 5 language in books data.

5. /toprating/<rating>, method = GET
Return data from books that have rating more than or equals to <rating>.

6. /revenuebyday, method = GET
Return data total revenue from sales in days name that already sorted.

7. /stock, method = GET
Return comparison between BBRI and BBCA stock.

8. /bestgenres, method = GET
Return top 10 genres.

9. /artists, method = GET
Return top 10 artists based on best genres in number 8.
```

If you want to try it, you can access (copy-paste it) : 
- https://simpleapijans.herokuapp.com/
- https://simpleapijans.herokuapp.com/data/get/books_c.csv
- https://simpleapijans.herokuapp.com/data/get/pulsar_stars.csv
- https://simpleapijans.herokuapp.com/data2/chinook.db/invoices
- https://simpleapijans.herokuapp.com/toplanguage
- https://simpleapijans.herokuapp.com/toprating/4.5
- https://simpleapijans.herokuapp.com/revenuebyday
- https://simpleapijans.herokuapp.com/stock
- https://simpleapijans.herokuapp.com/bestgenres
- https://simpleapijans.herokuapp.com/artists
