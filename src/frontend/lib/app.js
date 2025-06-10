/**
 * Main Application Orchestrator
 * Coordinates all modules and handles application lifecycle
 */

import { AutomataAPI } from './api.js';
import { state, setState } from './state.js';
import { router, registerRoute } from './router.js';
import { APP_CONFIG } from '../config/app.js';

// Import page modules
import { dashboardPage } from '../pages/dashboard.js';
import { systemPage } from '../pages/system.js';
import { settingsPage } from '../pages/settings.js';

export class AutomataApp {
    constructor() {
        this.isInitialized = false;
        this.pages = new Map();
    }
    
    /**
     * Initialize the application
     */
    async init() {
        if (this.isInitialized) {
            return;
        }
        
        console.log('🚀 Initializing Automata Application...');
        
        try {
            // Initialize core systems
            await this.initCore();
            
            // Initialize pages
            await this.initPages();
            
            // Setup routes
            this.setupRoutes();
            
            // Initialize router
            router.init();
            
            // Load initial data
            await this.loadInitialData();
            
            // Navigate to default route
            await router.navigate(APP_CONFIG.routes.default);
            
            this.isInitialized = true;
            console.log('✅ Application initialized successfully');
            
        } catch (error) {
            console.error('❌ Failed to initialize application:', error);
            this.handleInitializationError(error);
        }
    }
    
    /**
     * Initialize core systems
     */
    async initCore() {
        console.log('🔧 Initializing core systems...');
        
        // Initialize API
        await AutomataAPI.init();
        
        // Initialize theme
        this.initTheme();
        
        // Set initialization flag in state
        setState('isInitialized', true);
        
        console.log('✅ Core systems initialized');
    }
    
    /**
     * Initialize theme system
     */
    initTheme() {
        const savedTheme = localStorage.getItem(APP_CONFIG.storage.theme) || APP_CONFIG.ui.defaultTheme;
        setState('theme', savedTheme);
        document.body.className = `theme-${savedTheme}`;
    }
    
    /**
     * Initialize page modules
     */
    async initPages() {
        console.log('📄 Initializing page modules...');
        
        // Register pages
        this.pages.set('dashboard', dashboardPage);
        this.pages.set('system', systemPage);
        this.pages.set('settings', settingsPage);
        
        // Initialize each page
        for (const [name, page] of this.pages) {
            try {
                await page.init();
                console.log(`✅ ${name} page initialized`);
            } catch (error) {
                console.error(`❌ Failed to initialize ${name} page:`, error);
            }
        }
        
        console.log('✅ Page modules initialized');
    }
    
    /**
     * Setup application routes
     */
    setupRoutes() {
        console.log('🛣️ Setting up routes...');
        
        // Dashboard route
        registerRoute('dashboard', {
            title: 'Dashboard',
            onEnter: () => dashboardPage.onEnter(),
            onLeave: () => dashboardPage.onLeave()
        });
        
        // System route
        registerRoute('system', {
            title: 'System Information',
            onEnter: () => systemPage.onEnter(),
            onLeave: () => systemPage.onLeave()
        });
        
        // Settings route
        registerRoute('settings', {
            title: 'Settings',
            onEnter: () => settingsPage.onEnter(),
            onLeave: () => settingsPage.onLeave()
        });
        
        console.log('✅ Routes configured');
    }
    
    /**
     * Load initial application data
     */
    async loadInitialData() {
        console.log('📊 Loading initial data...');
        
        try {
            // Test API connectivity
            const ping = await AutomataAPI.ping();
            console.log('📡 Backend connectivity verified:', ping);
            
        } catch (error) {
            console.warn('⚠️ Backend connectivity test failed:', error);
            window.showToast?.('Backend connection failed - some features may not work', 'warning');
        }
        
        console.log('✅ Initial data loading completed');
    }
    
    /**
     * Handle initialization errors
     * @param {Error} error - The initialization error
     */
    handleInitializationError(error) {
        console.error('💥 Application initialization failed:', error);
        
        // Show error to user
        document.body.innerHTML = `
            <div class="init-error">
                <div class="error-container">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h2>Application Failed to Initialize</h2>
                    <p class="error-message">${error.message}</p>
                    <div class="error-actions">
                        <button class="btn btn-primary" onclick="location.reload()">
                            <i class="fas fa-sync"></i>
                            Reload Application
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add error styles
        const style = document.createElement('style');
        style.textContent = `
            .init-error {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 2rem;
                background: #f8fafc;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            }
            .error-container {
                text-align: center;
                max-width: 500px;
                padding: 3rem;
                background: white;
                border-radius: 0.75rem;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }
            .init-error i {
                font-size: 3rem;
                color: #ef4444;
                margin-bottom: 1rem;
            }
            .init-error h2 {
                font-size: 1.5rem;
                color: #1e293b;
                margin-bottom: 1rem;
            }
            .error-message {
                color: #64748b;
                margin-bottom: 2rem;
                line-height: 1.6;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.75rem 1.5rem;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 0.5rem;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s;
            }
            .btn:hover {
                background: #2563eb;
            }
        `;
        document.head.appendChild(style);
    }
    
    /**
     * Get application information
     * @returns {Object} Application info
     */
    getAppInfo() {
        return {
            name: APP_CONFIG.name,
            version: APP_CONFIG.version,
            description: APP_CONFIG.description,
            isInitialized: this.isInitialized,
            currentRoute: router.getCurrentRoute()?.path,
            availablePages: Array.from(this.pages.keys()),
            features: APP_CONFIG.features
        };
    }
    
    /**
     * Cleanup application
     */
    destroy() {
        console.log('🗑️ Cleaning up application...');
        
        // Cleanup pages
        this.pages.forEach((page, name) => {
            try {
                if (page.destroy) {
                    page.destroy();
                }
                console.log(`✅ ${name} page cleaned up`);
            } catch (error) {
                console.error(`❌ Error cleaning up ${name} page:`, error);
            }
        });
        
        this.isInitialized = false;
        console.log('✅ Application cleanup completed');
    }
}

// Create and export singleton instance
export const app = new AutomataApp();

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});

// Export for global access
window.AutomataApp = app; 