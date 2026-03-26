// profile.js - Complete JavaScript, jQuery, and AJAX implementation
// For WAD2 Project - Demonstrates JavaScript, jQuery, and AJAX functionality

$(document).ready(function() {
    console.log("🚀 Profile page loaded with JavaScript, jQuery, and AJAX");
    
    // Initialize all features
    initProfileFeatures();
    loadActivityFeed();
    loadRecommendations();
    setupAJAXHandlers();
    setupjQueryEffects();
});

// ============= 1. jQuery Initialization & Effects =============
function initProfileFeatures() {
    // Animated counter on page load
    $('.stat-number').each(function() {
        const $this = $(this);
        const countTo = parseInt($this.text());
        
        $({ countNum: 0 }).animate({
            countNum: countTo
        }, {
            duration: 1000,
            easing: 'swing',
            step: function() {
                $this.text(Math.floor(this.countNum));
            },
            complete: function() {
                $this.text(countTo);
            }
        });
    });
    
    // Fade in content
    $('.profile-content').hide().fadeIn(800);
    
    // Tooltip effect
    $('.stat').each(function() {
        const label = $(this).find('.stat-label').text();
        $(this).attr('title', `Click to view ${label}`);
    });
    
    // Add hover animation to cards
    $('.analytics-card, .recommendation-item').hover(
        function() {
            $(this).css('transform', 'translateY(-5px)');
        },
        function() {
            $(this).css('transform', 'translateY(0)');
        }
    );
}

// ============= 2. AJAX: Load Activity Feed =============
function loadActivityFeed() {
    $.ajax({
        url: '/api/user/activity/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function() {
            $('#activity-list').html('<div class="loading-spinner"></div><p>Loading activity...</p>');
        },
        success: function(data) {
            const activityList = $('#activity-list');
            activityList.empty();
            
            if (data.activities && data.activities.length > 0) {
                $.each(data.activities.slice(0, 10), function(index, activity) {
                    const activityHtml = `
                        <div class="activity-item fade-in">
                            <div class="activity-icon">${getActivityIcon(activity.type)}</div>
                            <div class="activity-details">
                                <p><strong>${escapeHtml(activity.user)}</strong> ${activity.description}</p>
                                <div class="activity-time">${activity.time_ago}</div>
                            </div>
                        </div>
                    `;
                    activityList.append(activityHtml);
                });
            } else {
                activityList.html(`
                    <div class="empty-state">
                        <p>📭 No recent activity yet</p>
                        <small>Start interacting with songs and artists!</small>
                    </div>
                `);
            }
        },
        error: function(xhr) {
            console.error('Error loading activity:', xhr);
            $('#activity-list').html(`
                <div class="empty-state">
                    <p>⚠️ Unable to load activity</p>
                    <small>Please refresh the page</small>
                </div>
            `);
        }
    });
}

// ============= 3. AJAX: Load Recommendations =============
function loadRecommendations() {
    $.ajax({
        url: '/api/recommendations/',
        method: 'GET',
        dataType: 'json',
        beforeSend: function() {
            $('#recommendations-list').html('<div class="loading-spinner"></div><p>Finding recommendations...</p>');
        },
        success: function(data) {
            const recommendationsList = $('#recommendations-list');
            recommendationsList.empty();
            
            if (data.recommendations && data.recommendations.length > 0) {
                $.each(data.recommendations.slice(0, 6), function(index, song) {
                    const songHtml = `
                        <div class="recommendation-item" data-song-id="${song.id}">
                            <div class="recommendation-info">
                                <h4>🎵 ${escapeHtml(song.title)}</h4>
                                <p>🎤 ${escapeHtml(song.artist)}</p>
                                <div class="recommendation-stats">
                                    <span>❤️ ${song.like_count}</span>
                                    <span>🎧 ${song.view_count} plays</span>
                                </div>
                            </div>
                            <audio controls preload="none">
                                <source src="/stream/${song.id}/" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                            <button class="like-song-btn" data-song-id="${song.id}">
                                ❤️ <span class="like-count">${song.like_count}</span>
                            </button>
                        </div>
                    `;
                    recommendationsList.append(songHtml);
                });
                
                // Attach event handlers to dynamically loaded content
                $('.like-song-btn').off('click').on('click', function() {
                    const songId = $(this).data('song-id');
                    likeSong(songId);
                });
            } else {
                recommendationsList.html(`
                    <div class="empty-state">
                        <p>🎧 No recommendations available</p>
                        <small>Follow more artists to get personalized recommendations!</small>
                    </div>
                `);
            }
        },
        error: function() {
            $('#recommendations-list').html(`
                <div class="empty-state">
                    <p>⚠️ Unable to load recommendations</p>
                </div>
            `);
        }
    });
}

// ============= 4. AJAX: Like a Song =============
function likeSong(songId) {
    const $btn = $(`.like-song-btn[data-song-id="${songId}"]`);
    $btn.prop('disabled', true);
    
    $.ajax({
        url: `/api/song/${songId}/like/`,
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(data) {
            const likeCount = $btn.find('.like-count');
            if (data.is_liked) {
                $btn.addClass('liked');
                likeCount.text(data.like_count);
                showNotification('❤️ Song added to your likes!', 'success');
                
                // Add to activity feed
                addActivityToFeed('You liked a song');
            } else {
                $btn.removeClass('liked');
                likeCount.text(data.like_count);
                showNotification('💔 Removed from your likes', 'info');
            }
            
            // Animate the button
            $btn.addClass('pulse');
            setTimeout(() => $btn.removeClass('pulse'), 300);
        },
        error: function(xhr) {
            if (xhr.status === 401) {
                showNotification('Please login to like songs', 'error');
                setTimeout(() => window.location.href = '/signin/', 1500);
            } else {
                showNotification('Error liking song', 'error');
            }
        },
        complete: function() {
            $btn.prop('disabled', false);
        }
    });
}

// ============= 5. AJAX: Follow/Unfollow User =============
function toggleFollow(username) {
    const $btn = $(`.follow-btn`);
    $btn.prop('disabled', true);
    
    $.ajax({
        url: `/api/follow/${username}/`,
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(data) {
            if (data.is_following) {
                $btn.text('Following').addClass('following');
                showNotification(`✅ You are now following ${username}!`, 'success');
            } else {
                $btn.text('Follow').removeClass('following');
                showNotification(`👋 You unfollowed ${username}`, 'info');
            }
            $('#follower-count').text(data.follower_count);
            
            // Animate the count
            $('#follower-count').addClass('pulse');
            setTimeout(() => $('#follower-count').removeClass('pulse'), 300);
        },
        error: function() {
            showNotification('Error following user', 'error');
        },
        complete: function() {
            $btn.prop('disabled', false);
        }
    });
}

// ============= 6. AJAX: Increment Profile Views =============
function incrementProfileView() {
    $.ajax({
        url: '/api/profile/view/',
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(data) {
            $('#profile-views').text(data.view_count);
        }
    });
}

// ============= 7. jQuery: Color Picker Effect =============
function setupColorPicker() {
    $('#color-picker').on('change', function() {
        const color = $(this).val();
        $('.profile-header').css('background', `linear-gradient(135deg, ${color} 0%, #764ba2 100%)`);
        showNotification('🎨 Theme color updated!', 'success');
        
        // Save preference
        localStorage.setItem('profileThemeColor', color);
    });
    
    // Load saved color
    const savedColor = localStorage.getItem('profileThemeColor');
    if (savedColor) {
        $('#color-picker').val(savedColor);
        $('.profile-header').css('background', `linear-gradient(135deg, ${savedColor} 0%, #764ba2 100%)`);
    }
}

// ============= 8. jQuery: Dark Mode Toggle =============
function setupDarkMode() {
    $('#dark-mode-toggle').on('click', function() {
        $('body').toggleClass('dark-mode');
        
        const isDark = $('body').hasClass('dark-mode');
        $(this).html(isDark ? '☀️ Light Mode' : '🌙 Dark Mode');
        
        showNotification(isDark ? '🌙 Dark mode activated!' : '☀️ Light mode activated!', 'info');
        
        // Save preference via AJAX
        $.ajax({
            url: '/api/preferences/darkmode/',
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: JSON.stringify({ enabled: isDark }),
            contentType: 'application/json'
        });
    });
    
    // Check for saved preference
    $.ajax({
        url: '/api/preferences/darkmode/',
        method: 'GET',
        success: function(data) {
            if (data.enabled) {
                $('body').addClass('dark-mode');
                $('#dark-mode-toggle').html('☀️ Light Mode');
            }
        }
    });
}

// ============= 9. jQuery: Live Search =============
function setupSearch() {
    let searchTimeout;
    
    $('#profile-search').on('input', function() {
        const query = $(this).val();
        clearTimeout(searchTimeout);
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => {
                $.ajax({
                    url: '/api/search/',
                    method: 'GET',
                    data: { q: query, type: 'songs' },
                    success: function(data) {
                        const results = $('#search-results');
                        results.empty().show();
                        
                        if (data.results && data.results.length > 0) {
                            $.each(data.results.slice(0, 5), function(index, song) {
                                results.append(`
                                    <div class="search-result" data-song-id="${song.id}">
                                        <strong>🎵 ${escapeHtml(song.title)}</strong><br>
                                        <small>by ${escapeHtml(song.artist)}</small>
                                    </div>
                                `);
                            });
                            
                            // Click handler for search results
                            $('.search-result').off('click').on('click', function() {
                                const songId = $(this).data('song-id');
                                window.location.href = `/stream/${songId}/`;
                            });
                        } else {
                            results.html('<div class="search-result">No results found</div>');
                        }
                    }
                });
            }, 300);
        } else {
            $('#search-results').hide();
        }
    });
    
    // Hide results when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.search-container').length) {
            $('#search-results').hide();
        }
    });
}

// ============= 10. AJAX: Share Profile =============
function setupShareButton() {
    $('#share-profile-btn').on('click', function() {
        const profileUrl = window.location.href;
        
        // Copy to clipboard
        navigator.clipboard.writeText(profileUrl).then(() => {
            showNotification('📋 Profile link copied to clipboard!', 'success');
            
            // Track share via AJAX
            $.ajax({
                url: '/api/share/profile/',
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                data: JSON.stringify({ url: profileUrl }),
                contentType: 'application/json'
            });
        }).catch(() => {
            showNotification('Unable to copy link', 'error');
        });
    });
}

// ============= 11. AJAX: Like Page =============
function setupLikePage() {
    let pageLikes = parseInt($('#page-likes-count').text()) || 0;
    
    $('#like-page-btn').on('click', function() {
        const $btn = $(this);
        $btn.prop('disabled', true);
        
        $.ajax({
            url: '/api/page/like/',
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(data) {
                pageLikes = data.like_count;
                $('#page-likes-count').text(pageLikes);
                $btn.html(`❤️ ${pageLikes} Likes`);
                
                // Animate
                $btn.addClass('pulse');
                setTimeout(() => $btn.removeClass('pulse'), 300);
                
                showNotification('Thanks for liking this page!', 'success');
            },
            error: function() {
                showNotification('Please login to like pages', 'error');
            },
            complete: function() {
                $btn.prop('disabled', false);
            }
        });
    });
}

// ============= 12. jQuery: Modal Popup =============
function setupModal() {
    $('#edit-profile-btn').on('click', function() {
        $('#edit-profile-modal').fadeIn(300);
    });
    
    $('.close-modal, .modal').on('click', function(e) {
        if ($(e.target).hasClass('modal') || $(e.target).hasClass('close-modal')) {
            $('#edit-profile-modal').fadeOut(300);
        }
    });
}

// ============= 13. AJAX: Save Profile Changes =============
function setupProfileSave() {
    $('#edit-profile-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const $btn = $(this).find('button[type="submit"]');
        $btn.prop('disabled', true).html('<span class="loading-spinner"></span> Saving...');
        
        $.ajax({
            url: '/api/profile/update/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function(data) {
                showNotification('✅ Profile updated successfully!', 'success');
                setTimeout(() => location.reload(), 1500);
            },
            error: function() {
                showNotification('Error updating profile', 'error');
            },
            complete: function() {
                $btn.prop('disabled', false).html('Save Changes');
            }
        });
    });
}

// ============= 14. jQuery: Infinite Scroll =============
let activityPage = 1;
let loading = false;
let hasMore = true;

function setupInfiniteScroll() {
    $(window).on('scroll', function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            if (!loading && hasMore) {
                loadMoreActivity();
            }
        }
    });
}

function loadMoreActivity() {
    loading = true;
    activityPage++;
    
    $.ajax({
        url: `/api/user/activity/?page=${activityPage}`,
        method: 'GET',
        success: function(data) {
            if (data.activities && data.activities.length > 0) {
                $.each(data.activities, function(index, activity) {
                    const activityHtml = `
                        <div class="activity-item fade-in">
                            <div class="activity-icon">${getActivityIcon(activity.type)}</div>
                            <div class="activity-details">
                                <p>${escapeHtml(activity.description)}</p>
                                <div class="activity-time">${activity.time_ago}</div>
                            </div>
                        </div>
                    `;
                    $('#activity-list').append(activityHtml);
                });
            } else {
                hasMore = false;
            }
        },
        complete: function() {
            loading = false;
        }
    });
}

// ============= Setup All AJAX Handlers =============
function setupAJAXHandlers() {
    // Setup all AJAX features
    setupColorPicker();
    setupDarkMode();
    setupSearch();
    setupShareButton();
    setupLikePage();
    setupModal();
    setupProfileSave();
    setupInfiniteScroll();
}

// ============= Setup jQuery Effects =============
function setupjQueryEffects() {
    // Smooth scroll for anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.hash);
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 500);
        }
    });
    
    // Tooltip effect on hover
    $('[data-tooltip]').hover(
        function() {
            const tooltip = $(this).data('tooltip');
            $('<div class="custom-tooltip">' + tooltip + '</div>')
                .appendTo('body')
                .css({
                    position: 'absolute',
                    top: $(this).offset().top - 30,
                    left: $(this).offset().left,
                    background: '#333',
                    color: '#fff',
                    padding: '5px 10px',
                    borderRadius: '5px',
                    fontSize: '12px',
                    zIndex: 1000
                })
                .fadeIn();
        },
        function() {
            $('.custom-tooltip').remove();
        }
    );
}

// ============= Helper Functions =============

function addActivityToFeed(description) {
    const activityHtml = `
        <div class="activity-item fade-in">
            <div class="activity-icon">✨</div>
            <div class="activity-details">
                <p>${escapeHtml(description)}</p>
                <div class="activity-time">just now</div>
            </div>
        </div>
    `;
    $('#activity-list').prepend(activityHtml);
}

function getActivityIcon(type) {
    const icons = {
        'like': '❤️',
        'comment': '💬',
        'follow': '👥',
        'upload': '🎵',
        'share': '📤',
        'view': '👁️'
    };
    return icons[type] || '📝';
}

function showNotification(message, type = 'info') {
    const notification = $(`
        <div class="notification notification-${type}">
            ${message}
            <button class="notification-close">&times;</button>
        </div>
    `);
    
    $('body').append(notification);
    notification.fadeIn(300);
    
    notification.find('.notification-close').on('click', function() {
        notification.fadeOut(300, () => notification.remove());
    });
    
    setTimeout(() => {
        notification.fadeOut(300, () => notification.remove());
    }, 3000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}