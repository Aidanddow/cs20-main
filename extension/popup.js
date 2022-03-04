// Option1 = Enable Preview
check1 = document.getElementById("option1");
check2 = document.getElementById("option2");

check1.addEventListener("click", SaveOption1);
check2.addEventListener("click", SaveOption2);

console.log(check1);
console.log(check2);

function SaveOption1 (){
	if (check1.checked){
		chrome.storage.local.set({"Option1" : '1'}, function(){});
		console.log(0)
	}
	else {
		chrome.storage.local.set({"Option1" : '0'}, function(){});
		console.log(1)
	}
}

function SaveOption2 (){

	if (check1.checked){
		chrome.storage.local.set({"Option2" : '1'}, function(){});
		console.log(0)
	}
	else {
		chrome.storage.local.set({"Option2" : '0'}, function(){});
		console.log(1)	
	}
}

function loadOptions (){
	
	chrome.storage.local.get(["Option1", "Option2"], function(data){

		if (data.Option1 == 0){
			check1.checked = false
		}else{
			check1.checked = true
		}

		if (data.Option2 == 0){
			check2.checked = false
		}else{
			check2.checked = true
		}

		document.getElementById("test").innerHTML = data.Option1 + data.Option2
		
	});
};

loadOptions()
