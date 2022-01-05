var serverhost = 'http://127.0.0.1:8000';

//Creates context menu in right click menu and listener
chrome.runtime.onInstalled.addListener( function( ) {
    chrome.contextMenus.create( {
        id: 'MainContext',
        title: 'Streamline Table',
        contexts: [ 'all' ],
		
    } );
} );

pageUrl = "string";

//Listener to the click of the context menu, add function
chrome.contextMenus.onClicked.addListener( (info,tab) => {
	
	//get page URl - includes the url for a PDF 
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
		var url = tabs[0].url;

		//debug info
		console.log(document.getSelection().toString())
		console.log('context menu clicked');
		console.log(info)

		console.log("SrcUrl")
		console.log(info.srcUrl)
		console.log(info.mediaType)
		
		//on rightclick information about the object the mouse is on is avaliable 
		//checks if the DOM element is a image, if so them gets the src of the image and passes 
		//it to the views 
		if (info.mediaType == "image"){
			//check if source for image exists
			if (info.srcUrl){
				//creates url with the src of image in it to be collected by the webapp 
				console.log("Image")
				var url = serverhost + '/streamline/get_page_data_image/?topic='+ encodeURIComponent(info["srcUrl"]);

				//console.log("WORKING");

				fetch(url)
				.then(response => response.json())
				.then(response => sendResponse({farewell: response}))
				.catch(error => console.log(error))
					
				
				return true;
			}
		//no way to get dom info from pdf, so checks the url - not checks for imbeded pdfs 
		//dosent check what type of pdf
		}else if (url.includes(".pdf")) {

			console.log("PDF Page")
			var url = serverhost + '/streamline/get_page_data_pdf/?topic='+ encodeURIComponent(url);

			fetch(url)
				.then(response => response.json())
				.then(response => sendResponse({farewell: response}))
				.catch(error => console.log(error))

			return true;

		//if not image or pdf doc then checks the html for a table and hands url to 
		//HTML extraction script 
		}else{
			//Create URL and page url to give to get_page_data function 
			var url = serverhost + '/streamline/get_page_data_HTML/?topic='+ encodeURIComponent(info["pageUrl"]);
				
			//console.log(url);
			
			fetch(url)
			.then(response => response.json())
			.then(response => sendResponse({farewell: response}))
			.catch(error => console.log(error))
				
			return true;  // Will respond asynchronously.
		}
	});
	
} );




	