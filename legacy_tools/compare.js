var holdStockPage = require('webpage').create();
var soldStockPage = require('webpage').create();
var fs = require('fs');
var system = require('system')

if(system.args.length!==7){
  console.log('Usage: phantomjs <this-script-name> <argRatio> <argOutputFile> <stock-code-current-hold> <the-price-bought-last-time> <stock-code-want-to-buy> <the-price-sold-last-time>');
  phantom.exit(-1);
}

var argRatio=system.args[1];
var argOutputFile=system.args[2];
var argHoldStock=system.args[3];
var argHoldStockOriginPrice=system.args[4];
var argSoldStock=system.args[5];
var argSoldStockOriginPrice=system.args[6];


var holdStockURL="http://hq.sinajs.cn/list="+argHoldStock;
var soldStockURL="http://hq.sinajs.cn/list="+argSoldStock;

var originRatio=argHoldStockOriginPrice/argSoldStockOriginPrice;

holdStockPage.open(holdStockURL, function(status) {
  var split=holdStockPage.plainText.split(",");
  var holdStockPrice=split[3];

  soldStockPage.open(soldStockURL, function(status) {
    var split=soldStockPage.plainText.split(",");
    soldStockPrice=split[3];
    
    if(holdStockPrice/soldStockPrice/originRatio>argRatio){
      // write information to file system
      console.log("holdStockPrice becomes relatively more expensive than soldStockPrice, so, I want to sell one and buy another."+"\nholdStockPrice: "+holdStockPrice+", soldStockPrice: "+soldStockPrice+", holdStockPrice/soldStockPrice/originalRatio: "+String(holdStockPrice/soldStockPrice/originRatio));
      fs.write(argOutputFile, "holdStockPrice becomes relatively more expensive than soldStockPrice, so, I want to sell one and buy another."+"\nholdStockPrice: "+holdStockPrice+", soldStockPrice: "+soldStockPrice+", holdStockPrice/soldStockPrice/originalRatio: "+String(holdStockPrice/soldStockPrice/originRatio));
      phantom.exit(1);
    }
    console.log("holdStockPrice: "+holdStockPrice+", soldStockPrice: "+soldStockPrice+", holdStockPrice/soldStockPrice/originalRatio: "+String(holdStockPrice/soldStockPrice/originRatio)+"\nholdStockPrice has not become relatively more expensive than soldStockPrice, so, I don't take action.");
    phantom.exit();
  });
});

