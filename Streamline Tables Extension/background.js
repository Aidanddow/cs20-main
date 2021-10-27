
var pluckHandler = function() {
	alert("Clicked");
};

chrome.contextMenus.removeAll();
chrome.contextMenus.create({"title": "Pluck", "contexts":["page"], "onclick": pluckHandler})