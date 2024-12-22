// Check if the user has a preferred theme stored
const currentTheme = localStorage.getItem('theme') || 'dark-mode';
document.body.classList.add(currentTheme);

// Theme toggle button event listener
const toggleButton = document.getElementById('theme-toggle');
toggleButton.addEventListener('click', () => {
    if (document.body.classList.contains('dark-mode')) {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
        localStorage.setItem('theme', 'light-mode'); // Store user's preference
    } else {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark-mode'); // Store user's preference
    }
});

setInterval(function(){ 
    axios.get('/suggestions')
    .then(function (response) {
        const myNode = document.getElementById("sugg-content");
        myNode.textContent = ''; // Clear previous suggestions

        response.data.forEach(function(suggestion) {
            var item = document.createElement('li');
            // Wrap each suggestion in a <kbd> tag
            item.innerHTML = `<kbd>${suggestion}</kbd>`;
            document.getElementById('sugg-content').appendChild(item);
        });
    })
    .catch(function (error) {
        console.log(error);
    });
}, 1000);

setInterval(function(){ 
    axios.get('/sentence')
    .then(function (response) {
        console.log(response.data)
        document.getElementById("sugg-sentence").textContent = response.data;
    })
    .catch(function (error) {
        console.log(error);
    });
}, 1000);

document.body.onkeyup = function(e){
    if(e.keyCode == 13){
        axios.get('/trigger')
        .then(function (response) {
            console.log(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    else if(e.keyCode == 32){
        axios.get('/char?character=space')
        .then(function (response) {
            console.log(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    else if(e.keyCode >= 49 && e.keyCode <= 53){
        axios.get(`/char?character=${e.keyCode - 48}`)
        .then(function (response) {
            console.log(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
    }
}
function tts() {
    // Get the text to speak from the element
    var text = document.getElementById("sugg-sentence").innerHTML;

    // Create a new SpeechSynthesisUtterance instance
    var speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'en-US';

    // Get the button elements
    var speakBtn = document.getElementById('speak-btn');
    var loadingBtn = document.getElementById('loading-btn');
    
    // Show the loading button and hide the TTS button
    speakBtn.classList.add('hidden');
    loadingBtn.classList.remove('hidden');
    loadingBtn.disabled = true;  // Disable the button while speaking

    // Set an event listener to know when the speech has ended
    speech.onend = function() {
        // Hide the loading button and restore the original speak button
        loadingBtn.classList.add('hidden');
        speakBtn.classList.remove('hidden');
        speakBtn.disabled = false;
    };

    // Start the TTS process
    window.speechSynthesis.speak(speech);
}

