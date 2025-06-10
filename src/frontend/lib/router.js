/**
 * Simple Router for Single Page Application
 * Handles navigation between different sections/pages
 */

import { setState, subscribeToState } from './state.js';

export class Router {
    static instance = null;
    
    constructor() {
        if (Router.instance) {
            return Router.instance;
        }
        
        this.routes = new Map();
        this.currentRoute = null;
        this.beforeNavigateHooks = [];
        this.afterNavigateHooks = [];
        
        Router.instance = this;
    }
    
    /**
     * Register a route
     * @param {string} path - Route path
     * @param {Object} config - Route configuration
     */
    register(path, config) {
        this.routes.set(path, {
            path,
            title: config.title || path,
            component: config.component,
            onEnter: config.onEnter || null,
            onLeave: config.onLeave || null,
            data: config.data || {}
        });
    }
    
    /**
     * Navigate to a route
     * @param {string} path - Route path
     * @param {Object} options - Navigation options
     */
    async navigate(path, options = {}) {
        const route = this.routes.get(path);
        
        if (!route) {
            console.error(`Route not found: ${path}`);
            return false;
        }
        
        try {
            // Run before navigate hooks
            for (const hook of this.beforeNavigateHooks) {
                const result = await hook(path, route, this.currentRoute);
                if (result === false) {
                    return false; // Navigation cancelled
                }
            }
            
            // Leave current route
            if (this.currentRoute && this.currentRoute.onLeave) {
                await this.currentRoute.onLeave();
            }
            
            // Hide all sections
            this.hideAllSections();
            
            // Update current route
            const oldRoute = this.currentRoute;
            this.currentRoute = route;
            
            // Update state
            setState('currentSection', path);
            
            // Update navigation UI
            this.updateNavigationUI(path);
            
            // Show new section
            this.showSection(path);
            
            // Enter new route
            if (route.onEnter) {
                await route.onEnter();
            }
            
            // Update page title
            if (route.title) {
                document.title = `Automata - ${route.title}`;
            }
            
            // Run after navigate hooks
            for (const hook of this.afterNavigateHooks) {
                await hook(path, route, oldRoute);
            }
            
            console.log(`✅ Navigated to: ${path}`);
            return true;
            
        } catch (error) {
            console.error(`Error navigating to ${path}:`, error);
            return false;
        }
    }
    
    /**
     * Get current route
     * @returns {Object|null} Current route
     */
    getCurrentRoute() {
        return this.currentRoute;
    }
    
    /**
     * Add before navigate hook
     * @param {Function} hook - Hook function
     */
    beforeNavigate(hook) {
        this.beforeNavigateHooks.push(hook);
    }
    
    /**
     * Add after navigate hook
     * @param {Function} hook - Hook function
     */
    afterNavigate(hook) {
        this.afterNavigateHooks.push(hook);
    }
    
    /**
     * Hide all sections
     */
    hideAllSections() {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
    }
    
    /**
     * Show specific section
     * @param {string} sectionName - Section name
     */
    showSection(sectionName) {
        const section = document.getElementById(`${sectionName}-section`);
        if (section) {
            section.classList.add('active');
        }
    }
    
    /**
     * Update navigation UI
     * @param {string} activePath - Active route path
     */
    updateNavigationUI(activePath) {
        // Update menu items
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const activeItem = document.querySelector(`[data-section="${activePath}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }
    
    /**
     * Initialize router
     */
    init() {
        // Subscribe to navigation clicks
        document.addEventListener('click', (e) => {
            const menuItem = e.target.closest('.menu-item');
            if (menuItem) {
                e.preventDefault();
                const section = menuItem.dataset.section;
                if (section) {
                    this.navigate(section);
                }
            }
        });
        
        // Handle browser back/forward
        window.addEventListener('popstate', (e) => {
            const path = e.state?.path || 'dashboard';
            this.navigate(path, { replace: true });
        });
        
        console.log('✅ Router initialized');
    }
    
    /**
     * Get all registered routes
     * @returns {Array} Array of routes
     */
    getRoutes() {
        return Array.from(this.routes.values());
    }
}

// Export singleton instance
export const router = new Router();

// Helper functions
export function navigate(path, options) {
    return router.navigate(path, options);
}

export function registerRoute(path, config) {
    return router.register(path, config);
}

export function getCurrentRoute() {
    return router.getCurrentRoute();
} 