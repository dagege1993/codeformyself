# -*- coding: UTF-8 -*-
import scrapy

tt = '''
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="renderer" content="webkit" />
  <meta name="keywords" content="" />
  <meta name="description" content="" />
  <title>我的支付宝 － 支付宝</title>
Thu, 30 Aug 2018 15:33:53 connectionpool.py[line:393] DEBUG http://127.0.0.1:52246 "GET /session/cc8d1cc27d4b548681b083ba57269b0d/source HTTP/1.1" 200 97687
  <link rel="icon" href="https://i.alipayobjects.com/common/favicon/favicon.ico" type="image/x-icon" />
Thu, 30 Aug 2018 15:33:53 remote_connection.py[line:440] DEBUG Finished Request
  <link rel="shortcut icon" href="https://i.alipayobjects.com/common/favicon/favicon.ico" type="image/x-icon" />
  <!--[if lte IE 6]><meta http-equiv="refresh" content="0; url=https://www.alipay.com/x/kill-ie.htm"><![endif]-->
  
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


<link href="https://a.alipayobjects.com" rel="dns-prefetch" />
<link href="https://app.alipay.com" rel="dns-prefetch" />
<link href="https://my.alipay.com" rel="dns-prefetch" />
<link href="https://lab.alipay.com" rel="dns-prefetch" />
<link href="https://cashier.alipay.com" rel="dns-prefetch" />
<link href="https://financeprod.alipay.com" rel="dns-prefetch" />
<link href="https://shenghuo.alipay.com" rel="dns-prefetch" />

<script async="" src="https://gw.alipayobjects.com/os/secjs/ad96ea50-5431-49ab-9122-11b4ec1acf14/personalweb_portal_account.js"></script><script type="text/javascript">
window._to = { start: new Date() };
</script>

<!-- FD:106:alipay/tracker/monitor.vm:START --><!-- FD:106:alipay/tracker/sai_seer.vm:START --><script type="text/javascript">

!function(n){function o(r){if(t[r])return t[r].exports;var i=t[r]={exports:{},id:r,loaded:!1};return n[r].call(i.exports,i,i.exports,o),i.loaded=!0,i.exports}var t={};return o.m=n,o.c=t,o.p="",o(0)}([function(n,o){"use strict";window.Sai={log:function(){},error:function(){},lost:function(){},off:function(){},on:function(){},_DATAS:[],_EVENTS:[]}}]);

</script>
<!-- FD:106:alipay/tracker/sai_seer.vm:END -->
<!-- FD:106:alipay/tracker/monitor.vm:END -->
<!-- FD:106:alipay/tracker/seajs.vm:START -->






<!-- monitor 防错代码 -->
<script>
(function(win){
  if(!win.monitor){win.monitor = {};}

  var METHODS = ["lost", "log", "error", "on", "off"];

  for(var i=0,method,l=METHODS.length; i&lt;l; i++){
    method = METHODS[i];
    if("function" !== typeof win.monitor[method]){
      win.monitor[method] = function(){};
    }
  }
})(window);
</script>

<!-- seajs以及插件 -->
<script charset="utf-8" crossorigin="anonymous" id="seajsnode" onerror="window.monitor &amp;&amp; monitor.lost &amp;&amp; monitor.lost(this.src)" src="https://a.alipayobjects.com/??seajs/seajs/2.2.3/sea.js,seajs/seajs-combo/1.0.0/seajs-combo.js,seajs/seajs-style/1.0.2/seajs-style.js,seajs/seajs-log/1.0.0/seajs-log.js,jquery/jquery/1.7.2/jquery.js,gallery/json/1.0.3/json.js,alipay-request/3.0.8/index.js"></script>

<!-- seajs config 配置 -->
<script>
seajs.config({
  alias: {
    '$': 'jquery/jquery/1.7.2/jquery',
    '$-debug': 'jquery/jquery/1.7.2/jquery',
    'jquery': 'jquery/jquery/1.7.2/jquery',
    'jquery-debug': 'jquery/jquery/1.7.2/jquery-debug',
    'seajs-debug': 'seajs/seajs-debug/1.1.1/seajs-debug'
  },
  crossorigin: function(uri){

    function typeOf(type){
	  return function(object){
	    return Object.prototype.toString.call(object) === '[object ' + type + ']';
	  }
	}
	var isString = typeOf("String");
	var isRegExp = typeOf("RegExp");

	var whitelist = [];

  whitelist.push('https://a.alipayobjects.com/');

	for (var i=0, rule, l=whitelist.length; i&lt;l; i++){
	  rule = whitelist[i];
	  if (
	    (isString(rule) &amp;&amp; uri.indexOf(rule) === 0) ||
	    (isRegExp(rule) &amp;&amp; rule.test(uri))
		) {

	    return "anonymous";
	  }
	}
  },
  vars: {
    locale: 'zh-cn'
  }
});
</script>

<!-- 兼容原有的 plugin-i18n 写法 -->
<!-- https://github.com/seajs/seajs/blob/1.3.1/src/plugins/plugin-i18n.js -->
<script>
seajs.pluginSDK = seajs.pluginSDK || {
  Module: {
    _resolve: function() {}
  },
  config: {
    locale: ''
  }
};
// 干掉载入 plugin-i18n.js，避免 404
seajs.config({
  map: [
	[/^.*\/seajs\/plugin-i18n\.js$/, ''],
	[/^.*\i18n!lang\.js$/, '']
  ]
});
</script>

<!-- 路由旧 ID，解决 seajs.use('select/x.x.x/select') 的历史遗留问题 -->
<script>
(function(){

var JQ = '/jquery/1.7.2/jquery.js';
seajs.cache['https://a.alipayobjects.com/gallery' + JQ] = seajs.cache['https://a.alipayobjects.com/jquery' + JQ];

var GALLERY_MODULES = [
  'async','backbone','coffee','cookie','es5-safe','handlebars','iscroll',
  'jasmine','jasmine-jquery','jquery','jquery-color','json','keymaster',
  'labjs','less','marked','moment','mustache','querystring','raphael',
  'socketio','store','swfobject','underscore','zepto','ztree'
];

var ARALE_MODULES = [
  'autocomplete','base','calendar','class','cookie','dialog','easing',
  'events','iframe-uploader','iframe-shim','messenger','overlay','popup',
  'position','select','switchable','tip','validator','widget'
];

var util = {};
util.indexOf = Array.prototype.indexOf ?
  function(arr, item) {
    return arr.indexOf(item);
  } :
  function(arr, item) {
    for (var i = 0; i &lt; arr.length; i++) {
      if (arr[i] === item) {
        return i;
      }
    }
    return -1;
  };
util.map = Array.prototype.map ?
  function(arr, fn) {
    return arr.map(fn);
  } :
  function(arr, fn) {
    var ret = [];
	for (var i = 0; i &lt; arr.length; i++) {
        ret.push(fn(arr[i], i, arr));
    }
    return ret;
  };

function contains(arr, item) {
  return util.indexOf(arr, item) &gt; -1
}

function map(id) {
  id = id.replace('#', '');

  var parts = id.split('/');
  var len = parts.length;
  var root, name;

  // id = root/name/x.y.z/name
  if (len === 4) {
    root = parts[0];
    name = parts[1];

    // gallery 或 alipay 开头的没有问题
    if (root === 'alipay' || root === 'gallery') {
      return id;
    }

    // arale 开头的
    if (root === 'arale') {
      // 处理 arale/handlebars 的情况
      if (contains(GALLERY_MODULES, name)) {
        return id.replace('arale/', 'gallery/');
      } else {
        return id;
      }
    }
  }
  // id = name/x.y.z/name
  else if (len === 3) {
    name = parts[0]

    // 开头在 GALLERY_MODULES 或 ARALE_MODULES
    if (contains(GALLERY_MODULES, name)) {
      return 'gallery/' + id;
    } else if (contains(ARALE_MODULES, name)) {
      return 'arale/' + id;
    }
  }

  return id;
}

var _use = seajs.use;

seajs.use = function(ids, callback) {
  if (typeof ids === 'string') {
    ids = [ids];
  }

  ids = util.map(ids, function(id) {
    return map(id);
  });

  return _use(ids, callback);
}

})();
</script>
<!-- FD:106:alipay/tracker/seajs.vm:END -->
<!-- FD:106:alipay/tracker/tracker_time.vm:START --><!-- FD:106:alipay/tracker/tracker_time.vm:784:tracker_time.schema:全站 tracker 开关:START --><script charset="utf-8" crossorigin="crossorigin" src="https://a.alipayobjects.com/static/ar/alipay.light.base-1.8.js"></script>


<script type="text/javascript">
if (!window._to) {
  window._to = { start: new Date() };
}
</script>

<script charset="utf-8" src="https://as.alipayobjects.com/??g/component/tracker/2.3.2/index.js,g/component/smartracker/2.0.2/index.js"></script>
<script charset="utf-8" src="https://a.alipayobjects.com/g/utiljs/rd/1.0.2/rd.js"></script>



<script>
  window.Tracker &amp;&amp; Tracker.start &amp;&amp;  Tracker.start();
</script>







<!-- FD:106:alipay/tracker/tracker_time.vm:784:tracker_time.schema:全站 tracker 开关:END -->
<!-- FD:106:alipay/tracker/tracker_time.vm:END -->

<script src="https://a.alipayobjects.com/chair-request/0.1.0/index.js"></script>
<!-- clue-tracker -->
<script type="text/javascript" src="https://g.alicdn.com/dt/tracker/3.4.11/tracker.Tracker.js" crossorigin=""></script>
<script type="text/javascript">
  var ClueTracker = Tracker.noConflict();
  var tracker = new ClueTracker({
    pid: 'personalweb-portal',
  });
  // 监听 window.onerror 事件并打点
  tracker.onGlobalError();
</script>

  <link charset="utf-8" rel="stylesheet" type="text/css" href="https://a.alipayobjects.com/personalweb/app_views_home_html_css-08dd831d08374164471e.css" /><style>@-moz-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-webkit-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-o-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-ms-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}.message-clock-animate{-webkit-animation:spaceboots 5s infinite;-moz-animation:spaceboots 5s infinite;-o-animation:spaceboots 5s infinite;-ms-animation:spaceboots 5s infinite;animation:spaceboots 5s infinite;display:block}.message-clock-animate:hover{-webkit-animation:none;-moz-animation:none;-o-animation:none;-ms-animation:none;animation:none;text-decoration:none}</style><style>@-moz-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-webkit-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-o-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-ms-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}.message-clock-animate{-webkit-animation:spaceboots 5s infinite;-moz-animation:spaceboots 5s infinite;-o-animation:spaceboots 5s infinite;-ms-animation:spaceboots 5s infinite;animation:spaceboots 5s infinite;display:block}.message-clock-animate:hover{-webkit-animation:none;-moz-animation:none;-o-animation:none;-ms-animation:none;animation:none;text-decoration:none}</style><style>@-moz-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-webkit-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-o-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@-ms-keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}@keyframes spaceboots{1%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}2%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}3%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}4%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}5%{-webkit-transform:rotate(8deg);-moz-transform:rotate(8deg);-o-transform:rotate(8deg);-ms-transform:rotate(8deg);transform:rotate(8deg)}6%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}7%{-webkit-transform:rotate(-8deg);-moz-transform:rotate(-8deg);-o-transform:rotate(-8deg);-ms-transform:rotate(-8deg);transform:rotate(-8deg)}8%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}100%{-webkit-transform:rotate(0);-moz-transform:rotate(0);-o-transform:rotate(0);-ms-transform:rotate(0);transform:rotate(0)}}.message-clock-animate{-webkit-animation:spaceboots 5s infinite;-moz-animation:spaceboots 5s infinite;-o-animation:spaceboots 5s infinite;-ms-animation:spaceboots 5s infinite;animation:spaceboots 5s infinite;display:block}.message-clock-animate:hover{-webkit-animation:none;-moz-animation:none;-o-animation:none;-ms-animation:none;animation:none;text-decoration:none}</style><style type="text/css" class="iconStyle">.icon-apps30-10015 {background-position: 0px -0px; }
.icon-apps30-10016 {background-position: 0px -30px; }
.icon-apps30-10017 {background-position: 0px -60px; }
.icon-apps30-10020 {background-position: 0px -90px; }
.icon-apps30-10024 {background-position: 0px -120px; }
.icon-apps30-10053 {background-position: 0px -150px; }
.icon-apps30-10108 {background-position: 0px -180px; }
.icon-apps30-10110 {background-position: 0px -210px; }
.icon-apps30-10120 {background-position: 0px -240px; }
.icon-apps30-10015, .icon-apps30-10016, .icon-apps30-10017, .icon-apps30-10020, .icon-apps30-10024, .icon-apps30-10053, .icon-apps30-10108, .icon-apps30-10110, .icon-apps30-10120 {text-indent: -9999px; background-image: url("https://i.alipayobjects.com/combo32.png?d=apps/30&amp;t=10015,10016,10017,10020,10024,10053,10108,10110,10120");} </style><link charset="utf-8" rel="stylesheet" href="https://gw.alipayobjects.com/os/rmsportal/BAjEiJgLNsuAonLHiOli.css" /></head>
  <!--[if lt IE 7]><body class="ie6 "><![endif]-->
  <!--[if IE 7]><body class="ie7 "><![endif]-->
  <!--[if IE 8]><body class="ie8 "><![endif]-->
  <!--[if IE 9]><body class="ie9 "><![endif]-->
  <!--[if !IE]>--><body><!--<![endif]-->
  


  




  









  



  



  
















  





  





  







<!-- FD:231:alipay/nav/navSwitch.vm:START --><!-- FD:231:alipay/nav/navSwitch.vm:1740:nav/navSwitch.schema:navSwitch-ABTEST_GLOBAL_P:START -->










<script>
MSGSWITCH = true;
</script>



<script>
MERCHANT_SWITCH = 'true';
</script>



<!-- FD:231:alipay/nav/versionSwitch.vm:START --><!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:START -->



























<!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:END --><!-- FD:231:alipay/nav/versionSwitch.vm:END --><!-- FD:231:alipay/nav/navSwitch.vm:1740:nav/navSwitch.schema:navSwitch-ABTEST_GLOBAL_P:END --><!-- FD:231:alipay/nav/navSwitch.vm:END -->
<!-- abtestEnabled:  -->


<!-- FD:231:alipay/nav/uribroker.vm:START --><!-- FD:231:alipay/nav/uribroker.vm:1742:nav/uribroker.schema:uribroker-URIBroker列表:START -->

  
  <script type="text/javascript">
  window.GLOBAL || (GLOBAL = {});
  GLOBAL.system = {};
   GLOBAL.system["assetsServer"] = "https://a.alipayobjects.com"; GLOBAL.system["apimgServer"] = "https://i.alipayobjects.com"; GLOBAL.system["personalportalServer"] = "https://my.alipay.com"; GLOBAL.system["personalServer"] = "https://lab.alipay.com"; GLOBAL.system["personalprodServer"] = "https://shenghuo.alipay.com"; GLOBAL.system["memberprodServer"] = "https://memberprod.alipay.com"; GLOBAL.system["tfsImageServer"] = "https://tfs.alipayobjects.com"; GLOBAL.system["merchantwebServer"] = "https://shanghu.alipay.com"; GLOBAL.system["authCenterServer"] = "https://auth.alipay.com"; GLOBAL.system["securityServer"] = "https://securitycenter.alipay.com"; GLOBAL.system["tradecmtServer"] = "https://pingjia.alipay.com"; GLOBAL.system["appstoreServer"] = "https://app.alipay.com"; GLOBAL.system["zhangdanServer"] = "https://zd.alipay.com"; GLOBAL.system["uninavServer"] = "https://uninav.alipay.com"; GLOBAL.system["pucprodServer"] = "https://jiaofei.alipay.com"; GLOBAL.system["benefitprodServer"] = "https://zht.alipay.com"; GLOBAL.system["enterpriseportalServer"] = "https://enterpriseportal.alipay.com"; GLOBAL.system["couriercoreServer"] = "https://couriercore.alipay.com"; GLOBAL.system["uemprodServer"] = "https://uemprod.alipay.com"; GLOBAL.system["bizfundprodServer"] = "https://bizfundprod.alipay.com"; GLOBAL.system["morderprodServer"] = "https://b.alipay.com"; GLOBAL.system["consumeprodServer"] = "https://consumeprod.alipay.com"; GLOBAL.system["emembercenterServer"] = "https://emembercenter.alipay.com"; GLOBAL.system["crmhomeServer"] = "https://e.alipay.com"; GLOBAL.system["cshallServer"] = "https://cshall.alipay.com"; GLOBAL.system["openhomeServer"] = "https://openhome.alipay.com"; GLOBAL.system["yebprodServer"] = "https://yebprod.alipay.com"; GLOBAL.system["financeprodServer"] = "https://financeprod.alipay.com"; GLOBAL.system["goldetfprodServer"] = "https://goldetfprod.alipay.com"; GLOBAL.system["certifyServer"] = "https://certify.alipay.com"; GLOBAL.system["securitycenterServer"] = "https://securitycenter.alipay.com"; GLOBAL.system["couponwebServer"] = "https://hongbao.alipay.com"; GLOBAL.system["pointprodServer"] = "https://jf.alipay.com"; GLOBAL.system["pcreditprodServer"] = "https://huabei.alipay.com"; GLOBAL.system["cardServer"] = "https://card.alipay.com"; GLOBAL.system["membercenterServer"] = "https://accounts.alipay.com"; GLOBAL.system["custwebServer"] = "https://custweb.alipay.com"; GLOBAL.system["zcbprodServer"] = "https://zcbprod.alipay.com";
  </script>
  
  

<!-- FD:231:alipay/nav/uribroker.vm:1742:nav/uribroker.schema:uribroker-URIBroker列表:END --><!-- FD:231:alipay/nav/uribroker.vm:END -->

























<div id="J-global-notice-container" class="global-notice-container" style="position: relative; z-index: 999; background: #ff6600;">



<!-- FD:231:alipay/nav/global_ad.vm:START --><!-- FD:231:alipay/nav/global_ad.vm:1735:nav/global_ad.schema:global_ad-全站广告:START --><!-- FD:231:alipay/nav/global_ad.vm:1735:nav/global_ad.schema:global_ad-全站广告:END --><!-- FD:231:alipay/nav/global_ad.vm:END -->



<!-- FD:231:alipay/notice/headNotice.vm:START --><!-- FD:231:alipay/notice/headNotice.vm:5381:notice/headNotice.schema:headNotice-全站公告:START --><!--[if lte IE 7]>
<style>.kie-bar { display: none; height: 24px; line-height: 1.8; font-weight:normal; text-align: center; border:1px solid #fce4b5; background-color:#FFFF9B; color:#e27839; position: relative; font-size: 12px; margin: 5px 0 0 0; padding: 5px 0 2px 0; } .kie-bar a { text-decoration: none; color:#08c; background-repeat: none; } .kie-bar a#kie-setup-IE8,.kie-bar a#kie-setup-taoBrowser { padding: 0 0 2px 20px; *+padding-top: 2px; *_padding-top: 2px; background-repeat: no-repeat; background-position: 0 0; } .kie-bar a:hover { text-decoration: underline; } .kie-bar a#kie-setup-taoBrowser { background-position: 0 -20px; }</style>
<div id="kie-bar" class="kie-bar">您现在使用的浏览器版本过低，可能会导致部分图片和信息的缺失。请立即 <a href="http://www.microsoft.com/china/windows/IE/upgrade/index.aspx" id="kie-setup-IE8" seed="kie-setup-IE8" target="_blank" title="免费升级至IE8浏览器">免费升级</a> 或下载使用 <a href="http://download.browser.taobao.com/client/browser/down.php?pid=0080_2062" id="kie-setup-taoBrowser" seed="kie-setup-taoBrowser" target="_blank" title="淘宝浏览器">淘宝浏览器</a> ，安全更放心！ <a title="查看帮助" target="_blank" seed="kie-setup-help" href="https://help.alipay.com/lab/help_detail.htm?help_id=260579">查看帮助</a></div>
<script type="text/javascript">
(function () {
    function IEMode() {
        var ua = navigator.userAgent.toLowerCase();
        var re_trident = /\btrident\/([0-9.]+)/;
        var re_msie = /\b(?:msie |ie |trident\/[0-9].*rv[ :])([0-9.]+)/;
        var version;
        if (!re_msie.test(ua)) {
            return false;
        }
        var m = re_trident.exec(ua);
        if (m) {
            version = m[1].split(".");
            version[0] = parseInt(version[0], 10) + 4;
            version = version.join(".");
        } else {
            m = re_msie.exec(ua);
            version = m[1];
        }
        return parseFloat(version);
    }
    var ie = IEMode();
    if (ie && ie < 8 && (self.location.href.indexOf("_xbox=true") < 0)) {
        document.getElementById('kie-bar').style.display = 'block';
        document.getElementById('kie-setup-IE8').style.backgroundImage = 'url(https://i.alipayobjects.com/e/201307/jYwARebNl.png)';
        document.getElementById('kie-setup-taoBrowser').style.backgroundImage = 'url(https://i.alipayobjects.com/e/201307/jYwARebNl.png)';
    }
})();
</script>
<![endif]-->





<style>
  .global-notice-announcement { width: 100%; min-width: 990px; height: 24px; line-height: 24px; }
  .global-notice-announcement p { width: 990px; margin: 0 auto; text-align: left; font-size: 12px; color: #fff; }
  .ssl-v3-rc4 { display: none; }
</style>

<script>
  /*
   * 获取cookie
   * @param {String} ctoken
   */
  function getCookie(name) {
    if (document.cookie.length &gt; 0) {
      var begin = document.cookie.indexOf(name + '=');
      if (begin !== -1) {
        begin += name.length + 1;
        var end = document.cookie.indexOf(';', begin);
        if (end === -1) {
          end = document.cookie.length;
        }
        return unescape(document.cookie.substring(begin, end));
      }
    }
    return null;
  }
  window.onload = function() {
    var globalNoticeSsl = document.getElementById('J-global-notice-ssl');
    if (globalNoticeSsl) {
      var sslUpgradeTag = getCookie('ssl_upgrade');
      if (sslUpgradeTag &amp;&amp; sslUpgradeTag === '1') {
        // 展示升级公告
        globalNoticeSsl.setAttribute('class', 'global-notice-announcement');
      } else {
        // 删除升级公告
        globalNoticeSsl.parentNode.removeChild(globalNoticeSsl);
      }
    }
  }
</script>

<!-- FD:231:alipay/notice/headNotice.vm:5381:notice/headNotice.schema:headNotice-全站公告:END --><!-- FD:231:alipay/notice/headNotice.vm:END -->
</div>





<link rel="stylesheet" type="text/css" charset="utf-8" href="https://a.alipayobjects.com/alipay-nav/1.3.12/src/nav-global.css" />
<div id="globalContainer" class="global-reset global-container global-type-global"><div class="global-top-a"> <div class="global-top"><div class="global-top-container">  <ul class="global-top-right">    <li class="global-top-item global-top-item-last">      <a id="globalBirthIcon" href="http://abc.alipay.com/jiniance/index.htm" class="global-icon global-icon-birth global-hide" target="_blank" seed="globalTopItem-globalBirthIcon" smartracker="on"></a>          </li><li class="global-top-item">你好,</li>    <li id="globalUser" class="global-top-item">      <span class="global-top-text">        黄令志        <i class="iconfont global-top-angle"></i>      </span>    </li>                          <li class="global-top-item">            <a href="https://auth.alipay.com/login/logout.htm?goto=https://auth.alipay.com" class="global-top-link" seed="global-exit-v1">退出</a>          </li>    <em class="global-top-item global-top-seperator">|</em>    <li class="global-top-item">      <a class="global-top-link" href="https://my.alipay.com" seed="global-portal-v1" target="_blank">我的支付宝</a>    </li>    <em class="global-top-item global-top-seperator">|</em>    <li id="globalSecurity" class="global-top-item">      <a class="global-top-link" href="https://securitycenter.alipay.com/sc/index.htm" seed="global-security-v1" target="_blank">安全中心</a>    </li>    <em class="global-top-item global-top-seperator">|</em>    <li id="globalHelp" class="global-top-item">      <a class="global-top-link" href="http://help.alipay.com/lab/index.htm" seed="global-help" target="_blank">服务大厅</a>      <i class="iconfont global-top-angle"></i>    </li>    <li id="globalMore" class="global-top-item global-top-item-last">        <i class="iconfont" title="记录"></i>    </li>  </ul>  <ul class="global-top-left">          </ul></div></div></div><div class="global-common-a"> <div class="global">            <div class="global-header fn-clear " coor="headarea">      <div class="global-header-content">        <div class="global-logo">            <a href="https://my.alipay.com/portal/i.htm" seed="global-logo" title="我的支付宝"></a>        </div>        <div class="global-logo-neighbor">        </div>        <ul class="global-nav">            <li class="global-nav-item global-nav-item-current">                <i class="iconfont" title="菱形"></i>                <a href="https://my.alipay.com/portal/i.htm" seed="global-user-i">我的支付宝</a>                <span class="global-nav-item-arrow">◆</span>                <span class="global-nav-item-arrow global-nav-item-arrow-border">◆</span>            </li>            <li class="global-nav-item ">                <i class="iconfont" title="菱形"></i>                <a href="https://consumeprod.alipay.com/record/index.htm" seed="global-record">交易记录</a>                <span class="global-nav-item-arrow">◆</span>                <span class="global-nav-item-arrow global-nav-item-arrow-border">◆</span>            </li>            <li class="global-nav-item ">                <i class="iconfont" title="菱形"></i>                <a href="https://my.alipay.com/portal/account/safeguard.htm" seed="global-safeguard">会员保障</a>                <span class="global-nav-item-arrow">◆</span>                <span class="global-nav-item-arrow global-nav-item-arrow-border">◆</span>            </li>            <li class="global-nav-item ">                <i class="iconfont" title="菱形"></i>                <a href="https://app.alipay.com/container/web/index.htm" seed="global-appstore">应用中心</a>                <span class="global-nav-item-arrow">◆</span>                <span class="global-nav-item-arrow global-nav-item-arrow-border">◆</span>            </li>        </ul>      </div>    </div>        <div class="global-subheader">        <ul class="global-subnav">                            <li class="global-subnav-item global-subnav-item-current">                    <a href="https://my.alipay.com/portal/i.htm" seed="global-user-i">首页</a>                </li>                <li class="global-subnav-item ">                    <a href="https://my.alipay.com/portal/assets/index.htm" seed="global-account-info">账户资产</a>                </li>                <li class="global-subnav-item ">                    <a href="https://my.alipay.com/portal/account/index.htm" seed="global-account-member">账户设置</a>                </li>                <li class="global-subnav-item ">                    <a href="https://zht.alipay.com/asset/index.htm" seed="global-account-zht">账户通</a>                </li>                <li class="global-subnav-item  global-hide" id="global-subnav-merchant">                    <a href="https://enterpriseportal.alipay.com/index.htm?channel=psl" seed="global-merchant">商户服务</a>                </li>                <div class="global-subnav-input">                    <form action="https://zizhu.alipay.com/lab/search_new_result.htm" method="GET" id="J-my-app-search-form" class="my-app-search-form fn-hide" target="_blank" accept-charset="gb2312" style="display: block;">                        <input type="text" id="J-my-app-search-input" placeholder="输入关键字，如“密码”" seed="my-app-search-input" name="word" autocomplete="off" />                        <i class="iconfont global-subnav-input-scan" seed="my-app-search-icon" title="查询/搜索"></i>                    </form>                </div>                                            </ul>    </div>    </div></div></div>
<script src="https://a.alipayobjects.com/alipay-nav/1.3.12/src/nav-global.js" charset="utf-8"></script>
<script type="text/javascript">

document.domain=document.domain.split(".").slice(-2).join("."),seajs.use(["alipay-nav/1.3.12/src/nav-global","$"],function(a,b){window.navInit(b.extend({menu:"s1_index",appKey:"",catKey:"",title:"我的支付宝 － 支付宝",userName:"黄令志",email:"182******29",mobile:"182******29",logonIdType:"MOBILE",userId:"2088702698723581",portraitPath:"/images/partner/T1sGlfXbpXXXXXXXXX",container:"#globalContainer",timestamp:(new Date).getTime(),pageAbsUrl:"https://my.alipay.com/portal/i.htm?referer=https%3A%2F%2Fauth.alipay.com%2Flogin%2Findex.htm",isLogin:true,msgSwitch:window.MSGSWITCH,msgHide:1,needLoadMsg:"Y",showTaobaoLogin:false,showAlibabaLogin:false,showMerchant:false,showPersonal:false,abtestEnabled:false,abtest:"",abtestType:"GLOBAL_P",merchantSwitch:window.MERCHANT_SWITCH},GLOBAL.system))});


</script>



  <div id="container" class="ui-container">
  

    <script type="text/javascript">
    var json_ua = null;
    var form_tk = 'hZiiowI15Wla9IuvephNE7ngzxhCyMOW';
    </script>
    <script type="text/javascript" charset="utf-8" src="https://rds.alipay.com/ua_personalweb_portal_account.js?t=2018083015"></script>
  

    <script type="text/javascript">
      window.createFontFace = function(fontContent) {
        var fontStyle = fontContent.fontStyle || 'dynamic-font-style';
        var fontBase64 = 'data:application/font-woff;charset=utf-8;base64,' + fontContent.value;
        var fontFormat = 'woff';
        if (fontContent.contentType === 'ADDR_URL') {
          fontBase64 = fontContent.value + '?#iefix';
          fontFormat = 'embedded-opentype';
        }
        var cssText =
          "@font-face {"
        + "  font-family: '" + fontStyle + "';"
        + "  src: url(" + fontBase64 + ") format('" + fontFormat + "');"
        + "}"
        + "." + fontStyle + "{"
        + "  font-family: '" + fontStyle + "';"
        + "}";

        // 获取原有fontFace节点&lt;避免用户重复请求时，重复添加&gt;
        var fontFaceNode = document.getElementById(fontStyle);
        if (fontFaceNode) return;
        var fragmentDiv = document.createElement('div');
        fragmentDiv.innerHTML = 'x&lt;style id="' + fontStyle + '" &gt;' + cssText + '&lt;/style&gt;';
        var head = document.getElementsByTagName('head')[0];
        head.appendChild(fragmentDiv.lastChild);
        fragmentDiv = null;
      }
    </script>
  

<!-- FD:17:personalweb/bannerBg/data.vm:START --><!-- FD:17:personalweb/bannerBg/data.vm:60:bannerBg/data.schema:旧版我的支付宝不同时段banner背景图:START -->
<style>
.i-banner {
  background: #4e7199 no-repeat center;
    
    background-color: #4f5914;
    background-image: url(https://i.alipayobjects.com/e/201309/19jDyAPbtn.jpg);
    
}

#J-app-mobile-qrcode .icon-qrcode {
  background:url(https://i.alipayobjects.com/i/ecmng/jpg/201501/4JY5AwHWrN.jpg) 0 0 no-repeat;
}

@media only screen and (-webkit-min-device-pixel-ratio: 2), not all, not all, not all, only screen and (min-resolution: 192dpi), only screen and (min-resolution: 2dppx){
#J-app-mobile-qrcode .icon-qrcode {
background-size:90px 90px;
background-image:url(https://i.alipayobjects.com/i/ecmng/jpg/201501/4JY4XVvRV7.jpg);
}

}
.i-banner-main-detail .i-banner-stat-safeguard-0 {display:none;}
body .i-app .apps-list .app-name {
  float: none;
}
</style>
<script>
  var trackerImg = new Image();
  var rnd_id = "_img_" + Math.random();
  window[rnd_id] = trackerImg;
  trackerImg.onload = trackerImg.onerror = function() {
    window[rnd_id] = null;
  }
  trackerImg.src = 'https://my.alipay.com/m.gif?from=home' + '&amp;t=' + Date.now();
</script>
<!-- FD:17:personalweb/bannerBg/data.vm:60:bannerBg/data.schema:旧版我的支付宝不同时段banner背景图:END -->
<!-- FD:17:personalweb/bannerBg/data.vm:END -->

<div class="i-banner">
  <div class="i-banner-message">
    <a id="J-portal-message" class="message-entrance message-stat-none" href="https://couriercore.alipay.com/messager/new.htm" target="_blank" title="点击展开消息" seed="msg-icon-myalipay-v1">
      <i class="iconfont message-back" title="点击展开消息"></i>
      <span class="message-fore message-clock-animate">
        <i class="iconfont"></i>
        <span class="message-count">1</span>
      </span>
    </a>
  </div>

  <div class="i-banner-content fn-clear" coor-rate="0.1" coor="default-banner">
    <div class="i-banner-portrait">
    
  
  <a href="/portal/account/index.htm" class="userInfo-portrait" seed="account-headshot-y-myalipay-v1">
  
    
    <img src="https://tfsimg.alipay.com/images/partner/T1sGlfXbpXXXXXXXXX" id="J-portrait-user" alt="当前LOGO" /></a>

    </div>
    <div class="i-banner-main">
      <div class="i-banner-main-hello fn-clear">
        <p class="userName fn-left">
          下午好, <a href="https://lab.alipay.com/user/myAccount/index.htm" target="_blank" seed="account-name-myalipay-v1" title="黄令志">黄令志</a>
        </p>

        <div class="notice fn-left">
          
            <!-- CMS:个人版门户cms/portal/care.vm开始:personalportal/portal/care.vm -->
<a href="https://my.alipay.com/portal/account/index.htm" target="_blank" seed="personlweb-home-avatar-link">转账看头像，安全有保障 修改头像</a><!-- CMS:个人版门户cms/portal/care.vm结束:personalportal/portal/care.vm -->
        
        </div>
      </div>

      <div class="i-banner-main-detail fn-clear">
        <div class="fn-left fn-mr-5">
          账户名：
          <a href="https://lab.alipay.com/user/myAccount/index.htm" seed="account-zhangh-myalipay-v1" target="_blank" title="182******29" id="J-userInfo-account-userEmail">182******29</a>
        </div>

        

<ul class="i-banner-stat fn-left">
  <li>
  
  <a class="j-atip i-banner-stat-certify-1" target="_blank" seed="account-certify-y-myalipay-v1" data-content="您已通过支付宝实名认证" data-content-link-text="查看详情" data-content-link="https://certify.alipay.com/certifyInfo.htm" href="https://certify.alipay.com/certifyInfo.htm">
      <i class="icon"></i>
    </a>
  </li>
  <li>
  
  
    <a class="j-atip i-banner-stat-mobile-1" seed="account-mobile-y-myalipay-v1" data-content="您已绑定手机182******29" data-content-link-text="管理" data-content-link="https://lab.alipay.com/user/mobile/index.htm" href="https://lab.alipay.com/user/mobile/index.htm">
      <i class="icon"></i>
    </a>
  </li>
</ul>

        
        <i class="separator-20 fn-left">|</i>
        <div class="fn-left">
          
          
          上次登录时间：2018.08.30 15:31:04
        </div>
        
      </div>
    </div>
  </div>
</div>

<!-- FD:140:personalportal/portal/onoff.vm:START --><!-- FD:140:personalportal/portal/onoff.vm:1744:portal/onoff.schema:onoff-我的支付宝开关:START -->
<input type="hidden" id="J-visibility-zhsq" value="1" />
<input type="hidden" id="J-visibility-zht" value="0" />
<input type="hidden" id="J-visibility-app" value="1" />



	



	<input type="hidden" id="J-visibility-app-cache" value="0" />


	<input type="hidden" id="J-visibility-behavior" value="0" />






	<input type="hidden" id="J-wapshow-reset" value="20140902" />


	<input type="hidden" id="J-promo-close" value="" />
<!-- FD:140:personalportal/portal/onoff.vm:1744:portal/onoff.schema:onoff-我的支付宝开关:END -->
<!-- FD:140:personalportal/portal/onoff.vm:END -->
<!-- FD:17:personalweb/homePage/searchApp.vm:START --><!-- FD:17:personalweb/homePage/searchApp.vm:1677:homePage/searchApp.schema:支付宝应用地址大全:START -->
<script type="text/javascript">
  window.searchAppSource = "https://os.alipayobjects.com/rmsportal/HBrVXElUKRNfXYz.js";
</script>
<!-- FD:17:personalweb/homePage/searchApp.vm:1677:homePage/searchApp.schema:支付宝应用地址大全:END --><!-- FD:17:personalweb/homePage/searchApp.vm:END -->
<div class="i-content">
  <div class="i-assets fn-clear" coor="default-assets">

    <table class="i-assets-table" cellspacing="0">
  <tbody><tr>
    
    
    
    <td class="i-assets-balance">
      <div class="wrap ui-bookblock-bookblock" id="J-assets-balance" data-tair-key="PERSONAL_USERINFO_HIDDEN" data-behavior-key="ISBALANCESHOW" data-behavior-value="">
      







<div class="i-assets-container ui-bookblock-item" style="display: block;">
  <div class="i-assets-content">
    
      <div class="i-assets-header fn-clear">
        <h3 class="fn-left">
          
            账户余额
          
        </h3>
        <p id="showAccountAmount" class="fn-left fn-ml-10">
          <a class="show-text" href="javascript:void(0)" seed="showAccountAmount-showText" smartracker="on">显示金额</a>
          <a class="hide-text" href="javascript:void(0)" seed="showAccountAmount-hideText" smartracker="on">隐藏金额</a>
        </p>
        
      </div>
      <div class="i-assets-body fn-clear">
        <div id="account-amount-container" class="i-assets-balance-amount fn-left"><span class="df-integer">39<span class="df-decimal">.00</span></span>元</div>
        <ul class="i-assets-balance-actions fn-clear">
          

            <li>
              
              <a class="ui-button ui-button-swhite j-deposit-link" title="充值" target="_blank" href="https://shenghuo.alipay.com/transfer/deposit/depositPreprocessGw.htm" seed="app-recharge-myalipay-yue-v1">充 值</a>
            </li>
            <li>
              <a class="ui-button ui-button-swhite" title="提现" target="_blank" href="https://memberprod.alipay.com/fund/withdraw/apply.htm" seed="app-draw-myalipay-yue-v1">提 现</a>
            </li>
            <li>
              <a class="ui-button ui-button-swhite" title="转账" href="https://shenghuo.alipay.com/send/payment/fill.htm?_pdType=adbhajcaccgejhgdaeih" seed="app-transfer-myalipay-yue-v1">转 账</a>
            </li>
            <li>
              <a class="i-assets-balance-record-link" title="查看" href="https://lab.alipay.com/consume/record/items.htm" seed="app-transfer-myalipay-yue-v1">
                查看
              </a>
            </li>
        </ul>
      </div>
      <!-- <i class="i-assets-visible-icon main" title="点击隐藏金额" seed="asset-yue-fronturn-myalipay-v1"></i> -->
      <div class="i-assets-footer fn-clear">
      
      
      
      
      
      </div>
      
    </div>
</div>


<div class="i-assets-container ui-bookblock-item" style="display: none;">
  <div class="i-assets-content">
    <div class="i-assets-header fn-clear">
      <h3 class="fn-left">账户余额</h3>
    </div>

    <div class="i-assets-body fn-clear">
      <span class="ft-gray fn-mr-10">
        
        余额支付：<a class="ft-gray" href="https://lab.alipay.com/user/balance/index.htm" target="_blank" seed="asset-yue-on-myalipay-v1">已开启</a>
        
      </span>
      <span>
        <a title="充值" class="j-deposit-link" target="_blank" seed="app-recharge-myalipay-yue-v1" href="https://shenghuo.alipay.com/transfer/deposit/depositPreprocessGw.htm">充值</a>
        <i class="separator">|</i>
        <a title="提现" target="_blank" seed="app-draw-myalipay-yue-v1" href="https://memberprod.alipay.com/fund/withdraw/apply.htm">提现</a>
        <i class="separator">|</i>
        <a title="转账" seed="app-transfer-myalipay-yue-v1" href="https://shenghuo.alipay.com/send/payment/fill.htm?_pdType=adbhajcaccgejhgdaeih">转账</a>
      </span>
    </div>

    <i class="i-assets-visible-icon" title="点击显示金额" seed="asset-yue-oppiturn-myalipay-v1"></i>
  </div>
</div>




<input type="hidden" id="J-mfund-xbox" data-tair-key="PERSONAL_USERINFO_HIDDEN" data-behavior-key="ISSHOWMFUNDXBOX" data-behavior-value="" />

      </div>
    </td>

    
    
    
 
        
        
        <td class="i-assets-pcredit  i-assets-2rows" rowspan="2">
          <div class="wrap ui-bookblock-bookblock" id="J-assets-pcredit" data-tair-key="PERSONAL_USERINFO_HIDDEN" data-behavior-key="ISPCREDITSHOW" data-behavior-value="">
          





<style>
  .i-assets-pcredit {position: relative;}
  #J-assets-pcredit {position: static;}
  #J-assets-pcredit .amount-des {margin-bottom: 5px;}
  #J-assets-pcredit .amount {color: #A1A1A1;}
  #J-assets-pcredit .highlight .amount {color: #333;font-size: 25px;}
  #J-assets-pcredit .highlight .amount .fen{font-size: 18px;}
  #J-assets-pcredit .i-assets-body { height: auto; margin-bottom: 20px;}
  #J-assets-pcredit .i-assets-foot { position: absolute;bottom: 20px;left: 15px;}
  #J-assets-pcredit-amountShow {height:92px;}
  #J-assets-pcredit .not-signed .amount-des {padding-top: 7px;}
  #J-assets-pcredit .overdue .amount, #J-assets-pcredit .overdue .fen{font-size:12px;}
  #J-assets-pcredit .j-deposit-link {float: left;margin-right: 5px;}
</style>

<div class="i-assets-container ui-bookblock-item">
  
  <div class="i-assets-content">
    
    
    
    <style>
      #J-assets-pcredit .amount, #J-assets-pcredit .amount .fen {
        font-size: 12px;
      }
    </style>
    <div class="i-assets-header fn-clear">
      <h3 class="fn-left">花呗</h3>
      <p id="showHuabeiAmount" class="hide-amount fn-left fn-ml-10">
        <a class="show-text" href="javascript:void(0)" seed="showHuabeiAmount-showText" smartracker="on">显示金额</a>
        <a class="hide-text" href="javascript:void(0)" seed="showHuabeiAmount-hideText" smartracker="on">隐藏金额</a>
      </p>
      <i class="icon-ask fn-right j-atip" data-content="支持余额、余额宝、借记卡快捷自动还款，全额按时还款不收费，账户安全有保障！"></i>
    </div>

    <div class="i-assets-body">
      <div class="amount-des-error" id="amount-des-error" style="display: none">显示出错啦，请重试</div>
      <div class="amount-des" id="amount-des-success">
        <p class="ft-gray">可用额度<br />
        <span id="available-amount-container" class="highlight huabei-amount-container">
          <strong class="fen"><span class="fen">**.**</span></strong>元
        </span></p>
        <p class="ft-gray">总额度：<span id="credit-amount-container" class="huabei-amount-container"><strong><span class="fen">**.**</span></strong>元</span></p>
      </div>
    </div>
    <a class="ui-button ui-button-swhite" target="_blank" href="https://f.alipay.com/moonlight/index.htm" seed="iAssetsContent-link" smartracker="on">查 看</a>
    <div class="i-assets-foot">
      <p class="ft-gray">这月买，下月还</p>
    </div>

    
    
  </div>
  
</div>

          </div>
        </td>
      
    

    <td class="i-assets-other i-assets-2rows i-assets-2rows-3col" rowspan="2" id="J-assets-other">
      <div class="i-assets-content">
  <div class="i-assets-header fn-clear">
    <h3 class="fn-left">其他账户</h3>
    <a class="fn-right" href="https://zht.alipay.com/asset/newIndex.htm" seed="zhanght-more-myalipay-v1">更多&gt;</a>
  </div>

  <div class="i-assets-body">
    <div id="J-assets-other-zht">
      <ul class="content">
        <li class="fn-clear first">
          <span class="fn-left bank">
            <i class="icon"></i>银行卡:
            <a href="https://zht.alipay.com/asset/bankList.htm" seed="">管理</a>
          </span>
        </li>


        <li class="fn-clear">
          <span class="fn-left ALI">
            <i class="icon"></i>阿里账户:
            <a href="https://zht.alipay.com/asset/newIndex.htm#ALI" seed="zhanght-zht_nokpi_AMADTH_TZLI_ALI-manage-myalipay-v1">管理</a>
          </span>
        </li>

        <li class="fn-clear">
          <span class="fn-left SHOPPING">
            <a href="https://zht.alipay.com/asset/newIndex.htm">进入账户通</a>
          </span>
        </li>
      </ul>
    </div>
    
    <script type="text/x-handlebars-template" id="J-tpl-assets-other-zht">
      &lt;ul class="content"&gt;
        &lt;li class="fn-clear first"&gt;
          &lt;span class="fn-left bank"&gt;
            &lt;i class="icon"&gt;&lt;/i&gt;银行卡:
            &lt;a href="https://zht.alipay.com/asset/bankList.htm" seed=""&gt;管理&lt;/a&gt;
          &lt;/span&gt;
        &lt;/li&gt;


        &lt;li class="fn-clear"&gt;
          &lt;span class="fn-left ALI"&gt;
            &lt;i class="icon"&gt;&lt;/i&gt;阿里账户:
            &lt;a href="https://zht.alipay.com/asset/newIndex.htm#ALI"
            seed="zhanght-zht_nokpi_AMADTH_TZLI_ALI-manage-myalipay-v1"&gt;管理&lt;/a&gt;
          &lt;/span&gt;
        &lt;/li&gt;

        &lt;li class="fn-clear"&gt;
          &lt;span class="fn-left SHOPPING"&gt;
            &lt;a href="https://zht.alipay.com/asset/newIndex.htm"&gt;进入账户通&lt;/a&gt;
          &lt;/span&gt;
        &lt;/li&gt;
      &lt;/ul&gt;
    </script>
    
  </div>
  <div class="i-assets-foot">
    
    
    

    
      <p>花呗: <a href="https://f.alipay.com/moonlight/index.htm" seed="app-f-manage-zhanght-myalipay-v1">管理</a></p>

    
      <p>
  集分宝:<a href="https://jf.alipay.com/prod/pintegral.htm" title="我的集分宝0个" seed="asset-jfb-zero-myalipay-v1">0</a> 个
</p>

    
    <p>
      支付宝购物卡:<a href="https://card.alipay.com/pcardprocess/overseaCategory.htm" title="支付宝购物卡" seed="asset-card-myalipay-v1">管理</a>
    </p>

  </div>
</div>

    </td>
  </tr>

  <tr>
    
    
    <td class="i-assets-mfund">
      <div class="wrap ui-bookblock-bookblock" id="J-assets-mfund" data-tair-key="PERSONAL_USERINFO_HIDDEN" data-behavior-key="ISMFUNDSHOW" data-behavior-value="">
      









<div class="i-assets-container ui-bookblock-item" style="display: block;">
  <div class="i-assets-content">
    
    <div class="">
      <div class="i-assets-header fn-clear">
        <h3 class="fn-left">余额宝</h3>
        <p id="showYuebaoAmount" class="fn-left fn-ml-10">
          <a class="show-text" href="javascript:void(0)" seed="showYuebaoAmount-showText" smartracker="on">显示金额</a>
          <a class="hide-text" href="javascript:void(0)" seed="showYuebaoAmount-hideText" smartracker="on">隐藏金额</a>
        </p>
        
      </div>
      <div class="i-assets-header-body fn-clear">
        <p class="i-assets-mFund-amount" id="J-assets-mfund-amount"><span class="df-integer">1961<span class="df-decimal">.67</span></span>元</p>
          
           <p class="i-assets-mFund-desc">
          <a class="ui-button ui-button-sorange fn-mr-15" title="转入" href="https://yebprod.alipay.com/yeb/purchase.htm" target="_blank" seed="app-yuebao-transfer-in-myalipay-v1">
            转 入
          </a>
            <a href="https://yebprod.alipay.com/yeb/mfWithdraw.htm" target="_blank" seed="app-yuebao-transfer-out-myalipay-v1">转出</a>
            <i class="separator-2">|</i>
            <a href="https://bao.alipay.com/" target="_blank" seed="app-yuebao-manage-myalipay-v1">管理</a>
              <i class="separator-2">|</i>
                累计收益: <a id="J-income-num" class="income ft-gray" href="https://yebprod.alipay.com/yeb/asset.htm" seed="asset-yuebao-benefit-myalipay-v1">327.75</a> 元
              [<i class="pop-help-mark j-atip" data-content="收益介绍，" data-content-link="https://bao.alipay.com/" data-content-link-online="true" data-content-link-text="查看" data-arrowposition="5" seed="mFund-asset-help-apop">?</i>]
             </p>
             
             
          
      </div>
    </div>
    <!-- <i id="J-assets-mfund-visible-icon" class="i-assets-visible-icon main" title="点击隐藏金额" seed="asset-yuebao-fronturn-myalipay-v1"></i> -->
    <p id="J-assets-mfund-guide" class="icon-mfund-guide fn-hide"></p>
  </div>
</div>

<div class="i-assets-container ui-bookblock-item" style="display: none;">
  <div class="i-assets-content">
    <div class="i-assets-header">
      <h3>余额宝</h3>
    </div>
    <div class="i-assets-header-body">
      <div class="i-assets-mFund-other">
        
        
          08月29日收益：
          <a href="https://yebprod.alipay.com/yeb/asset.htm" class="ft-orange" seed="asset-yuebao-benefit-myalipay-v1">0.19</a> 元
        

        
          <span class="ft-gray fn-ml-20">
            七日年化收益率：3.2009%
          </span>
        

        <a class="fn-ml-10" href="https://yebprod.alipay.com/yeb/purchase.htm" target="_blank" seed="app-yuebao-transfer-in-myalipay-v1">转入</a>
        <i class="separator">|</i>
        <a href="https://yebprod.alipay.com/yeb/mfWithdraw.htm" target="_blank" seed="app-yuebao-transfer-out-myalipay-v1">转出</a>
        <i class="separator">|</i>
        <a href="https://bao.alipay.com/" target="_blank" seed="app-yuebao-manage-myalipay-v1">管理</a>
      </div>
    </div>
    <i class="i-assets-visible-icon" title="点击显示金额" seed="asset-yuebao-oppiturn-myalipay-v1"></i>
  </div>
  
</div>


      </div>
    </td>
  </tr>
</tbody></table>


    <div class="i-side">
      <i class="icon-arrow"></i>
      <i class="icon"></i>
    </div>
  </div>
  <div class="i-trend" coor="default-trend">
    <div class="content" id="J-trend-tabs" data-tair-key="PERSONAL_USERINFO_HIDDEN" data-behavior-key="trendTabPosition">
  <div class="header trend-record">
    <h3>交易记录</h3>
    <!-- 交易记录业务入口 -->
    <a class="fn-ml10" seed="i-record-chongzhi" title="充值记录" href="https://lab.alipay.com/consume/record/inpour.htm" target="_blank">充值记录</a>
    <span class="ui-separator-pd">|</span>
    <a seed="i-record-tixian" title="提现记录" href="https://lab.alipay.com/consume/record/draw.htm" target="_blank">提现记录</a>
    <span class="ui-separator-pd">|</span>
    <a seed="i-record-refund" title="退款记录" href="https://consumeprod.alipay.com/record/index.htm?status=refund" target="_blank">退款记录</a>
    <span class="ui-separator-pd">|</span>
    <a class="more" seed="i-record-more" title="查看所有交易记录" target="_blank" href="https://consumeprod.alipay.com/record/index.htm">查看所有交易记录</a>
    <!-- 资金明细相关入口 -->
    <select id="asset-items" class="fn-hide" style="display: none;" seed="header-assetItems" smartracker="on">
      <option value="personal">余额收支明细</option>
      <option value="yeb">余额宝收支明细</option>
      <option value="huabei">花呗额度明细</option>
    </select><div class="jui-select " data-role="jui-select" data-selid="sel1535614429968" style="width: 160px; display: inline-block;"><p class="jui-select-view" title="余额收支明细">余额收支明细</p><ul class="jui-select-list" style="height: 90px; display: none;"><li title="余额收支明细" data-val="personal" data-selected="" style="">余额收支明细</li><li title="余额宝收支明细" data-val="yeb">余额宝收支明细</li><li title="花呗额度明细" data-val="huabei">花呗额度明细</li></ul><div class="cover-trigger" style="position: absolute;top: 0;left: 0;width: 100%;height: 100%;background: #fff;z-index: 1000000;opacity: 0;filter: alpha(opacity=0);"></div></div>
  </div>
</div>

    <div class="i-side">
      <i class="icon-arrow"></i>
      <i class="icon"></i>
    </div>
  </div>
  <div id="J-cooperant-banner" class="i-cooperant-banner" coor="default-cooperant">
    <div class="content fn-clear">
    
        <div class="main fn-left" seed="cooperant-banner-1">
            <img src="https://zos.alipayobjects.com/rmsportal/BMypdYqYwsisFYkJuvEY.jpg" usemap="#cooperant-banner-1" />
            <map name="cooperant-banner-1" id="cooperant-banner-1">
                <area href="https://pages.tmall.com/wow/act/17370/industry_z4dn_4332?wh_weex=true" title="天猫汽车" shape="rect" coords="105,22,582,194" target="_blank" />
            </map>
        </div>
        <div class="aside fn-left" seed="cooperant-banner-2">
            <img src="https://gw.alipayobjects.com/zos/rmsportal/ILfAEVtyeCavpSFmgXpo.png" usemap="#cooperant-banner-2" />
            <map name="cooperant-banner-2" id="cooperant-banner-2">
                <area href="https://zhaocaibao.bbs.taobao.com/detail.html?postId=7922076" title="数米淘宝店迁移" shape="rect" coords="43,19,219,213" target="_blank" />
            </map>
        </div>
    
</div>

    <div class="i-side">
      <i class="icon-arrow"></i>
      <i class="icon"></i>
    </div>
  </div>

  
<div class="ad-cornerbox" id="J-ads-corner" data-adid="1" data-tpl-id="J-tpl-corner">
</div>

<script type="text/x-handlebars-template" id="J-tpl-corner">
    &lt;div class="ad-cornerbox-wrap" id="j-ad-cornerbox-wrap"&gt;
        &lt;div class="ad-cornerbox-title"&gt;
            &lt;h2&gt;小二推荐&lt;/h2&gt;
            &lt;div class="close" title="关闭"&gt;关闭&lt;/div&gt;
        &lt;/div&gt;
        {{safeAdsHtmlCode}}
    &lt;/div&gt;
</script>




</div>


<div class="i-app" id="J-app-container" coor="default-app" data-tair-key="PERSONAL_USERINFO_HIDDEN" data-behavior-key="MYALIPAYHOMEAPP" data-behavior-value="">
  <div class="container">
    <div class="aside">
      <div class="unfold trigger-item fn-clear" seed="app-assistant-myalipay-v1">
        <div class="default trigger">
          <i class="icon-guide"></i>
          <em>生活好助手</em>
        </div>
        <div class="active trigger">
          <em>收 起</em>
          <i class="icon-arrow"></i>
        </div>
      </div>
      <div class="fold trigger-item fn-clear">
        <div class="default trigger">
          <em>我的应用(<span id="J-app-num"></span>)</em>
          <i class="icon-arrow"></i>
        </div>
        <div class="active trigger">
          <em>展 开</em>
          <i class="icon-arrow"></i>
        </div>
      </div>
    </div>
    <div class="content fn-clear">
      <div class="i-app-list fn-left" id="J-app-list"><div class="apps-list">
    <ul class="apps-list-myAppList fn-clear ">
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000017" target="_blank" seed="app-10017-myalipay-v1">
                    
                    
                    <i class="app-icon fn-left icon-apps30-10017" data-id="10017"></i>
                    <span class="app-name">转账到支付宝</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000015" target="_blank" seed="app-10015-myalipay-v1">
                    <i class="hot-icon fn-left"></i>
                    
                    <i class="app-icon fn-left icon-apps30-10015" data-id="10015"></i>
                    <span class="app-name">信用卡还款</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000053" target="_blank" seed="app-10053-myalipay-v1">
                    
                    
                    <i class="app-icon fn-left icon-apps30-10053" data-id="10053"></i>
                    <span class="app-name">转账到银行卡</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000016" target="_blank" seed="app-10016-myalipay-v1">
                    <i class="hot-icon fn-left"></i>
                    
                    <i class="app-icon fn-left icon-apps30-10016" data-id="10016"></i>
                    <span class="app-name">水电煤缴费</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000020" target="_blank" seed="app-10020-myalipay-v1">
                    
                    
                    <i class="app-icon fn-left icon-apps30-10020" data-id="10020"></i>
                    <span class="app-name">手机充值</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000024" target="_blank" seed="app-10024-myalipay-v1">
                    
                    
                    <i class="app-icon fn-left icon-apps30-10024" data-id="10024"></i>
                    <span class="app-name">爱心捐赠</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000117" target="_blank" seed="app-10110-myalipay-v1">
                    
                    
                    <i class="app-icon fn-left icon-apps30-10110" data-id="10110"></i>
                    <span class="app-name">话费卡充值</span>
                </a>
            </li>
            <li>
                <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000113" target="_blank" seed="app-10108-myalipay-v1">
                    
                    
                    <i class="app-icon fn-left icon-apps30-10108" data-id="10108"></i>
                    <span class="app-name">医院挂号</span>
                </a>
            </li>
        <li>
            <a href="#" class="j-myApp-openSetting app-link" seed="app-add-myalipay-v1">
                <em class="add-icon"><span>+</span></em>
                添加
            </a>
        </li>
    </ul>
    <p class="recommend fn-clear">
        <a class="app-link" href="http://app.alipay.com/appGateway.htm?appId=1000000401" target="_blank" seed="app-introduce-10120-myalipay-v1">
            <i class="app-icon fn-left icon-apps30-10120" data-id="10120"></i>
            <span class="app-name">网购还款</span>
        </a>
        <span class="desc">先消费，后还款 <a href="#" class="j-app-add fn-ml-10" data-id="1000000401" seed="app-introduce-add-myalipay-v1">+ 添加</a></span>
    </p>
</div></div>
      <div class="i-app-mobile fn-right">
        <i class="icon-mobile" id="J-app-mobile">
          <a class="j-xbox" href="https://cmspromo.alipay.com/down/index.htm" seed="moblie-appDownload-myalipay-v1"></a>
        </i>
        <a href="https://cmspromo.alipay.com/down/index.htm" class="j-xbox download" seed="moblie-appDownload-myalipay-v1">立即下载</a>
      </div>
      <div class="i-app-action fn-clear fn-right">
        <i class="icon-more" id="J-app-action-more-close" seed="app-close-myalipay-v1"></i>
        <a href="https://app.alipay.com/container/web/index.htm" class="link-mng j-myApp-openSetting" target="_blank" seed="app-manage-myalipay-v1">
          <i class="icon-mng" title="管理"></i>
        </a>
        <a href="https://app.alipay.com/container/web/index.htm" class="link-apps" seed="app-whole-myalipay-v1" target="_blank">
          <i class="icon-apps" title="全部应用"></i>
        </a>
      </div>
    </div>
  </div>

  <div class="mobile-qrcode fn-clear fn-hide" id="J-app-mobile-qrcode" data-widget-cid="widget-1">
    <div class="qrcode-content fn-clear">
      <div class="fn-left">
        <a class="j-xbox" href="https://cmspromo.alipay.com/down/index.htm" seed="moblie-appDownload-myalipay-v1">
          <i class="icon-qrcode"></i>
        </a>
      </div>
      <div class="fn-right">
        <h3>支付宝钱包</h3>
        <p>随时随地使用应用</p>
        <a href="https://cmspromo.alipay.com/down/index.htm" class="j-xbox download" seed="moblie-appDownload-myalipay-v1" smartracker="on">
          立即下载
        </a>
      </div>
    </div>

    <i class="icon-arrow"></i>
  </div>
</div>

























<!-- CMS:个人版门户cms/home/door.vm开始:personalportal/home/door.vm --><!-- CMS:个人版门户cms/home/door.vm结束:personalportal/home/door.vm -->



  </div>

  

<!-- /component/footCommon.vm -->

<!-- FD:231:alipay/nav/versionSwitch.vm:START --><!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:START -->



























<!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:END --><!-- FD:231:alipay/nav/versionSwitch.vm:END -->







<style>
.ui-footer {margin-top: 30px; border-top: 1px solid #cccccc; height: 100px; color:#808080;}
.ui-footer .ui-separator{font-weight: normal;}
.ui-footer-ctn {border-top: 1px solid #ffffff;padding-top: 15px;text-align: center;}
.ui-footer-link a {padding: 0 3px 0 2px;}
.ui-footer-copyright,.ui-footer-phone {padding-top: 10px;}
.ui-footer-copyright a,.ui-footer-copyright a:hover {color:#808080;}
.server{color:#fff;}
</style>



<div class="ui-footer fn-clear" coor="footer">
    

    <div class="ui-footer-ctn">
        <!-- FD:231:alipay/foot/links.vm:START --><!-- FD:231:alipay/foot/links.vm:2600:foot/links.schema:links-底部链接:START --><div class="ui-footer-link">
  
    <a href="https://job.alibaba.com/zhaopin/index.htm" target="_blank" seed="foot-1">诚征英才</a>

    
       <em class="ui-separator">|</em>
       <a seed="foot-2" href="https://ab.alipay.com/i/lianxi.htm" title="联系我们" target="_blank">联系我们</a>
    
       <em class="ui-separator">|</em>
       <a seed="foot-3" href="https://global.alipay.com/" title="International Business" target="_blank">International Business</a>
    
  
</div><!-- FD:231:alipay/foot/links.vm:2600:foot/links.schema:links-底部链接:END --><!-- FD:231:alipay/foot/links.vm:END -->

        <div class="ui-footer-copyright">
            <!-- FD:231:alipay/foot/copyright.vm:START --><!-- FD:231:alipay/foot/copyright.vm:2604:foot/copyright.schema:支付宝copyright:START -->
<style>
.copyright,.copyright a,.copyright a:hover{color:#808080;}
</style>
<div class="copyright">
  
    <a href="https://fun.alipay.com/certificate/jyxkz.htm" target="_blank" seed="copyright-link" smartracker="on">ICP证：沪B2-20150087</a>
  
</div>
<div class="server" id="ServerNum">
  personalweb-30-5410   0be9214815356144297997303ef3b8
</div>
<!-- FD:231:alipay/foot/copyright.vm:2604:foot/copyright.schema:支付宝copyright:END --><!-- FD:231:alipay/foot/copyright.vm:END -->
        </div>
    </div>
</div>
<!-- /component/footCommon.vm -->

<!-- FD:alipay-foot:alipay/foot/cliveService.vm:START --><!-- FD:alipay-foot:alipay/foot/cliveService.vm:cliveService.schema:START -->
    <div style="display:none">onlineServer</div>
    <script type="text/javascript">
    try {
        (function () {
            var loadOnlineServer = function() {
                seajs.config({
                    comboExcludes: /\/u\/(js|css|cschannel|ecmng)\//,
                    alias: {
						'$': 'jquery/jquery/1.7.2/jquery',
                        'onlineServerConfig': 'https://os.alipayobjects.com/rmsportal/iwBOQWtuJpTikoO.js',
                        'portalServerConfig': 'https://os.alipayobjects.com/rmsportal/FiPHyRpEbxSvFkDoPXIQ.js',
                        'merchantServerConfig': 'https://gw.alipayobjects.com/os/cschannel/GzeMRFgcwZUcSDQmqnyQ.js',
                        'customerServerConfig': 'https://gw.alipayobjects.com/os/cschannel/eKIrsHTTgHXrEJIaDKxq.js',
			'koubeiServerConfig': 'https://gw.alipayobjects.com/os/cschannel/pQmbmblGTxzzURaFbUca.js',
			'defaultDataConfig': 'https://a.alipayobjects.com/u/js/201311/1acIoVU1Xx.js',
                        'onlineServerJS': 'https://gw.alipayobjects.com/os/rmsportal/mSjEKuaHQmFkwmPHOEJA.js',//云客服匹配
                        'onlineServerCSS': 'https://gw.alipayobjects.com/os/rmsportal/BAjEiJgLNsuAonLHiOli.css'//云客服通用样式
                    }
                });
                seajs.use(['onlineServerConfig', 'portalServerConfig','merchantServerConfig','koubeiServerConfig', 'customerServerConfig'], function(){
                    jQuery(function(){
                        window.OS = OS = {},
                        OS.server = {
                            cliveServer: 'https://clive.alipay.com',
                            cschannelServer: 'https://cschannel.alipay.com',
                            initiativeServer: 'https://webpushgw.alipay.com',
			    cshallServer: 'https://cshall.alipay.com'
                        },
                        OS.params = {
                            'uid': '2088702698723581'
                        };
			var tradeNos4Clive = '' || '';
			OS.params.featureStr = "{'tradeNos':'" + tradeNos4Clive + "'}";
                        OS.config = {
                            onlineServerURL: OS.server.cliveServer + '/csrouter.htm',
                            portalServerURL: OS.server.cschannelServer + '/csrouter.htm',
			    newPortalServerURL: OS.server.cschannelServer + '/newPortal.htm',
                            webpushFlashURL: 'https://t.alipayobjects.com/tfscom/T1JsNfXoxiXXXXXXXX.swf',
                            onlineServerIconDefault: 'https://a.alipayobjects.com/u/css/201401/1v9cu1dxaf.css' //在线客服默认图片
                        };
                        seajs.use('onlineServerCSS');
                        seajs.use('onlineServerJS');
                    });
                });
            }
            var bindOnlineServer = function(func){
                var w = window;
                if (w.attachEvent) {
                    w.attachEvent('onload', func);
                } else {
                    w.addEventListener('load', func, false);
                }
            };
            window.initOnlineServer = function() {
                var w = window, o = 'seajs', d = document;
                if(w[o]) { return loadOnlineServer() }
                var s = d.createElement("script")
                s.id = o + "node"
                s.charset = "utf-8";
                s.type = "text/javascript";
                s.src = "https://a.alipayobjects.com/??seajs/seajs/2.1.1/sea.js,jquery/jquery/1.7.2/jquery.js";
                var head = d.head || d.getElementsByTagName( "head" )[0] || d.documentElement;
                head.appendChild(s);
                s.onload = s.onreadystatechange = function(){ if (!s.readyState || /loaded|complete/.test(s.readyState)) { loadOnlineServer() } };
            };
            if (!window.isLazyLoadOnlineService) {
                bindOnlineServer(initOnlineServer);
            };
        })();
    } catch (e) {
        window.console &amp;&amp; console.log &amp;&amp; console.log(e);
        window.Tracker &amp;&amp; Tracker.click('onlineServer-error-init-' + e);
    }
    </script>
<!-- FD:alipay-foot:alipay/foot/cliveService.vm:cliveService.schema:END -->

<!-- FD:alipay-foot:alipay/foot/cliveService.vm:END -->




<!-- uitpl:/component/tracker.vm -->
<!-- FD:106:alipay/tracker/tracker.vm:START --><!-- FD:106:alipay/tracker/tracker.vm:785:tracker.schema:全站自动化/性能/敏感信息打点开关:START -->



<script type="text/javascript">
window.Smartracker &amp;&amp; Smartracker.sow &amp;&amp; Smartracker.sow();
</script>






<script type="text/javascript">

window.agp_custom_config = {
  BASE_URL: '//kcart.alipay.com/p.gif',
  TIMING_ACTION_URL: '//kcart.alipay.com/x.gif'
}

</script>
<script charset="utf-8" src="https://a.alipayobjects.com/g/memberAsset/securityMsg/1.0.3/index.js"></script>





<!-- FD:106:alipay/tracker/sai.vm:START --><script>
    sensScanConfig={
        ratio: 0.01,
        modules: '*',
        types: '*'
      };
</script>

<script src="https://as.alipayobjects.com/g/alipay_security/monitor-sens/1.0.1/monitor-sens.min.js"></script>
<!-- FD:106:alipay/tracker/sai.vm:END -->




<!-- FD:106:alipay/tracker/cmsbuffer.vm:START --><!-- FD:106:alipay/tracker/cmsbuffer.vm:997:cmsbuffer.schema:main-CMS全站修复:START -->

























<script>
try {
  (function() {
  var logServer = 'https://magentmng.alipay.com/m.gif';
  var sample = 0.0001;
  var url = "https://a.alipayobjects.com/http-watch/1.0.7/index.js";

  // 判断比例
  if (!!window.addEventListener &amp;&amp; Array.prototype.map &amp;&amp; Math.random() &lt; sample) {
    var HEAD = document.head || document.getElementsByTagName('head')[0];

    var spt = document.createElement('script');
    spt.src = url;
    HEAD.appendChild(spt);

	setTimeout(function() {
	  window.httpWatch &amp;&amp; window.httpWatch({ sample: 1, appname: 'personalweb-30-5410', logServer: logServer });
	}, 1000);
  }
  })();
} catch(e) {}
</script>

<!-- FD:106:alipay/tracker/cmsbuffer.vm:997:cmsbuffer.schema:main-CMS全站修复:END -->
<!-- FD:106:alipay/tracker/cmsbuffer.vm:END -->
<!-- FD:106:alipay/tracker/tracker.vm:785:tracker.schema:全站自动化/性能/敏感信息打点开关:END -->
<!-- FD:106:alipay/tracker/tracker.vm:END -->
  <!-- FD:106:alipay/tracker/heat_tracker.vm:START -->

<script type="text/javascript" charset="utf-8" src="https://a.alipayobjects.com/ar/??alipay.heatmap.heattracker-1.3.js"></script>
<!-- FD:106:alipay/tracker/heat_tracker.vm:END -->
  <script>window.context = {"userBehavior":{"trendTabPosition":1},"xboxSwitch":{"securityUser":"on","wirelessUser":"off","mFundDeposited":"on","yebAutoTransferred":"off","realName":"on","quickPay":"on"},"uriBroker":{"personalportal.url":"https://personalportal.alipay.com","personal.url":"https://lab.alipay.com","couriercore.url":"https://couriercore.alipay.com","personalweb.url":"https://personalweb.alipay.com","tfsImage.url":"https://tfsimg.alipay.com","shenghuo.url":"https://shenghuo.alipay.com","cbu.url":"http://china.alibaba.com","consumeprod.url":"https://consumeprod.alipay.com","consumeprod.tile.url":"http://consumeprod-pool.rz12a.alipay.com","zhangdan.url":"https://zd.alipay.com","pointprod.url":"https://jf.alipay.com","fundcardprod.url":"https://card.alipay.com","pcreditprod.url":"https://f.alipay.com","memberprod.url":"https://memberprod.alipay.com","financeprod.url":"https://financeprod.alipay.com","yebprod.url":"https://yebprod.alipay.com","benefitprod.url":"https://zht.alipay.com","appstore.url":"https://app.alipay.com","couponweb.url":"https://hongbao.alipay.com","securitycenter.url":"https://securitycenter.alipay.com","certify.url":"https://certify.alipay.com","productchannelKuai.url":"https://kuai.alipay.com","zhaocaibao.url":"https://zhaocaibao.alipay.com","merchantweb.url":"https://shanghu.alipay.com","uemprod.url":"http://uemprod.rz12a.alipay.com","mrchportalweb.url":"https://mrchportalweb.alipay.com","enterpriseportal.url":"https://enterpriseportal.alipay.com","membercenter.url":"https://accounts.alipay.com","securityassistant.url":"https://securityassistant.alipay.com","member.taobao.url":"http://member1.taobao.com:80","cshall.url":"https://cshall.alipay.com","baoxianprod.url":"https://baoxian.alipay.com","goldetfprod.url":"https://goldetfprod.alipay.com","openauth.url":"https://openauth.alipay.com","promoadprod.url":"https://promoadprod.alipay.com","custweb.url":"https://custweb.alipay.com","consumeweb.url":"https://consumeweb.alipay.com","lab.url":"https://lab.alipay.com","jf.url":"https://jf.alipay.com","hongbao.url":"https://hongbao.alipay.com","card.url":"https://card.alipay.com","zht.url":"https://zht.alipay.com","f.url":"https://f.alipay.com","aliloan.aso.url":"http://login.taobao.com","aliloan.cbu.url":"https://dk.aliloan.com","aliloan.gateway.url":"https://openapi.aliloan.com","aliloan.taobao.url":"https://taobao.aliloan.com","zdrmdata.rest.url":"http://zdrmdata-pool.rz12a.alipay.com","assets.url":"https://a.alipayobjects.com","favicon.ico.url":"https://i.alipayobjects.com/common/favicon/favicon.ico","app.404.url":"https://www.alipay.com/404.html","app.errorpage.url":"https://www.alipay.com/50x.html","authcenter.url":"https://auth.alipay.com","app.goto.url":"https://my.alipay.com/portal/i.htm","bumng.url":"https://bumng.alipay.com","rds.url":"https://rds.alipay.com"}};</script><script crossorigin="anonymous" type="text/javascript" src="https://a.alipayobjects.com/personalweb/app_views_home_html_js-a64f5b3f5eadb886037b.js"></script>

<div id="onlineService" style="top:228px;right:0" seed="online-service" data-sourceid="scene_59"><a href="javascript:void(0)" seed="" style="position:relative;display:inline-block;"><img style="display: block;" src="https://i.alipayobjects.com/e/201401/1tdi7nR70h.png" /><span title="关闭" class="J-close-online-service-trigger" style="position: absolute;right:5px;top:-12px;font-size:14px;background:#eee;padding:1px 2px;border-radius:3px;font-family:simsun;line-height: normal;color: #AC593F;" seed="pcportal_close_icon_trigger">×</span></a></div><div class="ui-autocomplete" data-widget-cid="widget-7" style="z-index: 99; display: none; position: absolute; left: -9999px; top: -9999px;">
    <ul class="ui-autocomplete-ctn" data-role="items">
        <li class="search-no-item">
            无匹配的产品和服务
        </li>
        <li class="search-help" data-value="">
            <a id="J-search-help-link" href="" target="_blank" seed="myalipay-search-help">
                “<span id="J-search-help-text"></span>” 相关的帮助
            </a>
        </li>
    </ul>
</div></body></html>

'''
# tt.encode('utf8').decode('utf8')
page_sel = scrapy.Selector(text=tt)
# result = page_sel.xpath('string(//*[@id="J-assets-pcredit"]/div/div/div[2]/div/p[2]/span/strong)').extract_first()
result = page_sel.xpath('//*[@id="credit-amount-container"]/span/text()').extract_first()
print(result)

# python本身默认编码为unicode
# 所有编码转换时都需通过unicode
msg = "北京"
print(msg.encode(encoding="utf-8"))  # unicode编码转换为utf-8编码
print(msg.encode(encoding="utf-8").decode(encoding="utf-8"))  # unicode编码转换为utf-8编码，再转化为unicode编码
