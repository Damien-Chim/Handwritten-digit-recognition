
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const clearButton = document.getElementById('clear')
const submitButton = document.getElementById('submit')
const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;

canvas.width = parseInt("175px")
canvas.height = parseInt("175px")

let isPainting = false;
let lineWidth = 10;
let startX;
let startY;
let a_values;
const draw = (e) => {
    if(!isPainting) {
        return;
    }

    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';

    ctx.lineTo(e.pageX - canvasOffsetX, e.pageY - canvasOffsetY);
    ctx.stroke();
}

canvas.addEventListener('pointerdown', (e) => {
    isPainting = true;
    startX = e.clientX;
    startY = e.clientY;
});

canvas.addEventListener('pointerup', e => {
    isPainting = false;
    ctx.stroke();
    ctx.beginPath();
});

canvas.addEventListener('pointermove', draw);

clearButton.addEventListener('click', () => {
    clear()
    
})

submitButton.addEventListener('click', () => {
    submit()
    
})


addEventListener("keydown", (event) => {
    if (event.ctrlKey === true && event.key === 'z') {
        clear();
    }
})

addEventListener('keydown', (event) => {
    if (event.ctrlKey === true && event.key === 'q') {
        submit();
    }
})

addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        submit()
    }
})

function clear() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var resultDiv = document.getElementById('displayResultElement');
    resultDiv.innerHTML = "";
    document.getElementById("askForClarification").style.display = 'none';
}

function submit() {
    var scannedImage = ctx.getImageData(0, 0, canvas.width, canvas.height);
    scannedData = scannedImage.data;
    a_values = [];
    for (i = 3; i < scannedData.length; i += 4) {
        a_values.push(scannedData[i] / 255);
    }

    sendDataToPython(a_values);
}

const reportButton = document.getElementById('reportButton')
reportButton.addEventListener('click', () => {
    var trueNumber = window.prompt("What should be the correct number?")
    if (trueNumber != null) {
        sendReportToPython(trueNumber, a_values)
        clear()
    }
    
    
    
})

async function sendDataToPython(a_values) {
    document.getElementById('displayResultElement').innerHTML = "Analysing your handwriting..."
    const url = 'http://localhost:5000/process_data'; // Replace with your server URL
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pixels: a_values }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const jsonResponse = await response.json();
        document.getElementById('displayResultElement').innerHTML = "Prediction: " + jsonResponse.prediction
        document.getElementById('askForClarification').style.display = 'block'

    } catch (error) {
        console.error('Error sending data to Python:', error);
    }
}

async function sendReportToPython(trueNumber, a_values) {
    const url = 'http://localhost:5000/user_reports'; // Replace with your server URL
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({actualNumber: trueNumber, pixels: a_values }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const jsonResponse = await response.json();
        console.log(jsonResponse)
        alert("Your report has been received, thank you!")
        return

    } catch (error) {
        console.error('Error sending data to Python:', error);
    }
}
