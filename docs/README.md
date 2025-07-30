# Intellivest Web Interface

This directory contains the modern web interface for Intellivest, designed to be hosted on GitHub Pages at `cmorgenfeld.github.io/Intellivest`.

## Features

- **Modern, Responsive Design**: Built with vanilla HTML, CSS, and JavaScript
- **Interactive Charts**: Real-time sentiment analysis visualization using Chart.js
- **Live Demo Section**: Interactive stock rankings and sentiment trends
- **Comprehensive Documentation**: Links to all project resources
- **Mobile-First Design**: Fully responsive across all devices
- **Performance Optimized**: Fast loading with minimal dependencies

## Files

- `index.html` - Main HTML file with complete structure
- `styles.css` - Modern CSS with CSS variables and responsive design
- `script.js` - JavaScript for interactivity and chart functionality

## Setup for GitHub Pages

1. Ensure these files are in a `docs/` folder in your repository
2. Go to your GitHub repository settings
3. Navigate to "Pages" section
4. Set source to "Deploy from a branch"
5. Select branch: `master` or `main`
6. Select folder: `/docs`
7. Save settings

Your site will be available at: `https://cmorgenfeld.github.io/Intellivest`

## Customization

### Colors and Theming
The CSS uses CSS variables for easy theming. Modify the `:root` section in `styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --accent-color: #10b981;
    /* ... other variables */
}
```

### Mock Data
The JavaScript includes mock data for demonstration. Replace with real API calls:

```javascript
// In script.js, replace mockData with actual API calls
async function fetchRealData() {
    const response = await fetch('/api/rankings');
    return response.json();
}
```

### Chart Configuration
Charts are built with Chart.js. Customize in the `initializeCharts()` functions.

## Dependencies

- **Chart.js**: For interactive charts
- **Font Awesome**: For icons
- **Google Fonts (Inter)**: For typography

All dependencies are loaded via CDN for simplicity.

## Performance

- Optimized images and assets
- Minimal JavaScript bundle
- CSS Grid and Flexbox for layout
- Lazy loading for animations
- Efficient chart rendering

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Mobile Optimization

- Responsive grid layouts
- Touch-friendly navigation
- Optimized chart interactions
- Fast mobile loading

The interface is designed to showcase Intellivest's capabilities while providing an excellent user experience across all devices.
