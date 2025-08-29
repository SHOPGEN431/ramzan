// Utility functions
function formatPhoneNumber(phone) {
    if (!phone) return '';
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 11 && cleaned.startsWith('1')) {
        return `+1 (${cleaned.slice(1, 4)}) ${cleaned.slice(4, 7)}-${cleaned.slice(7)}`;
    }
    if (cleaned.length === 10) {
        return `+1 (${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }
    return phone;
}

function createSlug(text) {
    return text.toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .trim();
}

// Search functionality
function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.toLowerCase().trim();
    
    if (!query) return;
    
    // Redirect to search results
    window.location.href = `/search?q=${encodeURIComponent(query)}`;
}

// Allow Enter key to trigger search
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    // Contact form validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Simple validation
            if (!data.name || !data.email || !data.message) {
                alert('Please fill in all required fields.');
                return;
            }
            
            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(data.email)) {
                alert('Please enter a valid email address.');
                return;
            }
            
            // Show success message (in a real app, you'd send this to your server)
            alert('Thank you for your message! We\'ll get back to you soon.');
            this.reset();
        });
    }
    
    // Initialize navigation
    initializeNavigation();
});

// Load navigation dropdowns with top 25 states and cities
async function loadNavigationDropdowns() {
    try {
        // Load top states
        const statesResponse = await fetch('/api/top-states');
        const states = await statesResponse.json();
        
        const navStateLinks = document.getElementById('navStateLinks');
        if (navStateLinks) {
            states.forEach(state => {
                const link = document.createElement('a');
                link.href = `/states/${state.slug}`;
                link.textContent = state.name;
                navStateLinks.appendChild(link);
            });
        }
        
        // Load top cities
        const citiesResponse = await fetch('/api/top-cities');
        const cities = await citiesResponse.json();
        
        const navCityLinks = document.getElementById('navCityLinks');
        if (navCityLinks) {
            cities.forEach(city => {
                const link = document.createElement('a');
                link.href = `/cities/${city.slug}`;
                link.textContent = `${city.name}, ${city.state}`;
                navCityLinks.appendChild(link);
            });
        }
    } catch (error) {
        console.error('Error loading navigation dropdowns:', error);
    }
}

// Initialize navigation
function initializeNavigation() {
    // Load navigation dropdowns
    loadNavigationDropdowns();
    console.log('Navigation initialized');
}

// API functions for dynamic content loading
async function loadStates() {
    try {
        const response = await fetch('/api/states');
        const states = await response.json();
        return states;
    } catch (error) {
        console.error('Error loading states:', error);
        return [];
    }
}

async function loadCities(stateSlug) {
    try {
        const response = await fetch(`/api/cities/${stateSlug}`);
        const cities = await response.json();
        return cities;
    } catch (error) {
        console.error('Error loading cities:', error);
        return [];
    }
}

// Dynamic content loading functions
function populateStatesGrid(containerId, states) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = states.map(state => `
        <a href="/states/${state.slug}" class="state-card">
            <h3>${state.name}</h3>
            <p>Find ${state.business_count} businesses across ${state.city_count} cities in ${state.name}</p>
            <div class="state-stats">
                <span>${state.business_count} Businesses</span>
                <span>${state.city_count} Cities</span>
            </div>
        </a>
    `).join('');
}

function populateCitiesGrid(containerId, cities) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = cities.map(city => `
        <a href="/cities/${city.slug}" class="city-card">
            <h3>${city.name}</h3>
            <p>${city.business_count} businesses</p>
        </a>
    `).join('');
}

// URL parsing utilities
function getCurrentState() {
    const path = window.location.pathname;
    const stateMatch = path.match(/\/states\/([^\/]+)/);
    return stateMatch ? stateMatch[1] : null;
}

function getCurrentCity() {
    const path = window.location.pathname;
    const cityMatch = path.match(/\/cities\/([^\/]+)/);
    return cityMatch ? cityMatch[1] : null;
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const overlay = document.getElementById('mobileMenuOverlay');
    const body = document.body;
    
    if (navMenu && mobileToggle) {
        navMenu.classList.toggle('active');
        mobileToggle.classList.toggle('active');
        
        if (overlay) {
            overlay.classList.toggle('active');
        }
        
        // Toggle body scroll
        body.classList.toggle('menu-open');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const navMenu = document.getElementById('navMenu');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const overlay = document.getElementById('mobileMenuOverlay');
    
    if (navMenu && mobileToggle) {
        if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target) && !overlay.contains(e.target)) {
            navMenu.classList.remove('active');
            mobileToggle.classList.remove('active');
            overlay.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    }
});

// Close mobile menu when pressing Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('navMenu');
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const overlay = document.getElementById('mobileMenuOverlay');
        
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            mobileToggle.classList.remove('active');
            overlay.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    }
});

// Add loading states to buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;
    return () => {
        button.textContent = originalText;
        button.disabled = false;
    };
}

// Error handling utility
function showError(message) {
    // Create a simple error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff6b6b;
        color: white;
        padding: 1rem 2rem;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Success notification utility
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #51cf66;
        color: white;
        padding: 1rem 2rem;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
