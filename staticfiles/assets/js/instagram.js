/**
 * Instagram Posts Enhancement Script
 * Provides carousel functionality, lazy loading, and enhanced UX
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeInstagramPosts();
});

function initializeInstagramPosts() {
    // Initialize carousel functionality
    initializeCarousels();
    
    // Initialize lazy loading
    initializeLazyLoading();
    
    // Initialize error handling
    initializeErrorHandling();
    
    // Initialize accessibility features
    initializeAccessibility();
}

/**
 * Initialize carousel functionality for Instagram posts with multiple images
 */
function initializeCarousels() {
    const carousels = document.querySelectorAll('.instagram-carousel-fallback');
    
    carousels.forEach(carousel => {
        const items = carousel.querySelectorAll('.instagram-carousel-item');
        const indicator = carousel.querySelector('.instagram-carousel-indicator');
        
        if (items.length <= 1) return;
        
        let currentIndex = 0;
        let autoPlayInterval;
        
        // Create navigation dots
        const dotsContainer = document.createElement('div');
        dotsContainer.className = 'instagram-carousel-dots';
        dotsContainer.setAttribute('role', 'tablist');
        dotsContainer.setAttribute('aria-label', 'Instagram post images');
        
        items.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.className = `instagram-carousel-dot ${index === 0 ? 'active' : ''}`;
            dot.setAttribute('role', 'tab');
            dot.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
            dot.setAttribute('aria-label', `Image ${index + 1} of ${items.length}`);
            dot.addEventListener('click', () => goToSlide(index));
            dotsContainer.appendChild(dot);
        });
        
        carousel.appendChild(dotsContainer);
        
        // Navigation functions
        function goToSlide(index) {
            // Remove active class from current item and dot
            items[currentIndex].classList.remove('active');
            dotsContainer.children[currentIndex].classList.remove('active');
            dotsContainer.children[currentIndex].setAttribute('aria-selected', 'false');
            
            // Add active class to new item and dot
            currentIndex = index;
            items[currentIndex].classList.add('active');
            dotsContainer.children[currentIndex].classList.add('active');
            dotsContainer.children[currentIndex].setAttribute('aria-selected', 'true');
            
            // Update indicator
            if (indicator) {
                const countSpan = indicator.querySelector('.carousel-count');
                if (countSpan) {
                    countSpan.textContent = `${currentIndex + 1} of ${items.length} images`;
                }
            }
        }
        
        function nextSlide() {
            const nextIndex = (currentIndex + 1) % items.length;
            goToSlide(nextIndex);
        }
        
        function prevSlide() {
            const prevIndex = (currentIndex - 1 + items.length) % items.length;
            goToSlide(prevIndex);
        }
        
        // Auto-play functionality
        function startAutoPlay() {
            autoPlayInterval = setInterval(nextSlide, 4000);
        }
        
        function stopAutoPlay() {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
        }
        
        // Start auto-play
        startAutoPlay();
        
        // Pause on hover
        carousel.addEventListener('mouseenter', stopAutoPlay);
        carousel.addEventListener('mouseleave', startAutoPlay);
        
        // Pause on focus
        carousel.addEventListener('focusin', stopAutoPlay);
        carousel.addEventListener('focusout', startAutoPlay);
        
        // Keyboard navigation
        carousel.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    prevSlide();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    nextSlide();
                    break;
            }
        });
        
        // Touch/swipe support
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        carousel.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, { passive: true });
        
        carousel.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const minSwipeDistance = 50;
            
            // Only handle horizontal swipes
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    prevSlide();
                } else {
                    nextSlide();
                }
            }
        }
    });
}

/**
 * Initialize lazy loading for Instagram images
 */
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Initialize error handling for failed Instagram embeds
 */
function initializeErrorHandling() {
    // Handle iframe load errors
    const iframes = document.querySelectorAll('.instagram-embed-container iframe');
    
    iframes.forEach(iframe => {
        iframe.addEventListener('error', () => {
            showFallbackContent(iframe.closest('.instagram-post-card'));
        });
        
        // Timeout for slow-loading embeds
        setTimeout(() => {
            if (!iframe.contentDocument && !iframe.contentWindow) {
                showFallbackContent(iframe.closest('.instagram-post-card'));
            }
        }, 10000);
    });
    
    // Handle image load errors
    const images = document.querySelectorAll('.instagram-fallback-image');
    
    images.forEach(img => {
        img.addEventListener('error', () => {
            showImageError(img);
        });
    });
}

/**
 * Show fallback content when embed fails
 */
function showFallbackContent(postCard) {
    if (!postCard) return;
    
    const embedContainer = postCard.querySelector('.instagram-embed-container');
    if (embedContainer) {
        embedContainer.innerHTML = `
            <div class="instagram-error">
                <i class="fab fa-instagram"></i>
                <p>Unable to load Instagram post</p>
                <p><small>Please visit Instagram to view this content</small></p>
            </div>
        `;
    }
}

/**
 * Show error state for failed images
 */
function showImageError(img) {
    const fallbackContainer = img.closest('.instagram-fallback-media');
    if (fallbackContainer) {
        fallbackContainer.innerHTML = `
            <div class="instagram-error">
                <i class="bi bi-image"></i>
                <p>Image unavailable</p>
            </div>
        `;
    }
}

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Add ARIA labels to Instagram links
    const instagramLinks = document.querySelectorAll('.instagram-view-link, .instagram-fallback-link');
    
    instagramLinks.forEach(link => {
        if (!link.getAttribute('aria-label')) {
            link.setAttribute('aria-label', 'View this post on Instagram (opens in new tab)');
        }
    });
    
    // Add keyboard navigation to post cards
    const postCards = document.querySelectorAll('.instagram-post-card');
    
    postCards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'article');
        card.setAttribute('aria-label', 'Instagram post');
        
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                const link = card.querySelector('.instagram-view-link, .instagram-fallback-link');
                if (link) {
                    e.preventDefault();
                    link.click();
                }
            }
        });
    });
}

/**
 * Initialize enhanced "Read More" functionality for Instagram captions
 */
function initializeReadMore() {
    const readMoreButtons = document.querySelectorAll('.read-more-btn');
    
    readMoreButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            
            const captionContent = button.closest('.caption-content');
            if (!captionContent) return;
            
            const truncatedDiv = captionContent.querySelector('.caption-truncated');
            const fullDiv = captionContent.querySelector('.caption-full');
            const isExpanded = button.getAttribute('data-expanded') === 'true';
            
            if (isExpanded) {
                // Collapse
                truncatedDiv.style.display = 'block';
                fullDiv.style.display = 'none';
                button.setAttribute('data-expanded', 'false');
                button.setAttribute('aria-expanded', 'false');
                
                // Update button text based on language
                const lang = document.documentElement.lang || 'en';
                if (lang === 'sq') {
                    button.textContent = 'Lexo më shumë';
                } else if (lang === 'de') {
                    button.textContent = 'Mehr lesen';
                } else {
                    button.textContent = 'Read more';
                }
            } else {
                // Expand
                truncatedDiv.style.display = 'none';
                fullDiv.style.display = 'block';
                button.setAttribute('data-expanded', 'true');
                button.setAttribute('aria-expanded', 'true');
                
                // Update button text based on language
                const lang = document.documentElement.lang || 'en';
                if (lang === 'sq') {
                    button.textContent = 'Lexo më pak';
                } else if (lang === 'de') {
                    button.textContent = 'Weniger lesen';
                } else {
                    button.textContent = 'Read less';
                }
            }
        });
    });
}

/**
 * Initialize retry functionality for unavailable posts
 */
function initializeRetryFunctionality() {
    const retryButtons = document.querySelectorAll('.retry-post-btn');
    
    retryButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            
            const postUrl = button.getAttribute('data-post-url');
            if (!postUrl) return;
            
            // Show loading state
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i> Retrying...';
            button.disabled = true;
            
            try {
                // Make a request to refresh the post
                const response = await fetch('/api/refresh-instagram-post/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify({ post_url: postUrl })
                });
                
                if (response.ok) {
                    // Reload the page to show updated content
                    window.location.reload();
                } else {
                    throw new Error('Failed to refresh post');
                }
            } catch (error) {
                console.error('Error retrying post:', error);
                
                // Show error state briefly
                button.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Failed';
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.disabled = false;
                }, 2000);
            }
        });
    });
}

/**
 * Get CSRF token for AJAX requests
 */
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

// Initialize enhanced functionality after DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeReadMore();
    initializeRetryFunctionality();
});