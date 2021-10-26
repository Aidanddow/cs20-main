
check1 = document.getElementById("option1");
check2 = document.getElementById("option2");


check1.addEventListener("click", SaveOption1);
check2.addEventListener("click", SaveOption2);

function test(){
  document.getElementById("test").innerHTML = check2.checked;
}


function SaveOption1 (){
  chrome.storage.sync.set({ "Option1" : check1.checked });
  document.getElementById("test").innerHTML = check1.checked + " check1"
}

function SaveOption2 (){
  chrome.storage.sync.set({ "Option2" : check2.checked }); 
  document.getElementById("test").innerHTML = check2.checked + " check2"
}



function loadOptions (){
  check1.checked = chrome.storage.sync.get({ Option1: false }, function (items) {
    document.getElementById("Option1").checked = items.Option1
    document.getElementById("test").innerHTML = items.Option1
  });

  check2.checked = chrome.storage.local.get("Option2");
  
};

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