from flask import Flask, render_template, request
from products_scraper import scrape_and_store_products  # Import the scraping function
import sqlite3

app = Flask(__name__)

# Initialize database when app starts
def init_db():
    conn = sqlite3.connect('verdi_products.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price TEXT NOT NULL,
        link TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    product_name = request.form['product_name']
    
    # Get products from the database that match the search query
    conn = sqlite3.connect('verdi_products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + product_name + '%',))
    results = c.fetchall()
    conn.close()
    
    return render_template('search_results.html', results=results, query=product_name)

@app.route('/scrape')
def scrape():
    scrape_and_store_products()  # Run the product scraping and storage function
    return "Scraping done and products stored!"

if __name__ == '__main__':
    app.run(debug=True)
