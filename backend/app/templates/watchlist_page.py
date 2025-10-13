"""
Beautiful, sleek HTML template for public watchlist pages
Mobile-first, Netflix-inspired design
"""

def generate_sleek_watchlist_html(user_name: str, movies_json: str) -> str:
    """
    Generate a beautiful, sleek watchlist page
    
    Args:
        user_name: Name of the user
        movies_json: JSON string of movies array
    
    Returns:
        Complete HTML string
    """
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{user_name}'s Watchlist - Binger</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0f0f0f;
            color: #ffffff;
            min-height: 100vh;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(180deg, rgba(15,15,15,0.95) 0%, transparent 100%);
            padding: 20px;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        
        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .brand-logo {{
            font-size: 28px;
        }}
        
        .brand-text h1 {{
            font-size: 20px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}
        
        .brand-text p {{
            font-size: 13px;
            color: #888;
            font-weight: 400;
        }}
        
        .stats-mini {{
            display: flex;
            gap: 20px;
            font-size: 14px;
        }}
        
        .stat-mini {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .stat-mini-number {{
            font-weight: 700;
            color: #ff4444;
        }}
        
        .stat-mini-label {{
            color: #999;
        }}
        
        /* Controls */
        .controls {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        
        .sort-container {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .sort-label {{
            font-size: 14px;
            color: #999;
            font-weight: 500;
        }}
        
        .sort-select {{
            background: #1a1a1a;
            border: 1px solid #333;
            color: white;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .sort-select:hover {{
            border-color: #555;
        }}
        
        .sort-select:focus {{
            outline: none;
            border-color: #ff4444;
        }}
        
        .filters {{
            display: flex;
            gap: 8px;
        }}
        
        .filter-btn {{
            background: transparent;
            border: 1px solid #333;
            color: #ccc;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .filter-btn:hover {{
            border-color: #ff4444;
            color: white;
        }}
        
        .filter-btn.active {{
            background: #ff4444;
            border-color: #ff4444;
            color: white;
        }}
        
        /* Movies Grid */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px 60px;
        }}
        
        .movies-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
            gap: 24px;
        }}
        
        .movie-card {{
            background: #1a1a1a;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            border: 1px solid #222;
        }}
        
        .movie-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            border-color: #333;
        }}
        
        .movie-poster-container {{
            position: relative;
            width: 100%;
            padding-top: 150%;
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            overflow: hidden;
        }}
        
        .movie-poster {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .watched-badge {{
            position: absolute;
            top: 12px;
            right: 12px;
            background: #10b981;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 8px rgba(16,185,129,0.3);
        }}
        
        .movie-info {{
            padding: 16px;
        }}
        
        .movie-title {{
            font-size: 17px;
            font-weight: 600;
            margin-bottom: 8px;
            line-height: 1.3;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .movie-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 13px;
            color: #999;
            flex-wrap: wrap;
        }}
        
        .movie-year {{
            font-weight: 500;
        }}
        
        .meta-separator {{
            color: #555;
        }}
        
        .movie-type {{
            color: #888;
        }}
        
        .movie-rating {{
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 4px;
            color: #fbbf24;
            font-weight: 600;
        }}
        
        .movie-genres {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }}
        
        .genre-tag {{
            background: #252525;
            color: #ccc;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 0.3px;
        }}
        
        .movie-languages {{
            font-size: 12px;
            color: #777;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        
        .movie-description {{
            font-size: 13px;
            line-height: 1.5;
            color: #aaa;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 100px 20px;
        }}
        
        .empty-state-icon {{
            font-size: 64px;
            margin-bottom: 16px;
        }}
        
        .empty-state-text {{
            font-size: 18px;
            color: #666;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 13px;
        }}
        
        /* Detail View */
        .detail-view {{
            display: none;
            animation: slideIn 0.3s ease;
        }}
        
        .detail-view.active {{
            display: block;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .detail-nav {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(15,15,15,0.95);
            backdrop-filter: blur(10px);
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .detail-nav-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .back-btn, .nav-btn {{
            background: rgba(255,255,255,0.1);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .back-btn:hover, .nav-btn:hover {{
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }}
        
        .nav-btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
            transform: none;
        }}
        
        .detail-nav-right {{
            display: flex;
            gap: 8px;
        }}
        
        .detail-hero {{
            position: relative;
            height: 60vh;
            min-height: 400px;
            background: #1a1a1a;
            overflow: hidden;
        }}
        
        .detail-hero-bg {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.3;
        }}
        
        .detail-hero-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 60px 40px;
            background: linear-gradient(0deg, rgba(15,15,15,1) 0%, transparent 100%);
        }}
        
        .detail-title {{
            font-size: clamp(32px, 5vw, 56px);
            font-weight: 700;
            margin-bottom: 20px;
            line-height: 1.1;
        }}
        
        .detail-meta {{
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 16px;
            color: #999;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        
        .detail-meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .detail-rating {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #fbbf24;
            font-size: 24px;
            font-weight: 700;
        }}
        
        .detail-watched {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #10B981;
            color: white;
            padding: 8px 16px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 14px;
        }}
        
        .detail-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .detail-section {{
            margin-bottom: 40px;
        }}
        
        .detail-section-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #ff4444;
        }}
        
        .detail-description {{
            font-size: 18px;
            line-height: 1.8;
            color: #ccc;
        }}
        
        .detail-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
        }}
        
        .detail-info-card {{
            background: rgba(255,255,255,0.05);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .detail-info-label {{
            font-size: 13px;
            color: #888;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .detail-info-value {{
            font-size: 17px;
            color: #fff;
            font-weight: 500;
            line-height: 1.5;
        }}
        
        .detail-genres {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .detail-genre-tag {{
            background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .detail-cast {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .detail-cast-item {{
            background: rgba(255,255,255,0.08);
            color: #ddd;
            padding: 10px 16px;
            border-radius: 10px;
            font-size: 14px;
        }}
        
        /* Mobile Responsive */
        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .controls {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .sort-container {{
                width: 100%;
                justify-content: space-between;
            }}
            
            .filters {{
                width: 100%;
                justify-content: space-between;
            }}
            
            .filter-btn {{
                flex: 1;
                text-align: center;
            }}
            
            .movies-grid {{
                grid-template-columns: repeat(auto-fill, minmax(min(100%, 150px), 1fr));
                gap: 16px;
            }}
            
            .movie-info {{
                padding: 12px;
            }}
            
            .movie-title {{
                font-size: 15px;
            }}
            
            .movie-meta {{
                font-size: 12px;
            }}
            
            .movie-description {{
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="brand">
                <div class="brand-logo">🎬</div>
                <div class="brand-text">
                    <h1>{user_name}'s Watchlist</h1>
                    <p>Shared via Binger</p>
                </div>
            </div>
            <div class="stats-mini">
                <div class="stat-mini">
                    <span class="stat-mini-number" id="total-count">0</span>
                    <span class="stat-mini-label">Total</span>
                </div>
                <div class="stat-mini">
                    <span class="stat-mini-number" id="watched-count">0</span>
                    <span class="stat-mini-label">Watched</span>
                </div>
                <div class="stat-mini">
                    <span class="stat-mini-number" id="towatch-count">0</span>
                    <span class="stat-mini-label">To Watch</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="sort-container">
            <span class="sort-label">Sort by:</span>
            <select class="sort-select" id="sort-select">
                <option value="recent">Recently Added</option>
                <option value="oldest">Oldest First</option>
                <option value="az">A-Z</option>
                <option value="za">Z-A</option>
                <option value="rating">Highest Rated</option>
                <option value="year-desc">Release Year (Newest)</option>
                <option value="year-asc">Release Year (Oldest)</option>
            </select>
        </div>
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="watched">Watched</button>
            <button class="filter-btn" data-filter="towatch">To Watch</button>
        </div>
    </div>
    
    <div class="container">
        <div class="movies-grid" id="movies-grid"></div>
        <div class="empty-state" id="empty-state" style="display: none;">
            <div class="empty-state-icon">🎬</div>
            <div class="empty-state-text">No movies found</div>
        </div>
    </div>
    
    <div class="footer">
        <p>Powered by Binger • Share your watchlist with friends</p>
    </div>
    
    <!-- Movie Detail View -->
    <div class="detail-view" id="detail-view"></div>
    
    <script>
        let movies = {movies_json};
        let currentFilter = 'all';
        let currentSort = 'recent';
        
        function updateStats() {{
            const totalCount = movies.length;
            const watchedCount = movies.filter(m => m.watched).length;
            const toWatchCount = totalCount - watchedCount;
            
            document.getElementById('total-count').textContent = totalCount;
            document.getElementById('watched-count').textContent = watchedCount;
            document.getElementById('towatch-count').textContent = toWatchCount;
        }}
        
        function sortMovies(movies) {{
            const sorted = [...movies];
            switch (currentSort) {{
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
            const grid = document.getElementById('movies-grid');
            const emptyState = document.getElementById('empty-state');
            
            let filteredMovies = movies;
            if (currentFilter === 'watched') {{
                filteredMovies = movies.filter(m => m.watched);
            }} else if (currentFilter === 'towatch') {{
                filteredMovies = movies.filter(m => !m.watched);
            }}
            
            const sortedMovies = sortMovies(filteredMovies);
            
            if (sortedMovies.length === 0) {{
                grid.innerHTML = '';
                emptyState.style.display = 'block';
                return;
            }}
            
            emptyState.style.display = 'none';
            
            grid.innerHTML = sortedMovies.map((movie, index) => {{
                const genreTags = movie.genres ? movie.genres.split(',').map(g => 
                    `<span class="genre-tag">${{g.trim()}}</span>`
                ).join('') : '';
                
                return `
                    <div class="movie-card" data-movie-index="${{index}}" onclick="openModal(${{index}})">
                        <div class="movie-poster-container">
                            ${{movie.watched ? '<div class="watched-badge">✓ Watched</div>' : ''}}
                            <img src="${{movie.poster || 'data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 400 600\\'%3E%3Crect fill=\\'%231a1a1a\\' width=\\'400\\' height=\\'600\\'/%3E%3Ctext x=\\'50%25\\' y=\\'50%25\\' text-anchor=\\'middle\\' dominant-baseline=\\'middle\\' font-size=\\'24\\' fill=\\'%23666\\' font-family=\\'Arial\\'%3ENo Image%3C/text%3E%3C/svg%3E'}}" 
                                 alt="${{movie.title}}" 
                                 class="movie-poster"
                                 onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 400 600\\'%3E%3Crect fill=\\'%231a1a1a\\' width=\\'400\\' height=\\'600\\'/%3E%3Ctext x=\\'50%25\\' y=\\'50%25\\' text-anchor=\\'middle\\' dominant-baseline=\\'middle\\' font-size=\\'24\\' fill=\\'%23666\\' font-family=\\'Arial\\'%3ENo Image%3C/text%3E%3C/svg%3E'">
                        </div>
                        <div class="movie-info">
                            <div class="movie-title">${{movie.title}}</div>
                            <div class="movie-meta">
                                <span class="movie-year">${{movie.year || 'N/A'}}</span>
                                ${{movie.type ? `<span class="meta-separator">•</span><span class="movie-type">${{movie.type}}</span>` : ''}}
                                ${{movie.rating ? `<span class="movie-rating">⭐ ${{movie.rating.toFixed(1)}}</span>` : ''}}
                            </div>
                            ${{genreTags ? `<div class="movie-genres">${{genreTags}}</div>` : ''}}
                            ${{movie.languages ? `<div class="movie-languages">🌐 ${{movie.languages}}</div>` : ''}}
                            <div class="movie-description">${{movie.description}}</div>
                        </div>
                    </div>
                `;
            }}).join('');
            
            // Store currently displayed movies for modal navigation
            window.currentMovies = sortedMovies;
        }}
        
        // Event listeners
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderMovies();
            }});
        }});
        
        document.getElementById('sort-select').addEventListener('change', (e) => {{
            currentSort = e.target.value;
            renderMovies();
        }});
        
        // Detail View Functions
        let currentDetailIndex = 0;
        
        function openDetail(index) {{
            currentDetailIndex = index;
            renderDetailView();
            
            // Hide main content, show detail view
            document.querySelector('.header').style.display = 'none';
            document.querySelector('.controls').style.display = 'none';
            document.querySelector('.container').style.display = 'none';
            document.querySelector('.footer').style.display = 'none';
            document.getElementById('detail-view').classList.add('active');
            
            // Scroll to top
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        function closeDetail() {{
            document.getElementById('detail-view').classList.remove('active');
            document.querySelector('.header').style.display = 'block';
            document.querySelector('.controls').style.display = 'flex';
            document.querySelector('.container').style.display = 'block';
            document.querySelector('.footer').style.display = 'block';
        }}
        
        function showNextMovie() {{
            if (currentDetailIndex < window.currentMovies.length - 1) {{
                currentDetailIndex++;
                renderDetailView();
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        }}
        
        function showPrevMovie() {{
            if (currentDetailIndex > 0) {{
                currentDetailIndex--;
                renderDetailView();
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        }}
        
        function renderDetailView() {{
            const movie = window.currentMovies[currentDetailIndex];
            const isFirst = currentDetailIndex === 0;
            const isLast = currentDetailIndex === window.currentMovies.length - 1;
            
            const genresList = movie.genres ? movie.genres.split(',').map(g => 
                `<span class="detail-genre-tag">${{g.trim()}}</span>`
            ).join('') : '<span class="detail-info-value">N/A</span>';
            
            const castList = movie.cast ? (Array.isArray(movie.cast) ? movie.cast : [movie.cast]).slice(0, 10).map(c => 
                `<span class="detail-cast-item">${{c}}</span>`
            ).join('') : '<span class="detail-info-value">N/A</span>';
            
            const html = `
                <div class="detail-nav">
                    <div class="detail-nav-left">
                        <button class="back-btn" onclick="closeDetail()">
                            ← Back to List
                        </button>
                    </div>
                    <div class="detail-nav-right">
                        <button class="nav-btn" onclick="showPrevMovie()" ${{isFirst ? 'disabled' : ''}}>
                            ← Previous
                        </button>
                        <button class="nav-btn" onclick="showNextMovie()" ${{isLast ? 'disabled' : ''}}>
                            Next →
                        </button>
                    </div>
                </div>
                
                <div class="detail-hero">
                    <img src="${{movie.poster || ''}}" alt="${{movie.title}}" class="detail-hero-bg" 
                         onerror="this.style.display='none'">
                    <div class="detail-hero-overlay">
                        <div class="detail-title">${{movie.title}}</div>
                        <div class="detail-meta">
                            <div class="detail-meta-item">
                                📅 ${{movie.year || 'N/A'}}
                            </div>
                            <div class="detail-meta-item">
                                🎬 ${{movie.type || 'Film'}}
                            </div>
                            ${{movie.languages ? `<div class="detail-meta-item">🌐 ${{movie.languages}}</div>` : ''}}
                        </div>
                        <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
                            ${{movie.rating ? `<div class="detail-rating">⭐ ${{movie.rating.toFixed(1)}}</div>` : ''}}
                            ${{movie.watched ? '<div class="detail-watched">✓ Watched</div>' : ''}}
                        </div>
                    </div>
                </div>
                
                <div class="detail-content">
                    <div class="detail-section">
                        <div class="detail-section-title">📖 Synopsis</div>
                        <div class="detail-description">${{movie.description || 'No description available.'}}</div>
                    </div>
                    
                    <div class="detail-section">
                        <div class="detail-section-title">🎭 Genres</div>
                        <div class="detail-genres">${{genresList}}</div>
                    </div>
                    
                    <div class="detail-section">
                        <div class="detail-section-title">ℹ️ Details</div>
                        <div class="detail-info-grid">
                            <div class="detail-info-card">
                                <div class="detail-info-label">Release Year</div>
                                <div class="detail-info-value">${{movie.year || 'N/A'}}</div>
                            </div>
                            <div class="detail-info-card">
                                <div class="detail-info-label">Type</div>
                                <div class="detail-info-value">${{movie.type || 'Film'}}</div>
                            </div>
                            <div class="detail-info-card">
                                <div class="detail-info-label">Language</div>
                                <div class="detail-info-value">${{movie.languages || 'N/A'}}</div>
                            </div>
                            <div class="detail-info-card">
                                <div class="detail-info-label">Rating</div>
                                <div class="detail-info-value">${{movie.rating ? `⭐ ${{movie.rating.toFixed(1)}} / 10` : 'N/A'}}</div>
                            </div>
                        </div>
                    </div>
                    
                    ${{movie.cast && castList !== '<span class="detail-info-value">N/A</span>' ? `
                        <div class="detail-section">
                            <div class="detail-section-title">🎬 Cast</div>
                            <div class="detail-cast">${{castList}}</div>
                        </div>
                    ` : ''}}
                </div>
            `;
            
            document.getElementById('detail-view').innerHTML = html;
        }}
        
        // Make openDetail available globally
        window.openModal = openDetail;
        
        // Initial render
        updateStats();
        renderMovies();
    </script>
</body>
</html>
    """

