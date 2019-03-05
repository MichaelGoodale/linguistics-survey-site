let is_recording = false;
let is_uploading = false;
let survey_name = "";
let next_buttons = document.getElementsByClassName("submit-page");

let story_chunks = {};

window.onload = () => {
	survey_name = document.getElementById("survey_name").getAttribute('data-survey_name');
}

let mediaRecorder = {};
navigator.mediaDevices.getUserMedia({audio: true, video: false})
    .then(stream => {
	    mediaRecorder = new MediaRecorder(stream);
	    mediaRecorder.mimeType = 'audio/wav'
    });

function upload_file(file, file_id, btn_fn) {
	is_uploading = true;
	btn_fn();
	const xhr = new XMLHttpRequest();
	const formData = new FormData();
	formData.append("recording", file);
	xhr.open('POST', `/upload_audio/${survey_name}/${file_id}`);
	xhr.onload = e => {
		is_uploading = false;
		btn_fn();
		for (let b of next_buttons){
			b.disabled = false;
		}
	}
	xhr.send(formData);
}

function create_word_list(word_list) {
	for (let b of next_buttons){
		b.disabled = true;
	}
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

	let btn_fn = () => {
		if(is_uploading){
			button.value = "Uploading..."
		}else if(is_uploading == false){
			button.value = "Finished uploading!"
		        setTimeout(() => {
				button.disabled = false;
			        button.value = "Re-record"}
				, 3000);
		}
	};

	button.onclick = function () {
		word_times.push(new Date() - begin_time);
		if (current_word_i == words.length -1){
			is_uploading = true;
			document.getElementById(word_list).value = word_times;
			word_span.innerHTML = "Done!"
		        setTimeout(() => mediaRecorder.stop(), 350);
			button.classList.add('btn-primary');
			button.classList.remove('btn-danger');
		        button.disabled = true;
			button.onclick = function() {
				create_word_list(word_list);
			}
		}else{
			current_word_i = current_word_i + 1;
			word_span.innerHTML = words[current_word_i];
		        button.disabled = true;
		        setTimeout(() => button.disabled = false, 250);
		}
	}

	mediaRecorder.onstop = function(e) {
		const buffer = new Blob(chunks, { 'type' : 'audio/wav' });
		upload_file(buffer, word_list, btn_fn);
		is_recording = false;
	}

	mediaRecorder.ondataavailable = function (e) {
		chunks.push(e.data);
	}
}

function stop_record_audio(recording) {
	if (!is_recording) {
		return false;
	}
	is_recording = false;
	mediaRecorder.stop()
	let stop_button = document.getElementById(`${recording}-stop-button`);
	let start_button = document.getElementById(`${recording}-start-button`);
	start_button.classList.remove('btn-danger');
	start_button.classList.add('btn-primary');
	stop_button.classList.remove('btn-danger');
	stop_button.classList.add('btn-primary');
	stop_button.disabled = true;
	let form_field = document.getElementById(`${recording}`);
	form_field.value = "completed";
}

function record_audio(recording) {
	for (let b of next_buttons){
		b.disabled = true;
	}
	if (is_recording) {
		return false;
	}

	if (!(mediaRecorder instanceof MediaRecorder)){
		is_recording = false;
		alert("Please enable media recorder and refresh the page");
		return false;
	}

	is_recording = true;

	let button = document.getElementById(`${recording}-start-button`);
	button.value = "Recording";
	button.disabled = true;
	button.classList.add('btn-danger');
	button.classList.remove('btn-primary');
	let stop_button = document.getElementById(`${recording}-stop-button`);
	stop_button.value = "Finish recording";
	stop_button.classList.remove('btn-primary');
	stop_button.classList.add('btn-danger');
	stop_button.disabled = false;
	story_chunks[recording] = [];
	mediaRecorder.start();
        
	let btn_fn = () =>{
		if(is_uploading){
			stop_button.value = "Uploading..."
		}else if(is_uploading == false){
			stop_button.value = "Finished uploading!"
			button.disabled = false;
		}
	};

	mediaRecorder.onstop = function(e) {
		console.log(`recording:${recording} stopped`);
		const buffer = new Blob(story_chunks[recording], { 'type' : 'audio/wav' });
		upload_file(buffer, recording, btn_fn);
		is_recording = false;
	}

	mediaRecorder.ondataavailable = function (e) {
		story_chunks[recording].push(e.data);
	}
}
