document.addEventListener('DOMContentLoaded', function() {
  const videoGrid = document.getElementById('videoGrid');

  // Fetch stream URLs from the JSON config file asynchronously
  fetch('./config.json')
    .then(response => response.json())
    .then(data => {
      const streams = data.simulation_instances;

      // Function to convert time_of_day to am/pm format
      function formatTime(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        const formattedTime = `${hours % 12 || 12}:${mins < 10 ? '0' : ''}${mins} ${hours < 12 ? 'am' : 'pm'}`;
        return formattedTime;
      }

      // Mapping weather_id to weather description
      const weatherDescriptions = {
        1: 'Sunny',
        2: 'Cloudy',
        3: 'Light Fog',
        4: 'Heavy Fog',
        5: 'Light Rain',
        6: 'Heavy Rain',
        7: 'Light Snow',
        8: 'Heavy Snow',
      };

      // Function to add a stream to the grid
      function addStreamToGrid(stream, index) {
        const streamBox = document.createElement('div');
        streamBox.className = 'stream-box';

        const title = document.createElement('div');
        title.className = 'stream-title';
        const time = formatTime(stream.time_of_day);
        const weather = weatherDescriptions[stream.weather_id];
        const model = stream.model;
        title.textContent = `${weather} - ${time} - ${model}`;
        streamBox.appendChild(title);

        const videoWrapper = document.createElement('div');
        videoWrapper.className = 'video-wrapper';

        const video = document.createElement('video');
        video.controls = true;
        video.autoplay = true;
        video.muted = true;
        video.loop = true;

        videoWrapper.appendChild(video);
        streamBox.appendChild(videoWrapper);
        videoGrid.appendChild(streamBox);

        return {streamBox, video};
      }

      // Create and load the streams
      streams.forEach((stream, index) => {
        const { video } = addStreamToGrid(stream, index);

        fetch(stream.url, { method: 'HEAD' })
          .then(response => {
            if (response.ok) {
              if (Hls.isSupported()) {
                const hls = new Hls();
                hls.attachMedia(video);
                hls.on(Hls.Events.MEDIA_ATTACHED, function () {
                  hls.loadSource(stream.url);
                });
              } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = stream.url;
              }
            }
          })
          .catch(error => console.error(`Error fetching stream ${stream.url}:`, error));
      });
    })
    .catch(error => console.error("Failed to load config.json:", error));
});
