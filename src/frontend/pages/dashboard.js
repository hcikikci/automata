/**
 * Dashboard Page Module
 * Handles dashboard-specific functionality and UI interactions
 */

import { AutomataAPI } from '../lib/api.js';
import { state, setState, getState } from '../lib/state.js';
import { formatUptime, getErrorMessage } from '../utils/helpers.js';
import { APP_CONFIG } from '../config/app.js';

export class DashboardPage {
    constructor() {
        this.uptimeInterval = null;
        this.isActive = false;
    }
    
    /**
     * Initialize dashboard page
     */
    async init() {
        console.log('📊 Initializing Dashboard page...');
        
        // Set up uptime counter
        this.startUptimeCounter();
        
        // Set up periodic data refresh
        this.startDataRefresh();
        
        console.log('✅ Dashboard page initialized');
    }
    
    /**
     * Called when entering the dashboard page
     */
    async onEnter() {
        this.isActive = true;
        console.log('📊 Entering Dashboard page');
        
        try {
            // Load initial data
            await this.loadDashboardData();
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            window.showToast?.(`Failed to load dashboard: ${getErrorMessage(error)}`, 'error');
        }
    }
    
    /**
     * Called when leaving the dashboard page
     */
    async onLeave() {
        this.isActive = false;
        console.log('📊 Leaving Dashboard page');
    }
    
    /**
     * Load dashboard-specific data
     */
    async loadDashboardData() {
        if (!this.isActive) return;
        
        setState('isLoading', true);
        
        try {
            // Test backend connectivity
            const ping = await AutomataAPI.ping();
            console.log('📡 Backend connection verified:', ping);
            
            // Load features status for app info
            if (APP_CONFIG.features.healthMonitoring) {
                const featuresStatus = await AutomataAPI.getFeaturesStatus();
                setState('featuresStatus', featuresStatus);
                console.log('📊 Features status loaded:', featuresStatus);
            }
            
            // Update version info
            this.updateVersionInfo();
            
        } catch (error) {
            console.warn('Could not load dashboard data:', error);
            setState('lastError', error);
        } finally {
            setState('isLoading', false);
        }
    }
    
    /**
     * Start uptime counter
     */
    startUptimeCounter() {
        if (this.uptimeInterval) {
            clearInterval(this.uptimeInterval);
        }
        
        const updateUptime = () => {
            const uptimeElement = document.getElementById('uptime');
            if (uptimeElement) {
                const startTime = getState('startTime');
                const formattedUptime = formatUptime(startTime);
                uptimeElement.textContent = formattedUptime;
            }
        };
        
        // Update immediately
        updateUptime();
        
        // Update every second
        this.uptimeInterval = setInterval(updateUptime, APP_CONFIG.ui.updateInterval);
    }
    
    /**
     * Start periodic data refresh
     */
    startDataRefresh() {
        // Refresh health status periodically
        if (APP_CONFIG.features.healthMonitoring) {
            setInterval(async () => {
                if (this.isActive) {
                    try {
                        const quickHealth = await AutomataAPI.getQuickHealth();
                        setState('healthStatus', quickHealth);
                    } catch (error) {
                        console.warn('Failed to refresh health status:', error);
                    }
                }
            }, APP_CONFIG.refresh.healthStatus);
        }
    }
    
    /**
     * Update version information in UI
     */
    updateVersionInfo() {
        const versionElement = document.getElementById('app-version');
        if (versionElement) {
            versionElement.textContent = APP_CONFIG.version;
        }
    }
    
    /**
     * Test backend connection
     */
    async testBackendConnection() {
        try {
            setState('isLoading', true);
            const ping = await AutomataAPI.ping();
            window.showToast?.(`Backend connection successful: ${ping.message}`, 'success');
            console.log('🏓 Backend ping successful:', ping);
            return true;
        } catch (error) {
            console.error('Error testing backend connection:', error);
            window.showToast?.(`Backend connection failed: ${getErrorMessage(error)}`, 'error');
            return false;
        } finally {
            setState('isLoading', false);
        }
    }
    
    /**
     * Refresh health status
     */
    async refreshHealthStatus() {
        try {
            setState('isLoading', true);
            window.showToast?.('Checking health status...', 'info');
            
            const healthStatus = await AutomataAPI.getHealthStatus();
            setState('healthStatus', healthStatus);
            
            const statusType = healthStatus.status === 'healthy' ? 'success' : 'warning';
            window.showToast?.(`Health status: ${healthStatus.status}`, statusType);
            
            console.log('🏥 Health status checked:', healthStatus);
            return healthStatus;
        } catch (error) {
            console.error('Error checking health status:', error);
            window.showToast?.(`Health check failed: ${getErrorMessage(error)}`, 'error');
            throw error;
        } finally {
            setState('isLoading', false);
        }
    }
    
    /**
     * Export system data
     */
    async exportSystemData() {
        try {
            setState('isLoading', true);
            
            const exportData = {
                metadata: {
                    appName: APP_CONFIG.name,
                    version: APP_CONFIG.version,
                    exportTime: new Date().toISOString(),
                    platform: navigator.platform || 'Unknown'
                },
                systemInfo: getState('systemInfo'),
                healthStatus: getState('healthStatus'),
                featuresStatus: getState('featuresStatus'),
                browserInfo: {
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    onLine: navigator.onLine
                }
            };
            
            const fileName = `automata-export-${new Date().toISOString().split('T')[0]}.json`;
            
            // Use helper function to download
            const { downloadData } = await import('../utils/helpers.js');
            downloadData(exportData, fileName);
            
            window.showToast?.(`Data exported successfully as ${fileName}`, 'success');
            console.log('💾 System data exported successfully');
            
        } catch (error) {
            console.error('Error exporting data:', error);
            window.showToast?.(APP_CONFIG.messages.ui.exportFailed, 'error');
        } finally {
            setState('isLoading', false);
        }
    }
    
    /**
     * Cleanup dashboard page
     */
    destroy() {
        if (this.uptimeInterval) {
            clearInterval(this.uptimeInterval);
        }
        this.isActive = false;
    }
}

// Export dashboard page instance
export const dashboardPage = new DashboardPage();

// Export action functions for global access
export async function testBackendConnection() {
    return await dashboardPage.testBackendConnection();
}

export async function refreshHealthStatus() {
    return await dashboardPage.refreshHealthStatus();
}

export async function exportSystemData() {
    return await dashboardPage.exportSystemData();
} 