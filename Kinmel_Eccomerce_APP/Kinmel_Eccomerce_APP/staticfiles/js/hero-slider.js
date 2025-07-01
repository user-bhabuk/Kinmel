// ===== KINMEL HERO SLIDER - ADVANCED ANIMATIONS =====

document.addEventListener('DOMContentLoaded', function() {
    // Add loading class initially
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        heroSection.classList.add('loading');
    }

    // Initialize hero slider
    initHeroSlider();

    // Initialize typing animation
    initTypingAnimation();

    // Initialize counter animations
    initCounterAnimations();

    // Initialize particle effects
    initParticleEffects();

    // Initialize mouse parallax
    initMouseParallax();

    // Initialize AOS (Animate On Scroll) if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            easing: 'ease-out-cubic',
            once: true,
            offset: 100
        });
    }

    // Remove loading screen after everything is initialized
    setTimeout(() => {
        const heroLoading = document.getElementById('heroLoading');
        if (heroLoading) {
            heroLoading.classList.add('hidden');
            setTimeout(() => {
                heroLoading.remove();
            }, 800);
        }

        if (heroSection) {
            heroSection.classList.remove('loading');
            heroSection.classList.add('loaded');
        }
    }, 2000); // Show loading for 2 seconds
});

// ===== HERO SLIDER FUNCTIONALITY =====

let currentSlideIndex = 0;
let slideInterval;
const slides = document.querySelectorAll('.hero-slide');
const indicators = document.querySelectorAll('.indicator');
const totalSlides = slides.length;

function initHeroSlider() {
    if (slides.length === 0) return;
    
    // Set initial slide background
    updateSlideBackground();
    
    // Start auto-slide
    startAutoSlide();
    
    // Add event listeners for navigation
    addNavigationListeners();
    
    // Add touch/swipe support
    addTouchSupport();
}

function changeSlide(direction) {
    // Remove active class from current slide and indicator
    slides[currentSlideIndex].classList.remove('active');
    indicators[currentSlideIndex].classList.remove('active');
    
    // Calculate new slide index
    currentSlideIndex += direction;
    
    if (currentSlideIndex >= totalSlides) {
        currentSlideIndex = 0;
    } else if (currentSlideIndex < 0) {
        currentSlideIndex = totalSlides - 1;
    }
    
    // Add active class to new slide and indicator
    slides[currentSlideIndex].classList.add('active');
    indicators[currentSlideIndex].classList.add('active');
    
    // Update background
    updateSlideBackground();
    
    // Restart typing animation for new slide
    restartTypingAnimation();
    
    // Restart auto-slide
    restartAutoSlide();
}

function currentSlide(index) {
    const direction = index - 1 - currentSlideIndex;
    changeSlide(direction);
}

function updateSlideBackground() {
    const activeSlide = slides[currentSlideIndex];
    const bgValue = activeSlide.getAttribute('data-bg');
    
    if (bgValue) {
        document.querySelector('.hero-section').style.background = bgValue;
    }
}

function startAutoSlide() {
    slideInterval = setInterval(() => {
        changeSlide(1);
    }, 8000); // Change slide every 8 seconds
}

function restartAutoSlide() {
    clearInterval(slideInterval);
    startAutoSlide();
}

function addNavigationListeners() {
    // Previous/Next buttons
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => changeSlide(-1));
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => changeSlide(1));
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            changeSlide(-1);
        } else if (e.key === 'ArrowRight') {
            changeSlide(1);
        }
    });
}

function addTouchSupport() {
    let startX = 0;
    let endX = 0;
    
    const heroSection = document.querySelector('.hero-section');
    
    heroSection.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    });
    
    heroSection.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = startX - endX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                changeSlide(1); // Swipe left - next slide
            } else {
                changeSlide(-1); // Swipe right - previous slide
            }
        }
    }
}

// ===== TYPING ANIMATION =====

const typingTexts = [
    "Your Shopping Paradise",
    "Trusted by Millions",
    "Best Deals Worldwide",
    "Shop with Confidence"
];

let typingIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typingSpeed = 100;

function initTypingAnimation() {
    const typingElement = document.querySelector('.typing-text');
    if (typingElement) {
        typeText(typingElement);
    }
}

function typeText(element) {
    const currentText = typingTexts[typingIndex];
    
    if (isDeleting) {
        element.textContent = currentText.substring(0, charIndex - 1);
        charIndex--;
        typingSpeed = 50;
    } else {
        element.textContent = currentText.substring(0, charIndex + 1);
        charIndex++;
        typingSpeed = 100;
    }
    
    if (!isDeleting && charIndex === currentText.length) {
        // Pause at end of text
        typingSpeed = 2000;
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        typingIndex = (typingIndex + 1) % typingTexts.length;
        typingSpeed = 500;
    }
    
    setTimeout(() => typeText(element), typingSpeed);
}

function restartTypingAnimation() {
    // Reset typing animation when slide changes
    typingIndex = 0;
    charIndex = 0;
    isDeleting = false;
    typingSpeed = 100;
}

// ===== COUNTER ANIMATIONS =====

function initCounterAnimations() {
    const counters = document.querySelectorAll('.stat-number');
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-count'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// ===== BUTTON RIPPLE EFFECT =====

document.addEventListener('click', function(e) {
    if (e.target.closest('.pulse-btn')) {
        const button = e.target.closest('.pulse-btn');
        const ripple = button.querySelector('.btn-ripple');
        
        if (ripple) {
            ripple.style.width = '0';
            ripple.style.height = '0';
            
            setTimeout(() => {
                ripple.style.width = '300px';
                ripple.style.height = '300px';
            }, 10);
        }
    }
});

// ===== FLOATING ELEMENTS INTERACTION =====

document.querySelectorAll('.floating-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-15px) scale(1.08) rotateY(5deg)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1) rotateY(0deg)';
    });
});

// ===== TOY ELEMENTS INTERACTION (Kids Slide) =====

document.querySelectorAll('.toy-element').forEach(toy => {
    toy.addEventListener('click', function() {
        // Add bounce animation
        this.style.animation = 'none';
        setTimeout(() => {
            this.style.animation = 'bounce 0.6s ease-in-out';
        }, 10);
        
        // Create sparkle effect
        createSparkleEffect(this);
    });
});

function createSparkleEffect(element) {
    const sparkles = ['✨', '⭐', '🌟', '💫'];
    const rect = element.getBoundingClientRect();
    
    for (let i = 0; i < 5; i++) {
        const sparkle = document.createElement('div');
        sparkle.textContent = sparkles[Math.floor(Math.random() * sparkles.length)];
        sparkle.style.position = 'fixed';
        sparkle.style.left = rect.left + Math.random() * rect.width + 'px';
        sparkle.style.top = rect.top + Math.random() * rect.height + 'px';
        sparkle.style.fontSize = '1.5rem';
        sparkle.style.pointerEvents = 'none';
        sparkle.style.zIndex = '9999';
        sparkle.style.animation = 'sparkleFloat 1s ease-out forwards';
        
        document.body.appendChild(sparkle);
        
        setTimeout(() => {
            sparkle.remove();
        }, 1000);
    }
}

// Add sparkle animation CSS
const sparkleCSS = `
@keyframes sparkleFloat {
    0% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
    100% {
        opacity: 0;
        transform: translateY(-50px) scale(0.5);
    }
}
`;

const style = document.createElement('style');
style.textContent = sparkleCSS;
document.head.appendChild(style);

// ===== TREND CARDS INTERACTION (Teen Slide) =====

document.querySelectorAll('.trend-card').forEach(card => {
    card.addEventListener('click', function() {
        // Add glow effect
        this.style.boxShadow = '0 0 60px rgba(102, 126, 234, 0.8)';
        this.style.transform = 'scale(1.15)';
        
        setTimeout(() => {
            this.style.boxShadow = '0 0 30px rgba(102, 126, 234, 0.3)';
            this.style.transform = 'scale(1)';
        }, 300);
    });
});

// ===== SCROLL INDICATOR =====

const scrollIndicator = document.querySelector('.scroll-indicator');
if (scrollIndicator) {
    scrollIndicator.addEventListener('click', () => {
        const categoriesSection = document.querySelector('#categories');
        if (categoriesSection) {
            categoriesSection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}

// ===== PERFORMANCE OPTIMIZATION =====

// Pause animations when tab is not visible
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        clearInterval(slideInterval);
        // Pause CSS animations
        document.body.style.animationPlayState = 'paused';
    } else {
        startAutoSlide();
        // Resume CSS animations
        document.body.style.animationPlayState = 'running';
    }
});

// Reduce motion for users who prefer it
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Disable auto-slide
    clearInterval(slideInterval);
    
    // Reduce animation durations
    const style = document.createElement('style');
    style.textContent = `
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    `;
    document.head.appendChild(style);
}

// ===== UTILITY FUNCTIONS =====

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

// Debounced resize handler
window.addEventListener('resize', debounce(() => {
    // Recalculate positions if needed
    updateSlideBackground();
}, 250));

// ===== PARTICLE EFFECTS =====

function initParticleEffects() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    // Create floating particles
    for (let i = 0; i < 20; i++) {
        createFloatingParticle(heroSection);
    }
}

function createFloatingParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'floating-particle';
    particle.style.cssText = `
        position: absolute;
        width: ${Math.random() * 6 + 2}px;
        height: ${Math.random() * 6 + 2}px;
        background: rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2});
        border-radius: 50%;
        pointer-events: none;
        z-index: 1;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: floatParticle ${Math.random() * 10 + 10}s linear infinite;
    `;

    container.appendChild(particle);

    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 20000);
}

// Add particle animation CSS
const particleCSS = `
@keyframes floatParticle {
    0% {
        transform: translateY(100vh) translateX(0px) rotate(0deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(-100px) translateX(${Math.random() * 200 - 100}px) rotate(360deg);
        opacity: 0;
    }
}
`;

const particleStyle = document.createElement('style');
particleStyle.textContent = particleCSS;
document.head.appendChild(particleStyle);

// ===== MOUSE PARALLAX EFFECT =====

function initMouseParallax() {
    const heroSection = document.querySelector('.hero-section');
    const floatingCards = document.querySelectorAll('.floating-card');
    const toyElements = document.querySelectorAll('.toy-element');
    const trendCards = document.querySelectorAll('.trend-card');

    if (!heroSection) return;

    heroSection.addEventListener('mousemove', (e) => {
        const rect = heroSection.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;

        // Apply parallax to floating cards
        floatingCards.forEach((card, index) => {
            const intensity = (index + 1) * 0.5;
            const moveX = (x - 0.5) * intensity * 20;
            const moveY = (y - 0.5) * intensity * 20;

            card.style.transform = `translate(${moveX}px, ${moveY}px) translateY(0px) scale(1)`;
        });

        // Apply parallax to toy elements
        toyElements.forEach((toy, index) => {
            const intensity = (index + 1) * 0.3;
            const moveX = (x - 0.5) * intensity * 15;
            const moveY = (y - 0.5) * intensity * 15;

            toy.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });

        // Apply parallax to trend cards
        trendCards.forEach((card, index) => {
            const intensity = (index + 1) * 0.4;
            const moveX = (x - 0.5) * intensity * 10;
            const moveY = (y - 0.5) * intensity * 10;

            card.style.transform = `translate(${moveX}px, ${moveY}px) scale(1)`;
        });
    });

    // Reset positions when mouse leaves
    heroSection.addEventListener('mouseleave', () => {
        floatingCards.forEach(card => {
            card.style.transform = 'translate(0px, 0px) translateY(0px) scale(1)';
        });

        toyElements.forEach(toy => {
            toy.style.transform = 'translate(0px, 0px)';
        });

        trendCards.forEach(card => {
            card.style.transform = 'translate(0px, 0px) scale(1)';
        });
    });
}

// ===== ENHANCED INTERACTIONS =====

// Add click sound effect (optional)
function playClickSound() {
    // Create audio context for click sounds
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);

    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

// Enhanced button interactions
document.addEventListener('click', function(e) {
    // Add click effect to all buttons
    if (e.target.closest('button') || e.target.closest('.btn')) {
        const element = e.target.closest('button') || e.target.closest('.btn');

        // Add click animation
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);

        // Optional: Play click sound (uncomment if desired)
        // playClickSound();
    }
});

// ===== PERFORMANCE MONITORING =====

// Monitor FPS and adjust animations accordingly
let fps = 60;
let lastTime = performance.now();
let frameCount = 0;

function monitorPerformance() {
    const currentTime = performance.now();
    frameCount++;

    if (currentTime - lastTime >= 1000) {
        fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
        frameCount = 0;
        lastTime = currentTime;

        // Reduce animations if FPS is low
        if (fps < 30) {
            document.body.classList.add('low-performance');
        } else {
            document.body.classList.remove('low-performance');
        }
    }

    requestAnimationFrame(monitorPerformance);
}

// Start performance monitoring
requestAnimationFrame(monitorPerformance);

// Add low performance CSS
const lowPerfCSS = `
.low-performance * {
    animation-duration: 0.5s !important;
    transition-duration: 0.2s !important;
}

.low-performance .floating-card,
.low-performance .toy-element,
.low-performance .trend-card {
    animation: none !important;
}
`;

const lowPerfStyle = document.createElement('style');
lowPerfStyle.textContent = lowPerfCSS;
document.head.appendChild(lowPerfStyle);

// ===== EXPORT FOR GLOBAL ACCESS =====

window.HeroSlider = {
    changeSlide,
    currentSlide,
    startAutoSlide,
    restartAutoSlide,
    initParticleEffects,
    initMouseParallax
};
