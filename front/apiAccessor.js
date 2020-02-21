const APIURL = "http://localhost:3000/";

function api__voice_calc(sound) {
  let url = APIURL + 'voice/calc/1';


  fetch(url, {
    method: 'POST',
    body: sound,
    headers: {
      'Content-Type': 'audio/wav'
    }
  }).then(res => res.json())
    .then(response => {
      console.log('Success:', JSON.stringify(response));
      curScore = response.score;
      document.querySelector("#score").innerHTML = String(curScore).substr(0, 4);
      showSec("result");
      setTimeout(api__rank_post, 1000);
    })
    .catch(error => console.error('Error:', error));
}

function api__rank_post() {
  let name = prompt("君の名は？", "名無しリッツ");
  if (!name) return -1;
  let url = APIURL + 'rank/' + curChar.id;
  let data = {
    name: name,
    score: curScore
  };

  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

function api__rank_get() {
  let url = APIURL + 'rank/' + curChar.id;
  fetch(url)
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      console.log(JSON.stringify(myJson));
      userRanking = myJson.ranks;
      renderRanking();
    }).catch(error => alert('[Error] Connection to Server Failed...\n\n'+ error));
}

