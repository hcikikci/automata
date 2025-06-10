/**
 * UI Components JavaScript
 * Handles toast notifications, modals, and other interactive components
 */

// Toast notification system
const ToastManager = {
    container: null,
    toasts: new Map(),
    
    init() {
        // Create toast container if it doesn't exist
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },
    
    show(message, type = 'info', duration = 5000) {
        if (!this.container) this.init();
        
        const toastId = Date.now() + Math.random();
        const toast = this.createToast(toastId, message, type);
        
        this.container.appendChild(toast);
        this.toasts.set(toastId, toast);
        
        // Auto remove after duration
        if (duration > 0) {
            setTimeout(() => this.remove(toastId), duration);
        }
        
        return toastId;
    },
    
    createToast(id, message, type) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.dataset.toastId = id;
        
        toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-message">${this.escapeHtml(message)}</div>
            </div>
            <button class="toast-close" onclick="ToastManager.remove(${id})">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Add click to dismiss
        toast.addEventListener('click', (e) => {
            if (e.target.classList.contains('toast-close') || e.target.parentElement.classList.contains('toast-close')) {
                this.remove(id);
            }
        });
        
        return toast;
    },
    
    remove(toastId) {
        const toast = this.toasts.get(toastId);
        if (toast) {
            toast.classList.add('removing');
            
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
                this.toasts.delete(toastId);
            }, 300); // Match CSS animation duration
        }
    },
    
    clear() {
        this.toasts.forEach((toast, id) => this.remove(id));
    },
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Global toast function
window.showToast = function(message, type = 'info', duration = 5000) {
    return ToastManager.show(message, type, duration);
};

// Modal system
const ModalManager = {
    activeModal: null,
    backdropHandler: null,
    escapeHandler: null,
    
    show(modalId, options = {}) {
        const modal = document.getElementById(modalId);
        if (!modal) {
            console.error(`Modal with id '${modalId}' not found`);
            return;
        }
        
        // Close existing modal
        if (this.activeModal && this.activeModal !== modal) {
            this.hide(this.activeModal.id);
        }
        
        modal.classList.remove('hidden');
        modal.classList.add('active');
        this.activeModal = modal;
        
        // Create bound handlers for proper cleanup
        this.backdropHandler = this.handleBackdropClick.bind(this);
        this.escapeHandler = this.handleEscapeKey.bind(this);
        
        // Add event handlers
        modal.addEventListener('click', this.backdropHandler);
        document.addEventListener('keydown', this.escapeHandler);
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus first input or button
        const firstFocusable = modal.querySelector('input, button, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (firstFocusable) {
            setTimeout(() => firstFocusable.focus(), 100);
        }
    },
    
    hide(modalId) {
        const modal = modalId ? document.getElementById(modalId) : this.activeModal;
        if (!modal) return;
        
        modal.classList.add('hidden');
        modal.classList.remove('active');
        
        if (this.activeModal === modal) {
            this.activeModal = null;
        }
        
        // Remove event listeners with bound handlers
        if (this.backdropHandler) {
            modal.removeEventListener('click', this.backdropHandler);
            this.backdropHandler = null;
        }
        if (this.escapeHandler) {
            document.removeEventListener('keydown', this.escapeHandler);
            this.escapeHandler = null;
        }
        
        // Restore body scroll
        document.body.style.overflow = '';
    },
    
    handleBackdropClick(e) {
        if (e.target === e.currentTarget) {
            this.hide();
        }
    },
    
    handleEscapeKey(e) {
        if (e.key === 'Escape') {
            this.hide();
        }
    }
};

// Global modal functions
window.showModal = function(modalId, options = {}) {
    return ModalManager.show(modalId, options);
};

window.hideModal = function(modalId) {
    return ModalManager.hide(modalId);
};

// Dropdown component
class Dropdown {
    constructor(element) {
        this.element = element;
        this.trigger = element.querySelector('.dropdown-trigger');
        this.menu = element.querySelector('.dropdown-menu');
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        if (this.trigger) {
            this.trigger.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggle();
            });
        }
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.element.contains(e.target)) {
                this.close();
            }
        });
        
        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }
    
    toggle() {
        this.isOpen ? this.close() : this.open();
    }
    
    open() {
        if (this.menu) {
            this.menu.classList.remove('hidden');
            this.element.classList.add('open');
            this.isOpen = true;
        }
    }
    
    close() {
        if (this.menu) {
            this.menu.classList.add('hidden');
            this.element.classList.remove('open');
            this.isOpen = false;
        }
    }
}

// Tooltip component
class Tooltip {
    constructor(element) {
        this.element = element;
        this.tooltip = null;
        this.content = element.getAttribute('data-tooltip') || element.getAttribute('title');
        this.position = element.getAttribute('data-tooltip-position') || 'top';
        
        this.init();
    }
    
    init() {
        if (!this.content) return;
        
        // Remove title attribute to prevent browser tooltip
        this.element.removeAttribute('title');
        
        this.element.addEventListener('mouseenter', () => this.show());
        this.element.addEventListener('mouseleave', () => this.hide());
        this.element.addEventListener('focus', () => this.show());
        this.element.addEventListener('blur', () => this.hide());
    }
    
    show() {
        if (this.tooltip) return;
        
        this.tooltip = document.createElement('div');
        this.tooltip.className = `tooltip tooltip-${this.position}`;
        this.tooltip.textContent = this.content;
        
        document.body.appendChild(this.tooltip);
        this.position_tooltip();
    }
    
    hide() {
        if (this.tooltip) {
            document.body.removeChild(this.tooltip);
            this.tooltip = null;
        }
    }
    
    position_tooltip() {
        if (!this.tooltip) return;
        
        const rect = this.element.getBoundingClientRect();
        const tooltipRect = this.tooltip.getBoundingClientRect();
        
        let top, left;
        
        switch (this.position) {
            case 'top':
                top = rect.top - tooltipRect.height - 8;
                left = rect.left + (rect.width - tooltipRect.width) / 2;
                break;
            case 'bottom':
                top = rect.bottom + 8;
                left = rect.left + (rect.width - tooltipRect.width) / 2;
                break;
            case 'left':
                top = rect.top + (rect.height - tooltipRect.height) / 2;
                left = rect.left - tooltipRect.width - 8;
                break;
            case 'right':
                top = rect.top + (rect.height - tooltipRect.height) / 2;
                left = rect.right + 8;
                break;
            default:
                top = rect.top - tooltipRect.height - 8;
                left = rect.left + (rect.width - tooltipRect.width) / 2;
        }
        
        // Keep tooltip in viewport
        top = Math.max(8, Math.min(top, window.innerHeight - tooltipRect.height - 8));
        left = Math.max(8, Math.min(left, window.innerWidth - tooltipRect.width - 8));
        
        this.tooltip.style.top = `${top}px`;
        this.tooltip.style.left = `${left}px`;
    }
}

// Progress bar component
class ProgressBar {
    constructor(element) {
        this.element = element;
        this.fill = element.querySelector('.progress-fill');
        this.value = 0;
        this.max = 100;
        
        this.init();
    }
    
    init() {
        const value = this.element.getAttribute('data-value');
        const max = this.element.getAttribute('data-max');
        
        if (value !== null) this.value = parseFloat(value);
        if (max !== null) this.max = parseFloat(max);
        
        this.update();
    }
    
    setValue(value) {
        this.value = Math.max(0, Math.min(value, this.max));
        this.update();
    }
    
    setMax(max) {
        this.max = Math.max(1, max);
        this.update();
    }
    
    update() {
        if (this.fill) {
            const percentage = (this.value / this.max) * 100;
            this.fill.style.width = `${percentage}%`;
        }
        
        this.element.setAttribute('data-value', this.value);
        this.element.setAttribute('data-max', this.max);
    }
}

// Loading spinner component
class LoadingSpinner {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.options = {
            size: options.size || 'medium',
            color: options.color || 'primary',
            message: options.message || 'Loading...',
            overlay: options.overlay !== false
        };
        this.element = null;
    }
    
    show() {
        if (this.element) return;
        
        this.element = document.createElement('div');
        this.element.className = `loading-spinner ${this.options.overlay ? 'loading-overlay' : ''}`;
        
        this.element.innerHTML = `
            <div class="spinner-content">
                <div class="spinner ${this.options.size} ${this.options.color}"></div>
                ${this.options.message ? `<div class="spinner-message">${this.options.message}</div>` : ''}
            </div>
        `;
        
        if (this.container) {
            this.container.appendChild(this.element);
        } else {
            document.body.appendChild(this.element);
        }
    }
    
    hide() {
        if (this.element) {
            if (this.element.parentNode) {
                this.element.parentNode.removeChild(this.element);
            }
            this.element = null;
        }
    }
    
    setMessage(message) {
        if (this.element) {
            const messageEl = this.element.querySelector('.spinner-message');
            if (messageEl) {
                messageEl.textContent = message;
            }
        }
        this.options.message = message;
    }
}

// Auto-initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize toast manager
    ToastManager.init();
    
    // Initialize dropdowns
    document.querySelectorAll('.dropdown').forEach(el => new Dropdown(el));
    
    // Initialize tooltips
    document.querySelectorAll('[data-tooltip], [title]').forEach(el => new Tooltip(el));
    
    // Initialize progress bars
    document.querySelectorAll('.progress-bar').forEach(el => new ProgressBar(el));
    
    console.log('✅ UI Components initialized');
});

// Export components for global use
window.Dropdown = Dropdown;
window.Tooltip = Tooltip;
window.ProgressBar = ProgressBar;
window.LoadingSpinner = LoadingSpinner;
window.ToastManager = ToastManager;
window.ModalManager = ModalManager; 