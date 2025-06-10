/**
 * Application State Management
 * Centralized state management with event system
 */

export class AppState {
    static instance = null;
    
    constructor() {
        if (AppState.instance) {
            return AppState.instance;
        }
        
        this.state = {
            // App metadata
            currentSection: 'dashboard',
            startTime: Date.now(),
            theme: localStorage.getItem('theme') || 'light',
            isInitialized: false,
            
            // Data
            systemInfo: null,
            healthStatus: null,
            featuresStatus: null,
            
            // UI state
            isLoading: false,
            lastError: null,
            lastUpdate: null
        };
        
        this.listeners = new Map();
        AppState.instance = this;
    }
    
    /**
     * Get current state value
     * @param {string} key - State key
     * @returns {any} State value
     */
    get(key) {
        return this.state[key];
    }
    
    /**
     * Set state value and notify listeners
     * @param {string|Object} key - State key or object of key-value pairs
     * @param {any} value - State value (if key is string)
     */
    set(key, value) {
        if (typeof key === 'object') {
            // Bulk update
            const oldState = { ...this.state };
            Object.assign(this.state, key);
            
            // Notify listeners for each changed key
            Object.keys(key).forEach(k => {
                if (oldState[k] !== this.state[k]) {
                    this.notify(k, this.state[k], oldState[k]);
                }
            });
        } else {
            // Single update
            const oldValue = this.state[key];
            this.state[key] = value;
            
            if (oldValue !== value) {
                this.notify(key, value, oldValue);
            }
        }
    }
    
    /**
     * Subscribe to state changes
     * @param {string} key - State key to watch
     * @param {Function} callback - Callback function
     * @returns {Function} Unsubscribe function
     */
    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, new Set());
        }
        
        this.listeners.get(key).add(callback);
        
        // Return unsubscribe function
        return () => {
            const listeners = this.listeners.get(key);
            if (listeners) {
                listeners.delete(callback);
                if (listeners.size === 0) {
                    this.listeners.delete(key);
                }
            }
        };
    }
    
    /**
     * Notify listeners of state change
     * @param {string} key - State key
     * @param {any} newValue - New value
     * @param {any} oldValue - Old value
     */
    notify(key, newValue, oldValue) {
        const listeners = this.listeners.get(key);
        if (listeners) {
            listeners.forEach(callback => {
                try {
                    callback(newValue, oldValue);
                } catch (error) {
                    console.error(`Error in state listener for ${key}:`, error);
                }
            });
        }
    }
    
    /**
     * Get all state
     * @returns {Object} Complete state object
     */
    getAll() {
        return { ...this.state };
    }
    
    /**
     * Reset state to initial values
     */
    reset() {
        const oldState = { ...this.state };
        
        this.state = {
            currentSection: 'dashboard',
            startTime: Date.now(),
            theme: localStorage.getItem('theme') || 'light',
            isInitialized: false,
            systemInfo: null,
            healthStatus: null,
            featuresStatus: null,
            isLoading: false,
            lastError: null,
            lastUpdate: null
        };
        
        // Notify all listeners
        Object.keys(oldState).forEach(key => {
            if (oldState[key] !== this.state[key]) {
                this.notify(key, this.state[key], oldState[key]);
            }
        });
    }
    
    /**
     * Update system data
     * @param {Object} data - System data object
     */
    updateSystemData(data) {
        this.set({
            systemInfo: data.systemInfo || this.state.systemInfo,
            healthStatus: data.healthStatus || this.state.healthStatus,
            featuresStatus: data.featuresStatus || this.state.featuresStatus,
            lastUpdate: Date.now()
        });
    }
    
    /**
     * Set loading state
     * @param {boolean} isLoading - Loading state
     */
    setLoading(isLoading) {
        this.set('isLoading', isLoading);
    }
    
    /**
     * Set error state
     * @param {Error|string|null} error - Error object or message
     */
    setError(error) {
        this.set('lastError', error);
    }
    
    /**
     * Clear error state
     */
    clearError() {
        this.set('lastError', null);
    }
}

// Export singleton instance
export const state = new AppState();

// Helper functions
export function getState(key) {
    return state.get(key);
}

export function setState(key, value) {
    return state.set(key, value);
}

export function subscribeToState(key, callback) {
    return state.subscribe(key, callback);
} 