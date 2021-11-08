//importScripts('jquery-3.6.0.js')

//Creates context menu in right click menu and listener
chrome.runtime.onInstalled.addListener( function( ) {
    chrome.contextMenus.create( {
        id: 'Main',
        title: 'Streamline Table',
        contexts: [ 'all' ]
    } );
} );

//Listener to the click of the context menu, add function
chrome.contextMenus.onClicked.addListener( (info,tabs) => {

    console.log( 'context menu clicked' );
    console.log( info );
    console.log( tabs );   
} );

$.ajax({
  type: "POST",
  url: "~/Test.py",
  data: { param: text}
}).done(function( o ) {
  console.log("THIS IS WORKING");
});