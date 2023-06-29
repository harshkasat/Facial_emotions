var player = document.getElementById('player');


document.getElementById("previousButton").addEventListener("click", function() {
  window.location.href = "?page={{ page_obj.previous_number }}";
});

document.getElementById("nextButton").addEventListener("click", function() {
  window.location.href = "?page={{ page_obj.next_page_number }}";
});

function fetch_emotions() {
  $.ajax({
    url: '/get_emotions/',
    success: function(data) {
      // Update the emotion text on the webpage
      $('#emotionText').text(data.result_emotions);

      if (data.result_emotions === "Sad") {
        // if (!isMusicPlaying) {
          playAudio();
          isMusicPlaying = true;
        
      }
    }
  });
}

// Start fetching emotions every 10 seconds
setInterval(fetch_emotions, 1000);

var player = document.getElementById('player');
var playButton = document.getElementById('playButton');
var pauseButton = document.getElementById('pauseButton');
var currentTimeSpan = document.getElementById('currentTime');

// Play the audio
function playAudio() {
  player.play();
}

// Pause the audio
function pauseAudio() {
  player.pause();
}

// Update the current time display
function updateCurrentTime() {
  currentTimeSpan.textContent = formatTime(player.currentTime);
}

// Format time in seconds to hh:mm:ss format
function formatTime(time) {
  var minutes = Math.floor(time / 60);
  var seconds = Math.floor(time % 60);
  var hours = Math.floor(minutes / 60);
  minutes %= 60;

  return (
    (hours > 0 ? hours.toString().padStart(2, '0') + ':' : '') +
    minutes.toString().padStart(2, '0') +
    ':' +
    seconds.toString().padStart(2, '0')
  );
}

// Event listeners for play and pause buttons
playButton.addEventListener('click', playAudio);
pauseButton.addEventListener('click', pauseAudio);

// Update current time every second
setInterval(updateCurrentTime, 1000);
