window.onload = () => {
  const initialSecId = "top";
  showSec(initialSecId);
}
const allSecIds = ["top", "charSelector", "recording", "result", "ranking"];

function hideAllSec() {
  for (let id of allSecIds) {
    document.getElementById(id).style.display = "none";
  }
}

function showSec(id) {
  hideAllSec();
  if(id === "result") updateTwitterLink();
  if(id === "ranking") api__rank_get();
  document.getElementById(id).style.display = "block";
}

