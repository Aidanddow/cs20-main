chrome.runtime.onInstalled.addListener( function( ) {
    chrome.contextMenus.create( {
        id: 'Main',
        title: 'Streamline Table',
        contexts: [ 'all' ]
    } );
} );

chrome.contextMenus.onClicked.addListener( (info,tabs) => {

    console.log( 'context menu clicked' );
    console.log( info );
    console.log( tabs );   
} );