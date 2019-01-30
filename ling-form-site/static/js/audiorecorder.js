is_recording = false;
let mediaRecorder = {};
navigator.mediaDevices.getUserMedia({audio: true, video: false})
    .then(stream => {
	    mediaRecorder = new MediaRecorder(stream);
    });

function record_audio(recording) {
	if (is_recording) {
		return false;
	}
	if (!(mediaRecorder instanceof MediaRecorder)){
		is_recording = false;
		console.log("Please enable media recorder");
		return false;
	}

	is_recording = true;

	let stop_button = document.getElementById(`stop-${recording}`);
	let chunks = [];
	mediaRecorder.start();
	console.log(`recording:${recording} started`);

	stop_button.onclick = function () {
		mediaRecorder.stop()
	}

	mediaRecorder.onstop = function(e) {
		console.log(`recording:${recording} stopped`);
		const buffer = new Blob(chunks);
		const objectURL = window.URL.createObjectURL(buffer);
		let file_object = document.getElementById(recording);
		is_recording = false;
	}
	mediaRecorder.ondataavailable = function (e) {
		chunks.push(e.data);
	}

}



