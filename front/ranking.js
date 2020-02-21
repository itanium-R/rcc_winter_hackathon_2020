let userRanking = [];

function renderRanking() {

  let content = `
    <div class="rankingImg">
    <img src="${curChar.imgSrc}"/>
    </div>
    <div class="rankingStr">
    <p>${curChar.charName}</p>
    </div>
    `;

  for (let c of userRanking) {
    content += `
      <div class="userRanking-list">
      <p class="ranking">${c.rank}位</p>
      <p class="name">${c.name}</p>
      <p class="score2">${String(c.score).substr(0, 4)}％</p>
      </div>
    `;
  }

  content += (`<div class="otherRanking-list">`)

  for (let c of chars) {
    if (c.charName == curChar.charName) {
      continue;
    }
    content += (`
      <div class="otherRanking-img">
      <img onclick='curChar=${JSON.stringify(c)}; api__rank_get()' class="rankingImgSrc" src="${c.imgSrc}"/>
      </div>
    `);
  }

  content += (`</div>`);

  document.querySelector("#rankingContent").innerHTML = content;

}

curChar = chars[0];
api__rank_get();