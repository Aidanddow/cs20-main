chrome.contextMenus.removeAll();
chrome.contextMenus.create({
      title: "StreamlineTable",
      contexts: ["browser_action"],
      onclick: function() {
        alert('first');
      }
});