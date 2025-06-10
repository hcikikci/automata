/**
 * Application Configuration
 */

export const APP_CONFIG = {
    // Application metadata
    name: 'Automata',
    version: '1.0.0',
    description: 'Modern Python Eel Application with Health Monitoring',
    
    // API settings
    api: {
        timeout: 10000, // 10 seconds
        retryAttempts: 3,
        retryDelay: 1000, // 1 second
    },
    
    // UI settings
    ui: {
        defaultTheme: 'light',
        animationDuration: 250,
        toastDuration: 5000,
        updateInterval: 1000, // For uptime counter
    },
    
    // Routes configuration
    routes: {
        default: 'dashboard',
        available: ['dashboard', 'system', 'settings']
    },
    
    // Feature flags
    features: {
        darkMode: true,
        notifications: true,
        dataExport: true,
        healthMonitoring: true,
        systemInfo: true,
    },
    
    // Data refresh intervals (in milliseconds)
    refresh: {
        systemInfo: 30000, // 30 seconds
        healthStatus: 10000, // 10 seconds
        uptime: 1000, // 1 second
    },
    
    // Storage keys
    storage: {
        theme: 'automata_theme',
        settings: 'automata_settings',
        lastVisited: 'automata_last_visited',
    },
    
    // Error messages
    messages: {
        api: {
            connectionFailed: 'Failed to connect to backend',
            timeout: 'Request timed out',
            invalidResponse: 'Invalid response from server',
            notReady: 'Backend is not ready'
        },
        ui: {
            loadingFailed: 'Failed to load data',
            navigationFailed: 'Navigation failed',
            exportFailed: 'Failed to export data'
        }
    },
    
    // Development settings
    development: {
        enableDebugLogs: true,
        mockData: false,
        showPerformanceMetrics: true,
    }
};

// Theme configuration
export const THEMES = {
    light: {
        name: 'Light',
        icon: 'fas fa-sun',
        primary: '#3b82f6',
        background: '#ffffff',
        text: '#1e293b'
    },
    dark: {
        name: 'Dark', 
        icon: 'fas fa-moon',
        primary: '#60a5fa',
        background: '#0f172a',
        text: '#f1f5f9'
    }
};

// Export helper function to get config values
export function getConfig(path) {
    return path.split('.').reduce((obj, key) => obj?.[key], APP_CONFIG);
}

// Export helper function to check if feature is enabled
export function isFeatureEnabled(feature) {
    return APP_CONFIG.features[feature] === true;
} 