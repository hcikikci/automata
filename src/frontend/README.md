# Automata Frontend - Modular Architecture

## 📁 Project Structure

```
frontend/
├── lib/                    # Core libraries
│   ├── api.js             # API service for backend communication
│   ├── state.js           # State management system
│   ├── router.js          # Client-side routing
│   └── app.js             # Main application orchestrator
├── pages/                  # Page modules
│   ├── dashboard.js       # Dashboard page logic
│   ├── system.js          # System information page
│   ├── settings.js        # Settings page
│   └── index.html         # Main HTML file
├── utils/                  # Utility functions
│   └── helpers.js         # General helper functions
├── config/                 # Configuration files
│   └── app.js             # Application configuration
├── assets/                 # Static assets
│   └── js/                # Component scripts
│       └── components.js  # UI components
└── styles/                 # CSS modules
    ├── styles.css         # Base styles
    ├── themes.css         # Theme definitions
    └── components.css     # Component styles
```

## 🧩 Architecture Overview

### Core Systems

#### 1. **API Service (`lib/api.js`)**
- Handles all backend communication via Eel
- Automatic initialization and error handling
- Centralized API calls with consistent error handling

```javascript
import { AutomataAPI } from '../lib/api.js';

// Usage
const healthStatus = await AutomataAPI.getHealthStatus();
const systemInfo = await AutomataAPI.getSystemInfo();
```

#### 2. **State Management (`lib/state.js`)**
- Centralized application state with reactive updates
- Subscribe to state changes for automatic UI updates
- Local storage integration for persistence

```javascript
import { setState, getState, subscribeToState } from '../lib/state.js';

// Set state
setState('theme', 'dark');

// Get state
const currentTheme = getState('theme');

// Subscribe to changes
const unsubscribe = subscribeToState('theme', (newTheme) => {
    console.log('Theme changed to:', newTheme);
});
```

#### 3. **Router (`lib/router.js`)**
- Simple client-side routing for single-page application
- Navigation hooks for page lifecycle management
- History API integration

```javascript
import { router, navigate, registerRoute } from '../lib/router.js';

// Register a route
registerRoute('dashboard', {
    title: 'Dashboard',
    onEnter: () => dashboardPage.onEnter(),
    onLeave: () => dashboardPage.onLeave()
});

// Navigate programmatically
navigate('dashboard');
```

### Page Modules

Each page is a self-contained module with:
- **Initialization**: Setup page-specific functionality
- **Lifecycle hooks**: `onEnter()` and `onLeave()` methods
- **State management**: Subscribe to relevant state changes
- **Data loading**: Handle page-specific API calls
- **UI updates**: Manage page-specific UI elements

#### Dashboard Page (`pages/dashboard.js`)
- Application overview and health monitoring
- Backend connectivity testing
- Data export functionality
- Real-time uptime counter

#### System Page (`pages/system.js`)
- System information display with real-time updates
- Progress bars for resource usage
- Auto-refresh functionality
- Detailed health metrics

#### Settings Page (`pages/settings.js`)
- Theme management
- Application preferences
- Configuration import/export
- Settings persistence

### Utility Functions (`utils/helpers.js`)

Common utilities used across the application:
- `formatUptime()` - Format time durations
- `debounce()` / `throttle()` - Function rate limiting
- `deepClone()` - Object cloning
- `downloadData()` - File download helper
- `getErrorMessage()` - Error message extraction

### Configuration (`config/app.js`)

Centralized configuration including:
- Application metadata
- API settings
- UI preferences
- Feature flags
- Error messages

## 🚀 Getting Started

### 1. Understanding the Module System

The frontend uses ES6 modules for better organization:

```javascript
// Import specific functions
import { AutomataAPI } from '../lib/api.js';
import { setState, getState } from '../lib/state.js';

// Import entire module
import * as helpers from '../utils/helpers.js';
```

### 2. Adding a New Page

1. **Create the page module**:
```javascript
// pages/new-page.js
export class NewPage {
    constructor() {
        this.isActive = false;
    }
    
    async init() {
        console.log('Initializing new page...');
    }
    
    async onEnter() {
        this.isActive = true;
        // Load page data
    }
    
    async onLeave() {
        this.isActive = false;
        // Cleanup
    }
}

export const newPage = new NewPage();
```

2. **Register the route**:
```javascript
// In lib/app.js
registerRoute('new-page', {
    title: 'New Page',
    onEnter: () => newPage.onEnter(),
    onLeave: () => newPage.onLeave()
});
```

3. **Add navigation**:
```html
<!-- In index.html -->
<a href="#new-page" class="menu-item" data-section="new-page">
    <i class="fas fa-star"></i>
    <span>New Page</span>
</a>
```

### 3. State Management Best Practices

```javascript
// Subscribe to specific state changes
const unsubscribe = subscribeToState('systemInfo', (systemInfo) => {
    if (systemInfo && this.isActive) {
        this.updateSystemDisplay(systemInfo);
    }
});

// Remember to unsubscribe when component is destroyed
this.stateUnsubscribers.push(unsubscribe);
```

### 4. Error Handling

```javascript
try {
    const data = await AutomataAPI.getSystemInfo();
    setState('systemInfo', data);
} catch (error) {
    console.error('Failed to load system info:', error);
    window.showToast?.(getErrorMessage(error), 'error');
    setState('lastError', error);
}
```

## 🎨 Styling and Themes

### Theme System
- CSS custom properties for theming
- Light and dark theme support
- Automatic theme persistence
- Smooth transitions between themes

### Adding Custom Styles
1. Use existing CSS custom properties when possible
2. Add new styles to appropriate CSS file:
   - `styles.css` - Base styles
   - `themes.css` - Theme-specific styles
   - `components.css` - Component styles

## 🔧 Development Tips

### 1. Console Logging
The application uses emoji prefixes for easy log filtering:
- 🚀 Application lifecycle
- 📊 Data loading
- 🖥️ System page
- ⚙️ Settings
- 📡 API calls
- 🎨 Theme changes

### 2. Feature Flags
Use configuration feature flags to enable/disable functionality:

```javascript
if (APP_CONFIG.features.healthMonitoring) {
    // Health monitoring code
}
```

### 3. Adding New API Endpoints
1. Add method to `AutomataAPI` class
2. Export from page modules for global access
3. Handle errors appropriately

## 📱 Browser Compatibility

The application uses modern JavaScript features:
- ES6 Modules
- Async/Await
- Template literals
- Destructuring
- Maps and Sets

Ensure your browser supports ES6 modules or use a bundler for production.

## 🐛 Debugging

### Common Issues

1. **Module loading errors**: Check file paths and ensure proper import/export
2. **State not updating**: Verify state subscriptions and unsubscription cleanup
3. **API calls failing**: Check backend connectivity and Eel initialization

### Debug Tools
- Browser DevTools console for logging
- Network tab for API call monitoring
- Application tab for localStorage inspection

## 🔄 Migration from Legacy Code

The old monolithic `app.js` has been refactored into:
- `lib/api.js` - API communication
- `lib/state.js` - State management
- `lib/router.js` - Navigation
- `pages/*.js` - Page-specific logic
- `lib/app.js` - Application orchestration

All functionality has been preserved while improving maintainability and modularity. 