#!/usr/bin/env python3
"""
LLC Directory Page Generator
Processes CSV data and generates SEO-optimized state and city pages
"""

import csv
import os
import re
from collections import defaultdict
from pathlib import Path

def clean_text(text):
    """Clean and format text for URLs and display"""
    if not text:
        return ""
    # Remove special characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', str(text))
    # Replace spaces with hyphens
    cleaned = re.sub(r'\s+', '-', cleaned.strip())
    return cleaned.lower()

def format_phone(phone):
    """Format phone number for display"""
    if not phone:
        return ""
    # Remove all non-digits
    digits = re.sub(r'\D', '', str(phone))
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]
    if len(digits) == 10:
        return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return str(phone)

def create_state_page(state_name, businesses, cities):
    """Generate HTML for a state page"""
    business_count = len(businesses)
    city_count = len(cities)
    
    # Create cities grid HTML
    cities_html = ""
    for city, city_businesses in cities.items():
        city_slug = clean_text(city)
        cities_html += f'''
                <a href="../cities/{city_slug}.html" class="city-card">
                    <h3>{city}</h3>
                    <p>{len(city_businesses)} businesses</p>
                </a>'''
    
    # Create businesses list HTML
    businesses_html = ""
    for business in businesses:
        businesses_html += f'''
                <div class="business-card">
                    <h3>{business['name']}</h3>
                    <div class="business-info">
                        <div>
                            <i>📞</i>
                            <span>{business['phone']}</span>
                        </div>
                        <div>
                            <i>📍</i>
                            <span>{business['full_address']}</span>
                        </div>
                        <div>
                            <i>🏢</i>
                            <span>{business['city']}, {business['state']} {business['postal_code']}</span>
                        </div>
                    </div>
                </div>'''
    
    # Generate the complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{state_name} LLC Directory - Find Local Businesses in {state_name}</title>
    <meta name="description" content="Find LLC businesses in {state_name}. Browse local companies, contact information, and business details across cities in {state_name}.">
    <meta name="keywords" content="{state_name} LLC directory, {state_name} businesses, {state_name} companies, local businesses {state_name}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://yourdomain.com/states/{clean_text(state_name)}.html">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{state_name} LLC Directory - Find Local Businesses in {state_name}">
    <meta property="og:description" content="Find LLC businesses in {state_name}. Browse local companies, contact information, and business details.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://yourdomain.com/states/{clean_text(state_name)}.html">
    
    <link rel="stylesheet" href="../styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="container">
                <div class="nav-brand">
                    <h1>LLC Directory</h1>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../states.html">States</a></li>
                    <li><a href="../about.html">About</a></li>
                    <li><a href="../contact.html">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <div class="breadcrumb">
        <div class="container">
            <a href="../index.html">Home</a> / <a href="../states.html">States</a> / <span>{state_name}</span>
        </div>
    </div>

    <div class="page-title">
        <div class="container">
            <h1>{state_name} LLC Directory</h1>
            <p>Find {business_count}+ businesses across {city_count} cities in {state_name}</p>
        </div>
    </div>

    <main class="main">
        <div class="container">
            <div class="cities-grid">{cities_html}
            </div>

            <div class="business-list" id="businessList">{businesses_html}
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>LLC Directory</h3>
                    <p>Your comprehensive source for LLC business information across the United States.</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="../index.html">Home</a></li>
                        <li><a href="../states.html">All States</a></li>
                        <li><a href="../about.html">About Us</a></li>
                        <li><a href="../contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Popular States</h4>
                    <ul>
                        <li><a href="florida.html">Florida</a></li>
                        <li><a href="california.html">California</a></li>
                        <li><a href="texas.html">Texas</a></li>
                        <li><a href="new-york.html">New York</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 LLC Directory. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="../script.js"></script>
</body>
</html>'''
    
    return html

def create_city_page(city_name, state_name, businesses):
    """Generate HTML for a city page"""
    business_count = len(businesses)
    
    # Create businesses list HTML
    businesses_html = ""
    for business in businesses:
        businesses_html += f'''
                <div class="business-card">
                    <h3>{business['name']}</h3>
                    <div class="business-info">
                        <div>
                            <i>📞</i>
                            <span>{business['phone']}</span>
                        </div>
                        <div>
                            <i>📍</i>
                            <span>{business['full_address']}</span>
                        </div>
                        <div>
                            <i>🏢</i>
                            <span>{business['city']}, {business['state']} {business['postal_code']}</span>
                        </div>
                    </div>
                </div>'''
    
    # Generate the complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{city_name}, {state_name} LLC Directory - Local Businesses in {city_name}</title>
    <meta name="description" content="Find LLC businesses in {city_name}, {state_name}. Browse local companies, contact information, and business details in {city_name}.">
    <meta name="keywords" content="{city_name} LLC directory, {city_name} businesses, {state_name} companies, local businesses {city_name}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://yourdomain.com/cities/{clean_text(city_name)}.html">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{city_name}, {state_name} LLC Directory - Local Businesses in {city_name}">
    <meta property="og:description" content="Find LLC businesses in {city_name}, {state_name}. Browse local companies, contact information, and business details.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://yourdomain.com/cities/{clean_text(city_name)}.html">
    
    <link rel="stylesheet" href="../styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="container">
                <div class="nav-brand">
                    <h1>LLC Directory</h1>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../states.html">States</a></li>
                    <li><a href="../about.html">About</a></li>
                    <li><a href="../contact.html">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <div class="breadcrumb">
        <div class="container">
            <a href="../index.html">Home</a> / <a href="../states.html">States</a> / <a href="../states/{clean_text(state_name)}.html">{state_name}</a> / <span>{city_name}</span>
        </div>
    </div>

    <div class="page-title">
        <div class="container">
            <h1>{city_name}, {state_name} LLC Directory</h1>
            <p>Find {business_count} businesses in {city_name}, {state_name}</p>
        </div>
    </div>

    <main class="main">
        <div class="container">
            <div class="business-list" id="businessList">{businesses_html}
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>LLC Directory</h3>
                    <p>Your comprehensive source for LLC business information across the United States.</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="../index.html">Home</a></li>
                        <li><a href="../states.html">All States</a></li>
                        <li><a href="../about.html">About Us</a></li>
                        <li><a href="../contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Popular States</h4>
                    <ul>
                        <li><a href="../states/florida.html">Florida</a></li>
                        <li><a href="../states/california.html">California</a></li>
                        <li><a href="../states/texas.html">Texas</a></li>
                        <li><a href="../states/new-york.html">New York</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 LLC Directory. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="../script.js"></script>
</body>
</html>'''
    
    return html

def process_csv_data(csv_file_path):
    """Process CSV data and generate pages"""
    # Create directories if they don't exist
    states_dir = Path("states")
    cities_dir = Path("cities")
    states_dir.mkdir(exist_ok=True)
    cities_dir.mkdir(exist_ok=True)
    
    # Data structures to organize businesses
    state_businesses = defaultdict(list)
    city_businesses = defaultdict(list)
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Extract and clean data
                business = {
                    'name': row.get('name', '').strip(),
                    'phone': format_phone(row.get('phone', '')),
                    'full_address': row.get('full_address', '').strip(),
                    'city': row.get('city', '').strip(),
                    'postal_code': row.get('postal_code', '').strip(),
                    'state': row.get('state', '').strip()
                }
                
                # Skip if missing essential data
                if not business['name'] or not business['state']:
                    continue
                
                # Organize by state
                state_businesses[business['state']].append(business)
                
                # Organize by city (within state)
                city_key = f"{business['city']}_{business['state']}"
                city_businesses[city_key].append(business)
        
        # Generate state pages
        for state_name, businesses in state_businesses.items():
            if not state_name:
                continue
                
            # Group businesses by city for this state
            state_cities = defaultdict(list)
            for business in businesses:
                if business['city']:
                    state_cities[business['city']].append(business)
            
            # Generate state page
            state_html = create_state_page(state_name, businesses, state_cities)
            state_filename = f"states/{clean_text(state_name)}.html"
            
            with open(state_filename, 'w', encoding='utf-8') as f:
                f.write(state_html)
            
            print(f"Generated state page: {state_filename} ({len(businesses)} businesses)")
        
        # Generate city pages
        for city_key, businesses in city_businesses.items():
            if not businesses:
                continue
                
            city_name, state_name = city_key.split('_', 1)
            if not city_name or not state_name:
                continue
            
            # Generate city page
            city_html = create_city_page(city_name, state_name, businesses)
            city_filename = f"cities/{clean_text(city_name)}.html"
            
            with open(city_filename, 'w', encoding='utf-8') as f:
                f.write(city_html)
            
            print(f"Generated city page: {city_filename} ({len(businesses)} businesses)")
        
        print(f"\nGeneration complete!")
        print(f"Total states: {len(state_businesses)}")
        print(f"Total cities: {len(city_businesses)}")
        
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"Error processing CSV: {e}")

if __name__ == "__main__":
    # Path to your CSV file
    csv_file = r"C:\Users\webd5\Downloads\LLC Data.csv"
    
    print("LLC Directory Page Generator")
    print("=" * 40)
    print(f"Processing CSV file: {csv_file}")
    print()
    
    process_csv_data(csv_file)
