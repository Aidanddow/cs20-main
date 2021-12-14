


$(function(){
	//on button click
    $('#keywordsubmit').click(function(){
		chrome.tabs.query({
			active: true,
			currentWindow: true
		}, function(tabs) {
			var search_topic = tabs[0].url;

			if (search_topic){
					//send event to background.js listener with topic aka URL
					chrome.runtime.sendMessage(
						{topic: search_topic},
						function(response) {
							result = response.farewell;
							//alert(result.summary);
							
							
						});
			}
		});	
    });
});