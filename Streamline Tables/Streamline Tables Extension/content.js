chrome.extension.onMessage.addListener(function (message, sender, response) {

	alert("clicked");

	console.log(message);
	console.log(document.getSelection())
})

console.log("message");