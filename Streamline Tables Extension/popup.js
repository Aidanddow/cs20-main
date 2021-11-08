
check1 = document.getElementById("option1");
check2 = document.getElementById("option2");


check1.addEventListener("click", SaveOption1);
check2.addEventListener("click", SaveOption2);


function SaveOption1 (){
	chrome.storage.local.set({"Option1" : check1.checked}, function(){});
}

function SaveOption2 (){
	chrome.storage.local.set({ "Option2" : check2.checked}, function(){}); 
}


function loadOptions (){
	chrome.storage.local.get(['Option1', 'Option2'], function(data){
		check1.checked = data.Option1;
		check2.checked = data.Option2;
	});
};

console.log("THIS IS WORKING");



loadOptions()

//alert(check1.checked)








// var check1 = document.querySelector('input[id="option1]')
// var check2 = document.querySelector("input['id=option2']")

// check1.addEventListener("click", function(e){
//   e.preventDefault();
// });

// check1.addEventListener("click",updateDisplay);

// function updateDisplay() {
 
//   if (check2.checked) {
//     check2.checked = false
//   }else{
//     check2.checked = true
//   }
// }








// // Initialize button with user's preferred color
// let changeColor = document.getElementById("changeColor");

// chrome.storage.sync.get("color", ({ color }) => {
//   changeColor.style.backgroundColor = color;
// });

// // When the button is clicked, inject setPageBackgroundColor into current page
// changeColor.addEventListener("click", async () => {
//     let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
//     chrome.scripting.executeScript({
//       target: { tabId: tab.id },
//       function: setPageBackgroundColor,
//     });
//   });
  
//   // The body of this function will be executed as a content script inside the
//   // current page
//   function setPageBackgroundColor() {
//     chrome.storage.sync.get("color", ({ color }) => {
//       document.body.style.backgroundColor = color;
//     });
//   