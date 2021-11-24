var serverhost = 'http://127.0.0.1:8000';

//Creates context menu in right click menu and listener
chrome.runtime.onInstalled.addListener( function( ) {
    chrome.contextMenus.create( {
        id: 'Main',
        title: 'Streamline Table',
        contexts: [ 'all' ],
		
    } );
} );



//Listener to the click of the context menu, add function
chrome.contextMenus.onClicked.addListener( (info,tab) => {
	

	console.log(document.getSelection().toString())
	console.log( 'context menu clicked' );
	console.log(info)


	//Create URL and page url to give to get_page_data function 
    var url = serverhost + '/streamline/get_page_data/?topic='+ encodeURIComponent(info["pageUrl"]);
			
			//console.log(url);
			
			fetch(url)
			.then(response => response.json())
			.then(response => sendResponse({farewell: response}))
			.catch(error => console.log(error))
				
			return true;  // Will respond asynchronously.
} );


	//Button Listener in the popup menu
	// chrome.runtime.onMessage.addListener(
	// 	function(request, sender, sendResponse) {
		  
			  
	// 		var url = serverhost + '/streamline/get_page_data/?topic='+ encodeURIComponent(info["pageUrl"]);
			
	// 		console.log(url);
			
	// 		//var url = "http://127.0.0.1:8000/wiki/get_wiki_summary/?topic=%22COVID19%22"	
	// 		fetch(url)
	// 		.then(response => response.json())
	// 		.then(response => sendResponse({farewell: response}))
	// 		.catch(error => console.log(error))
				
	// 		return true;  // Will respond asynchronously.
		  
	// });

	