// ===== MODERN PRODUCT PAGE INTERACTIONS =====

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all product page features
    initScrollAnimations();
    initProductCardInteractions();
    initSearchEnhancements();
    initFilterAnimations();
    initSortingFunctionality();
    initQuickActions();
});

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    document.querySelectorAll('.fade-in-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// ===== PRODUCT CARD INTERACTIONS =====
function initProductCardInteractions() {
    const productCards = document.querySelectorAll('.product-card-modern');
    
    productCards.forEach(card => {
        // Hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            this.querySelector('.product-actions').classList.add('show');
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.querySelector('.product-actions').classList.remove('show');
        });
        
        // Parallax effect on mouse move
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            this.style.transform = `translateY(-10px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1) rotateX(0deg) rotateY(0deg)';
        });
    });
}

// ===== SEARCH ENHANCEMENTS =====
function initSearchEnhancements() {
    const searchInput = document.querySelector('.modern-input[name="query"]');
    if (!searchInput) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(() => {
                // Add visual feedback
                this.style.background = 'linear-gradient(45deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05))';
                
                // Here you could implement live search suggestions
                console.log('Searching for:', query);
            }, 300);
        } else {
            this.style.background = '';
        }
    });
    
    // Search suggestions (placeholder for future implementation)
    searchInput.addEventListener('focus', function() {
        // Show search suggestions dropdown
        console.log('Show search suggestions');
    });
    
    searchInput.addEventListener('blur', function() {
        // Hide search suggestions dropdown
        setTimeout(() => {
            console.log('Hide search suggestions');
        }, 200);
    });
}

// ===== FILTER ANIMATIONS =====
function initFilterAnimations() {
    const filterInputs = document.querySelectorAll('.modern-input, .modern-select');
    
    filterInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            this.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Checkbox animations
    const checkboxes = document.querySelectorAll('.filter-checkbox input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                this.style.animation = 'checkboxPop 0.3s ease-out';
                setTimeout(() => {
                    this.style.animation = '';
                }, 300);
            }
        });
    });
}

// ===== SORTING FUNCTIONALITY =====
function initSortingFunctionality() {
    const sortButtons = document.querySelectorAll('.sort-btn');
    
    sortButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            sortButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const sortType = this.dataset.sort;
            
            // Add loading state
            this.style.opacity = '0.7';
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>' + this.textContent;
            
            // Simulate sorting (in real implementation, this would trigger a server request)
            setTimeout(() => {
                this.style.opacity = '1';
                this.innerHTML = this.innerHTML.replace('<i class="fas fa-spinner fa-spin me-1"></i>', '');
                
                // Here you would implement actual sorting logic
                console.log('Sorting by:', sortType);
                
                // Animate product grid
                const productGrid = document.querySelector('.product-grid');
                if (productGrid) {
                    productGrid.style.opacity = '0.5';
                    productGrid.style.transform = 'scale(0.98)';
                    
                    setTimeout(() => {
                        productGrid.style.opacity = '1';
                        productGrid.style.transform = 'scale(1)';
                    }, 300);
                }
            }, 500);
        });
    });
}

// ===== QUICK ACTIONS =====
function initQuickActions() {
    // Quick view functionality
    const quickViewButtons = document.querySelectorAll('.action-btn[title="Quick View"]');
    quickViewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            
            // Add loading state
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            // Simulate quick view modal (placeholder)
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-eye"></i>';
                console.log('Quick view for product:', productId);
                
                // Here you would open a modal with product details
                showQuickViewModal(productId);
            }, 500);
        });
    });
    
    // Wishlist functionality
    const wishlistButtons = document.querySelectorAll('.action-btn[title="Add to Wishlist"]');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            
            if (this.classList.contains('active')) {
                icon.className = 'fas fa-heart';
                this.style.color = '#ff6b6b';
                this.style.animation = 'heartBeat 0.6s ease-in-out';
                
                // Show success message
                showToast('Added to wishlist!', 'success');
            } else {
                icon.className = 'far fa-heart';
                this.style.color = '';
                this.style.animation = '';
                
                showToast('Removed from wishlist', 'info');
            }
            
            // Reset animation
            setTimeout(() => {
                this.style.animation = '';
            }, 600);
        });
    });
    
    // Compare functionality
    const compareButtons = document.querySelectorAll('.action-btn[title="Compare"]');
    compareButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            
            if (this.classList.contains('active')) {
                this.style.color = '#4ecdc4';
                showToast('Added to compare list', 'success');
            } else {
                this.style.color = '';
                showToast('Removed from compare list', 'info');
            }
        });
    });
}

// ===== UTILITY FUNCTIONS =====

function showQuickViewModal(productId) {
    // Placeholder for quick view modal
    console.log('Opening quick view modal for product:', productId);
    
    // In a real implementation, you would:
    // 1. Fetch product details via AJAX
    // 2. Create and show a modal with product information
    // 3. Allow adding to cart from the modal
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)} me-2"></i>
            ${message}
        </div>
    `;
    
    // Style the toast
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getToastColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 9999;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getToastColor(type) {
    const colors = {
        success: 'linear-gradient(45deg, #51cf66, #40c057)',
        error: 'linear-gradient(45deg, #ff6b6b, #ee5a52)',
        warning: 'linear-gradient(45deg, #ffd43b, #fab005)',
        info: 'linear-gradient(45deg, #667eea, #764ba2)'
    };
    return colors[type] || colors.info;
}

// ===== PERFORMANCE OPTIMIZATIONS =====

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Export functions for global access
window.ProductPage = {
    showQuickViewModal,
    showToast,
    initScrollAnimations,
    initProductCardInteractions
};
