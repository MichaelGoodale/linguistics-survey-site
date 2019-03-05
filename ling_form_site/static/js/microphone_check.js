function get_media_recorder(){
    let mediaRecorder = {};
    navigator.mediaDevices.getUserMedia({audio: true, video: false})
        .then(stream => {
		let button = document.getElementById("survey-start");
		button.disabled = false;
		button.classList.remove('btn-secondary');
		button.classList.add('btn-primary');
        });
}
