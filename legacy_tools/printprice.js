var system = require('system');

var page = require('webpage').create();

var code=system.args[1];

var stockURL="http://hq.sinajs.cn/list="+code;

page.open(stockURL, function(status) {
  var split=page.plainText.split("\n");
  split=page.plainText.split(",");
  var price=split[6];
  var percent=split[8];
  if(code.indexOf("sh") !== -1)
  {
    percent=(price-split[2])/split[2]*100;
  } 
  console.log(code + ": " + price + ", " + percent);

  phantom.exit();
});

