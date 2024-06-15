console.log('JavaScript loaded!');

// TODO: Add this to the secrets
API_URL = 'http://localhost:5000'

getServerStatus();

function getServerStatus() {

    fetch(API_URL, {
        method: 'GET',
        headers: {
            'Content-Type': 'text/html',
        }
    }).then(response => {
        if (!response.ok) {
            // TODO: Make the buttons uninteractable if the server is not available
            document.getElementById('api-status').innerHTML = "<p>Server Unavailable</p>";
        }
        return response.text();
    }).then(html => {
        // If the server is available, set the status and fetch the top videos
        document.getElementById('api-status').innerHTML = html;
        getTopVideos();
    }).catch(error => {
        // TODO: Make the buttons uninteractable if the server is not available
        document.getElementById('api-status').innerHTML = "<p>Server Unavailable</p>";
    });
}

function getTopVideos() {
    fetch(`${API_URL}/top-videos`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);

            // Get the grid to display the videos
            const container = document.getElementById('grid-renderer');

            // Clean the previous HTML content
            container.innerHTML = ''

            // This renders 4 rows of 4 items each
            const numOfRows = 4;
            const itemsPerRow = 4;

            for (let i = 0; i < numOfRows; i++) {
                const gridRow = document.createElement('div');
                gridRow.classList.add('grid-row', 'row');
                container.appendChild(gridRow);

                for (let j = 0; j < itemsPerRow; j++) {
                    const video = data[4*i + j];
                    const videoElement = createVideoElement(video);
                    gridRow.appendChild(videoElement);
                }
            }

        }).catch((error) => {
            console.error('Error:', error);
        });
}

function createVideoElement(video) {
    const div = document.createElement('div');
    div.classList.add('video-item', 'ml-3', 'mr-3', 'mb-3');

    const relativeTime = getRelativeTime(video.date);
    const formattedViews = getFormattedViews(video.views);

    div.innerHTML = `
        <img src="${video.thumbnail}" alt="${video.title}" class="thumbnail">
        <div class="video-info mt-2">
            <div class="d-flex align-items-center">
                <img src="${video.channelIcon}" alt="${video.channel}" class="icon">
                <div>
                    <div class="title">${video.title}</div>
                </div>
            </div>
            <div class="channel">${video.channel}</div>
            <div class="stats d-flex">
                <div class="views">${formattedViews}</div>
                <div class="date">${relativeTime}</div>
            </div>
        </div>
    `;

    return div;
}

function getRelativeTime(date) {
    const now = new Date();
    const past = new Date(date);
    const seconds = Math.floor((now - past) / 1000);

    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) return interval === 1 ? '1 year ago' : `${interval} years ago`;

    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) return interval === 1 ? '1 month ago' : `${interval} months ago`;

    interval = Math.floor(seconds / 86400);
    if (interval >= 1) return interval === 1 ? '1 day ago' : `${interval} days ago`;

    interval = Math.floor(seconds / 3600);
    if (interval >= 1) return interval === 1 ? '1 hour ago' : `${interval} hours ago`;

    interval = Math.floor(seconds / 60);
    if (interval >= 1) return interval === 1 ? '1 minute ago' : `${interval} minutes ago`;

    return 'Just now';
}

function getFormattedViews(views) {
    if (views >= 10000000) {
        views /= 1000000;
        res = Math.round(views);
        return `${res}M views`;
    }
    else if (views >= 1000000) {
        views /= 1000000;
        res = Math.round(views * 10) / 10;
        return `${res}M views`;
    }
    else if (views >= 10000) {
        views /= 1000;
        res = Math.round(views);
        return `${res}K views`;
    }
    else if (views >= 1000) {
        views /= 1000;
        res = Math.round(views * 10) / 10;
        return `${res}K views`;
    }
    else {
        return `${views} views`;
    }
}
