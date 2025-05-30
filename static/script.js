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
    document.getElementById("result1").textContent = data["result"]
}
async function estimateGlicko() {
    let player = parseFloat(document.getElementById("player2").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({player: player})
    });
    const data = await res.json();
    document.getElementById("result").textContent = data["result"]
}
async function getPlaystyle() {
    let player = parseFloat(document.getElementById("player3").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({player: player})
    });
    const data = await res.json();
    document.getElementById("result3").textContent = data["result"]
}
async function getMatchupPlayers() {
    let player = parseFloat(document.getElementById("player4").value);
    let opponent = parseFloat(document.getElementById("opponent4").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({player: player, opponent: opponent})
    });
    const data = await res.json();
    document.getElementById("result4").textContent = data["result"]
}
async function getMatchupStats() {
    let player = parseFloat(document.getElementById("player5").value);
    let apm = parseFloat(document.getElementById("apm5").value);
    let pps = parseFloat(document.getElementById("pps5").value);
    let vs = parseFloat(document.getElementById("vs5").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({player: player, apm: apm, pps: pps, vs: vs})
    });
    const data = await res.json();
    document.getElementById("result5").textContent = data["result"]
}
async function getOpenerCoefficient() {
    let player = parseFloat(document.getElementById("player6").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({player: player})
    });
    const data = await res.json();
    document.getElementById("result6").textContent = data["result"]
}