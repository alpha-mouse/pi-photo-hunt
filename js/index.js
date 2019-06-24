(function () {
	attachHandler('start-capture', startCapture);
	attachHandler('stop-capture', stopCapture);
	attachHandler('start-autopilot', startAutopilot);
	attachHandler('stop-autopilot', stopAutopilot);
	setInterval(updateStatus, 2000);
	return;

	function attachHandler(elementId, handler) {
		var element = document.getElementById(elementId);
		element.addEventListener('click', handler);
	}

	function updateStatus() {
		get('/status', function (response) {
			document.getElementById('server-status').innerHTML = response ? 'is fine': 'not responding';
			if (response) {
				var photosCount = response.photosCount;
				document.getElementById('photos-count').innerHTML = photosCount;
				document.getElementById('last-photo-link').href = '/photos/' + photosCount;
				document.getElementById('last-photo-text').innerHTML = photosCount;
				document.getElementById('is-capturing').innerHTML = response.isCapturing ? 'on' : 'off';
				document.getElementById('is-autopiloting').innerHTML = response.isAutopiloting ? 'on' : 'off';
				document.getElementById('vision-latency').innerHTML = response.latency;
				if (response.objects.length)
					document.getElementById('most-probable').innerHTML = response.objects[0].probability;
			}
		});
	}

	function startCapture() {
		post('/start-capture');
	}

	function stopCapture() {
		post('/stop-capture');
	}

	function startAutopilot() {
		post('/start-autopilot');
	}

	function stopAutopilot() {
		post('/stop-autopilot');
	}

	function post(url) {
		var request = new XMLHttpRequest();
		request.open('POST', url);
		request.send();
	}

	function get(url, callback) {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function () {
			if (request.readyState == XMLHttpRequest.DONE) {
				var isFine = request.responseText && 200 <= request.status && request.status < 300;
				callback(isFine ? JSON.parse(request.responseText) : null);
			}
		}
		request.open('GET', url);
		request.send(null);
	}
})();