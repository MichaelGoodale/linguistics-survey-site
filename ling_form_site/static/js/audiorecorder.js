is_recording = false;
is_uploading = false;
survey_name = "";

window.onload = () => {
	survey_name = document.getElementById("survey_name").getAttribute('data-survey_name');
}

let mediaRecorder = {};
navigator.mediaDevices.getUserMedia({audio: true, video: false})
    .then(stream => {
	    mediaRecorder = new MediaRecorder(stream);
	    mediaRecorder.mimeType = 'audio/wav'
    });

function upload_file(file, file_id) {
	is_uploading = true;
	const xhr = new XMLHttpRequest();
	const formData = new FormData();
	formData.append("recording", file);
	xhr.open('POST', `/upload_audio/${survey_name}/${file_id}`);
	xhr.onload = e => is_uploading = false;
	xhr.send(formData);
}

function create_word_list(word_list) {
	let word_span = document.getElementById(`${word_list}-words`);
	let words = document.getElementById(word_list).dataset.word_list;
	const re = /\'/gi;
	words = JSON.parse(words.replace(re, '"'));

	if (is_recording) {
		return false;
	}

	if (!(mediaRecorder instanceof MediaRecorder)){
		is_recording = false;
		alert("Please enable media recorder and refresh the page");
		return false;
	}

	is_recording = true;

	let button = document.getElementById(`${word_list}-button`);
	button.value = "Next word";
	button.classList.add('btn-danger');
	button.classList.remove('btn-primary');
	let chunks = [];
	mediaRecorder.start();
	
	let current_word_i = 0;
	word_span.innerHTML = words[current_word_i];
	let begin_time = new Date();
	word_times = [0]

	button.onclick = function () {
		word_times.push(new Date() - begin_time);
		if (current_word_i == words.length -1){
			document.getElementById(word_list).value = word_times;
			word_span.innerHTML = "Done!"
			mediaRecorder.stop()
			button.classList.add('btn-primary');
			button.classList.remove('btn-danger');
			button.value = "Re-record";
		        button.disabled = true;
		        setTimeout(() => button.disabled = false, 3000);
			button.onclick = function() {
				create_word_list(word_list);
			}
		}else{
			current_word_i = current_word_i + 1;
			word_span.innerHTML = words[current_word_i];
		}
	}

	mediaRecorder.onstop = function(e) {
		const buffer = new Blob(chunks, { 'type' : 'audio/wav' });
		upload_file(buffer, word_list);
		is_recording = false;
	}

	mediaRecorder.ondataavailable = function (e) {
		chunks.push(e.data);
	}
}

function record_audio(recording) {
	if (is_recording) {
		return false;
	}

	if (!(mediaRecorder instanceof MediaRecorder)){
		is_recording = false;
		alert("Please enable media recorder and refresh the page");
		return false;
	}

	is_recording = true;

	let button = document.getElementById(`${recording}-button`);
	button.value = "Finish recording";
	button.classList.add('btn-danger');
	button.classList.remove('btn-primary');
	let chunks = [];
	mediaRecorder.start();
	

	button.onclick = function () {
		mediaRecorder.stop()
		button.value = "Re-record";
		button.classList.remove('btn-danger');
		button.classList.add('btn-primary');
		button.disabled = true;
		setTimeout(() => button.disabled = false, 3000);
		button.onclick = function() {
			record_audio(recording);
		}
	}

	mediaRecorder.onstop = function(e) {
		console.log(`recording:${recording} stopped`);
		const buffer = new Blob(chunks, { 'type' : 'audio/wav' });
		upload_file(buffer, recording);
		is_recording = false;
	}

	mediaRecorder.ondataavailable = function (e) {
		chunks.push(e.data);
	}
}
