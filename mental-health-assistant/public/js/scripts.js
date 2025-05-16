document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyze-button');
    const analysisResult = document.getElementById('analysis-result');

    if (analyzeButton && analysisResult) {
        analyzeButton.addEventListener('click', function() {
            analysisResult.textContent = "Analyzing...";

            fetch('http://127.0.0.1:5000/analyze', { // Correct Flask URL
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                analysisResult.textContent = data.result;
            })
            .catch(error => {
                console.error('Error:', error);
                analysisResult.textContent = "Error analyzing emotion.";
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyze-button');
    const videoFeed = document.getElementById('video-feed');

    if (analyzeButton && videoFeed) {
        analyzeButton.addEventListener('click', function() {
            // Set video source to Flask's real-time stream
            videoFeed.src = "http://127.0.0.1:5000/video_feed";
        });
    }
});


