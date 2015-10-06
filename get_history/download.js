var system = require('system');
var fs = require('fs');
var page = require('webpage').create();

var args = system.args;

// e.g. cn_601318
var code = args[1];

// e.g. 20060101
var start = args[2];

// e.g. 20150831
var end = args[3]

var url = "http://q.stock.sohu.com/hisHq?code=" + code + "&start=" + start + "&end=" + end;
var outputFile = args[4];

page.open(url, function(status) {
    // console.log(page.plainText);  
    fs.write(outputFile,page.plainText);
    phantom.exit();
});

