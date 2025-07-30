// Intellivest Web Interface JavaScript

// Global variables
let sentimentChart;
let demoChart;
let mockData = {
    rankings: [
        { symbol: 'TSLA', score: 8.7, mentions: 1247, sentiment: 'bullish' },
        { symbol: 'AAPL', score: 8.2, mentions: 892, sentiment: 'bullish' },
        { symbol: 'NVDA', score: 7.9, mentions: 1034, sentiment: 'bullish' },
        { symbol: 'AMC', score: 7.5, mentions: 756, sentiment: 'bullish' },
        { symbol: 'GME', score: 7.1, mentions: 623, sentiment: 'bullish' },
        { symbol: 'PLTR', score: 6.8, mentions: 445, sentiment: 'neutral' },
        { symbol: 'HOOD', score: 6.4, mentions: 334, sentiment: 'neutral' },
        { symbol: 'BB', score: 6.1, mentions: 287, sentiment: 'neutral' }
    ],
    sentimentTrends: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
            {
                label: 'TSLA',
                data: [7.2, 7.8, 8.1, 8.5, 8.7, 8.3, 8.6],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                tension: 0.4
            },
            {
                label: 'AAPL',
                data: [7.8, 7.6, 8.0, 8.2, 8.1, 7.9, 8.2],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4
            },
            {
                label: 'NVDA',
                data: [7.1, 7.4, 7.8, 7.9, 7.7, 7.9, 7.9],
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                tension: 0.4
            }
        ]
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeCharts();
    initializeDemoData();
    initializeModal();
    initializeAnimations();
});

// Navigation functionality
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Toggle mobile menu
    hamburger?.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger?.classList.remove('active');
            navMenu?.classList.remove('active');
        });
    });

    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add scroll effect to navbar
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Initialize charts
function initializeCharts() {
    initializeSentimentChart();
    initializeDemoChart();
}

function initializeSentimentChart() {
    const ctx = document.getElementById('sentimentChart');
    if (!ctx) return;

    // Set fixed dimensions
    ctx.width = 400;
    ctx.height = 300;

    sentimentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Portfolio Performance',
                data: [100, 112, 108, 125, 142, 138, 155],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#2563eb',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#2563eb',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `Performance: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    border: {
                        display: false
                    },
                    ticks: {
                        color: '#64748b'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    border: {
                        display: false
                    },
                    ticks: {
                        color: '#64748b',
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

function initializeDemoChart() {
    const ctx = document.getElementById('demoChart');
    if (!ctx) return;

    // Set fixed dimensions
    ctx.width = 400;
    ctx.height = 300;

    demoChart = new Chart(ctx, {
        type: 'line',
        data: mockData.sentimentTrends,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        color: '#64748b'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#2563eb',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(1)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    border: {
                        display: false
                    },
                    ticks: {
                        color: '#64748b'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    border: {
                        display: false
                    },
                    ticks: {
                        color: '#64748b'
                    },
                    min: 0,
                    max: 10
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Initialize demo data
function initializeDemoData() {
    populateStockRankings();
    
    // Demo controls
    const refreshBtn = document.getElementById('refreshDemo');
    const timeframeSelect = document.getElementById('timeframe');

    refreshBtn?.addEventListener('click', () => {
        refreshBtn.innerHTML = '<div class="loading"></div> Refreshing...';
        setTimeout(() => {
            updateDemoData();
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Data';
        }, 1500);
    });

    timeframeSelect?.addEventListener('change', () => {
        updateDemoData();
    });
}

function populateStockRankings() {
    const rankingsContainer = document.getElementById('stockRankings');
    if (!rankingsContainer) return;

    rankingsContainer.innerHTML = '';
    
    // Limit to top 5 rankings for cleaner presentation
    mockData.rankings.slice(0, 5).forEach((stock, index) => {
        const rankingItem = document.createElement('div');
        rankingItem.className = 'ranking-item fade-in-up';
        rankingItem.style.animationDelay = `${index * 0.1}s`;
        
        rankingItem.innerHTML = `
            <div>
                <span class="ranking-symbol">#${index + 1} ${stock.symbol}</span>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">
                    ${stock.mentions} mentions
                </div>
            </div>
            <div class="ranking-score">${stock.score.toFixed(1)}</div>
        `;
        
        rankingsContainer.appendChild(rankingItem);
    });
}

function updateDemoData() {
    // Simulate new data
    mockData.rankings = mockData.rankings.map(stock => ({
        ...stock,
        score: Math.max(1, Math.min(10, stock.score + (Math.random() - 0.5) * 2)),
        mentions: Math.max(50, stock.mentions + Math.floor((Math.random() - 0.5) * 200))
    }));

    // Sort by score
    mockData.rankings.sort((a, b) => b.score - a.score);

    // Update rankings display
    populateStockRankings();

    // Update chart data
    if (demoChart) {
        demoChart.data.datasets.forEach(dataset => {
            dataset.data = dataset.data.map(value => 
                Math.max(1, Math.min(10, value + (Math.random() - 0.5) * 1))
            );
        });
        demoChart.update('active');
    }
}

// Modal functionality
function initializeModal() {
    const modal = document.getElementById('disclaimer');
    const closeBtn = document.querySelector('.close');
    const disclaimerLinks = document.querySelectorAll('a[href="#disclaimer"]');

    disclaimerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });

    closeBtn?.addEventListener('click', () => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

// Animation and scroll effects
function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });

    // Observe performance cards
    document.querySelectorAll('.performance-card').forEach(card => {
        observer.observe(card);
    });

    // Observe doc cards
    document.querySelectorAll('.doc-card').forEach(card => {
        observer.observe(card);
    });

    // Animate accuracy bar when in view
    const accuracyBar = document.querySelector('.accuracy-fill');
    if (accuracyBar) {
        const barObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    accuracyBar.style.width = '43.8%';
                }
            });
        }, { threshold: 0.5 });

        barObserver.observe(accuracyBar.parentElement);
    }
}

// Utility functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function generateRandomData(count, min = 0, max = 10) {
    return Array.from({ length: count }, () => 
        Math.random() * (max - min) + min
    );
}

// Add some interactivity to buttons
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn')) {
        e.target.style.transform = 'translateY(-1px) scale(0.98)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 150);
    }
});

// Add typing effect to hero title (optional enhancement)
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Performance monitoring
function trackPagePerformance() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        });
    }
}

// Initialize performance tracking
trackPagePerformance();

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatNumber,
        generateRandomData,
        updateDemoData
    };
}
