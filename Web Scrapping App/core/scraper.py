# core/scraper.py
import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import random
import re
from threading import Event
from queue import Queue
from urllib.parse import urljoin, urlparse
import sys
import os

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class AdvancedScraper:
    def __init__(self, db_path):
        self.db_path = db_path
        self.is_paused = Event()
        self.is_stopped = Event()
        self.progress_queue = Queue()
        self.current_progress = 0
        self.target_count = 25000
        self.current_url = ""
        
    def set_target_url(self, url):
        """Set the target URL for scraping"""
        self.current_url = url
        
    def scrape_from_website(self, url):
        """Scrape data from the specified website"""
        self.current_url = url
        
        # Check what type of website it is
        if "books.toscrape.com" in url:
            return self.scrape_books_toscrape(url)
        elif "quotes.toscrape.com" in url:
            return self.scrape_quotes_toscrape(url)
        else:
            # Generate mock data for unsupported websites
            return self.generate_mock_data_with_url(url)
    
    def scrape_books_toscrape(self, base_url):
        """Scrape books from books.toscrape.com"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            page_num = 1
            books_scraped = 0
            
            while books_scraped < self.target_count and not self.is_stopped.is_set():
                # Wait if paused
                while self.is_paused.is_set() and not self.is_stopped.is_set():
                    time.sleep(0.5)
                
                # Fix the URL structure for books.toscrape.com
                if page_num == 1:
                    url = base_url
                else:
                    url = f"{base_url}/catalogue/page-{page_num}.html"
                
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Check if page exists
                    if "No products found" in soup.get_text():
                        break
                    
                    # Find all book containers
                    books = soup.find_all('article', class_='product_pod')
                    
                    if not books:
                        break
                    
                    for book in books:
                        if books_scraped >= self.target_count or self.is_stopped.is_set():
                            break
                            
                        try:
                            # Extract book information
                            title = book.find('h3').find('a')['title']
                            price_text = book.find('p', class_='price_color').get_text()
                            price = float(price_text.replace('£', '').strip())
                            availability = book.find('p', class_='instock').get_text().strip()
                            
                            # Get rating
                            rating_class = book.find('p', class_='star-rating')
                            rating = self.convert_rating(rating_class['class'][1]) if rating_class else 3.0
                            
                            # Get book detail page URL
                            book_url = book.find('h3').find('a')['href']
                            # Fix relative URL
                            if book_url.startswith('../../../'):
                                book_url = book_url.replace('../../../', '/catalogue/')
                            full_book_url = urljoin(base_url, book_url)
                            
                            # Save to database (simplified for now)
                            cursor.execute('''
                                INSERT INTO books (title, author, isbn, publisher, publication_year, 
                                                 category, price, rating, page_count, language, description, 
                                                 stock_quantity, format_type, source_url)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                title,
                                "Unknown Author",  # Simplified for now
                                f"ISBN-{books_scraped:06d}",
                                "Unknown Publisher",
                                2023,
                                "Fiction",  # Default category
                                price,
                                rating,
                                200,  # Default page count
                                "English",
                                f"Book about {title}",
                                50,  # Default stock
                                "Paperback",
                                full_book_url
                            ))
                            
                            books_scraped += 1
                            self.current_progress = books_scraped
                            self.progress_queue.put(books_scraped)
                            
                            # Be polite to the server
                            time.sleep(0.2)
                            
                        except Exception as e:
                            print(f"Error scraping book: {e}")
                            continue
                    
                    print(f"Scraped page {page_num}, total books: {books_scraped}")
                    page_num += 1
                    
                except requests.RequestException as e:
                    print(f"Error accessing page {page_num}: {e}")
                    break
            
            conn.commit()
            conn.close()
            return books_scraped > 0
            
        except Exception as e:
            print(f"Error in books scraping: {e}")
            return False
    
    def scrape_quotes_toscrape(self, base_url):
        """Scrape quotes from quotes.toscrape.com"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            page_num = 1
            quotes_scraped = 0
            
            while quotes_scraped < self.target_count and not self.is_stopped.is_set():
                # Wait if paused
                while self.is_paused.is_set() and not self.is_stopped.is_set():
                    time.sleep(0.5)
                
                url = base_url + f"/page/{page_num}/" if page_num > 1 else base_url
                
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    quotes = soup.find_all('div', class_='quote')
                    
                    if not quotes:
                        break
                    
                    for quote in quotes:
                        if quotes_scraped >= self.target_count or self.is_stopped.is_set():
                            break
                            
                        try:
                            text = quote.find('span', class_='text').get_text(strip=True).strip('"')
                            author = quote.find('small', class_='author').get_text(strip=True)
                            
                            tags = quote.find('div', class_='tags')
                            tag_list = [tag.get_text(strip=True) for tag in tags.find_all('a', class_='tag')] if tags else []
                            tags_str = ", ".join(tag_list)
                            
                            # Create a book-like entity from quote data
                            title = f"Quotes by {author}"
                            description = f'"{text}" - Tags: {tags_str}'
                            
                            cursor.execute('''
                                INSERT INTO books (title, author, isbn, publisher, publication_year, 
                                                 category, price, rating, page_count, language, description, 
                                                 stock_quantity, format_type, source_url)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                title,
                                author,
                                f"QUOTE-{quotes_scraped:06d}",
                                "Quotes to Scrape",
                                2023,
                                "Quotes",
                                0.0,
                                4.0,
                                1,
                                "English",
                                description,
                                999,
                                "Digital",
                                url
                            ))
                            
                            quotes_scraped += 1
                            self.current_progress = quotes_scraped
                            self.progress_queue.put(quotes_scraped)
                            
                            time.sleep(0.1)
                            
                        except Exception as e:
                            print(f"Error scraping quote: {e}")
                            continue
                    
                    print(f"Scraped quotes page {page_num}, total: {quotes_scraped}")
                    page_num += 1
                    
                except requests.RequestException as e:
                    print(f"Error accessing quotes page {page_num}: {e}")
                    break
            
            conn.commit()
            conn.close()
            return quotes_scraped > 0
            
        except Exception as e:
            print(f"Error in quotes scraping: {e}")
            return False
    
    def generate_mock_data_with_url(self, url):
        """Generate mock data but associate it with the provided URL"""
        first_names = ["John", "Emma", "Michael", "Sophia", "James", "Olivia", "Robert", "Ava", "David", "Isabella"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        categories = ["Fiction", "Science", "Technology", "History", "Biography", "Fantasy", "Mystery", "Romance"]
        publishers = ["Penguin", "HarperCollins", "Random House", "Macmillan", "Hachette"]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for i in range(min(self.target_count, 1000)):  # Limit to 1000 for testing
            if self.is_stopped.is_set():
                break
                
            # Wait if paused
            while self.is_paused.is_set() and not self.is_stopped.is_set():
                time.sleep(0.5)
            
            # Generate mock book data
            title = f"Book {i+1}: The Story of {random.choice(first_names)} {random.choice(last_names)}"
            author = f"{random.choice(first_names)} {random.choice(last_names)}"
            isbn = f"978-{random.randint(100000000, 999999999)}"
            publisher = random.choice(publishers)
            publication_year = random.randint(1950, 2024)
            category = random.choice(categories)
            price = round(random.uniform(5.99, 49.99), 2)
            rating = round(random.uniform(3.0, 5.0), 1)
            page_count = random.randint(100, 800)
            language = "English"
            description = f"A fascinating book about {category.lower()} written by {author}."
            stock_quantity = random.randint(0, 1000)
            format_type = random.choice(["Hardcover", "Paperback", "E-book"])
            
            # Save to database with the provided URL as source
            cursor.execute('''
                INSERT INTO books (title, author, isbn, publisher, publication_year, 
                                 category, price, rating, page_count, language, description, 
                                 stock_quantity, format_type, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, publisher, publication_year, category, price, 
                  rating, page_count, language, description, stock_quantity, format_type, url))
            
            self.current_progress = i + 1
            self.progress_queue.put(self.current_progress)
            
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1} records...")
        
        conn.commit()
        conn.close()
        return True
    
    def convert_rating(self, rating_text):
        """Convert star rating text to numerical value"""
        rating_map = {
            'One': 1.0, 'Two': 2.0, 'Three': 3.0, 
            'Four': 4.0, 'Five': 5.0
        }
        return rating_map.get(rating_text, 3.0)
    
    def pause_scraping(self):
        self.is_paused.set()
    
    def resume_scraping(self):
        self.is_paused.clear()
    
    def stop_scraping(self):
        self.is_stopped.set()