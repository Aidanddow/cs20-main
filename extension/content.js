chrome.extension.onMessage.addListener(function (message, sender, response) {


	console.log(message);
	console.log(document.getSelection())
})

console.log("message");

