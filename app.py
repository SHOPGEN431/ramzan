from flask import Flask, render_template, request, jsonify, make_response
import csv
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
import os

app = Flask(__name__)

# Global data storage
businesses_data = []
states_data = defaultdict(list)
cities_data = defaultdict(list)

def load_data_from_csv():
    """Load business data from CSV file"""
    # Check if running on Vercel (production) or local development
    if os.environ.get('VERCEL_ENV'):
        # For Vercel deployment, use a different path or handle data differently
        # For now, we'll create some sample data
        create_sample_data()
    else:
        # Local development - load from CSV
        csv_file = r"C:\Users\webd5\Downloads\LLC Data.csv"
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
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
                    
                    businesses_data.append(business)
                    
                    # Organize by state
                    states_data[business['state']].append(business)
                    
                    # Organize by city (within state)
                    city_key = f"{business['city']}_{business['state']}"
                    cities_data[city_key].append(business)
            
            print(f"Loaded {len(businesses_data)} businesses")
            print(f"States: {len(states_data)}")
            print(f"Cities: {len(cities_data)}")
            
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_file}")
            create_sample_data()
        except Exception as e:
            print(f"Error processing CSV: {e}")
            create_sample_data()

def create_sample_data():
    """Create sample data for Vercel deployment"""
    sample_businesses = [
        {
            'name': 'ABC Legal Services',
            'phone': '+1 (555) 123-4567',
            'full_address': '123 Main St, Los Angeles, CA 90210',
            'city': 'Los Angeles',
            'postal_code': '90210',
            'state': 'California'
        },
        {
            'name': 'XYZ Business Solutions',
            'phone': '+1 (555) 987-6543',
            'full_address': '456 Oak Ave, New York, NY 10001',
            'city': 'New York',
            'postal_code': '10001',
            'state': 'New York'
        },
        {
            'name': 'Best LLC Services',
            'phone': '+1 (555) 456-7890',
            'full_address': '789 Pine St, Chicago, IL 60601',
            'city': 'Chicago',
            'postal_code': '60601',
            'state': 'Illinois'
        }
    ]
    
    for business in sample_businesses:
        businesses_data.append(business)
        states_data[business['state']].append(business)
        city_key = f"{business['city']}_{business['state']}"
        cities_data[city_key].append(business)
    
    print(f"Created {len(businesses_data)} sample businesses")

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

def clean_text(text):
    """Clean and format text for URLs"""
    if not text:
        return ""
    # Remove special characters and replace spaces with hyphens
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', str(text))
    cleaned = re.sub(r'\s+', '-', cleaned.strip())
    return cleaned.lower()

# Load data when app starts
load_data_from_csv()

@app.route('/')
def index():
    """Homepage"""
    # Get top 25 states by business count
    top_states = sorted(states_data.items(), key=lambda x: len(x[1]), reverse=True)[:25]
    
    # Get top 25 cities by business count - format as tuples for template
    top_cities = []
    for city_key, businesses in cities_data.items():
        city_name, state_name = city_key.split('_', 1)
        top_cities.append((city_name, businesses))
    top_cities = sorted(top_cities, key=lambda x: len(x[1]), reverse=True)[:25]
    
    # Get all states for the browse section
    states = []
    for state_name, businesses in states_data.items():
        states.append((state_name, businesses))
    states = sorted(states, key=lambda x: len(x[1]), reverse=True)
    
    stats = {
        'states': min(len(states_data), 50),  # Cap at 50 states
        'cities': len(cities_data),
        'businesses': len(businesses_data)
    }
    
    return render_template('index.html', 
                         top_states=top_states, 
                         top_cities=top_cities, 
                         states=states,
                         businesses=businesses_data,
                         cities=cities_data,
                         stats=stats)

@app.route('/states')
def states():
    """All states page"""
    # Sort states by business count
    sorted_states = sorted(states_data.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Add business count and city count to each state
    states_with_counts = []
    for state_name, businesses in sorted_states:
        cities = set(business['city'] for business in businesses if business['city'])
        states_with_counts.append({
            'name': state_name,
            'slug': clean_text(state_name),
            'business_count': len(businesses),
            'city_count': len(cities),
            'description': f"Find {len(businesses)} businesses across {len(cities)} cities in {state_name}"
        })
    
    return render_template('states.html', states=states_with_counts)

@app.route('/states/<state_slug>')
def state_page(state_slug):
    """Individual state page"""
    # Find state by slug
    state_name = None
    for name in states_data.keys():
        if clean_text(name) == state_slug:
            state_name = name
            break
    
    if not state_name:
        return "State not found", 404
    
    businesses = states_data[state_name]
    
    # Group businesses by city
    cities = defaultdict(list)
    for business in businesses:
        if business['city']:
            cities[business['city']].append(business)
    
    # Sort cities by business count
    sorted_cities = sorted(cities.items(), key=lambda x: len(x[1]), reverse=True)
    
    return render_template('state.html', 
                         state_name=state_name,
                         businesses=businesses,
                         cities=sorted_cities)

@app.route('/cities/<city_slug>')
def city_page(city_slug):
    """Individual city page"""
    # Find city by slug
    city_name = None
    state_name = None
    
    for city_key, businesses in cities_data.items():
        city, state = city_key.split('_', 1)
        if clean_text(city) == city_slug:
            city_name = city
            state_name = state
            break
    
    if not city_name or not state_name:
        return "City not found", 404
    
    businesses = cities_data[f"{city_name}_{state_name}"]
    
    return render_template('city.html',
                         city_name=city_name,
                         state_name=state_name,
                         businesses=businesses)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@app.route('/locations')
def locations():
    """All locations page - simple listing of states and cities"""
    # Get all states sorted by business count
    all_states = []
    for state_name, businesses in states_data.items():
        cities = set(business['city'] for business in businesses if business['city'])
        all_states.append({
            'name': state_name,
            'slug': clean_text(state_name),
            'business_count': len(businesses),
            'city_count': len(cities)
        })
    
    # Get all cities sorted by business count
    all_cities = []
    for city_key, businesses in cities_data.items():
        city_name, state_name = city_key.split('_', 1)
        all_cities.append({
            'name': city_name,
            'state': state_name,
            'slug': clean_text(city_name),
            'business_count': len(businesses)
        })
    
    # Sort by business count
    all_states = sorted(all_states, key=lambda x: x['business_count'], reverse=True)
    all_cities = sorted(all_cities, key=lambda x: x['business_count'], reverse=True)
    
    return render_template('locations.html', states=all_states, cities=all_cities)

@app.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap"""
    # Create XML structure
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Get base URL for sitemap
    base_url = request.host_url.rstrip('/')
    
    # Add static pages
    static_pages = [
        {'loc': f"{base_url}/", 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': f"{base_url}/about", 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': f"{base_url}/contact", 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': f"{base_url}/privacy", 'priority': '0.6', 'changefreq': 'monthly'},
        {'loc': f"{base_url}/locations", 'priority': '0.9', 'changefreq': 'weekly'},
    ]
    
    for page in static_pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = page['loc']
        ET.SubElement(url, 'priority').text = page['priority']
        ET.SubElement(url, 'changefreq').text = page['changefreq']
        ET.SubElement(url, 'lastmod').text = '2025-01-15'
    
    # Add state pages
    for state_name in states_data.keys():
        state_slug = clean_text(state_name)
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f"{base_url}/states/{state_slug}"
        ET.SubElement(url, 'priority').text = '0.9'
        ET.SubElement(url, 'changefreq').text = 'weekly'
        ET.SubElement(url, 'lastmod').text = '2025-01-15'
    
    # Add city pages
    for city_key in cities_data.keys():
        city_name, state_name = city_key.split('_', 1)
        city_slug = clean_text(city_name)
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f"{base_url}/cities/{city_slug}"
        ET.SubElement(url, 'priority').text = '0.8'
        ET.SubElement(url, 'changefreq').text = 'weekly'
        ET.SubElement(url, 'lastmod').text = '2025-01-15'
    
    # Create XML string
    xml_string = ET.tostring(urlset, encoding='unicode')
    
    # Create response
    response = make_response(xml_string)
    response.headers['Content-Type'] = 'application/xml'
    return response

# API endpoints for navigation dropdowns
@app.route('/api/top-states')
def api_top_states():
    """API endpoint for top states"""
    top_states = sorted(states_data.items(), key=lambda x: len(x[1]), reverse=True)[:25]
    result = []
    for state_name, businesses in top_states:
        result.append({
            'name': state_name,
            'slug': clean_text(state_name),
            'business_count': len(businesses)
        })
    return jsonify(result)

@app.route('/api/top-cities')
def api_top_cities():
    """API endpoint for top cities"""
    top_cities = []
    for city_key, businesses in cities_data.items():
        city_name, state_name = city_key.split('_', 1)
        top_cities.append({
            'name': f"{city_name}, {state_name}",
            'slug': clean_text(city_name),
            'business_count': len(businesses)
        })
    
    # Sort by business count and take top 25
    top_cities = sorted(top_cities, key=lambda x: x['business_count'], reverse=True)[:25]
    return jsonify(top_cities)

@app.route('/api/states')
def api_states():
    """API endpoint for all states"""
    result = []
    for state_name, businesses in states_data.items():
        result.append({
            'name': state_name,
            'slug': clean_text(state_name),
            'business_count': len(businesses)
        })
    return jsonify(result)

@app.route('/api/cities')
def api_cities():
    """API endpoint for all cities"""
    result = []
    for city_key, businesses in cities_data.items():
        city_name, state_name = city_key.split('_', 1)
        result.append({
            'name': city_name,
            'state': state_name,
            'slug': clean_text(city_name),
            'business_count': len(businesses)
        })
    return jsonify(result)

@app.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '').lower().strip()
    
    if not query:
        return render_template('search.html', results=[], query='')
    
    # Search in business names, cities, and states
    results = []
    for business in businesses_data:
        if (query in business['name'].lower() or 
            query in business['city'].lower() or 
            query in business['state'].lower()):
            results.append(business)
    
    return render_template('search.html', results=results, query=query)

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
