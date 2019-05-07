# -*- coding: UTF-8 -*-
import datetime
import re
import time

import scrapy

tt = """
<!DOCTYPE html>
<html class="">
<head>
<meta charset="GBK" />
<meta name="keywords" content="" />
<meta name="description" content="" />
<meta name="renderer" content="webkit" />
<meta name="force-rendering" content="webkit" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<title>我的账单 - 支付宝</title>


<link rel="icon" href="https://i.alipayobjects.com/common/favicon/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="https://i.alipayobjects.com/common/favicon/favicon.ico" type="image/x-icon" /><link href="https://a.alipayobjects.com" rel="dns-prefetch" />
<link href="https://app.alipay.com" rel="dns-prefetch" />
<link href="https://my.alipay.com" rel="dns-prefetch" />
<link href="https://lab.alipay.com" rel="dns-prefetch" />
<link href="https://cashier.alipay.com" rel="dns-prefetch" />
<link href="https://financeprod.alipay.com" rel="dns-prefetch" />
<link href="https://shenghuo.alipay.com" rel="dns-prefetch" />


<!-- uitpl:/component/trackerTime.vm -->
    <!-- FD:106:alipay/tracker/iconfont.vm:START --><style>
@font-face {
    font-family: "rei";
    src: url("https://i.alipayobjects.com/common/fonts/rei.eot?20150616"); /* IE9 */
    src: url("https://i.alipayobjects.com/common/fonts/rei.eot?20150616#iefix") format("embedded-opentype"), /* IE6-IE8 */
    url("https://i.alipayobjects.com/common/fonts/rei.woff?20150616") format("woff"), /* chrome 6+、firefox 3.6+、Safari5.1+、Opera 11+ */
    url("https://i.alipayobjects.com/common/fonts/rei.ttf?20150616")  format("truetype"), /* chrome、firefox、opera、Safari, Android, iOS 4.2+ */
    url("https://i.alipayobjects.com/common/fonts/rei.svg?20150616#rei") format("svg"); /* iOS 4.1- */
}
.iconfont {
    font-family:"rei";
    font-style: normal;
    font-weight: normal;
    cursor: default;
    -webkit-font-smoothing: antialiased;
}
</style>
<!-- FD:106:alipay/tracker/iconfont.vm:END -->
<script type="text/javascript">
  window._to = { start: new Date() };
</script>

<!-- FD:106:alipay/tracker/monitor.vm:START --><!-- FD:106:alipay/tracker/sai_seer.vm:START --><script type="text/javascript">

!function(n){function o(r){if(t[r])return t[r].exports;var i=t[r]={exports:{},id:r,loaded:!1};return n[r].call(i.exports,i,i.exports,o),i.loaded=!0,i.exports}var t={};return o.m=n,o.c=t,o.p="",o(0)}([function(n,o){"use strict";window.Sai={log:function(){},error:function(){},lost:function(){},off:function(){},on:function(){},_DATAS:[],_EVENTS:[]}}]);

</script>
<!-- FD:106:alipay/tracker/sai_seer.vm:END --><!-- FD:106:alipay/tracker/monitor.vm:END -->
<!-- FD:106:alipay/tracker/seajs.vm:START -->


<!-- monitor 防错代码 -->
<script>
(function(win){
  if(!win.monitor){win.monitor = {};}

  var METHODS = ["lost", "log", "error", "on", "off"];

  for(var i=0,method,l=METHODS.length; i<l; i++){
    method = METHODS[i];
    if("function" !== typeof win.monitor[method]){
      win.monitor[method] = function(){};
    }
  }
})(window);
</script>

<!-- seajs以及插件 -->
<script charset="utf-8" crossorigin="anonymous" id="seajsnode" onerror="window.monitor && monitor.lost && monitor.lost(this.src)" src="https://a.alipayobjects.com:443/??seajs/seajs/2.2.3/sea.js,seajs/seajs-combo/1.0.0/seajs-combo.js,seajs/seajs-style/1.0.2/seajs-style.js,seajs/seajs-log/1.0.0/seajs-log.js,jquery/jquery/1.7.2/jquery.js,gallery/json/1.0.3/json.js,alipay-request/3.0.8/index.js"></script>

<!-- seajs config 配置 -->
<script>
seajs.config({
  alias: {
    '$': 'jquery/jquery/1.7.2/jquery',
    '$-debug': 'jquery/jquery/1.7.2/jquery',

"""
page_sel = scrapy.Selector(text=hong_dun)
# result = page_sel.xpath('//div[contains(@class,"show-content"]//text()').extract()
result = page_sel.xpath(
	'//div[contains(@class, "show-content") and contains(@class, "art-content")]/p[2]/span[2]//text()').extract()
print(len(result), result)
