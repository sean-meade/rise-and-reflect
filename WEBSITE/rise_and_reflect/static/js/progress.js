document.addEventListener("DOMContentLoaded", function () {
    let circleProgress = document.querySelector(".circular-progress");
    let progressValue = document.querySelector(".progress-value");

    let progressStartValue = 0;
    let progressEndValue = 100;
    let speed = 100;

    let progress = setInterval(() => {
      progressStartValue++;

      progressValue.textContent = `${progressStartValue}%`;
      circleProgress.style.background = `conic-gradient(#99b4df ${progressStartValue * 3.6}deg, #ededed 0deg)`;

      if (progressStartValue === progressEndValue) {
        clearInterval(progress);
      }
    }, speed);
  });