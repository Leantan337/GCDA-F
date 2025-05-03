// Engagement tracking functionality
document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Track page views
    trackEngagement('view', {
        path: window.location.pathname,
        title: document.title
    });

    // Track clicks on share buttons
    document.querySelectorAll('.share-button').forEach(button => {
        button.addEventListener('click', function(e) {
            trackEngagement('share', {
                platform: this.dataset.platform,
                url: window.location.href
            });
        });
    });

    // Track downloads
    document.querySelectorAll('.download-link').forEach(link => {
        link.addEventListener('click', function(e) {
            trackEngagement('download', {
                fileType: this.dataset.type,
                fileName: this.dataset.filename
            });
        });
    });

    // Function to send engagement data to server
    function trackEngagement(eventType, metadata = {}) {
        const data = new FormData();
        data.append('event_type', eventType);
        data.append('page_id', document.body.dataset.pageId || '');
        data.append('content_type', document.body.dataset.contentType || '');
        data.append('object_id', document.body.dataset.objectId || '');
        data.append('metadata', JSON.stringify(metadata));

        fetch('/engagement/track/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: data
        }).catch(console.error); // Silent fail on error
    }
});
