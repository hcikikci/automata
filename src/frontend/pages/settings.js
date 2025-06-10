/**
 * Settings Page Module
 * Handles application settings and preferences
 */

import { setState, getState, subscribeToState } from '../lib/state.js';
import { APP_CONFIG, THEMES } from '../config/app.js';

export class SettingsPage {
    constructor() {
        this.isActive = false;
        this.stateUnsubscribers = [];
    }
    
    /**
     * Initialize settings page
     */
    async init() {
        console.log('⚙️ Initializing Settings page...');
        
        // Setup state subscriptions
        this.setupStateSubscriptions();
        
        // Setup event listeners
        this.setupEventListeners();
        
        console.log('✅ Settings page initialized');
    }
    
    /**
     * Called when entering the settings page
     */
    async onEnter() {
        this.isActive = true;
        console.log('⚙️ Entering Settings page');
        
        // Load current settings
        this.loadCurrentSettings();
    }
    
    /**
     * Called when leaving the settings page
     */
    async onLeave() {
        this.isActive = false;
        console.log('⚙️ Leaving Settings page');
    }
    
    /**
     * Setup state subscriptions
     */
    setupStateSubscriptions() {
        // Subscribe to theme changes
        const unsubscribeTheme = subscribeToState('theme', (theme) => {
            if (this.isActive) {
                this.updateThemeUI(theme);
            }
        });
        
        this.stateUnsubscribers.push(unsubscribeTheme);
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Theme select change
        document.addEventListener('change', (e) => {
            if (e.target.id === 'theme-select') {
                this.changeTheme(e.target.value);
            }
        });
        
        // Theme toggle button
        document.addEventListener('click', (e) => {
            if (e.target.closest('#theme-toggle')) {
                this.toggleTheme();
            }
        });
    }
    
    /**
     * Load current settings into UI
     */
    loadCurrentSettings() {
        const currentTheme = getState('theme');
        this.updateThemeUI(currentTheme);
        
        // Update theme select dropdown
        const themeSelect = document.getElementById('theme-select');
        if (themeSelect) {
            themeSelect.value = currentTheme;
        }
    }
    
    /**
     * Update theme UI elements
     * @param {string} theme - Theme name
     */
    updateThemeUI(theme) {
        // Update theme toggle icon
        const themeIcon = document.querySelector('#theme-toggle i');
        if (themeIcon) {
            const iconClass = THEMES[theme]?.icon || 'fas fa-sun';
            themeIcon.className = iconClass;
        }
        
        // Update theme select
        const themeSelect = document.getElementById('theme-select');
        if (themeSelect && themeSelect.value !== theme) {
            themeSelect.value = theme;
        }
        
        // Apply theme to body
        document.body.className = `theme-${theme}`;
    }
    
    /**
     * Change theme
     * @param {string} theme - New theme name
     */
    changeTheme(theme) {
        if (!THEMES[theme]) {
            console.error(`Unknown theme: ${theme}`);
            return;
        }
        
        // Update state
        setState('theme', theme);
        
        // Save to localStorage
        localStorage.setItem(APP_CONFIG.storage.theme, theme);
        
        // Show feedback
        window.showToast?.(`Theme changed to ${THEMES[theme].name} mode`, 'info');
        
        console.log(`🎨 Theme changed to: ${theme}`);
    }
    
    /**
     * Toggle between light and dark theme
     */
    toggleTheme() {
        const currentTheme = getState('theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.changeTheme(newTheme);
    }
}

// Export settings page instance
export const settingsPage = new SettingsPage();

// Export utility functions for global access
export function changeTheme(theme) {
    return settingsPage.changeTheme(theme);
}

export function toggleTheme() {
    return settingsPage.toggleTheme();
} 