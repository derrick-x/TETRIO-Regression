async function statsToGlicko() {
    let apm = parseFloat(document.getElementById("apm1").value);
    let pps = parseFloat(document.getElementById("pps1").value);
    let vs = parseFloat(document.getElementById("vs1").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({apm: apm, pps: pps, vs: vs})
    });
    const data = await res.json();
    document.getElementById("result").textContent = data["result"]
}
async function estimateGlicko() {

}
async function getPlaystyle() {

}
async function getMatchupPlayers() {

}
async function getMatchupStats() {

}
async function getOpenerCoefficient() {

}