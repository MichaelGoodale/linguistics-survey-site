is_recording = false;
is_uploading = false;

let mediaRecorder = {};
navigator.mediaDevices.getUserMedia({audio: true, video: false})
    .then(stream => {
	    mediaRecorder = new MediaRecorder(stream);
    });

function upload_file(file, file_id) {
	is_uploading = true;
	const xhr = new XMLHttpRequest();
	const formData = new FormData();
	formData.append("recording", file);
	xhr.open('POST', `http://localhost:5000/upload_audio/${file_id}`);
	xhr.onload = e => is_uploading = false;
	xhr.send(formData);
}

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
		upload_file(buffer, recording);
		is_recording = false;
	}
	mediaRecorder.ondataavailable = function (e) {
		chunks.push(e.data);
	}
}
