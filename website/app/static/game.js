const question = document.getElementById('question');
const progressText = document.getElementById('progressText');
const scorePercentText = document.getElementById('hud-score-text-percent');
const scorePointsText = document.getElementById('hud-score-text-points');
const progressBarFull = document.getElementById('progressBarFull');

let divID = "";
let currentQuestion = {};
let acceptingAnswers = false;
let symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
let questionCounter = 0;
let score = 0;
let score_percent = 0;
let score_points = 0;

//PASSING DJANGO VALUES
const passQuestions = JSON.parse(document.getElementById('passQuestions').textContent);
const passAnswers = JSON.parse(document.getElementById('passAnswers').textContent);
const passCorrects = JSON.parse(document.getElementById('passCorrects').textContent);
const passID = document.getElementById('passID').textContent;
const timerLimit = document.getElementById('passTimer').textContent*1000;
const passNq = Number(document.getElementById('passNq').textContent);
const passNa = Number(document.getElementById('passNa').textContent);

//Array for random quiz' elements picking
let availableQuesionsIndexes = [];
for (var i=0; i < passNq; ++i) {
  availableQuesionsIndexes.push(i);
}

var timeoutHandle;

const FULL_DASH_ARRAY = 283;
var TIME_LIMIT = timerLimit;

let timePassed = 0;
let timeLeft = TIME_LIMIT;
let timerInterval = null;

const passHighUrl = "/pass_high/"+passID.toString();


function redirectToHigh() {
  window.location.href = 'https://quizgenerator.pythonanywhere.com/highscores';
}

function timeoutStart(time) {
    timeoutHandle = window.setTimeout(getNewQuestion, time);
}

function timeoutClear() {
    clearTimeout(timeoutHandle);
}

function savePlayerHigh() {
    var currentHigh = $.ajax({ type: "GET",
                        url: passHighUrl,
                        async: true, /*false works as well*/
                      }).responseText;
    const nickname = document.getElementById("nickname").value;
    /*const bannedchars = /^[;,/'$" +""xp_""--"]/;  // while regexp /[^/]/   accepts only '/'*/
    const emptyregexp = /^[" +"]/;
    if ( emptyregexp.test( nickname )) {
        document.getElementById("popup-valid-msg").innerHTML = "Too shady";
    } else if (nickname.length <1 || nickname.length > 20) {
        document.getElementById("popup-valid-msg").innerHTML = "1-20 characters";
    } else if (Number(score_points) <= Number(currentHigh) && Number(currentHigh) > 0) { /*  && currentHigh > 0  - let save high=0*/
      document.getElementById("popup-valid-msg").innerHTML = "Current highscore is "+currentHigh;
    }
     else {
        /*console.log(score_points);*/
        $.ajax({
            async: true,
            url: '/save_high',
            data: {
              score_points: score_points,
              score_percent: score_percent,
              forID: passID,
              nickname: nickname,
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            type: 'POST',
            success: function() {
              document.getElementById("popup-valid-msg").style.color =  "rgba(242, 188, 11, 0.8)";
              document.getElementById("popup-valid-msg").innerHTML = "Highscore saved. Redirecting in 2s.";
              setTimeout(redirectToHigh, 2000);
            },
            error: function() {
              document.getElementById("popup-valid-msg").innerHTML = "Error. Please try again.";
            },
        });
    }
};

startGame = () => {
    questionCounter = 0;
    score = 0;
    getNewQuestion();
};

getNewQuestion = () => {
    if (availableQuesionsIndexes.length === 0 || questionCounter >= passNq) {

      var currentHigh = $.ajax({ type: "GET",
      url: passHighUrl,
      async: false,
      }).responseText;

        if(Number(score_points) > Number(currentHigh) && Number(score) <= Number(passNq)) {
          document.querySelector(".popup").style.display = "flex";
          document.getElementById("popup-head").innerHTML = "New highscore!";
          document.getElementById("popup-msg").innerHTML = "Current highscore is " + currentHigh + " points.<br>You have scored " + score_points + " points.";
          document.getElementById("popup-content").style.border = "0.4rem solid rgba(242, 188, 11, 0.3)";
        }
        else {
          document.querySelector(".popup").style.display = "flex";
          document.getElementById("popup-head").innerHTML = "Game over";
          document.getElementById("popup-msg").innerHTML = "You have scored " + score_points + " points. <br> Current highscore is " + currentHigh + " points.";
          document.getElementById("popup-content").style.border = "0.4rem solid rgba(33, 187, 239, 0.3)";
          document.querySelector(".popup").style.display = "flex";
          document.querySelector(".popup-input").style.display = "none";
          document.querySelector(".popup-valid-msg").style.display = "none";
          document.querySelector(".popup-btn").style.display = "none";
        }
    } else {
    /*timeLeft = TIME_LIMIT;
    calculateTimeFraction();*/
    document.getElementById("base-timer-label").innerHTML = formatTime(TIME_LIMIT);
    questionCounter++;
    progressText.innerText = `Question ${questionCounter}/${passNq}`;
    //Update the progress bar
    progressBarFull.style.width = `${(questionCounter / passNq) * 100}%`;
    //Random question picking
    const randIndex = Math.floor(Math.random() * availableQuesionsIndexes.length)
    const questionIndex = availableQuesionsIndexes[randIndex]; //get random question
    currentQuestion = passQuestions[questionIndex];
    whichCorrect = passCorrects[questionIndex]-1;
    availableQuesionsIndexes.splice(randIndex, 1); //splice array to delete picked element
    document.getElementById("question").innerHTML = currentQuestion;
    //concatenate the string to display the answers
    var divText = "";
    for (i=0; i<=passAnswers[questionIndex].length-1; i++) // loop to create the whole html structure of answers
    {
        divID = "divID" + i;
        var insideText = '<div class="choice-prefix">'+symbols[i]+'</div><div class="choice-text">'+passAnswers[questionIndex][i]+'</div>';
        divText = divText + '<div class="choice-container" onclick = "Check('+i+')" id="' + divID +'">'+insideText+'</div>';
    }
    document.getElementById("QA-container").innerHTML = divText; //render answers

    /*console.log("RANDOM = " + String(questionIndex));
    console.log(availableQuesionsIndexes);
    console.log(currentQuestion);
    console.log(passAnswers[questionIndex][whichCorrect]);*/

    //console.log(availableQuesionsIndexes);
    acceptingAnswers = true;

    timeoutStart(timerLimit+10); /*get new querstion after some time + 10ms timer interval overlapping compensation*/
    onTimesUpTimer();
    resetTimer(); //when no answer is selected
    startTimer();
  }
};

function Check(ID){
    if (whichCorrect == ID && acceptingAnswers == true)
    {
        timeoutClear();
        onTimesUpTimer();
        whichDiv = "divID" + ID;
        document.getElementById(whichDiv).style.background = "rgba(40, 167, 69, 0.85)";
        acceptingAnswers = false;
        incrementScore();
        timeoutStart(500);
        resetTimer();
    }
    if (acceptingAnswers == true)
    {
        timeoutClear();
        onTimesUpTimer();
        whichDiv = "divID" + ID;
        whichDivCorr = "divID" + whichCorrect;
        document.getElementById(whichDiv).style.background = "rgba(220, 53, 69, 0.1)";
        document.getElementById(whichDivCorr).style.background = "rgba(40, 167, 69, 0.7)";
        acceptingAnswers = false;
        timeoutStart(700);
        resetTimer();
    }
}

incrementScore = (num) => {
    score += 1;
    score_percent = ((score/passNq)*100).toFixed(1);
    //console.log(score_percent)
    score_points = (Math.sqrt(passNa)*Math.sqrt(passNq)*score_percent).toFixed(0);
    //console.log(score_points)
    scorePercentText.innerText = score_percent +'%';
    scorePointsText.innerText = score_points;
};

/* TIMER */

function onTimesUpTimer() {
  clearInterval(timerInterval);
}

function resetTimer() {
    //clearInterval(timerInterval);
    timePassed = 0;
}

function startTimer() {
  timerInterval = setInterval(() => {
    timePassed = timePassed += 100; //100ms
    timeLeft = TIME_LIMIT - timePassed;
    document.getElementById("base-timer-label").innerHTML = formatTime(timeLeft);
    setCircleDasharray();

    if (timeLeft <= 0) {
      onTimesUpTimer();
    }
  }, 100); //100ms interval
}

function formatTime(time) {
  let seconds = Math.floor(time/1000);
  let secondspart = Math.round((time % 1000)/100); // /100 to leave only 1 digit

  if (secondspart == 10) {
    secondspart = 0;
    seconds = seconds +1;
  }
  //console.log(`${seconds}.${secondspart}`);
  return `${seconds}.${secondspart}`;
}

function calculateTimeFraction() {
  const rawTimeFraction = timeLeft / TIME_LIMIT;
  return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
}

function setCircleDasharray() {
  const circleDasharray = `${(
    calculateTimeFraction() * FULL_DASH_ARRAY
  ).toFixed(0)} 283`;
  document
    .getElementById("base-timer-path-remaining")
    .setAttribute("stroke-dasharray", circleDasharray);
}

//Run the game
startGame();