var player;

function onYouTubePlayerAPIReady() {
    
   player = new YT.Player('trailerVideo', {
      events: {
         'onReady': onPlayerReady
      }
   });
}

function onPlayerReady(event) {
    var playButton = document.getElementById("play-button");
    playButton.addEventListener("click", function () {
       player.playVideo();
       console.log('started');
    });
    var pauseButton = document.getElementById("pause-button");
    pauseButton.addEventListener("click", function () {
       player.pauseVideo();
       console.log('paused');
    });
    var stopButton = document.getElementById("stop-button");
    stopButton.addEventListener("click", function () {
       player.stopVideo();
       console.log('stopped');
    });
 }
