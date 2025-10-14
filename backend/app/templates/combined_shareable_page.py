"""
Combined shareable page template for movies and restaurants.
Displays movies and/or restaurants based on entity_types configuration.
"""

def generate_combined_shareable_html(user, watchlist_items, saved_restaurants, entity_types):
    """
    Generate HTML for a combined shareable page showing movies and/or restaurants.
    
    Args:
        user: User object
        watchlist_items: List of WatchlistItem objects
        saved_restaurants: List of SavedRestaurant objects
        entity_types: List of strings, e.g., ["movies"], ["restaurants"], or ["movies", "restaurants"]
    
    Returns:
        HTML string
    """
    show_movies = "movies" in entity_types
    show_restaurants = "restaurants" in entity_types
    
    # Prepare movie data
    movies_data = []
    if show_movies:
        for item in watchlist_items:
            movie_data = item.movie_data if isinstance(item.movie_data, dict) else {}
            
            # Handle poster/image
            poster = (movie_data.get('posterUrl', '') or 
                     movie_data.get('poster', '') or 
                     movie_data.get('poster_path', '') or 
                     movie_data.get('image', ''))
            if poster and not poster.startswith('http'):
                poster = f"https://image.tmdb.org/t/p/w500{poster}"
            
            # Handle description
            description = (movie_data.get('synopsis', '') or 
                          movie_data.get('description', '') or 
                          movie_data.get('overview', '') or 
                          'No description available')
            
            # Extract other fields
            title = movie_data.get('title', movie_data.get('name', 'Untitled'))
            year = str(movie_data.get('year', movie_data.get('release_date', ''))).split('-')[0] if movie_data.get('year') or movie_data.get('release_date') else ''
            media_type = movie_data.get('type', movie_data.get('media_type', 'Unknown'))
            
            # Handle genres
            genres_raw = movie_data.get('genres', [])
            if isinstance(genres_raw, list):
                if genres_raw and isinstance(genres_raw[0], dict):
                    genres = ', '.join([g.get('name', '') for g in genres_raw if g.get('name')])
                else:
                    genres = ', '.join([str(g) for g in genres_raw if g])
            else:
                genres = str(genres_raw) if genres_raw else 'N/A'
            
            # Handle languages
            languages_raw = movie_data.get('languages', [])
            if isinstance(languages_raw, list):
                languages = ', '.join([str(lang) for lang in languages_raw if lang])
            else:
                languages = str(languages_raw) if languages_raw else 'N/A'
            
            # Rating
            rating = movie_data.get('rating', movie_data.get('vote_average', ''))
            
            # Watched status
            watched = item.watched if hasattr(item, 'watched') else False
            added_at = item.added_at.isoformat() if hasattr(item, 'added_at') else ''
            
            movies_data.append({
                'title': title,
                'year': year,
                'type': media_type,
                'genres': genres,
                'languages': languages,
                'description': description,
                'poster': poster,
                'rating': rating,
                'watched': watched,
                'addedAt': added_at
            })
    
    # Prepare restaurant data
    restaurants_data = []
    if show_restaurants:
        for item in saved_restaurants:
            restaurant_data = item.restaurant_data if isinstance(item.restaurant_data, dict) else {}
            
            # Extract restaurant details
            restaurant_name = restaurant_data.get('restaurant_name', 'Unknown Restaurant')
            description = restaurant_data.get('description', 'No description available')
            cuisine = restaurant_data.get('cuisine', 'N/A')
            city = restaurant_data.get('city', '')
            country = restaurant_data.get('country', '')
            location = f"{city}, {country}" if city and country else city or country or 'N/A'
            
            # Images
            images = restaurant_data.get('images', [])
            image = images[0] if images else ''
            
            # Type
            restaurant_type = restaurant_data.get('type', 'Restaurant')
            
            # Known for
            known_for = restaurant_data.get('known_for', [])
            known_for_text = ', '.join(known_for[:3]) if known_for else 'N/A'
            
            # User-specific data
            visited = item.visited if hasattr(item, 'visited') else False
            personal_rating = item.personal_rating if hasattr(item, 'personal_rating') else None
            notes = item.notes if hasattr(item, 'notes') else ''
            tags = item.tags if hasattr(item, 'tags') else []
            added_at = item.added_at.isoformat() if hasattr(item, 'added_at') else ''
            
            # Full restaurant data for detail view
            restaurants_data.append({
                'name': restaurant_name,
                'description': description,
                'cuisine': cuisine,
                'location': location,
                'image': image,
                'type': restaurant_type,
                'knownFor': known_for_text,
                'visited': visited,
                'personalRating': personal_rating,
                'notes': notes,
                'tags': tags,
                'addedAt': added_at,
                'fullData': restaurant_data  # Keep full data for detail view
            })
    
    # Generate section titles
    movies_title = f"{user.name}'s Watchlist" if show_movies and not show_restaurants else f"{user.name}'s Movies"
    restaurants_title = f"{user.name}'s Restaurants" if show_restaurants and not show_movies else f"{user.name}'s Restaurants"
    page_title = f"{user.name}'s Binger List"
    
    import json
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #141414;
                color: #ffffff;
                line-height: 1.6;
            }}
            
            .header {{
                background: linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.7) 100%);
                padding: 20px;
                text-align: center;
                position: sticky;
                top: 0;
                z-index: 100;
                backdrop-filter: blur(10px);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            
            .header h1 {{
                font-size: clamp(24px, 5vw, 36px);
                font-weight: 600;
                margin-bottom: 8px;
                color: #e50914;
            }}
            
            .header p {{
                font-size: clamp(14px, 3vw, 18px);
                color: rgba(255,255,255,0.7);
            }}
            
            .section {{
                padding: 30px 20px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            
            .section-title {{
                font-size: clamp(20px, 4vw, 28px);
                font-weight: 600;
                margin-bottom: 20px;
                color: #ffffff;
                padding-left: 10px;
                border-left: 4px solid #e50914;
            }}
            
            .controls {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 25px;
                padding: 0 10px;
            }}
            
            .filter-buttons {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .filter-btn {{
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s ease;
            }}
            
            .filter-btn.active {{
                background: #e50914;
                border-color: #e50914;
            }}
            
            .sort-select {{
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                cursor: pointer;
            }}
            
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 20px;
                padding: 0 10px;
            }}
            
            .card {{
                background: #1a1a1a;
                border-radius: 8px;
                overflow: hidden;
                cursor: pointer;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
            }}
            
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(229,9,20,0.3);
            }}
            
            .card-image {{
                width: 100%;
                height: 400px;
                object-fit: cover;
                background: #2a2a2a;
            }}
            
            .card-content {{
                padding: 15px;
            }}
            
            .card-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 8px;
                color: #ffffff;
            }}
            
            .card-info {{
                font-size: 13px;
                color: rgba(255,255,255,0.6);
                margin-bottom: 4px;
            }}
            
            .card-description {{
                font-size: 14px;
                color: rgba(255,255,255,0.7);
                line-height: 1.4;
                margin-top: 10px;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}
            
            .watched-badge {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(0,128,0,0.8);
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: 600;
            }}
            
            .footer {{
                text-align: center;
                padding: 30px 20px;
                color: rgba(255,255,255,0.5);
                font-size: 14px;
            }}
            
            .empty-state {{
                text-align: center;
                padding: 60px 20px;
                color: rgba(255,255,255,0.5);
            }}
            
            .empty-state-icon {{
                font-size: 64px;
                margin-bottom: 20px;
            }}
            
            /* Detail View Styles */
            .detail-view {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100vh;
                background: #141414;
                z-index: 1000;
                overflow-y: auto;
            }}
            
            .detail-view.active {{
                display: block;
            }}
            
            .detail-header {{
                position: relative;
                height: 60vh;
                background-size: cover;
                background-position: center;
            }}
            
            .detail-overlay {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 40px 20px;
                background: linear-gradient(to top, rgba(20,20,20,1) 0%, rgba(20,20,20,0) 100%);
            }}
            
            .detail-nav {{
                position: absolute;
                top: 20px;
                left: 20px;
                right: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .nav-btn {{
                background: rgba(0,0,0,0.7);
                border: none;
                color: white;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.3s;
            }}
            
            .nav-btn:hover {{
                background: rgba(229,9,20,0.9);
            }}
            
            .detail-content {{
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            .detail-title {{
                font-size: clamp(28px, 6vw, 42px);
                font-weight: 700;
                margin-bottom: 15px;
            }}
            
            .detail-meta {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin-bottom: 20px;
                font-size: 16px;
                color: rgba(255,255,255,0.7);
            }}
            
            .detail-meta span {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            
            .detail-description {{
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 30px;
                color: rgba(255,255,255,0.9);
            }}
            
            .detail-section {{
                margin-bottom: 30px;
            }}
            
            .detail-section h3 {{
                font-size: 20px;
                margin-bottom: 10px;
                color: #e50914;
            }}
            
            .detail-section p {{
                font-size: 16px;
                line-height: 1.6;
                color: rgba(255,255,255,0.8);
            }}
            
            @media (max-width: 768px) {{
                .grid {{
                    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                    gap: 15px;
                }}
                
                .card-image {{
                    height: 250px;
                }}
                
                .detail-header {{
                    height: 40vh;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{page_title}</h1>
            <p>Curated collection by {user.name}</p>
        </div>
        
        <!-- Movies Section -->
        {"" if not show_movies else f'''
        <div class="section" id="movies-section">
            <h2 class="section-title">{movies_title}</h2>
            
            <div class="controls">
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="all" data-section="movies">All</button>
                    <button class="filter-btn" data-filter="watched" data-section="movies">Watched</button>
                    <button class="filter-btn" data-filter="to-watch" data-section="movies">To Watch</button>
                </div>
                <select class="sort-select" id="movies-sort">
                    <option value="recent">Recently Added</option>
                    <option value="oldest">Oldest First</option>
                    <option value="az">A-Z</option>
                    <option value="za">Z-A</option>
                    <option value="rating">Highest Rated</option>
                    <option value="year-desc">Release Year (Newest)</option>
                    <option value="year-asc">Release Year (Oldest)</option>
                </select>
            </div>
            
            <div class="grid" id="movies-grid"></div>
        </div>
        '''}
        
        <!-- Restaurants Section -->
        {"" if not show_restaurants else f'''
        <div class="section" id="restaurants-section">
            <h2 class="section-title">{restaurants_title}</h2>
            
            <div class="controls">
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="all" data-section="restaurants">All</button>
                    <button class="filter-btn" data-filter="visited" data-section="restaurants">Visited</button>
                    <button class="filter-btn" data-filter="to-visit" data-section="restaurants">To Visit</button>
                </div>
                <select class="sort-select" id="restaurants-sort">
                    <option value="recent">Recently Added</option>
                    <option value="oldest">Oldest First</option>
                    <option value="az">A-Z</option>
                    <option value="za">Z-A</option>
                    <option value="rating">Highest Rated</option>
                </select>
            </div>
            
            <div class="grid" id="restaurants-grid"></div>
        </div>
        '''}
        
        <div class="footer">
            <p>Powered by Binger | Shared with ❤️</p>
        </div>
        
        <!-- Detail View -->
        <div class="detail-view" id="detail-view"></div>
        
        <script>
            // Data
            const moviesData = {json.dumps(movies_data)};
            const restaurantsData = {json.dumps(restaurants_data)};
            const showMovies = {json.dumps(show_movies)};
            const showRestaurants = {json.dumps(show_restaurants)};
            
            // State
            let currentMoviesFilter = 'all';
            let currentMoviesSort = 'recent';
            let currentRestaurantsFilter = 'all';
            let currentRestaurantsSort = 'recent';
            let currentDetailData = null;
            let currentDetailType = null;
            let currentDetailIndex = 0;
            
            // Initialize
            document.addEventListener('DOMContentLoaded', () => {{
                if (showMovies) {{
                    renderMovies();
                    setupMoviesControls();
                }}
                if (showRestaurants) {{
                    renderRestaurants();
                    setupRestaurantsControls();
                }}
            }});
            
            // Movies
            function setupMoviesControls() {{
                const filterButtons = document.querySelectorAll('[data-section="movies"]');
                filterButtons.forEach(btn => {{
                    btn.addEventListener('click', () => {{
                        filterButtons.forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        currentMoviesFilter = btn.dataset.filter;
                        renderMovies();
                    }});
                }});
                
                document.getElementById('movies-sort').addEventListener('change', (e) => {{
                    currentMoviesSort = e.target.value;
                    renderMovies();
                }});
            }}
            
            function filterMovies() {{
                let filtered = [...moviesData];
                if (currentMoviesFilter === 'watched') {{
                    filtered = filtered.filter(m => m.watched);
                }} else if (currentMoviesFilter === 'to-watch') {{
                    filtered = filtered.filter(m => !m.watched);
                }}
                return filtered;
            }}
            
            function sortMovies(movies) {{
                const sorted = [...movies];
                switch(currentMoviesSort) {{
                    case 'recent':
                        sorted.sort((a, b) => (b.addedAt || '').localeCompare(a.addedAt || ''));
                        break;
                    case 'oldest':
                        sorted.sort((a, b) => (a.addedAt || '').localeCompare(b.addedAt || ''));
                        break;
                    case 'az':
                        sorted.sort((a, b) => a.title.localeCompare(b.title));
                        break;
                    case 'za':
                        sorted.sort((a, b) => b.title.localeCompare(a.title));
                        break;
                    case 'rating':
                        sorted.sort((a, b) => (b.rating || 0) - (a.rating || 0));
                        break;
                    case 'year-desc':
                        sorted.sort((a, b) => (parseInt(b.year) || 0) - (parseInt(a.year) || 0));
                        break;
                    case 'year-asc':
                        sorted.sort((a, b) => (parseInt(a.year) || 0) - (parseInt(b.year) || 0));
                        break;
                }}
                return sorted;
            }}
            
            function renderMovies() {{
                const filtered = filterMovies();
                const sorted = sortMovies(filtered);
                const grid = document.getElementById('movies-grid');
                
                if (sorted.length === 0) {{
                    grid.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🎬</div>
                            <p>No movies to display</p>
                        </div>
                    `;
                    return;
                }}
                
                grid.innerHTML = sorted.map((movie, index) => `
                    <div class="card" onclick="openDetail('movie', ${{index}}, ${{JSON.stringify(sorted)}})">
                        ${{movie.watched ? '<div class="watched-badge">✓ Watched</div>' : ''}}
                        <img class="card-image" src="${{movie.poster || 'https://via.placeholder.com/300x450?text=No+Image'}}" alt="${{movie.title}}" onerror="this.src='https://via.placeholder.com/300x450?text=No+Image'">
                        <div class="card-content">
                            <h3 class="card-title">${{movie.title}}</h3>
                            <div class="card-info">${{movie.year}} • ${{movie.type}}</div>
                            <div class="card-info">${{movie.genres}}</div>
                            <div class="card-info">🗣 ${{movie.languages}}</div>
                            ${{movie.rating ? `<div class="card-info">⭐ ${{movie.rating}}</div>` : ''}}
                            <div class="card-description">${{movie.description}}</div>
                        </div>
                    </div>
                `).join('');
            }}
            
            // Restaurants
            function setupRestaurantsControls() {{
                const filterButtons = document.querySelectorAll('[data-section="restaurants"]');
                filterButtons.forEach(btn => {{
                    btn.addEventListener('click', () => {{
                        filterButtons.forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        currentRestaurantsFilter = btn.dataset.filter;
                        renderRestaurants();
                    }});
                }});
                
                document.getElementById('restaurants-sort').addEventListener('change', (e) => {{
                    currentRestaurantsSort = e.target.value;
                    renderRestaurants();
                }});
            }}
            
            function filterRestaurants() {{
                let filtered = [...restaurantsData];
                if (currentRestaurantsFilter === 'visited') {{
                    filtered = filtered.filter(r => r.visited);
                }} else if (currentRestaurantsFilter === 'to-visit') {{
                    filtered = filtered.filter(r => !r.visited);
                }}
                return filtered;
            }}
            
            function sortRestaurants(restaurants) {{
                const sorted = [...restaurants];
                switch(currentRestaurantsSort) {{
                    case 'recent':
                        sorted.sort((a, b) => (b.addedAt || '').localeCompare(a.addedAt || ''));
                        break;
                    case 'oldest':
                        sorted.sort((a, b) => (a.addedAt || '').localeCompare(b.addedAt || ''));
                        break;
                    case 'az':
                        sorted.sort((a, b) => a.name.localeCompare(b.name));
                        break;
                    case 'za':
                        sorted.sort((a, b) => b.name.localeCompare(a.name));
                        break;
                    case 'rating':
                        sorted.sort((a, b) => (b.personalRating || 0) - (a.personalRating || 0));
                        break;
                }}
                return sorted;
            }}
            
            function renderRestaurants() {{
                const filtered = filterRestaurants();
                const sorted = sortRestaurants(filtered);
                const grid = document.getElementById('restaurants-grid');
                
                if (sorted.length === 0) {{
                    grid.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🍽</div>
                            <p>No restaurants to display</p>
                        </div>
                    `;
                    return;
                }}
                
                grid.innerHTML = sorted.map((restaurant, index) => `
                    <div class="card" onclick="openDetail('restaurant', ${{index}}, ${{JSON.stringify(sorted)}})">
                        ${{restaurant.visited ? '<div class="watched-badge">✓ Visited</div>' : ''}}
                        <img class="card-image" src="${{restaurant.image || 'https://via.placeholder.com/300x450?text=No+Image'}}" alt="${{restaurant.name}}" onerror="this.src='https://via.placeholder.com/300x450?text=No+Image'">
                        <div class="card-content">
                            <h3 class="card-title">${{restaurant.name}}</h3>
                            <div class="card-info">${{restaurant.cuisine}} • ${{restaurant.type}}</div>
                            <div class="card-info">📍 ${{restaurant.location}}</div>
                            ${{restaurant.personalRating ? `<div class="card-info">⭐ ${{restaurant.personalRating}}/5</div>` : ''}}
                            <div class="card-info">🌟 ${{restaurant.knownFor}}</div>
                            <div class="card-description">${{restaurant.description}}</div>
                        </div>
                    </div>
                `).join('');
            }}
            
            // Detail View
            function openDetail(type, index, data) {{
                currentDetailType = type;
                currentDetailIndex = index;
                currentDetailData = data;
                renderDetailView();
                
                // Hide main content
                document.querySelector('.header').style.display = 'none';
                document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
                document.querySelector('.footer').style.display = 'none';
                document.getElementById('detail-view').classList.add('active');
                
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
            
            function closeDetail() {{
                document.getElementById('detail-view').classList.remove('active');
                document.querySelector('.header').style.display = 'block';
                document.querySelectorAll('.section').forEach(s => s.style.display = 'block');
                document.querySelector('.footer').style.display = 'block';
            }}
            
            function showNext() {{
                if (currentDetailIndex < currentDetailData.length - 1) {{
                    currentDetailIndex++;
                    renderDetailView();
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}
            }}
            
            function showPrev() {{
                if (currentDetailIndex > 0) {{
                    currentDetailIndex--;
                    renderDetailView();
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}
            }}
            
            function renderDetailView() {{
                const item = currentDetailData[currentDetailIndex];
                const isFirst = currentDetailIndex === 0;
                const isLast = currentDetailIndex === currentDetailData.length - 1;
                
                let html = '';
                
                if (currentDetailType === 'movie') {{
                    html = `
                        <div class="detail-header" style="background-image: linear-gradient(to bottom, rgba(20,20,20,0.3), rgba(20,20,20,1)), url('${{item.poster || 'https://via.placeholder.com/1200x600?text=No+Image'}}');">
                            <div class="detail-nav">
                                <button class="nav-btn" onclick="closeDetail()">✕</button>
                                <div style="display: flex; gap: 10px;">
                                    <button class="nav-btn" onclick="showPrev()" ${{isFirst ? 'style="opacity:0.3;pointer-events:none;"' : ''}}>←</button>
                                    <button class="nav-btn" onclick="showNext()" ${{isLast ? 'style="opacity:0.3;pointer-events:none;"' : ''}}>→</button>
                                </div>
                            </div>
                            <div class="detail-overlay">
                                <div class="detail-title">${{item.title}}</div>
                                <div class="detail-meta">
                                    <span>${{item.year}}</span>
                                    <span>•</span>
                                    <span>${{item.type}}</span>
                                    ${{item.rating ? `<span>•</span><span>⭐ ${{item.rating}}</span>` : ''}}
                                    ${{item.watched ? '<span>•</span><span style="color: #4CAF50;">✓ Watched</span>' : ''}}
                                </div>
                            </div>
                        </div>
                        <div class="detail-content">
                            <div class="detail-section">
                                <h3>Overview</h3>
                                <p class="detail-description">${{item.description}}</p>
                            </div>
                            <div class="detail-section">
                                <h3>Genres</h3>
                                <p>${{item.genres}}</p>
                            </div>
                            <div class="detail-section">
                                <h3>Languages</h3>
                                <p>${{item.languages}}</p>
                            </div>
                        </div>
                    `;
                }} else {{
                    const fullData = item.fullData || {{}};
                    html = `
                        <div class="detail-header" style="background-image: linear-gradient(to bottom, rgba(20,20,20,0.3), rgba(20,20,20,1)), url('${{item.image || 'https://via.placeholder.com/1200x600?text=No+Image'}}');">
                            <div class="detail-nav">
                                <button class="nav-btn" onclick="closeDetail()">✕</button>
                                <div style="display: flex; gap: 10px;">
                                    <button class="nav-btn" onclick="showPrev()" ${{isFirst ? 'style="opacity:0.3;pointer-events:none;"' : ''}}>←</button>
                                    <button class="nav-btn" onclick="showNext()" ${{isLast ? 'style="opacity:0.3;pointer-events:none;"' : ''}}>→</button>
                                </div>
                            </div>
                            <div class="detail-overlay">
                                <div class="detail-title">${{item.name}}</div>
                                <div class="detail-meta">
                                    <span>${{item.cuisine}}</span>
                                    <span>•</span>
                                    <span>${{item.type}}</span>
                                    ${{item.personalRating ? `<span>•</span><span>⭐ ${{item.personalRating}}/5</span>` : ''}}
                                    ${{item.visited ? '<span>•</span><span style="color: #4CAF50;">✓ Visited</span>' : ''}}
                                </div>
                            </div>
                        </div>
                        <div class="detail-content">
                            <div class="detail-section">
                                <h3>About</h3>
                                <p class="detail-description">${{item.description}}</p>
                            </div>
                            <div class="detail-section">
                                <h3>Location</h3>
                                <p>${{item.location}}</p>
                                ${{fullData.google_maps_url ? `<p><a href="${{fullData.google_maps_url}}" target="_blank" style="color: #e50914;">View on Google Maps</a></p>` : ''}}
                            </div>
                            ${{fullData.known_for && fullData.known_for.length > 0 ? `
                            <div class="detail-section">
                                <h3>Known For</h3>
                                <p>${{fullData.known_for.join(', ')}}</p>
                            </div>
                            ` : ''}}
                            ${{fullData.phone_number ? `
                            <div class="detail-section">
                                <h3>Contact</h3>
                                <p>📞 ${{fullData.phone_number}}</p>
                                ${{fullData.website ? `<p><a href="${{fullData.website}}" target="_blank" style="color: #e50914;">Visit Website</a></p>` : ''}}
                            </div>
                            ` : ''}}
                            ${{item.notes ? `
                            <div class="detail-section">
                                <h3>Personal Notes</h3>
                                <p>${{item.notes}}</p>
                            </div>
                            ` : ''}}
                            ${{item.tags && item.tags.length > 0 ? `
                            <div class="detail-section">
                                <h3>Tags</h3>
                                <p>${{item.tags.join(', ')}}</p>
                            </div>
                            ` : ''}}
                        </div>
                    `;
                }}
                
                document.getElementById('detail-view').innerHTML = html;
            }}
        </script>
    </body>
    </html>
    """
    
    return html_content

