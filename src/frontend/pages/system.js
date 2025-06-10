/**
 * System Information Page Module
 * Handles system info display and functionality
 */

import { AutomataAPI } from '../lib/api.js';
import { state, setState, getState, subscribeToState } from '../lib/state.js';
import { getErrorMessage, formatFileSize, formatPercentage } from '../utils/helpers.js';
import { APP_CONFIG } from '../config/app.js';

export class SystemPage {
    constructor() {
        this.isActive = false;
        this.refreshInterval = null;
        this.stateUnsubscribers = [];
    }
    
    /**
     * Initialize system page
     */
    async init() {
        console.log('🖥️ Initializing System page...');
        
        // Subscribe to state changes
        this.setupStateSubscriptions();
        
        console.log('✅ System page initialized');
    }
    
    /**
     * Called when entering the system page
     */
    async onEnter() {
        this.isActive = true;
        console.log('🖥️ Entering System page');
        
        try {
            // Load system information
            await this.loadSystemInfo();
            
            // Start auto-refresh
            this.startAutoRefresh();
            
        } catch (error) {
            console.error('Error loading system page:', error);
            window.showToast?.(`Failed to load system info: ${getErrorMessage(error)}`, 'error');
        }
    }
    
    /**
     * Called when leaving the system page
     */
    async onLeave() {
        this.isActive = false;
        console.log('🖥️ Leaving System page');
        
        // Stop auto-refresh
        this.stopAutoRefresh();
    }
    
    /**
     * Setup state subscriptions
     */
    setupStateSubscriptions() {
        // Subscribe to system info changes
        const unsubscribeSystemInfo = subscribeToState('systemInfo', (systemInfo) => {
            if (this.isActive && systemInfo) {
                this.displaySystemInfo(systemInfo, getState('healthStatus'));
            }
        });
        
        // Subscribe to health status changes
        const unsubscribeHealthStatus = subscribeToState('healthStatus', (healthStatus) => {
            if (this.isActive && healthStatus) {
                this.displaySystemInfo(getState('systemInfo'), healthStatus);
            }
        });
        
        this.stateUnsubscribers.push(unsubscribeSystemInfo, unsubscribeHealthStatus);
    }
    
    /**
     * Load system information
     */
    async loadSystemInfo() {
        const systemInfoContainer = document.getElementById('system-info');
        if (!systemInfoContainer) {
            console.warn('System info container not found');
            return;
        }
        
        try {
            setState('isLoading', true);
            systemInfoContainer.innerHTML = '<div class="loading">Loading system information...</div>';
            
            const [systemInfo, healthStatus] = await Promise.all([
                AutomataAPI.getSystemInfo(),
                AutomataAPI.getHealthStatus()
            ]);
            
            // Update state
            state.updateSystemData({ systemInfo, healthStatus });
            
            console.log('📊 System information loaded successfully');
            
        } catch (error) {
            console.error('Error loading system info:', error);
            
            systemInfoContainer.innerHTML = `
                <div class="error">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h4>Failed to Load System Information</h4>
                    <p class="error-message">${getErrorMessage(error)}</p>
                    <div class="error-actions">
                        <button class="btn btn-primary" onclick="window.systemPage?.loadSystemInfo()">
                            <i class="fas fa-sync"></i>
                            Retry
                        </button>
                    </div>
                </div>
            `;
            
            window.showToast?.(`System info error: ${getErrorMessage(error)}`, 'error');
            setState('lastError', error);
        } finally {
            setState('isLoading', false);
        }
    }
    
    /**
     * Display system information in UI
     * @param {Object} systemInfo - System information data
     * @param {Object} healthStatus - Health status data
     */
    displaySystemInfo(systemInfo, healthStatus) {
        const container = document.getElementById('system-info');
        if (!container || !systemInfo || !healthStatus) return;
        
        const checks = healthStatus.checks || {};
        
        const html = `
            <div class="info-section">
                <h4>Platform Information</h4>
                <div class="info-grid">
                    ${this.createInfoItem('System', systemInfo.system || 'Unknown')}
                    ${this.createInfoItem('Platform', systemInfo.platform || 'Unknown')}
                    ${this.createInfoItem('Processor', systemInfo.processor || 'Unknown')}
                    ${this.createInfoItem('Hostname', systemInfo.hostname || 'Unknown')}
                    ${this.createInfoItem('Python Version', systemInfo.python_version || 'Unknown')}
                </div>
            </div>
            
            <div class="info-section">
                <h4>Memory Information</h4>
                <div class="info-grid">
                    ${this.createInfoItem('Total RAM', this.formatMemory(checks.memory_usage?.data?.total_gb))}
                    ${this.createInfoItem('Available RAM', this.formatMemory(checks.memory_usage?.data?.available_gb))}
                    ${this.createInfoItem('Used RAM', this.formatMemory(checks.memory_usage?.data?.used_gb))}
                    ${this.createInfoItem('Memory Usage', formatPercentage(checks.memory_usage?.data?.percentage || 0))}
                </div>
                ${this.createProgressBar('Memory Usage', checks.memory_usage?.data?.percentage || 0)}
            </div>
            
            <div class="info-section">
                <h4>CPU Information</h4>
                <div class="info-grid">
                    ${this.createInfoItem('Physical Cores', checks.cpu_usage?.data?.core_count || 0)}
                    ${this.createInfoItem('Logical Cores', checks.cpu_usage?.data?.logical_core_count || 0)}
                    ${this.createInfoItem('CPU Usage', formatPercentage(checks.cpu_usage?.data?.percentage || 0))}
                </div>
                ${this.createProgressBar('CPU Usage', checks.cpu_usage?.data?.percentage || 0)}
            </div>
            
            <div class="info-section">
                <h4>Disk Information</h4>
                <div class="info-grid">
                    ${this.createInfoItem('Total Disk', this.formatDiskSpace(checks.disk_usage?.data?.total_gb))}
                    ${this.createInfoItem('Used Disk', this.formatDiskSpace(checks.disk_usage?.data?.used_gb))}
                    ${this.createInfoItem('Free Disk', this.formatDiskSpace(checks.disk_usage?.data?.free_gb))}
                    ${this.createInfoItem('Disk Usage', formatPercentage(checks.disk_usage?.data?.percentage || 0))}
                </div>
                ${this.createProgressBar('Disk Usage', checks.disk_usage?.data?.percentage || 0)}
            </div>
            
            <div class="info-section">
                <h4>Application Status</h4>
                <div class="info-grid">
                    ${this.createInfoItem('Health Status', `<span class="status-${healthStatus.status === 'healthy' ? 'active' : 'warning'}">${healthStatus.status || 'Unknown'}</span>`)}
                    ${this.createInfoItem('Uptime', checks.application_uptime?.data?.uptime_formatted || 'Unknown')}
                    ${this.createInfoItem('Total Checks', healthStatus.summary?.total_checks || 0)}
                    ${this.createInfoItem('Passed Checks', `<span class="status-active">${healthStatus.summary?.passed || 0}</span>`)}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    /**
     * Create info item HTML
     * @param {string} label - Item label
     * @param {string} value - Item value
     * @returns {string} HTML string
     */
    createInfoItem(label, value) {
        return `
            <div class="info-item">
                <span class="info-label">${label}</span>
                <span class="info-value">${value}</span>
            </div>
        `;
    }
    
    /**
     * Create progress bar HTML
     * @param {string} label - Progress bar label
     * @param {number} percentage - Percentage value
     * @returns {string} HTML string
     */
    createProgressBar(label, percentage) {
        const colorClass = percentage > 80 ? 'error' : percentage > 60 ? 'warning' : 'success';
        return `
            <div class="progress-info">
                <span class="progress-label">${label}: ${formatPercentage(percentage)}</span>
                <div class="progress-bar">
                    <div class="progress-fill ${colorClass}" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }
    
    /**
     * Format memory value
     * @param {number} value - Memory value in GB
     * @returns {string} Formatted memory
     */
    formatMemory(value) {
        if (!value) return '0 GB';
        return `${parseFloat(value).toFixed(1)} GB`;
    }
    
    /**
     * Format disk space value
     * @param {number} value - Disk space value in GB
     * @returns {string} Formatted disk space
     */
    formatDiskSpace(value) {
        if (!value) return '0 GB';
        if (value >= 1024) {
            return `${(value / 1024).toFixed(1)} TB`;
        }
        return `${parseFloat(value).toFixed(1)} GB`;
    }
    
    /**
     * Refresh system information
     */
    async refreshSystemInfo() {
        try {
            window.showToast?.('Refreshing system information...', 'info');
            await this.loadSystemInfo();
            window.showToast?.('System information updated successfully', 'success');
            console.log('🔄 System information refreshed');
        } catch (error) {
            console.error('Error refreshing system info:', error);
            window.showToast?.(`Refresh failed: ${getErrorMessage(error)}`, 'error');
        }
    }
    
    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        
        this.refreshInterval = setInterval(async () => {
            if (this.isActive) {
                try {
                    // Silent refresh - no loading indicators
                    const [systemInfo, healthStatus] = await Promise.all([
                        AutomataAPI.getSystemInfo(),
                        AutomataAPI.getHealthStatus()
                    ]);
                    
                    state.updateSystemData({ systemInfo, healthStatus });
                } catch (error) {
                    console.warn('Auto-refresh failed:', error);
                }
            }
        }, APP_CONFIG.refresh.systemInfo);
    }
    
    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
    
    /**
     * Cleanup system page
     */
    destroy() {
        this.stopAutoRefresh();
        this.isActive = false;
        
        // Unsubscribe from state changes
        this.stateUnsubscribers.forEach(unsubscribe => unsubscribe());
        this.stateUnsubscribers = [];
    }
}

// Export system page instance
export const systemPage = new SystemPage();

// Export refresh function for global access
export async function refreshSystemInfo() {
    return await systemPage.refreshSystemInfo();
}

// Make it globally available for onclick handlers
window.systemPage = systemPage; 