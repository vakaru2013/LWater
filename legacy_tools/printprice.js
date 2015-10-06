var system = require('system');

var page = require('webpage').create();

var code=system.args[1];

var stockURL="http://hq.sinajs.cn/list="+code;

page.open(stockURL, function(status) {
  var split=page.plainText.split("\n");
  console.log(split[0]);
  split=page.plainText.split(",");
  var price=split[6];
  console.log(code + ": "+price);
  phantom.exit();
});

