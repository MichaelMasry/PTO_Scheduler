function sign_in(e) {
	e.preventDefault();
	let name = document.getElementById('nt_name').value;
	localStorage.setItem('user', name);
	console.log(localStorage.getItem('user'));
	let passwd = document.getElementById('nt_password').value;
	console.log(passwd);
	
	console.log("Clicked~!!!!!");
	
	(async () => {
		const rawResponse = await fetch('http://localhost:8080/login', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({'name': name, 'password': passwd})
		});
		const status_ = await rawResponse.json();
		console.log(status_['status_']);
		console.log(status_['isMod']);
		if (status_['status_'] != 0 && status_['status_'] != 500 && status_['isMod'] ==0) {
			console.log("FINE Not MOD");
			openCalenderWindow();
		}else{
			if (status_['status_'] != 1 && status_['status_'] != 500 && status_['isMod'] ==1){
				console.log("FINE MOD");
				openModWindow();
			}else{
				console.log("NOT OK");
			}
		}
	})();
	
	/*var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			res = JSON.stringify(xhr.responseText);
			res2 = res['status'];
			res3 = JSON.parse(res);
			console.log(typeof res);
			console.log(res3);
			console.log(res3['status_']);
			console.log(res3.status_);
		}
	}
	xhr.open("POST", 'http://localhost:8080/login', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	var obj = {"name":name, "password":passwd};
	console.log(obj);
	xhr.send(JSON.stringify({
		"value": obj
	}));
	console.log(xhr.response);*/
	
/*	var xhr = new XMLHttpRequest();
	/*xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
        alert(xhr.responseText);
		}
	}*/
	/*xhr.open('POST', 'http://localhost:8080/login', true);
    //xhr.setRequestHeader('Content-Type', 'application/json');
	var obj = {"name":name, "password":passwd};
	console.log(obj);
	// var jsonString= JSON.stringify(obj);
	/*xhr.send(JSON.stringify({
		"name": name,
		"password": passwd
	}));
	//console.log(jsonString);
	//xhr.send(obj);
	xhr.send(JSON.stringify({
		"value": obj
	}));
	console.log(xhr.responseText);
	
	*/

}

function openCalenderWindow(){
	window.open("./record.html","_self");
}

function openModWindow(){
	window.open("./show.html","_self");
}

function initButtons() {
	document.getElementById('nt_button').addEventListener('click', sign_in);
}

initButtons();
var owner_ = localStorage.getItem('user');
console.log(owner_);
