import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to scrape products from a given URL
def get_eco_products(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Extract product names and prices (adjust this for your target website)
    products = []
    for item in soup.find_all('div', class_='product-listing'):  # Modify based on the website structure
        name = item.find('h2').text.strip()
        price = item.find('span', class_='price').text.strip()
        link = item.find('a', href=True)['href']
        
        products.append({'name': name, 'price': price, 'link': link})
    
    return products

# Function to filter eco-friendly products based on keywords
def is_eco_friendly(product):
    eco_keywords = ['organic', 'bamboo', 'recycled', 'fair trade', 'eco-friendly', 'sustainable']
    description = product['name'].lower()
    return any(keyword in description for keyword in eco_keywords)

# Function to add product to database
def add_product_to_db(product):
    conn = sqlite3.connect('verdi_products.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO products (name, price, link)
    VALUES (?, ?, ?)
    ''', (product['name'], product['price'], product['link']))
    conn.commit()
    conn.close()

# Scrape and add eco-friendly products to the database
def scrape_and_store_products():
    # List of URLs to scrape
    urls = ["https://example.com/eco-friendly-products", "https://another-site.com/eco-products"]  # Replace with actual URLs
    for url in urls:
        products = get_eco_products(url)
        for product in products:
            if is_eco_friendly(product):
                add_product_to_db(product)

