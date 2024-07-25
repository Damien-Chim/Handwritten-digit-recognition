
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const clearButton = document.getElementById('clear')
const submitButton = document.getElementById('submit')
const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;

console.log(`x: ${canvasOffsetX}`)
console.log(`y: ${canvasOffsetY}`)
// canvas.width = window.innerWidth - canvasOffsetX;
// canvas.height = window.innerHeight - canvasOffsetY;

canvas.width = parseInt("150px")
canvas.height = parseInt("150px")

let isPainting = false;
let lineWidth = 10;
let startX;
let startY;

// toolbar.addEventListener('click', e => {
//     if (e.target.id === 'clear') {
//         ctx.clearRect(0, 0, canvas.width, canvas.height);
//     }
// });





// toolbar.addEventListener('change', e => {
//     if(e.target.id === 'stroke') {
//         ctx.strokeStyle = e.target.value;
//     }

//     if(e.target.id === 'lineWidth') {
//         lineWidth = e.target.value;
//     }
    
// });





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
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var resultDiv = document.getElementById('displayResultElement')
    resultDiv.innerHTML = ""
    
})

submitButton.addEventListener('click', () => {
    submit()
    
})


addEventListener("keydown", (event) => {
    if (event.ctrlKey === true && event.key === 'z') {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        var resultDiv = document.getElementById('displayResultElement')
        resultDiv.innerHTML = ""
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

function submit() {
    var scannedImage = ctx.getImageData(0, 0, canvas.width, canvas.height);
    scannedData = scannedImage.data;
    var a_values = [];
    for (i = 3; i < scannedData.length; i += 4) {
        a_values.push(scannedData[i] / 255);
    }
    console.log(a_values);

    // *$*$*$*$*$*$* ENABLE FOR TESTING *$*$*$*$*$*$*
    // label = window.prompt("number you wrote");


    sendDataToPython(a_values);
}

async function sendDataToPython(a_values) {
    document.getElementById('displayResultElement').innerHTML = "Analysing your handwriting..."
    const jsVariable = a_values; // Your JavaScript variable
    const url = 'http://localhost:5000/process_data'; // Replace with your server URL
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pix: jsVariable }),

            // *$*$*$*$*$*$* ENABLE FOR TESTING *$*$*$*$*$*$*
            // body: JSON.stringify({ pix: jsVariable, lab: label }),


        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const jsonResponse = await response.json();
        console.log('Response from Python:', jsonResponse);
        document.getElementById('displayResultElement').innerHTML = "Prediction: " + jsonResponse.prediction

    } catch (error) {
        console.error('Error sending data to Python:', error);
    }
}

