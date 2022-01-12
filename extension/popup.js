
check1 = document.getElementById("option1");
check2 = document.getElementById("option2");


check1.addEventListener("click", SaveOption1);
check2.addEventListener("click", SaveOption2);


console.log(check1);
console.log(check2);

function SaveOption1 (){
	chrome.storage.local.set({"Option1" : check1.checked}, function(){});
}

function SaveOption2 (){
	chrome.storage.local.set({ "Option2" : check2.checked}, function(){}); 
}


function loadOptions (){

	console.log("check1");
	console.log("check2");

	
	chrome.storage.local.get(["urlpass"], function(data){
		document.getElementById("test").innerHTML = data.urlpass;
	})
	

	chrome.storage.local.get(["Option1", "Option2"], function(data){
		check1.checked = data.Option1;
		check2.checked = data.Option2;
	});
};



loadOptions()

// $(function(){
// 	//on button click
//     $('#keywordsubmit').click(function(){
// 		chrome.tabs.query({
// 			active: true,
// 			currentWindow: true
// 		}, function(tabs) {
// 			var search_topic = tabs[0].url;

// 			if (search_topic){
// 					//send event to background.js listener with topic aka URL
// 					chrome.runtime.sendMessage(
// 						{topic: search_topic},
// 						function(response) {
// 							result = response.farewell;
// 							//alert(result.summary);
							
							
// 						});
// 			}
// 		});	
//     });
// });