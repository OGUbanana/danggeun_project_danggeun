function getRandomTemp(min, max) {
    return (Math.random() * (max - min) + min).toFixed(1);
}

function getColor(temperature) {
    if (temperature <= 40) return "#2196F3";
    if (temperature <= 50) return "#4CAF50";
    if (temperature <= 60) return "rgb(255, 208, 0)";
    return "#FF9800";
}
function getSmileImage(temperature) {
    if (temperature <= 40) return "/static/img/smile1.svg";
    if (temperature <= 50) return "/static/img/smile2.svg";
    if (temperature <= 60) return "/static/img/smile3.svg";
    if (temperature <= 70) return "/static/img/smile4.svg";
    return "/static/img/smile5.svg";
}

function updateTemp() {
    const mannerTempElement = document.getElementById('mannerTemp');
    const tempDisplayElement = document.getElementById('temperature');
    const smileImageElement = document.getElementById('smileImage');
    const temperature = getRandomTemp(36.5, 99.9);
    mannerTempElement.style.width = `${temperature}%`;
    const color = getColor(temperature);
    mannerTempElement.style.backgroundColor = color;
    tempDisplayElement.textContent = `${temperature}°C`;
    smileImageElement.src = getSmileImage(temperature);
}

window.onload = updateTemp;
