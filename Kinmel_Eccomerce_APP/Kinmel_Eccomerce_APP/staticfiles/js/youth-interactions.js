// ===== YOUTH-FOCUSED INTERACTIVE FEATURES =====

document.addEventListener('DOMContentLoaded', function() {
    initYouthFeatures();
});

function initYouthFeatures() {
    // Emoji Click Reactions
    initEmojiReactions();
    
    // Sound Effects (optional)
    initSoundEffects();
    
    // Particle Effects
    initParticleEffects();
    
    // Social Media Style Interactions
    initSocialInteractions();
    
    // Gaming-Style Achievements
    initAchievements();
}

// ===== EMOJI REACTIONS =====
function initEmojiReactions() {
    const emojis = document.querySelectorAll('.card-emoji, .deal-emoji, .reviewer-avatar');
    
    emojis.forEach(emoji => {
        emoji.addEventListener('click', function(e) {
            createEmojiExplosion(e.target, this.textContent);
        });
    });
}

function createEmojiExplosion(element, emojiChar) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    // Create multiple emoji particles
    for (let i = 0; i < 8; i++) {
        const particle = document.createElement('div');
        particle.textContent = emojiChar;
        particle.style.cssText = `
            position: fixed;
            left: ${centerX}px;
            top: ${centerY}px;
            font-size: 1.5rem;
            pointer-events: none;
            z-index: 9999;
            animation: emojiExplode 1s ease-out forwards;
            animation-delay: ${i * 0.1}s;
        `;
        
        // Random direction
        const angle = (i / 8) * Math.PI * 2;
        const distance = 100 + Math.random() * 50;
        const endX = centerX + Math.cos(angle) * distance;
        const endY = centerY + Math.sin(angle) * distance;
        
        particle.style.setProperty('--endX', endX + 'px');
        particle.style.setProperty('--endY', endY + 'px');
        
        document.body.appendChild(particle);
        
        // Remove after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 1500);
    }
}

// Add CSS for emoji explosion
const emojiStyle = document.createElement('style');
emojiStyle.textContent = `
    @keyframes emojiExplode {
        0% {
            transform: scale(1) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: scale(0.5) rotate(360deg) translate(var(--endX, 0), var(--endY, 0));
            opacity: 0;
        }
    }
`;
document.head.appendChild(emojiStyle);

// ===== SOUND EFFECTS =====
function initSoundEffects() {
    // Create audio context for sound effects
    let audioContext;
    
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) {
        console.log('Web Audio API not supported');
        return;
    }
    
    // Button click sounds
    const buttons = document.querySelectorAll('.trend-btn, .grab-btn');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            playClickSound(audioContext);
        });
    });
    
    // Hover sounds
    const cards = document.querySelectorAll('.trending-card, .deal-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            playHoverSound(audioContext);
        });
    });
}

function playClickSound(audioContext) {
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

function playHoverSound(audioContext) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.05);
    
    gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.05);
}

// ===== PARTICLE EFFECTS =====
function initParticleEffects() {
    const trendingSection = document.querySelector('.trending-section');
    if (!trendingSection) return;
    
    // Create particle container
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
    `;
    
    trendingSection.appendChild(particleContainer);
    
    // Create floating particles
    for (let i = 0; i < 20; i++) {
        createFloatingParticle(particleContainer);
    }
}

function createFloatingParticle(container) {
    const particle = document.createElement('div');
    const shapes = ['●', '★', '♦', '▲', '■'];
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
    
    particle.textContent = shapes[Math.floor(Math.random() * shapes.length)];
    particle.style.cssText = `
        position: absolute;
        color: ${colors[Math.floor(Math.random() * colors.length)]};
        font-size: ${Math.random() * 20 + 10}px;
        left: ${Math.random() * 100}%;
        top: 100%;
        opacity: 0.6;
        animation: floatUp ${Math.random() * 10 + 10}s linear infinite;
        animation-delay: ${Math.random() * 5}s;
    `;
    
    container.appendChild(particle);
    
    // Remove and recreate after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
            createFloatingParticle(container);
        }
    }, 15000);
}

// Add particle animation CSS
const particleStyle = document.createElement('style');
particleStyle.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.6;
        }
        90% {
            opacity: 0.6;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(particleStyle);

// ===== SOCIAL MEDIA STYLE INTERACTIONS =====
function initSocialInteractions() {
    // Double-tap to like
    let tapCount = 0;
    let tapTimer;
    
    const cards = document.querySelectorAll('.trending-card, .deal-card, .review-card');
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            tapCount++;
            
            if (tapCount === 1) {
                tapTimer = setTimeout(() => {
                    tapCount = 0;
                }, 300);
            } else if (tapCount === 2) {
                clearTimeout(tapTimer);
                tapCount = 0;
                
                // Create heart animation
                createHeartAnimation(e.target);
            }
        });
    });
}

function createHeartAnimation(element) {
    const heart = document.createElement('div');
    heart.innerHTML = '❤️';
    heart.style.cssText = `
        position: absolute;
        font-size: 3rem;
        pointer-events: none;
        z-index: 9999;
        animation: heartFloat 1.5s ease-out forwards;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    `;
    
    element.style.position = 'relative';
    element.appendChild(heart);
    
    setTimeout(() => {
        if (heart.parentNode) {
            heart.parentNode.removeChild(heart);
        }
    }, 1500);
}

// Add heart animation CSS
const heartStyle = document.createElement('style');
heartStyle.textContent = `
    @keyframes heartFloat {
        0% {
            transform: translate(-50%, -50%) scale(0);
            opacity: 1;
        }
        50% {
            transform: translate(-50%, -70%) scale(1.2);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -100%) scale(1);
            opacity: 0;
        }
    }
`;
document.head.appendChild(heartStyle);

// ===== GAMING-STYLE ACHIEVEMENTS =====
function initAchievements() {
    let clickCount = 0;
    let hoverCount = 0;
    
    // Track interactions
    document.addEventListener('click', () => {
        clickCount++;
        checkAchievements();
    });
    
    const interactiveElements = document.querySelectorAll('.trending-card, .deal-card, .review-card');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            hoverCount++;
            checkAchievements();
        });
    });
    
    function checkAchievements() {
        if (clickCount === 10 && !localStorage.getItem('achievement_clicker')) {
            showAchievement('🖱️ Click Master!', 'You clicked 10 times!');
            localStorage.setItem('achievement_clicker', 'true');
        }
        
        if (hoverCount === 5 && !localStorage.getItem('achievement_explorer')) {
            showAchievement('🔍 Explorer!', 'You explored 5 cards!');
            localStorage.setItem('achievement_explorer', 'true');
        }
    }
}

function showAchievement(title, description) {
    const achievement = document.createElement('div');
    achievement.innerHTML = `
        <div class="achievement-content">
            <div class="achievement-title">${title}</div>
            <div class="achievement-desc">${description}</div>
        </div>
    `;
    achievement.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: achievementSlide 3s ease-out forwards;
        max-width: 300px;
    `;
    
    document.body.appendChild(achievement);
    
    setTimeout(() => {
        if (achievement.parentNode) {
            achievement.parentNode.removeChild(achievement);
        }
    }, 3000);
}

// Add achievement animation CSS
const achievementStyle = document.createElement('style');
achievementStyle.textContent = `
    @keyframes achievementSlide {
        0% {
            transform: translateX(100%);
            opacity: 0;
        }
        20% {
            transform: translateX(0);
            opacity: 1;
        }
        80% {
            transform: translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .achievement-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .achievement-desc {
        font-size: 0.9rem;
        opacity: 0.9;
    }
`;
document.head.appendChild(achievementStyle);

// Export functions for global access
window.YouthInteractions = {
    createEmojiExplosion,
    createHeartAnimation,
    showAchievement
};
