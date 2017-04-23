(function() {
    attachHandler('start-capture', startCapture);
    attachHandler('stop-capture', stopCapture);
    updatePhotosCount();
    return;

    function attachHandler(elementId, handler) {
        var element = document.getElementById(elementId);
        element.addEventListener('click', handler);
    }

    function updatePhotosCount() {
        get('/photos-count', function(count) {
            document.getElementById('photos-count').innerHTML = count;
            document.getElementById('last-photo-link').href = '/photos/' + count;
            document.getElementById('last-photo-text').innerHTML = count;
            setTimeout(updatePhotosCount, 2000);
        });
    }

    function startCapture() {
        post('/start-capture');
    }

    function stopCapture() {
        post('/stop-capture');
    }

    function post(url) {
        var request = new XMLHttpRequest();
        request.open('POST', url);
        request.send();
    }

    function get(url, callback) {
        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (request.readyState == XMLHttpRequest.DONE) {
                callback(request.responseText);
            }
        }
        request.open('GET', url);
        request.send(null);
    }
})();