var powerOn=true;
chrome.storage.sync.set({'power': true}, function() {
});

chrome.browserAction.onClicked.addListener(function(tab) {


  if(powerOn==true){    
    powerOn=false;
    chrome.storage.sync.set({'power': false}, function() {
      chrome.browserAction.setIcon({path:{ "19": "icon1.png"}});
    }); 

}
  else{
    powerOn=true;
    chrome.storage.sync.set({'power': true}, function() {
    chrome.browserAction.setIcon({path:{ "19": "icon.png"}});
    }); 
  }
});

