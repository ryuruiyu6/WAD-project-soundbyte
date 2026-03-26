// profile.js - Complete JavaScript, jQuery, and AJAX implementation
// For WAD2 Project - 6 marks worth of interactive features

$(document).ready(function() {
    console.log("Profile page loaded with JavaScript, jQuery, and AJAX");
    
    // ============= 1. AJAX: Update Profile Stats =============
    updateProfileStats();
    
    // ============= 2. AJAX: Load Recent Activity =============
    loadRecentActivity();
    
    // ============= 3. AJAX: Load Recommendations =============
    loadRecommendations();
    
    // ============= 4. jQuery: Animated Counter =============
    animateStatsCounters();
    
    // ============= 5. jQuery: Hover Effects =============
    setupHoverEffects();
    
    // ============= 6. AJAX: Like Page =============
    setupLikeButton();
    
    // ============= 7. jQuery: Dynamic Color Picker =============
    setupColorPicker();
    
    // ============= 8. AJAX: Follow/Unfollow =============
    setupFollowButton();
    
    // ============= 9. jQuery: Modal Popup =============
    setupEditProfileModal();
    
    // ============= 10. AJAX: Save Profile Changes =============
    setupProfileSave();
    
    // ============= 11. jQuery: Infinite Scroll =============
    setupInfiniteScroll();
    
    // ============= 12. AJAX: Search Functionality =============
    setupSearch();
    
    // ============= 13. jQuery: Tooltips =============
    setupTooltips();
    
    // ============= 14. AJAX: Share Profile =============
    setupShareButton();
    
    // ============= 15. jQuery: Dark Mode Toggle =============
    setupDarkMode();
    
    // Increment profile view via AJAX
    incrementProfileView();
});

// ============= Function 1: AJAX to Update Profile Stats =============
function updateProfileStats() {
    $.ajax({
        url: '/api/profile/stats/',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#follower-count').text(data.follower_count);
            $('#following-count').text(data.following_count);
            $('#profile-views').text(data.profile_views);
            
            // jQuery animation for numbers
            $('.stat-number').each(function() {
                $(this).css('opacity', '0').animate({opacity: '1'}, 500);
            });
        },
        error: function() {
            console.log('Error loading profile stats');
        }
    });
}

// ============= Function 2: AJAX to Load Recent Activity =============
function loadRecentActivity() {
    $.ajax({
        url: '/api/user/activity/',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const activityList = $('#activity-list');
            activityList.empty();
            
            if (data.activities && data.activities.length > 0) {
                $.each(data.activities, function(index, activity) {
                    const activityHtml = `
                        <div class="activity-item fade-in">
                            <div class="activity-icon">${getActivityIcon(activity.type)}</div>
                            <div class="activity-details">
                                <p>${escapeHtml(activity.description)}</p>
                                <small class="activity-time">${activity.time_ago}</small>
                            </div>
                        </div>
                    `;
                    activityList.append(activityHtml);
                });
            } else {
                activityList.html('<div class="empty-state"><p>No recent activity yet. Start interacting!</p></div>');
            }
        },
        error: function() {
            $('#activity-list').html('<div class="empty-state"><p>Unable to load activity. Please refresh.</p></div>');
        }
    });
}

// ============= Function 3: AJAX to Load Recommendations =============
function loadRecommendations() {
    $.ajax({
        url: '/api/recommendations/',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const recommendationsList = $('#recommendations-list');
            if (recommendationsList.length) {
                recommendationsList.empty();
                
                if (data.recommendations && data.recommendations.length > 0) {
                    $.each(data.recommendations.slice(0, 5), function(index, song) {
                        const songHtml = `
                            <div class="recommendation-item" data-song-id="${song.id}">
                                <div class="recommendation-info">
                                    <h4>${escapeHtml(song.title)}</h4>
                                    <p>${escapeHtml(song.artist)}</p>
                                    <div class="recommendation-stats">
                                        <span>❤️ ${song.like_count}</span>
                                        <span>🎧 ${song.view_count}</span>
                                    </div>
                                </div>
                                <audio controls>
                                    <source src="/stream/${song.id}/" type="audio/mpeg">
                                </audio>
                                <button class="like-song-btn" data-song-id="${song.id}">
                                    ❤️ <span class="like-count">${song.like_count}</span>
                                </button>
                            </div>
                        `;
                        recommendationsList.append(songHtml);
                    });
                    
                    // jQuery click handler for like buttons
                    $('.like-song-btn').off('click').on('click', function() {
                        const songId = $(this).data('song-id');
                        likeSong(songId);
                    });
                } else {
                    recommendationsList.html('<div class="empty-state"><p>No recommendations available. Follow more artists!</p></div>');
                }
            }
        }
    });
}

// ============= Function 4: jQuery Animated Counters =============
function animateStatsCounters() {
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
}

// ============= Function 5: jQuery Hover Effects =============
function setupHoverEffects() {
    $('.stat').hover(
        function() {
            $(this).css('transform', 'translateY(-5px)');
            $(this).css('transition', 'all 0.3s');
        },
        function() {
            $(this).css('transform', 'translateY(0)');
        }
    );
    
    $('.recommendation-item').hover(
        function() {
            $(this).find('audio').css('opacity', '1');
        },
        function() {
            $(this).find('audio').css('opacity', '0.8');
        }
    );
}

// ============= Function 6: AJAX Like Page =============
let pageLikes = 0;
function setupLikeButton() {
    $('#like-page-btn').on('click', function() {
        const $btn = $(this);
        $btn.prop('disabled', true);
        
        $.ajax({
            url: '/api/page/like/',
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                pageLikes = data.like_count;
                $('#page-likes-count').text(pageLikes);
                $btn.html(`❤️ ${pageLikes} Likes`);
                
                // jQuery animation
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

// ============= Function 7: jQuery Color Picker =============
function setupColorPicker() {
    $('#color-picker').on('change', function() {
        const color = $(this).val();
        $('.profile-header').css('background', `linear-gradient(135deg, ${color} 0%, #764ba2 100%)`);
        showNotification('Theme color updated!', 'success');
    });
}

// ============= Function 8: AJAX Follow/Unfollow =============
function setupFollowButton() {
    $(document).on('click', '#follow-btn', function() {
        const $btn = $(this);
        const username = $btn.data('username');
        const isFollowing = $btn.hasClass('following');
        
        $btn.prop('disabled', true);
        
        $.ajax({
            url: `/api/follow/${username}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                if (data.is_following) {
                    $btn.text('Following').addClass('following');
                    showNotification(`You are now following ${username}!`, 'success');
                } else {
                    $btn.text('Follow').removeClass('following');
                    showNotification(`You unfollowed ${username}`, 'info');
                }
                $('#follower-count').text(data.follower_count);
                
                // jQuery animation
                $btn.addClass('animate');
                setTimeout(() => $btn.removeClass('animate'), 500);
            },
            error: function() {
                showNotification('Error following user', 'error');
            },
            complete: function() {
                $btn.prop('disabled', false);
            }
        });
    });
}

// ============= Function 9: jQuery Modal Popup =============
function setupEditProfileModal() {
    $('#edit-profile-btn').on('click', function() {
        $('#edit-profile-modal').fadeIn(300);
    });
    
    $('.close-modal').on('click', function() {
        $('#edit-profile-modal').fadeOut(300);
    });
    
    $(window).on('click', function(e) {
        if ($(e.target).is('#edit-profile-modal')) {
            $('#edit-profile-modal').fadeOut(300);
        }
    });
}

// ============= Function 10: AJAX Save Profile Changes =============
function setupProfileSave() {
    $('#edit-profile-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const $btn = $(this).find('button[type="submit"]');
        $btn.prop('disabled', true).text('Saving...');
        
        $.ajax({
            url: '/api/profile/update/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                if (data.success) {
                    showNotification('Profile updated successfully!', 'success');
                    setTimeout(() => location.reload(), 1500);
                }
            },
            error: function() {
                showNotification('Error updating profile', 'error');
            },
            complete: function() {
                $btn.prop('disabled', false).text('Save Changes');
            }
        });
    });
}

// ============= Function 11: jQuery Infinite Scroll =============
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
                                <small class="activity-time">${activity.time_ago}</small>
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

// ============= Function 12: AJAX Search =============
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
                                    <div class="search-result">
                                        <strong>${escapeHtml(song.title)}</strong> by ${escapeHtml(song.artist)}
                                    </div>
                                `);
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
    
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.search-container').length) {
            $('#search-results').hide();
        }
    });
}

// ============= Function 13: jQuery Tooltips =============
function setupTooltips() {
    $('.stat').each(function() {
        const label = $(this).find('.stat-label').text();
        $(this).attr('title', `Click to view ${label}`);
    });
    
    $('.stat').tooltipster ? $('.stat').tooltipster() : console.log('Tooltipster not loaded');
}

// ============= Function 14: AJAX Share Profile =============
function setupShareButton() {
    $('#share-profile-btn').on('click', function() {
        const profileUrl = window.location.href;
        
        $.ajax({
            url: '/api/share/profile/',
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: { url: profileUrl },
            success: function(data) {
                showNotification('Profile link copied to clipboard!', 'success');
                navigator.clipboard.writeText(profileUrl);
            }
        });
    });
}

// ============= Function 15: jQuery Dark Mode Toggle =============
function setupDarkMode() {
    $('#dark-mode-toggle').on('click', function() {
        $('body').toggleClass('dark-mode');
        
        const isDark = $('body').hasClass('dark-mode');
        $(this).html(isDark ? '☀️ Light Mode' : '🌙 Dark Mode');
        
        $.ajax({
            url: '/api/preferences/darkmode/',
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: { enabled: isDark }
        });
    });
}

// ============= Helper: Like Song via AJAX =============
function likeSong(songId) {
    const $btn = $(`.like-song-btn[data-song-id="${songId}"]`);
    $btn.prop('disabled', true);
    
    $.ajax({
        url: `/api/song/${songId}/like/`,
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function(data) {
            const likeCount = $btn.find('.like-count');
            if (data.is_liked) {
                $btn.addClass('liked');
                likeCount.text(data.like_count);
                showNotification('Song added to likes!', 'success');
            } else {
                $btn.removeClass('liked');
                likeCount.text(data.like_count);
            }
            
            $btn.addClass('animate');
            setTimeout(() => $btn.removeClass('animate'), 300);
        },
        complete: function() {
            $btn.prop('disabled', false);
        }
    });
}

// ============= Helper: Increment Profile View =============
function incrementProfileView() {
    $.ajax({
        url: '/api/profile/view/',
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function(data) {
            $('#profile-views').text(data.view_count);
        }
    });
}

// ============= Helper: Show Notification =============
function showNotification(message, type) {
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

// ============= Helper: Get Activity Icon =============
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

// ============= Helper: Escape HTML =============
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============= Helper: Get CSRF Token =============
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