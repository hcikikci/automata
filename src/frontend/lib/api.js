/**
 * API Service Module
 * Handles all communication with the Eel backend
 */

export class AutomataAPI {
    static isInitialized = false;
    static initPromise = null;

    /**
     * Initialize the API service
     * @returns {Promise<boolean>} 
     */
    static async init() {
        if (this.initPromise) {
            return this.initPromise;
        }

        this.initPromise = this.waitForReady();
        const result = await this.initPromise;
        this.isInitialized = result;
        return result;
    }

    /**
     * Base method for calling Eel functions
     * @param {string} functionName - Name of the Eel function
     * @param {...any} args - Arguments to pass to the function
     * @returns {Promise<any>} - Promise resolving to the response data
     */
    static async call(functionName, ...args) {
        if (!this.isInitialized) {
            await this.init();
        }

        try {
            console.log(`🔄 API Call: ${functionName}`);
            
            if (!window.eel || !window.eel[functionName]) {
                throw new Error(`Function '${functionName}' not available`);
            }
            
            const response = await window.eel[functionName](...args)();
            
            if (response && response.success) {
                console.log(`✅ API Success: ${functionName}`);
                return response.data;
            } else if (response && response.error) {
                console.error(`❌ API Error: ${functionName} - ${response.error}`);
                throw new Error(response.error);
            } else {
                throw new Error('Invalid response format');
            }
            
        } catch (error) {
            console.error(`💥 Error in ${functionName}:`, error);
            throw error;
        }
    }
    
    /**
     * Get comprehensive health status
     * @returns {Promise<Object>} Health status data
     */
    static async getHealthStatus() {
        return await this.call('get_health_status');
    }
    
    /**
     * Get quick health status
     * @returns {Promise<Object>} Quick health data
     */
    static async getQuickHealth() {
        return await this.call('get_quick_health');
    }
    
    /**
     * Get system information
     * @returns {Promise<Object>} System information
     */
    static async getSystemInfo() {
        return await this.call('get_system_info');
    }
    
    /**
     * Ping the backend
     * @returns {Promise<Object>} Ping response
     */
    static async ping() {
        return await this.call('ping');
    }
    
    /**
     * Get features status
     * @returns {Promise<Object>} Features status
     */
    static async getFeaturesStatus() {
        return await this.call('get_features_status');
    }
    
    /**
     * Check if the API is ready
     * @returns {boolean} API readiness status
     */
    static isReady() {
        return !!(window.eel && typeof window.eel === 'object');
    }
    
    /**
     * Wait for the API to become ready
     * @param {number} timeout - Timeout in milliseconds
     * @returns {Promise<boolean>} Promise resolving when ready
     */
    static async waitForReady(timeout = 5000) {
        return new Promise((resolve, reject) => {
            if (this.isReady()) {
                resolve(true);
                return;
            }
            
            const startTime = Date.now();
            const checkInterval = setInterval(() => {
                if (this.isReady()) {
                    clearInterval(checkInterval);
                    console.log('✅ Automata API is ready');
                    resolve(true);
                } else if (Date.now() - startTime > timeout) {
                    clearInterval(checkInterval);
                    reject(new Error(`API not ready after ${timeout}ms`));
                }
            }, 100);
        });
    }
} 