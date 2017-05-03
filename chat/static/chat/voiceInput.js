/**
 * Created by cerny on 03.05.2017.
 */
// HTML5 Speech Recognition API

function startDictation(onSuccessFunction) {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "cs-CZ";
        recognition.start();
        console.log('Ready to receive command');

        var diagnostic = document.querySelector('.output');
        var cmd = document.querySelector('html');

        recognition.onresult = function (e) {
            var commandReceived = e.results[0][0].transcript;

            document.getElementById('userReply').value
                = commandReceived;
            recognition.stop();

            onSuccessFunction();
            //document.getElementById('userReplyForm').submit(handleSubmit);
        };

        recognition.onerror = function (e) {
            recognition.stop();
        }

    }
}

// hide voice input if not supported
function hideVoiceIfNotSupported(buttonId) {
    if (!window.hasOwnProperty('webkitSpeechRecognition')) {
        hideButton(buttonId);
    }
}

function hideButton(buttonId) {
    $("#"+buttonId).hide();
}

