const chars = [
  { id: 1, charName: "大蛇丸", words: "潜影蛇手", imgSrc: "img/orochimaru.png" },
  { id: 4, charName: "悟空", words: "おっすオラ悟空", imgSrc: "img/goku.png" },
  { id: 5, charName: "フリーザ", words: "私の戦闘力は53万です", imgSrc: "img/hreeza.png" },
  { id: 2, charName: "ドラえもん", words: "僕ドラえもん", imgSrc: "img/doraemon.png" },
  { id: 3, charName: "しずかちゃん", words: "のび太さーん", imgSrc: "img/sizukachan.png" },
];
let curChar = "";

for (let c of chars) {
  document.write(`
    <button class="charB" onclick='decideChar(${JSON.stringify(c)});'>
    <div class="bImg">
    <img src="${c.imgSrc}" />
    </div>
    <div class="bStr">
    <p>${c.charName}</p>
    <p class="words">「${c.words}」</p>
    </div>
    </button>
  `);
}

function decideChar(c) {
  curChar = c;
  document.querySelector("#charNameP").innerHTML = c.charName;
  document.querySelector("#wordsP").innerHTML = "「" + c.words + "」";
  showSec('recording');
  renderRanking();
}