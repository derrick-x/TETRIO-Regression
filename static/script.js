async function statsToGlicko() {
    let apm = parseFloat(document.getElementById("apm1").value);
    let pps = parseFloat(document.getElementById("pps1").value);
    let vs = parseFloat(document.getElementById("vs1").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({function: "statsToGlicko", apm: apm, pps: pps, vs: vs})
    });
    const data = await res.json();
    document.getElementById("result1").textContent = data["result"]
}
async function estimateGlicko() {
    let player = document.getElementById("player2").value;
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({function: "estimateGlicko", player: player.toLowerCase()})
    });
    const data = await res.json();
    document.getElementById("result2").textContent = data["result"]
}
async function getPlaystyle() {
    let player = document.getElementById("player3").value.toLowerCase();
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({function: "getPlaystyle", player: player.toLowerCase()})
    });
    const data = await res.json();
    document.getElementById("result3").textContent = data["result"]
}
async function getMatchupPlayers() {
    let player = document.getElementById("player4").value;
    let opponent = document.getElementById("opponent4").value;
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({function: "getMatchupPlayers", player: player.toLowerCase(), opponent: opponent.toLowerCase()})
    });
    const data = await res.json();
    document.getElementById("result4").textContent = data["result"]
}
async function getMatchupStats() {
    let player = document.getElementById("player5").value;
    let apm = parseFloat(document.getElementById("apm5").value);
    let pps = parseFloat(document.getElementById("pps5").value);
    let vs = parseFloat(document.getElementById("vs5").value);
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({function: "getMatchupStats", player: player.toLowerCase(), apm: apm, pps: pps, vs: vs})
    });
    const data = await res.json();
    document.getElementById("result5").textContent = data["result"]
}
async function getOpenerCoefficient() {
    let player = document.getElementById("player6").value;
    const res = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({function: "getOpenerCoefficient", player: player.toLowerCase()})
    });
    const data = await res.json();
    document.getElementById("result6").textContent = data["result"]
}