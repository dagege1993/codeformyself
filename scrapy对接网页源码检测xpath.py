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

	for (var i=0, rule, l=whitelist.length; i<l; i++){
	  rule = whitelist[i];
	  if (
	    (isString(rule) && uri.indexOf(rule) === 0) ||
	    (isRegExp(rule) && rule.test(uri))
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
seajs.cache['https://a.alipayobjects.com:443/gallery' + JQ] = seajs.cache['https://a.alipayobjects.com:443/jquery' + JQ];

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
    for (var i = 0; i < arr.length; i++) {
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
	for (var i = 0; i < arr.length; i++) {
        ret.push(fn(arr[i], i, arr));
    }
    return ret;
  };

function contains(arr, item) {
  return util.indexOf(arr, item) > -1
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
  window.Tracker && Tracker.start &&  Tracker.start();
</script>







<!-- FD:106:alipay/tracker/tracker_time.vm:784:tracker_time.schema:全站 tracker 开关:END -->
<!-- FD:106:alipay/tracker/tracker_time.vm:END -->


<link charset="utf-8" rel="stylesheet" href="https://a.alipayobjects.com:443/al/alice.style.account-1.4.css" media="all" />
<link charset="utf-8" rel="stylesheet" href="https://a.alipayobjects.com:443/consumeprod-record/1.8.6/consumeprod.record.normal.css" media="all" />

  </head>
<!--[if lt IE 7]><body class="ie6 "><![endif]-->
<!--[if IE 7]><body class="ie7 "><![endif]-->
<!--[if IE 8]><body class="ie8 "><![endif]-->
<!--[if IE 9]><body class="ie9 "><![endif]-->
<!--[if !IE]><!--><body class=""><!--<![endif]-->
<script type="text/javascript">
AralePreload = [];
var AP = AP || {};
AP.PageVar = {
  app_domain:"https://consumeprod.alipay.com:443",
  appstore_domain: "https://app.alipay.com",
  personal_domain:"https://lab.alipay.com",
  personalprod_domain:"https://shenghuo.alipay.com",
  mipgw_domain:"",
  ccrprod_domain:"https://ccrprod.alipay.com",
  zhangdan_domain:"https://zd.alipay.com",
  benefits_domain:"",
  image_domain:"https://img.alipay.com:443",
  communityweb_domain: "",
  tfs_domain:"https://tfsimg.alipay.com:443",
  benefitprod_domain:"https://zht.alipay.com"
}
</script>
<style>
#container {padding-top: 1px;}
</style>

<!-- uninav -->








<!-- FD:231:alipay/nav/navSwitch.vm:START --><!-- FD:231:alipay/nav/navSwitch.vm:1740:nav/navSwitch.schema:navSwitch-ABTEST_GLOBAL_P:START -->







<script>
MSGSWITCH = true;
</script>



<script>
MERCHANT_SWITCH = 'true';
</script>


<!-- FD:231:alipay/nav/versionSwitch.vm:START --><!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:START -->







<!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:END --><!-- FD:231:alipay/nav/versionSwitch.vm:END --><!-- FD:231:alipay/nav/navSwitch.vm:1740:nav/navSwitch.schema:navSwitch-ABTEST_GLOBAL_P:END --><!-- FD:231:alipay/nav/navSwitch.vm:END --><!-- abtestEnabled: false -->

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
<div id="J-global-notice-ssl" class="global-notice-announcement ssl-v3-rc4" style="background-color: #ff6600;">
  <p>您的浏览器版本太低，为保障信息的安全，<a href="https://www.alipay.com/x/kill-ie.htm">请于2月28日前升级浏览器</a></p>
</div>
<script>
  /*
   * 获取cookie
   * @param {String} ctoken
   */
  function getCookie(name) {
    if (document.cookie.length > 0) {
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
      if (sslUpgradeTag && sslUpgradeTag === '1') {
        // 展示升级公告
        globalNoticeSsl.setAttribute('class', 'global-notice-announcement');
      } else {
        // 删除升级公告
        globalNoticeSsl.parentNode.removeChild(globalNoticeSsl);
      }
    }
  }
</script>

<!-- FD:231:alipay/notice/headNotice.vm:5381:notice/headNotice.schema:headNotice-全站公告:END --><!-- FD:231:alipay/notice/headNotice.vm:END --></div>




<!--[if lt IE 8]><script>location.href = 'https://www.alipay.com/x/kill-ie.htm';</script><![endif]-->



<div id="J-nav-container" class="nav-common">
</div>

<script type="text/javascript">

// Domain
document.domain = document.domain.split(".").slice(-2).join(".");

// Compatible for xbox
(function (win) {
  function noop() {}

  function fake(namespace, method) {
    namespace = namespace.split('.');

    var target = win, len = namespace.length, index = 0, ns;

    for (; index < len; index++) {
      ns = namespace[index];

      if (!target[ns]) {
        target[ns] = {};
      }

      target = target[ns];
    }

    if (typeof target[method] !== 'function') {
      target[method] = noop;
    }
  }

  fake('mytip', 'show');
  fake('AP.pk.pa.asidePortrait', 'renew');
}(window));

// Global nav data
window.GLOBAL_NAV_DATA = {
  nav: 'account:myrecord',
  navData: '',
  customNav: '',
  appKey: '',
  catKey: '',
  title: '我的账单 - 支付宝',
  pageName: '',
  userName : '黄令志',
  email: '182******29',
  mobile: '182******29',
  logonIdType: 'MOBILE',
  userId: '2088702698723581',
  portraitPath: '/images/partner/T1sGlfXbpXXXXXXXXX',
  container : '#J-nav-container',
  timestamp : new Date().getTime(),
  pageAbsUrl : 'http://consumeprod.alipay.com/record/standard.htm',
  isLogin : true,
  showTaobaoLogin : false,
  showAlibabaLogin : false,
  showMerchant : false,
  showPersonal : false,
  merchantSwitch: window.MERCHANT_SWITCH,
  uriBrokers: GLOBAL.system
};
</script>

<!-- FD:231:alipay/nav/nav_js.vm:START --><!-- FD:231:alipay/nav/nav_js.vm:1739:nav/nav_js.schema:nav_js-开启导航引用埋点隐藏为关闭:START -->


<script src="https://a.alipayobjects.com:443/alipay-nav/2.4.19/global.js" charset="utf-8"></script>
<!-- FD:231:alipay/nav/nav_js.vm:1739:nav/nav_js.schema:nav_js-开启导航引用埋点隐藏为关闭:END --><!-- FD:231:alipay/nav/nav_js.vm:END -->

 <div id="container" class="ui-container">
 
 
<div id="content" class="ui-content fn-clear" coor-rate="0.02" coor="default">



    <!--主交易记录区域start-->
    <div class="operate-area" coor="operate" >
		<div id="test_div"></div>
        <div class="area-content limit-width  ">
            <!--大促公告start-->
            <!-- FD:74:consumeprod/record/standard_notice.vm:START --><!-- FD:74:consumeprod/record/standard_notice.vm:413:standard_notice.schema:standard_notice-大促消费记录标准版公告:START -->
<style>
  .cms-ad{
    color: rgb(230, 68,3);
    font-size: 12px;
    background: rgb(254,243,127);
    margin-bottom: 10px;
    padding: 5px;
    display: block;
    text-align: center;
  }
</style>



<!-- FD:74:consumeprod/record/standard_notice.vm:413:standard_notice.schema:standard_notice-大促消费记录标准版公告:END --><!-- FD:74:consumeprod/record/standard_notice.vm:END -->            <!--标题区域start-->
            <div class="ui-title fn-clear gradient-line">
                <h2 class="fn-left">我的账单</h2>
                                    <div class="link">
                        <a href="https://consumeprod.alipay.com:443/record/switchVersion.htm">切换到高级版</a>
                    </div>
                                                <div class="action">
                                        可用余额
                    <em class="ft-green">
                      <strong>0.00</strong>
                    </em> 元
                  <em class="ft-bar">|</em>

                <a target="_blank" href="https://lab.alipay.com/consume/record/items.htm">
                    余额收支明细
                  </a>
                  <em class="ft-bar">|</em>
				                    <a target="_blank" href="https://consumeprod.alipay.com:443/record/trashIndex.htm" class="trash-index" seed="trash-link">
                    回收站
                  </a>
                </div>
            </div>
            <!--标题区域end-->

            <!--搜索区域start-->
            


<form coor="form"  name="topSearchForm" id="topSearchForm" class="record-search-form  record-search-min " action="" method="get">

<div class="record-search-date" id="J-search-date-container">
	<div class="ui-form-item ui-form-item-time">
		<label class="ui-form-label">时间：</label>
		<div class="ui-form-item-content">
			<div class="range-quick-date fn-clear" >
				<div class="quick-input-date fn-left">
					<input type="text" name="beginDate" id="beginDate" value="2018.08.18" readonly="readonly" tabindex="1" class="date-search-input" autocomplete="off" />
					<span class="ui-separator-pd">-</span>
					<input type="text" name="endDate" id="endDate" value="2018.09.18" readonly="readonly" tabindex="2" class="date-search-input" autocomplete="off" />
     
				</div>

                <div class="quick-link-date gray-links fn-left">
                    
                        <a id="J-today"  class="inline-item dateRange-trigger"  href="javascript:;" dateRange="today">今天</a>
                        <em class="ft-bar">|</em>
                        <span class="inline-text" >最近：</span>
                        <a id="J-one-month"  class="inline-item active dateRange-trigger"   href="javascript:;" dateRange="oneMonth">1个月</a>
                        <a id="J-three-month"  class="inline-item dateRange-trigger"  href="javascript:;" dateRange="threeMonths">3个月</a>
                        <a id="J-one-year"  class="inline-item dateRange-trigger"   href="javascript:;" dateRange="oneYear">1年</a>
                    
				</div>
			</div>
		</div>
	</div>
</div>    <div class="record-search-params">


<div class="record-search-cate">     <div class="ui-form-item">
		<label class="ui-form-label ui-label-text">分类：</label>
		<div class="ui-form-item-content gray-links" id="J-consume-category">
        			<a  class="active inline-item category-trigger"  href="javascript:;" tradeType="ALL">全部</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="SHOPPING">购物</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="OFFLINENETSHOPPING">线下</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="FINANCE">理财</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="TRANSFER">转账</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="CCR">还款</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="PUC_CHARGE">缴费</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="DEPOSIT">充值</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="WITHDRAW">提现</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="PERLOAN">还贷款</a>
					<a  class="inline-item category-trigger"  href="javascript:;" tradeType="MOBILE_RECHARGE">手机充值</a>
				</div>
	</div>
</div>

<div class="record-search-state fn-clear">      <!--小C交易状态-->
	<div class="ui-form-item">
		<label class="ui-form-label ui-label-text">状态：</label>
        <div class="ui-form-item-content gray-links" id="J-consume-category">
            			    <a  class="active inline-item status-trigger"  href="javascript:;" status="all">全部</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="inProcess">进行中</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="waitPay">未付款</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="waitSendGoods">等待发货</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="waitConfirmGoods">未确认收货</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="refund">退款</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="success">成功</a>
		    			    <a  class="inline-item status-trigger"   href="javascript:;" status="fail">失败</a>
		    		</div>
	</div>
	<a seed="CR-AdvancedFilter" href="javascript:;" class="ui-btn-mini-more fn-right J-toggle-advanced open">高级筛选<span class="record-icon">&#xe626;</span></a>
</div>

<div class="record-search-option">
	<div id="J-search-amount-container" class="record-search-amount">  		<div class="ui-form-item">
			<label class="ui-form-label" >金额：</label>
			<div class="ui-form-item-content J-edit-box fn-pr">
				<div class="amount-input fn-left">
					<input type="text" id="minAmount" value="" name="minAmount" seed="CR-money-min" style="ime-mode: disabled" class="ui-input ui-input-len10" autocomplete="off" />
					<span class="ui-separator-pd">-</span>
					<input type="text" id="maxAmount" value="" name="maxAmount" seed="CR-money-max" style="ime-mode: disabled" class="ui-input ui-input-len10" autocomplete="off" />
				</div>
				<a href="javascript:;" class="ui-button sure fn-left" id="J-amount-btn">
					确定
				</a>
                <a href="javascript:;" class="ui-button quit fn-left" id="J-amount-quit-btn">
                    清除
                </a>
			</div>
		</div>
	</div>


	<div id="J-search-keyword-container" class="record-search-keyword fn-clear">  		<div class="ui-form-item fn-left">
			<label class="ui-form-label">关键词：</label>
			<div class="ui-form-item-content J-edit-box fn-pr">
				<div class="amount-input fn-left">
					<input type="text" maxlength="200" placeholder="输入对方名称、交易名称、交易号、商户订单号、备注等关键词" id="J-keyword" value="" name="keyValue" class="search-keyword" seed="CR-keywords-import" autocomplete="off" />
                    <label for="J-keyword" class="placeholder-for-ie fn-hide">输入对方名称、交易名称、交易号、商户订单号、备注等关键词</label>
				</div>
				<a href="javascript:;" class="ui-button fn-left" id="J-keyword-btn">
					确定
				</a>
			</div>

		</div>
		<a href="" class="ui-btn-mini-more fn-right J-toggle-advanced close">基本筛选<span class="record-icon">&#xe627;</span></a>
	</div>
</div>

<script type="text/javascript">

seajs.use('consumeprod-record/1.1.7/knight', function(knight) {
    var knightObj = knight || window.knight;
    var $ = jquery = knightObj.$;

    $(function() {
        // 显示和隐藏高级筛选选项
        var moment = knightObj.gallery.moment;

        $('.J-toggle-advanced').click(function(e) {
            $('#topSearchForm').toggleClass('record-search-max').toggleClass('record-search-min');
            e.preventDefault();
        });

    });


    // 金额范围
    $(function() {
        var labelNode = $('.placeholder-for-ie');
        $('.J-edit-box :input').each(function(i, item) {
            item = $(item);
            item.data('oldValue', item.val());
        });

        // 金额范围和关键词，focus 时出现确定链接
        $('.J-edit-box :input').focus(function(e) {
            var c = $(e.target).parents('.J-edit-box');
            
            c.addClass('showBox');
            var target= $(e.target);
            var h = function(e) {

                if (!c.has(e.target).length) {
                    target.val(target.data('oldValue')).trigger('change');
                    c.removeClass('showBox');
                    if(labelNode.hasClass('ie')){
                        var oldValue = target.data('oldValue');
                 
                        oldValue && jquery.trim(oldValue) !== '' ? '' : labelNode.removeClass('fn-hide');
                    }
                    
                  
                    $(document.body).off('click', h);
                    $('.J-edit-box :input').off('focus', h);
                }
            };
            $(document.body).on('click', h);
            // firefox 下 focus 的时候有时候不会触发 body 的 click 事件，所以这里再绑定一下。
            $('.J-edit-box :input').on('focus', h);
        });

        // 关键词点击确定跳转查询
        $('#J-keyword-btn').click(function(e) {
            e.preventDefault();
			var keyvalue = $('#J-keyword').val();
			var URI = knightObj.biz.URI;
            if(labelNode.hasClass('ie')){
                keyvalue !== '' ? '' : labelNode.removeClass('fn-hide');
            }
            //var url = URI(document.location.href);
            //var data = url.search(true);
            //for(var e in data) {
                //url.removeSearch(e);
            //}
            //url.removeSearch('keyword').addSearch('keyword', 'ordinaryInfo').removeSearch('keyValue').addSearch('keyValue', keyvalue).removeSearch('pageNum').removeSearch('_input_charset').addSearch('_input_charset', 'utf-8');
            // 要做个正则替换，因为 ie6-7 中 url.toString 会生成'http://alipay.net//record/...' record 前面多斜杠，导致 cookie 获取失败
            //document.location.href = url.toString().replace(/\/+record\//g, '\/record\/');
			
			cleanQueryData();
			
			submitQueryForm({
			    "pageNum":"1",
				"keyword":"ordinaryInfo",
				"keyValue":keyvalue
			});
        });
        
    });
    $(function () {
        // placehoder 兼容IE
        function placeholderCompatibleToIE (nodes) {
            var inputNode = document.createElement('input');
            var labelNode = $('.placeholder-for-ie');
            if(nodes.length && !('placeholder' in inputNode)) {
                labelNode.addClass('ie');
                
                nodes.on('focus' ,function () {
                    labelNode.addClass('fn-hide');
                });

                var oldValue = nodes.data('oldValue');
                oldValue && jquery.trim(oldValue) !== '' ?  '' : labelNode.removeClass('fn-hide');
                
            }
            
        }
        placeholderCompatibleToIE($('#J-keyword'));
    })

});
</script>

    </div>
</form>


<style>
 .query-checkbox{
 display:none;
 }
</style>
<form name="queryForm" id="queryForm" action="standard.htm" method="post">
  <input type="hidden" name="dateType" id="query-dateType" class="query-text" value="createDate" />
  <input type="hidden" name="dateRange" id="query-dateRange" class="query-text" value="oneMonth" />
  <input type="hidden" name="beginDate" id="query-beginDate" class="query-text" value="2018.08.18" />
  <input type="hidden" name="endDate" id="query-endDate" class="query-text" value="2018.09.18" />
  <input type="hidden" name="beginTime" id="query-beginTime" class="query-text" value="00:00" />
  <input type="hidden" name="endTime" id="query-endTime" class="query-text" value="24:00" />
  <input type="hidden" name="tradeType" id="query-tradeType" class="query-text" value="ALL" />
  <input type="hidden" name="status" id="query-status" class="query-text" value="all" />
  <input type="hidden" name="fundFlow" id="query-fundFlow" class="query-text" value="all" />
  <input type="hidden" name="keyword" id="query-keyword" class="query-text" value="" />
  <input type="hidden" name="keyValue" id="query-keyValue" class="query-text" value="" />
  <input type="hidden" name="minAmount" id="query-minAmount" class="query-text" value="" />
  <input type="hidden" name="maxAmount" id="query-maxAmount" class="query-text" value="" />
  <input type="hidden" name="pageNum" id="query-pageNum" class="query-text" value="1" />
  <input type="hidden" name="rdsToken" id="query-rdsToken" class="query-text" value="" />
  <input type="hidden" name="rdsUa" id="query-rdsUa" class="query-text" value="" />
  <input type="checkbox" name="tradeModes" id="query-tradeModes_S" class="query-checkbox" value="S" />
  <input type="checkbox" name="tradeModes" id="query-tradeModes_FP" class="query-checkbox" value="FP" />
  <input type="checkbox" name="tradeModes" id="query-tradeModes_COD" class="query-checkbox" value="COD" />
</form>

<script type="text/javascript">
	var form_tk = "QKuyuU7xdpVdmTD6UdrzU9NJSrOylTzt";
	var json_ua = null;// 鍒嗗埆瀛樺偍token鍜寀a鏁版嵁
</script>
<script type="text/javascript" src="https://rds.alipay.com/ua_consumeprod_record_standard.js?t=2018091717"></script>

<script type="text/javascript">

/**
* 鏇存柊queryForm琛ㄥ崟鏁版嵁
*/
function freshQueryForm(query){
  
  var queryForm = $("#queryForm");
  if(!query){
    return;
  }

  var refreshTradeModes = false;
	
  for(var attrs in query){
    var attrsValue = query[attrs];
	var queryParam = queryForm.find('#query-'+attrs);
	
	//浜ゆ槗绫诲瀷checkbox鐗规畩澶勭悊锛屽疄闄呬笂骞朵笉浼氱敤鍒帮紝鍥犱负鐩墠灏廋涓嶆敮鎸乼radeMode checkbox
	if(attrs.match('^tradeModes')){
      if(!refreshTradeModes){
        queryForm.find('[name=tradeModes]').prop({checked:false});
		refreshTradeModes = true;
      }
	  queryParam.prop({checked:true});
	}else{
      if(queryParam.length > 0){
        queryParam.val(attrsValue);
      }
	}
  }
};

/**
* 鏇挎崲query涓殑鏁版嵁锛屽苟鍒锋柊rds鏁版嵁锛屾彁浜ueryForm
*/
function submitQueryForm(query){
  
  query.rdsToken = form_tk;
  query.rdsUa = json_ua;
  
  freshQueryForm(query);
  var queryForm = $("#queryForm");
  queryForm.submit();
};

/**
* 鑾峰彇queryForm涓綋鍓嶇殑鏌ヨ鍙傛暟
*/
function getQueryData(attrName){

  var queryForm = $("#queryForm");
  return queryForm.find('#query-'+attrName).val();

}

/**
* 娓呯┖琛ㄥ崟锛岀敤浜庡皬C鐢ㄦ埛鎸夌収鍏抽敭瀛楁悳绱㈠墠娓呯┖鍏朵粬鏉′欢
*/
function cleanQueryData(){
    $(".query-text").val("");
	$(".query-checkbox").prop({checked:false});
}
</script>
<script>
seajs.use('consumeprod-record/1.1.7/knight', function() {
    var $ = knight.$,
        jquery = $;
        

    $(function() {
        // 限制金额范围 input 只能输入数字
        $('#J-search-amount-container input').keydown(function(e) {
            var target = $(e.target);
            var val = target.val();
            if (!(isNaN(val) || /[a-zA-Z-]/.test(val))) {
                target.data('old_value', val)
            }
        });
        $('#J-search-amount-container input').keyup(function(e) {
            var target = $(e.target);
            var val = target.val();
            if (isNaN(val) || /[a-zA-Z-]/.test(val)) {
                target.val(target.data('old_value'));
            }
        });

        //金额范围处理：若最小值大于最小值，交换
        function validateAmount() {
            var AMOUNT_REGEXP = /^[1-9][0-9]*(\.[0-9]{0,2})?$/;
            var min_input = $('#J-search-amount-container [name=minAmount]'),
                max_input = $('#J-search-amount-container [name=maxAmount]'),
                min = jquery.trim(min_input.val()),
                max = jquery.trim(max_input.val());
              
            if ((min && max) && (Number(min) > Number(max))) {
                min_input.val(max);
                max_input.val(min);
            }

        }
        // 小C金额范围处理：点击提交时的处理
        $('#J-amount-btn').click(function(e) {
            e.preventDefault();
            validateAmount();
            var min_input = $('#J-search-amount-container [name=minAmount]'),
            max_input = $('#J-search-amount-container [name=maxAmount]'),
            min = min_input.val(),
            max = max_input.val();
            triggerQueryByAmount(max, min);
        });
        $('#J-amount-quit-btn').click(function (e) {
            e.preventDefault();
            var min_input = $('#J-search-amount-container [name=minAmount]'),
            max_input = $('#J-search-amount-container [name=maxAmount]');
            min_input.val('').data('oldValue', '');
            max_input.val('').data('oldValue', '');
            min_old = '',
            max_old = '';
            if(max_old === "" && min_old === "" ){
                max_input.parents('.ui-form-item-content').removeClass('showBox');
                return;
            }
            validateAmount();
            triggerQueryByAmount('', '');
        });
        $(document.body).keyup(function (e) {
            var event = e || window.event;
            var keyValue = event.which || event.keyCode;
            if(keyValue === 13){
                $('#J-search-amount-container .J-edit-box').hasClass('showBox') && $('#J-amount-btn').click();
                $('#J-search-keyword-container .J-edit-box').hasClass('showBox') && $('#J-keyword-btn').click();
            }
        })
        
    });
    function triggerQueryByAmount (max, min) {
        
        submitQueryForm({
            'pageNum':'1',
            'minAmount':min,
            'maxAmount':max
        });
    }
    
});
</script>

<script>
seajs.use('consumeprod-record/1.1.7/knight', function() {
    var $ = knight.$;
    $(function() {
	   
		$(".category-trigger").click(function (e) {
            e.preventDefault();
            $('#queryForm #query-keyValue').val('');//清空关键词
			triggerQueryByCategory($(this).attr("tradeType"));
		});
		$(".dateRange-trigger").click(function (e) {
            e.preventDefault();
			triggerQueryByDateRange($(this).attr("dateRange"));
		});
		$(".status-trigger").click(function (e) {
            e.preventDefault();
            $('#queryForm #query-keyValue').val('');//清空关键词
			triggerQueryByStatus($(this).attr("status"));
		});
		
	});
	//点击“今天” “一年”等dateRange
	function triggerQueryByDateRange(dateRange){
	    submitQueryForm({
            'pageNum':'1',
            'dateRange':dateRange
        });
	}
	//点击分类选项
	function triggerQueryByCategory(categoryName){
	    submitQueryForm({
            'pageNum':'1',
            'tradeType':categoryName
        });
	}
	//点击交易状态选项
	function triggerQueryByStatus(statusValue){
	    submitQueryForm({
            'pageNum':'1',
            'status':statusValue
        });
	}
});
</script>

<script>
seajs.use('consumeprod-record/1.1.7/knight', function() {
    var Calendar = knight.arale.Calendar,
        Validator = knight.arale.Validator,
        ValidatorCore = knight.arale.ValidatorCore,
        $ = knight.$,
        moment = knight.gallery.moment,
        URI = knight.biz.URI;

    $(function() {
        // 标志位
        var silent = false;

        var DATE_FORMAT = 'YYYY.MM.DD';
        var DATE_DEFAULT = '1999.09.09';

        var startCal = new Calendar({
            trigger: '#beginDate',
            startDay: 'Monday',
            format: DATE_FORMAT,
            showTime: false,
            range: [DATE_DEFAULT, moment('2018.09.18', DATE_FORMAT)],
            onSelectDate: function(date) {
                if (!silent) {
                    endCal.range([DATE_DEFAULT, date.format(DATE_FORMAT)])
                    $('#beginDate').val(date.format(DATE_FORMAT));
                    triggerQueryByCustomDate();
                }
            }
        });
        var endCal = new Calendar({
            trigger: '#endDate',
            startDay: 'Monday',
            format: DATE_FORMAT,
            showTime: false,
            range: [moment('2018.08.18', DATE_FORMAT), moment('2018.09.18', DATE_FORMAT)],
            onSelectDate: function(date) {
                if (!silent) {
                    $('#endDate').val(date.format(DATE_FORMAT));
                    startCal.range([DATE_DEFAULT, date.format(DATE_FORMAT)])
                    triggerQueryByCustomDate();
                }

            }

        });
		//点击自定义日期
        function triggerQueryByCustomDate() {
            var beginDate = $('#beginDate').val(),
                endDate = $('#endDate').val();
			if (getQueryData("beginDate") == beginDate && getQueryData("endDate") == endDate) {
                return;
            }
            
            submitQueryForm({
            	'pageNum':'1',
            	'beginDate':beginDate,
            	'endDate':endDate,
            	'dateRange':'customDate'
        	});
        }

    });
    
});

</script>

<script>
//小C翻页
seajs.use('consumeprod-record/1.1.7/knight', function() {
    var $ = knight.$;
    $(function() {
	   
		$(".page-trigger").click(function (e) {
            e.preventDefault();
			triggerQueryByPage($(this).attr("pageNum"));
		});
		
	});
	
	function triggerQueryByPage(pageNum){
	    submitQueryForm({
            'pageNum':pageNum
        });
	}
	
});
</script>







            <!--搜索区域end-->
            </div>

    </div>
    <div id="J_home-record-container" class="record-area" coor="content"  >
        <!--交易记录列表-->
		    

    <style type="text/css" media="screen">
    	.ui-poptip .ui-poptip-box{
    		min-height: 25px;
    	}
    </style>
    
    
    
    <table class="ui-record-table table-index-bill" id="tradeRecordsIndex" width="100%">
		    
    		<thead>
        		<tr class="record-list-header">
    				<th class="img" width=50>
                        分类
                    </th>
        			<th class="time" width=100>
        				创建时间
        			</th>

        			<th class="name" width=370>
                        名称
                        <em class="ft-bar">|</em>
                        对方
                        <em class="ft-bar">|</em>
                        交易号
                    </th>

        			<th class="amount" width=120>
                        <p>金额</p>
                        
                    </th>

        			<th class="detail" width=100>
                        <p>明细</p>
                    </th>

        			<th class="status" width=150>
                        状态
                    </th>
                    <th class="operation" width=100>
                        操作
                    </th>
        		</tr>
                <tr >
                    <td colspan="7">
                        <div class="record-list-header-bottom gradient-line"></div>
                    </td>
                </tr>

    		</thead>
    		<tbody>
           







        			<tr id="J-item-1" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/mukPPhtdXrnqECpCXXDq.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>今天</p>
        <p class="text-muted">			08:50
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091822001423580574182015&gmtBizCreate=20180918085032"  target="_blank">北京地铁-二维码乘车 9月18日07:55进站乘车，行程记录请前往易通行查看</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				北京轨道交通路网管理有限公司 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-1">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-1" href="javascript:;" data-clipboard-text="2018091822001423580574182015" title="2018091822001423580574182015">			2018...015
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">- 3.87</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091822001423580574182015&gmtBizCreate=			20180918085032
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
                                         



	

		
    
                                           <li class="btn-group-item" seed="trade-detail"  data-link="https://lab.alipay.com/consume/queryTradeDetail.htm?tradeNo=2018091822001423580574182015" data-target="_blank">详情</li>
              
     
 
                            




                            
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=2018091822001423580574182015&createDate=			20180918085032
	&bizType=TRADE" rel-id="" data-type="memo" data-bizId="biz2018091822001423580574182015">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-18 08:50:32
	~2018091822001423580574182015~TRADE" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
			
	    
	    <div class="year-month">
	        <p class="year" >
	          <img class="y2 p0" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png">
	          <img class="y0 p1" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png">
	          <img class="y1 p2" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png">
	          <img class="y8 p3" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png">
	      </p>
	      <p class="month">
	        <img class="m0 p0" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png">
	        <img class="m9 p1" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png">
	      </p>
	      <span class="arrow"></span>
	    </div>
	  </td>


        			</tr>
					


		


           







        			<tr id="J-item-2" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/mukPPhtdXrnqECpCXXDq.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>今天</p>
        <p class="text-muted">			07:42
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091822001423580573556218&gmtBizCreate=20180918074237"  target="_blank">商品</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				毛学莲 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-2">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-2" href="javascript:;" data-clipboard-text="2018091822001423580573556218" title="2018091822001423580573556218">			2018...218
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">- 4.50</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091822001423580573556218&gmtBizCreate=			20180918074237
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
                                         



	

		
    
                                           <li class="btn-group-item" seed="trade-detail"  data-link="https://lab.alipay.com/consume/queryTradeDetail.htm?tradeNo=2018091822001423580573556218" data-target="_blank">详情</li>
              
     
 
                            




                            
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=2018091822001423580573556218&createDate=			20180918074237
	&bizType=TRADE" rel-id="" data-type="memo" data-bizId="biz2018091822001423580573556218">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-18 07:42:37
	~2018091822001423580573556218~TRADE" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-3" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/HMrWjUrCzaboAbeczVqY.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>今天</p>
        <p class="text-muted">			05:08
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=MINITRANS&bizInNo=20180918314232314581&gmtBizCreate=20180918050841"  target="_blank">余额宝-2018.09.17-收益发放</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				中欧基金管理有限公司 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-3">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-3" href="javascript:;" data-clipboard-text="20180918314232314581" title="20180918314232314581">			2018...581
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">+ 0.79</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=MINITRANS&bizInNo=20180918314232314581&gmtBizCreate=			20180918050841
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
        




        
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=20180918314232314581&createDate=			20180918050841
	&bizType=MINITRANS" rel-id="" data-type="memo" data-bizId="biz20180918314232314581">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-18 05:08:41
	~20180918314232314581~MINITRANS"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-4" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/mukPPhtdXrnqECpCXXDq.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>昨天</p>

        <p class="text-muted">			20:57
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091722001423580573004325&gmtBizCreate=20180917205724"  target="_blank">北京地铁-二维码乘车 9月17日19:55进站乘车，行程记录请前往易通行查看</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				北京轨道交通路网管理有限公司 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-4">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-4" href="javascript:;" data-clipboard-text="2018091722001423580573004325" title="2018091722001423580573004325">			2018...325
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">- 3.90</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091722001423580573004325&gmtBizCreate=			20180917205724
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
                                         



	

		
    
                                           <li class="btn-group-item" seed="trade-detail"  data-link="https://lab.alipay.com/consume/queryTradeDetail.htm?tradeNo=2018091722001423580573004325" data-target="_blank">详情</li>
              
     
 
                            




                            
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=2018091722001423580573004325&createDate=			20180917205724
	&bizType=TRADE" rel-id="" data-type="memo" data-bizId="biz2018091722001423580573004325">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-17 20:57:24
	~2018091722001423580573004325~TRADE" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-5" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://pic.alipayobjects.com/oss-fix/i/mobileapp/png/201410/3jU228X11B.png_fix.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>昨天</p>

        <p class="text-muted">			18:06
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=YEB&bizInNo=20180917009130201010580024001279&gmtBizCreate=20180917180650"  target="_blank">余额宝-转出到银行卡</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				中国建设银行 |
                </p>
    		        	
        	        		<p class="no ft-gray p-inline">
        			...1974|*令志 |
        		</p>
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-5">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-5" href="javascript:;" data-clipboard-text="20180917009130201010580024001279" title="20180917009130201010580024001279">			2018...279
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay"> 100.00</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=YEB&bizInNo=20180917009130201010580024001279&gmtBizCreate=			20180917180650
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
          

          <li class="btn-group-item" data-link="https://yebprod.alipay.com/yeb/redeemDetail.htm?orderNo=20180917009130201010580024001279" data-target="_blank">详情</li>
    


          




          
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=20180917009130201010580024001279&createDate=			20180917180650
	&bizType=YEB" rel-id="" data-type="memo" data-bizId="biz20180917009130201010580024001279">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-17 18:06:50
	~20180917009130201010580024001279~YEB" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-6" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/mukPPhtdXrnqECpCXXDq.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>昨天</p>

        <p class="text-muted">			08:49
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091722001423580567924137&gmtBizCreate=20180917084952"  target="_blank">北京地铁-二维码乘车 9月17日07:53进站乘车，行程记录请前往易通行查看</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				北京轨道交通路网管理有限公司 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-6">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-6" href="javascript:;" data-clipboard-text="2018091722001423580567924137" title="2018091722001423580567924137">			2018...137
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">- 3.87</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091722001423580567924137&gmtBizCreate=			20180917084952
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
                                         



	

		
    
                                           <li class="btn-group-item" seed="trade-detail"  data-link="https://lab.alipay.com/consume/queryTradeDetail.htm?tradeNo=2018091722001423580567924137" data-target="_blank">详情</li>
              
     
 
                            




                            
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=2018091722001423580567924137&createDate=			20180917084952
	&bizType=TRADE" rel-id="" data-type="memo" data-bizId="biz2018091722001423580567924137">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-17 08:49:52
	~2018091722001423580567924137~TRADE" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-7" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/mukPPhtdXrnqECpCXXDq.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>昨天</p>

        <p class="text-muted">			07:39
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091722001423580567454054&gmtBizCreate=20180917073950"  target="_blank">商品</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				毛学莲 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-7">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-7" href="javascript:;" data-clipboard-text="2018091722001423580567454054" title="2018091722001423580567454054">			2018...054
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">- 4.50</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=TRADE&bizInNo=2018091722001423580567454054&gmtBizCreate=			20180917073950
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
                                         



	

		
    
                                           <li class="btn-group-item" seed="trade-detail"  data-link="https://lab.alipay.com/consume/queryTradeDetail.htm?tradeNo=2018091722001423580567454054" data-target="_blank">详情</li>
              
     
 
                            




                            
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=2018091722001423580567454054&createDate=			20180917073950
	&bizType=TRADE" rel-id="" data-type="memo" data-bizId="biz2018091722001423580567454054">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-17 07:39:50
	~2018091722001423580567454054~TRADE" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-8" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/HMrWjUrCzaboAbeczVqY.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>昨天</p>

        <p class="text-muted">			05:02
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=MINITRANS&bizInNo=20180917311317869581&gmtBizCreate=20180917050231"  target="_blank">余额宝-2018.09.16-收益发放</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				中欧基金管理有限公司 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-8">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-8" href="javascript:;" data-clipboard-text="20180917311317869581" title="20180917311317869581">			2018...581
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">+ 0.79</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=MINITRANS&bizInNo=20180917311317869581&gmtBizCreate=			20180917050231
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
        




        
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=20180917311317869581&createDate=			20180917050231
	&bizType=MINITRANS" rel-id="" data-type="memo" data-bizId="biz20180917311317869581">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-17 05:02:31
	~20180917311317869581~MINITRANS"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-9" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://gw.alipayobjects.com/zos/mwalletmng/HMrWjUrCzaboAbeczVqY.png >
    </p>
</td>
  <td class="time">
  	
    
          <p>昨天</p>

        <p class="text-muted">			02:12
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=YEB&bizInNo=20180917009130101000580028337767&gmtBizCreate=20180917021220"  target="_blank">余额宝-自动转入</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				中欧基金管理有限公司 |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-9">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-9" href="javascript:;" data-clipboard-text="20180917009130101000580028337767" title="20180917009130101000580028337767">			2018...767
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay"> 64.00</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=YEB&bizInNo=20180917009130101000580028337767&gmtBizCreate=			20180917021220
	">&#xe60b;</a>
	
        
          </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
          

          
          <li class="btn-group-item" seed="trade-detail" data-link="https://yebprod.alipay.com/yeb/payRecord.htm?tradeNo=20180917009130101000580028337767" data-target="_blank">详情</li>
      


          




          
    
        
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=20180917009130101000580028337767&createDate=			20180917021220
	&bizType=YEB" rel-id="" data-type="memo" data-bizId="biz20180917009130101000580028337767">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-17 02:12:20
	~20180917009130101000580028337767~YEB" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


           







        			<tr id="J-item-10" class="J-item ">
           
<td class="img">
  <p class="opposite-img">
        <img src=https://t.alipayobjects.com/images/partner/T1YV8eXolYXXXXXXXX_160X160 >
    </p>
</td>
  <td class="time">
  	
    
          <p>			2018-09-16
	</p>
        <p class="text-muted">			18:49
	</p>
  
  </td>

    



    <td class="name">
		    	<p class="consume-title">
    	                            	<a href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=D_TRANSFER&bizInNo=20180916200040011100070067703905&gmtBizCreate=20180916184907"  target="_blank">转账</a>
                    </p>
    	
				        	
    		                <p class="name p-inline ft-gray">
    				\u5229\u5f3a |
                </p>
    		        	
        			    	
    	    	                        <div class="consume-bizNo ft-gray fn-pr J-tradeNo-container  p-inline" id="J-tradeNo-container-10">
    			流水号
    			
                    			<a class="J-tradeNo-copy J-tradeNo" id="J-tradeNo-10" href="javascript:;" data-clipboard-text="20180916200040011100070067703905" title="20180916200040011100070067703905">			2018...905
	</a>
    		</div>
				
		    
    </td>

    


<td class="amount">
    		                <span class="amount-pay">+ 64.00</span>
        	    </td>

            	


<td class="detail">
  <div class="icon-group">
                        <a class="record-icon icon-detail icon-detail-trigger" data-type="detail" data-date="时间	" href="https://consumeprod.alipay.com:443/record/detail/simpleDetail.htm?bizType=D_TRANSFER&bizInNo=20180916200040011100070067703905&gmtBizCreate=			20180916184907
	">&#xe60b;</a>
	
        
                <span class="record-icon icon-memo " data-info="转账" data-type="memo" data-bizId="biz20180916200040011100070067703905" >&#xe608;</span>
      </div>

</td>



<td class="status">
    	<p class="text-muted">交易成功</p>
		<p class="text-muted"></p>
	
		<p class="ft-gray"></p>
	
	 

<td class="operation">
    <div class="btn-group-wrap">
        <ul class="btn-group">
        






			<li class="btn-group-item" data-link="https://shenghuo.alipay.com/send/queryTransferDetail.htm?tradeNo=20180916200040011100070067703905" data-target="_blank">详情</li>








    




    
    
    
    <li class="btn-group-item" class="split" seed="trade-memo" data-action="edit-memo" data-link="https://consumeprod.alipay.com:443/record/editMemo.htm?bizInNo=20180916200040011100070067703905&createDate=			20180916184907
	&bizType=D_TRANSFER" rel-id="" data-type="memo" data-bizId="biz20180916200040011100070067703905">备注</li>
    
    
            <li class="btn-group-item" seed="trade-delete" data-action="delete" data-link="https://consumeprod.alipay.com:443/record/delete.json?record=			2018-09-16 18:49:07
	~20180916200040011100070067703905~D_TRANSFER" data-fund-change="true"  rel-id="" data-type="del">删除</li>
         
         
        
         </ul>
    </div>

		
	</td>


        			</tr>
					


		


                       		</tbody>

                    </table>
    
            
            
            

            <script>
    seajs.use('consumeprod-record/1.1.7/knight', function() {
        var $ = knight.$,
            PopTip = knight.alipay.PopTip;

            Emoji = knight.biz.Emoji;

        $(function() {
            $('.J-memo-trigger').each(function(i, trigger) {
                trigger = $(trigger);

                // 鼠标悬浮在 pop 框和 trigger 链接上都不消失，离开后消失。

                var p = new PopTip({
                    target: trigger,
                    type: 'text',
                    content: function() {
                        var content = trigger.next('.content-memo');

                        var entry = content.find('.memo-info');
                        //注销emoji
                        //Emoji.render(entry);

                        return content.html();
                    },
                    width: 235,
                    arrowPosition: 7,
                    closable: false
                });
                var h;
                $(trigger).add(p.element).hover(function(e) {
                    clearTimeout(h);
                    p.show();
                    }, function(e) {
                    // 设置 200 ms 延迟使用户有时间用鼠标滑过 trigger 链接和 pop 框直接的缝隙而不隐藏。
                    h = setTimeout(function() {
                        p.hide();
                    }, 200);
                });


                // 点击 trigger 链接，弹出编辑备注 xbox

                var Xbox = knight.alipay.Xbox;
                var iframeurl = trigger.attr('href');
                var x = new Xbox({
                    trigger: trigger,
                    width: 520,
                    height: 414,
                    isOld: true,
                    classPrefix:"ui-newxbox",
                    content: iframeurl
                });

                x.after('show', function() {
                    x.element.find('iframe')[0].on('change:height', function(h) {
                        x.set('height', h);
                    });
                });


            });
        });

    });
</script>
        <script>
seajs.use('consumeprod-record/1.1.7/knight', function() {
    var $ = knight.$,
        ZeroClipboard = knight.biz.zeroclipboard,
        Overlay = knight.arale.Overlay;
    $(function() {
        var triggers = $('.J-tradeNo');
        var client = new ZeroClipboard(triggers);
        var showTip = function() {
            var o = new Overlay({
                template: '<div class="ui-tiptext-container ui-tiptext-container-success" style="padding:5px 8px;width:67px;">' + '<p class="ui-tiptext ui-tiptext-success" style="padding:0 0 0 17px;"><span class="ui-tiptext-icon"></span>复制成功</p>' + '</div>'
            });

            o.after('show', function() {
                setTimeout(function() {
                    o.hide();
                }, 1500);
            });

            return function(trigger) {
                o.set('align', {
                    selfXY: [-12, 20],
                    baseElement: trigger,
                    baseXY: ['100%', '100%']
                });
                o.set('parentNode', trigger.parent('.J-tradeNo-container'));
                o.show();
            }
        }();

        triggers.click(function(e) {
            e.preventDefault();
        });

        client.on('ready', function() {
            client.on('aftercopy', function(client, args) {
                showTip($(client.target));
            });
        });

        client.on('wrongflash noflash', function() {
            ZeroClipboard.destroy();
        });
    });
});
</script>
<script>
seajs.use('consumeprod-record/1.1.7/knight', function() {
    var $ = knight.$,
        jQuery = $;


    $(function() {
        var Xbox = knight.alipay.Xbox;


        $('.J-add-contact').each(function(i, trigger) {
            trigger = $(trigger);
            var x = new Xbox({
                trigger: trigger,
                content: trigger.attr('href'),
                classPrefix:"ui-newxbox",
                closeLink: null,
                isOld: true
            });

            var executed = false;
            x.on('complete:show', function() {
                if (executed) return;
                var iframe = $('iframe', x.element);
                // iframe 锟斤拷锟斤拷锟斤拷锟较碉拷顺晒锟斤拷锟结触锟斤拷锟斤拷锟铰硷拷
                iframe.get(0).on('add-contact-success', function(msg) {
                    var Overlay = knight.arale.Overlay;

                    var o = new Overlay({
                        template: '<div class="ui-tiptext-container ui-tiptext-container-success" style="padding:6px 0;position:fixed">' +
                                      '<p class="ui-tiptext">' + msg + '</p>' +
                                  '</div>',
                        align: {
                            selfXY: ['50%', 0],
                            baseXY: ['50%', 0]
                        }
                    });
                    o.show();
                    setTimeout(function() {
                        o.hide();
                        o.destroy();
                    }, 2000);

                    var cardNo = jQuery.trim(trigger.attr('data-card-no'));
                    if (cardNo) {
                        $('.J-add-contact[data-card-no=' + cardNo + ']').hide();
                    } else {
                        trigger.hide();
                    }
                });
            });
        });

        var apww = knight.alipay.apww;
	    apww.init({trigger: '.J-open-ww', classPrefix: 'icon-ww'});
    });

});
</script>

        <!-- CMS:消费记录产品系统cms/消费记录/控制是否hover显示明细开始:record/canHoverTriggerDetail.vm -->
<!-- CMS:消费记录产品系统cms/消费记录/控制是否hover显示明细结束:record/canHoverTriggerDetail.vm -->
<script>
    seajs.use('consumeprod-record/1.1.7/knight', function() {

        var jquery = $ = knight.$,
        PopTip = knight.alipay.PopTip,
        
        Emoji = knight.biz.Emoji;
        Tip = knight.arale.Tip;

        $(function() {

            // 服务费展示
            $('.J-fee-trigger').each(function(i, ele) {
                ele = $(ele);
                var p = new PopTip({
                    target: ele,
                    type: 'text',
                    closable: false,
                    content: function() {
                        var content = ele.next('.content-fee');
                        return content.html();
                    },
                    arrowPosition: 7
                });
                ele.hover(function(e) {
                    p.show();
                    }, function(e) {
                    p.hide();
                });
            });

            //余额宝分期购
            $('.J-yeb-fq-trigger').each(function(i, ele) {
                ele = $(ele);
                var p = new PopTip({
                    target: ele,
                    type: 'text',
                    closable: false,
                    content: function() {
                       return ele.data("tip");
                    },
                    arrowPosition: 7
                });
                ele.hover(function(e) {
                    p.show();
                    }, function(e) {
                    p.hide();
                });
            });

            // 资金明细
            var canHoverTriggerDetail = $('#J-canHoverTriggerDetail').length > 0;
            $('.J-details-trigger').each(function(i, detailTrigger) {
                detailTrigger = $(detailTrigger);

                // 缓存数据，防止多次请求
                var loadedData = null;

                // 明细
                var p2 = new Tip({
                    template: '<div class="ui-poptip ui-poptip-blue fn-hide">\
                        <div class="ui-poptip-shadow">\
                            <div class="ui-poptip-container">\
                                <div class="ui-poptip-arrow ui-poptip-arrow-11" style="left:99px">\
                                    <em>◆</em>\
                                    <span>◆</span>\
                                </div>\
                                <div class="ui-poptip-content" data-role="content">\
                                </div>\
                            </div>\
                        </div>\
                    </div>',
                    content: '<div style="width:307px;"><img src="https://i.alipayobjects.com/e/201202/2adw50Ek31.gif" width="16" height="16" alt="载入中" /></div>',
                    trigger: detailTrigger,
                    triggerType: 'click',
                    direction: 'down',
                    arrowShift: 110,
                    width: 346,
                    distance: 5,
                    zIndex: 10000
                });

                p2.after('show', function() {
                    if (!loadedData) {
                        retrieveDetailHtml(function(data) {
                            var html = data.html;
                            p2.set('content', html);
                            Emoji.render('td.emoji-explain');
                            p2.element.find('[data-role=content]').width(320);
                        });
                    }
                });

                // 如果是 hover 显示详情，不显示 tip　
                if (canHoverTriggerDetail) {
                  detailTrigger.parent('.detail') /* 小三角 wrapper */
                  .prev('.amount') /* 金额 wrapper */
                  .andSelf() /* 两个 wrapper 合并起来成为 hover 的区域 */
                  .hover(function (e) {
                    if (!p2.get('visible')) {
                      detailTrigger.trigger('click');
                    }
                  });
                } else {
                  var dp = new PopTip({
                    target: detailTrigger,
                    type: 'text',
                    closable: false,
                    content: '点此查看明细',
                    arrowPosition: 7
                  });

                  detailTrigger.hover(function() {
                    dp.show();
                  }, function() {
                    dp.hide();
                  });

                  p2.before('show', function(){
                    dp.hide();
                  });
                }

                // 异步请求数据
                function retrieveDetailHtml(success, failure) {
                    success = success || function() {};
                    failure = failure || function() {};
                    if (!loadedData) {
                        jquery.ajax(detailTrigger.attr('href'), {
                            dataType: "jsonp",
                            success: function(data) {
                                if (data.stat == 'ok') {
                                    loadedData = data;
                                    success(loadedData);
                                    } else {
                                    failure();
                                }
                            },
                            error: function(xhr, errType, err) {
                                failure();
                            }
                        });
                        } else {
                        success(loadedData);
                    }
                }
            });
 
        });

    });
</script>
        <style>

@font-face {
  font-family: 'xianrou';
  src: url('https://at.alicdn.com/t/font_1421143683_7113035.eot'); /* IE9*/
  src: url('https://at.alicdn.com/t/font_1421143683_7113035.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
  url('https://at.alicdn.com/t/font_1421143683_7113035.woff') format('woff'), /* chrome、firefox */
  url('https://at.alicdn.com/t/font_1421143683_7113035.ttf') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+*/
  url('https://at.alicdn.com/t/font_1421143683_7113035.svg#iconfont') format('svg'); /* iOS 4.1- */
}

.pop-content a:link {
  color: #08c;
}

.pop-content a:visited {
  color: #08c;
}

.pop-content a:hover {
  color: #08c;
  text-decoration: none;
  border-bottom: 1px solid;
}

.ui-dialog {
    border: 1px solid #ccc;
    outline: none;
    border-radius: 2px;
    -moz-box-shadow:0px 0px 10px #ccc;
    -webkit-box-shadow:0px 0px 10px #ccc;
    background: white;
    padding: 0px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
}
.ui-dialog-content {
    background: #fff;
}
:root .ui-dialog {
    FILTER: none\9;
}
.ui-dialog-close {
    font-family: 'xianrou'!important;
    font-size: 16px!important;
    color: #ccc!important;
    cursor: pointer;
    display: block;
    font-family: tahoma;
    font-size: 22px;
    height: 14px;
    line-height: 14px;
    position: absolute;
    right: 15px;
    text-decoration: none;
    top: 14px;
    z-index: 10;
}
.ui-dialog-close:hover {
    text-shadow: none!important;
    box-shadow: none!important;
    color: #ccc!important;
    text-decoration: none!important;
}
.ui-dialog-title {
	padding: 5px 6px;
    height: 30px;
    font-size: 14px;
    line-height: 30px;
    border: 0;
    border-bottom: 1px solid #E6E3DC;
    -moz-border-image: -moz-linear-gradient(left, rgba(12, 105, 9, .3) 0%, rgba(133, 34, 225, .3) 53%, rgba(46, 161, 219, .3) 100%);
    -webkit-border-image: -webkit-linear-gradient(left, #3acfd5 0%, #3a4ed5 100%);
    border-image: linear-gradient(to right, rgba(12, 105, 9, .3) 0%, rgba(133, 34, 225, .3) 53%, rgba(46, 161, 219, .3) 100%);
    border-image-slice: 1;
    color: #000;
    text-indent: 10px;
    background: white;
}
.ui-dialog-container {
    padding: 0;
    font-size: 12px;
}
.ui-dialog-message {
    padding: 25px;
    line-height: 22px;
    color: #000;
    margin-bottom: 0px;
}
.ui-dialog-operation {
    zoom: 1;
    height: 43px;
    text-align: center;
}

.ui-dialog-confirm, .ui-dialog-cancel {
    display: inline;
}
.ui-dialog-operation .ui-dialog-confirm {
    margin-right: 10px;
}
.ui-dialog-button-orange, .ui-dialog-button-white {
    font-weight: 500;
    display: inline-block;
    *display: inline;
    *zoom: 1;
    text-align: center;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
    font-size: 12px;
    border-radius: 2px;
      width: 43px;
  height: 20px;
  line-height: 20px;
    *overflow: visible; /* for a ie6/7 bug http://blog.csdn.net/jyy_12/article/details/6636099 */
    background-image:none!important;
    box-shadow: none!important;
    padding: 3px;
}
a.ui-dialog-button-orange:hover, a.ui-dialog-button-white:hover {
    text-decoration: none;
}
.ui-dialog-button-orange {
    color: #fff !important;
    background: #00aaee !important;
    border: 1px solid #00aaee;
}
.ui-dialog-button-orange:hover {
    background-color: #00aaee !important;
    box-shadow: none!important;
}
.ui-dialog-button-white {
    border: 1px solid #999;
    color: #000 !important;
    background-color: transparent;
    border-color: #999999;
}
.ui-dialog-button-white:hover {
    background: white!important;
    box-shadow: none!important;
}
.record-icon {
    font-family: 'xianrou';
    font-size:16px;
    font-style:normal;
    -webkit-font-smoothing: antialiased;
    -webkit-text-stroke-width: 0.2px;
    -moz-osx-font-smoothing: grayscale;
    color: #4ca9ec !important;
    cursor: default;
}

.record-icon:link {
    color: #4ca9ec;
}

.record-icon:hover {
    color: #4ca9ec;
}

.record-icon.active {

}

.icon-memo {
    font-size: 16px;
    cursor: pointer;
}

.table-list td {
    position: static;
}

.table-index-bill {
    margin-bottom: 10px;
}

.table-index-bill th {
    font-size: 12px;
}
.table-index-bill td {
    color: black;
    font-size: 12px;
    text-align: left;
}
.table-index-bill .text-muted:first-child{
	color: #000;
}
.table-index-bill .ft-gray{
	color: #999;
}
.table-index-bill td.operation .btn-group .disabled {
    color: #999!important;
}
.table-index-bill p {
    //margin-bottom: 5px;
}

.i-bills .table-index-bill tr.refund {
  border-top: 0px;
  height: 40px;
}

.table-index-bill tr.refund td.time {
  border-top: 0px;
}

.table-index-bill th.time {
    width: 90px;
}
.table-index-bill td.time p{
    width: 65px;
}
.table-index-bill td.title {
    width: 370px;
}

.table-index-bill td.title p {
    width: 370px;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

.table-index-bill td.amount {
    width: 100px;
    text-align: right;
    font-size: 16px;
}

.table-index-bill td.detail {
    width: 80px;
    text-align: left;
    position: relative;
}

.table-index-bill td.status {
    width: 120px;
    text-align: right;
    padding-right: 10px;
}

.table-index-bill td.operation {
    width: 100px;
    position: relative;
}


.table-index-bill td.operation p.refund {
    width: 75px;
    text-align: center;
}

.table-index-bill td.operation p.refund a {
    color: #0ae;
}


.table-index-bill td.operation .year-month {
    position: absolute;
    width: 40px;
    height: 40px;
    right: -45px;
    top: 20px;
    background: #999;
}

.table-index-bill td.operation .year-month .arrow {
    border-width: 5px 5px 5px 0;
    border-style: solid;
    width: 0;
    height: 0;
    display: block;
    border-color: rgba(255,255,255,0);
    border-right-color: #999;
    left: -5px;
    top: 15px;
    position: absolute;
}

.table-index-bill td.operation .year-month .year {
    height: 14px;
    overflow: hidden;
    position: relative;
}

.table-index-bill td.operation .year-month .year img {
    position: absolute;
    top: 5px;
    height: 29px;
}

.table-index-bill td.operation .year-month .year img.p1 {
    margin-left: 7px;
}

.table-index-bill td.operation .year-month .year img.p2 {
    margin-left: 13px;
}

.table-index-bill td.operation .year-month .year img.p3 {
    margin-left: 19px;
}

.table-index-bill td.operation .year-month .year .y0 {
    clip: rect(0,6px,9px,0);
    left: 6px;
}

.table-index-bill td.operation .year-month .year .y1 {
    clip: rect(0,13px,9px,7px);
    left: -1px;
}

.table-index-bill td.operation .year-month .year .y2 {
    clip: rect(0,20px,9px,14px);
    left: -8px;
}

.table-index-bill td.operation .year-month .year .y3 {
    clip: rect(0,27px,9px,21px);
    left: -15px;
}

.table-index-bill td.operation .year-month .year .y4 {
    clip: rect(0,34px,9px,28px);
    left: -22px;
}

.table-index-bill td.operation .year-month .year .y5 {
    clip: rect(0,41px,9px,35px);
    left: -29px;
}

.table-index-bill td.operation .year-month .year .y6 {
    clip: rect(0,48px,9px,42px);
    left: -36px;
}

.table-index-bill td.operation .year-month .year .y7 {
    clip: rect(0,55px,9px,49px);
    left: -43px;
}

.table-index-bill td.operation .year-month .year .y8 {
    clip: rect(0,62px,9px,56px);
    left: -50px;
}

.table-index-bill td.operation .year-month .year .y9 {
    clip: rect(0,69px,9px,63px);
    left: -57px;
}

.table-index-bill td.operation .year-month .month {
    height: 24px;
    margin-top: 2px;
    overflow: hidden;
    position: relative;
}

.table-index-bill td.operation .year-month .month img {
    position: absolute;
    top: -10px;
    height: 29px;
}

.table-index-bill td.operation .year-month .month img.p1 {
    margin-left: 14px;
}

.table-index-bill td.operation .year-month .month .m0 {
    clip: rect(13px,12px,29px,0);
    left: 6px;
}

.table-index-bill td.operation .year-month .month .m1 {
    clip: rect(13px,26px,29px,14px);
    left: -8px;
}

.table-index-bill td.operation .year-month .month .m2 {
    clip: rect(13px,40px,29px,28px);
    left: -22px;
}

.table-index-bill td.operation .year-month .month .m3 {
    clip: rect(13px,54px,29px,42px);
    left: -36px;
}

.table-index-bill td.operation .year-month .month .m4 {
    clip: rect(13px,68px,29px,56px);
    left: -50px;
}

.table-index-bill td.operation .year-month .month .m5 {
    clip: rect(13px,82px,29px,70px);
    left: -64px;
}

.table-index-bill td.operation .year-month .month .m6 {
    clip: rect(13px,96px,29px,84px);
    left: -78px;
}

.table-index-bill td.operation .year-month .month .m7 {
    clip: rect(13px,110px,29px,98px);
    left: -92px;
}

.table-index-bill td.operation .year-month .month .m8 {
    clip: rect(13px,124px,29px,112px);
    left: -106px;
}

.table-index-bill td.operation .year-month .month .m9 {
    clip: rect(13px,138px,29px,126px);
    left: -120px;
}


td.amount .total-fee {
    font-size: 12px;
}
















.i-bills .table-list tr:first-child {
    border-top: 0px;
}

.i-bills .table-list tr {
    border-bottom: 0px;
    border-top: 1px solid #ededed;
}
.i-bills .table-index-bill .last {
    text-align: center;
}
.table-index-bill .btn-group {
    float: right;
}


.btn-group-wrap {
    position: relative;
    width: 100px;
    height: 80px;
}
.btn-group {
    position: absolute;
    top: 28px;
    right: 20px;
}

.btn-group li.btn-group-item {
    display: none;
    text-align: center;
    color: black;
    min-width: 60px;
    white-space: nowrap;
    background-color: white;
    cursor: pointer;
}

.btn-group li.btn-group-item{
    line-height: 23px;
    margin: 0px;
    border: 0px;
    padding-left: 5px;
    padding-right: 5px;
}

.btn-group li.btn-group-item:first-child {
    display: block;
    color: #0ae;
}

.btn-group:hover li.btn-group-item:first-child{
    color: black;
}



.btn-group li:hover {
    background: #0ae;
    margin-left: -1px;
    margin-right: -1px;
    padding-left: 5px;
    padding-right: 20px;

    margin-bottom: -1px;
    padding-bottom: 1px;
    position: relative;
}

.btn-group li:hover{
    color: white!important;
}
.btn-group:hover>li>span {
  display:none;
}
.btn-group:hover li {
  padding-right:20px;
  text-align:right;
}
.btn-group:hover {
    border: 1px solid #cccccc;
    border-radius: 2px;
    z-index: 10;
}
.btn-group:hover li{
    display: block;
}

.table-index-bill .btn-group li.btn-group-item.init-orange {
    color: white;
    background: #0ae;
    padding: 1px;
    padding-left: 6px;
    padding-right: 6px;
    border-radius: 2px;
}

.table-index-bill {
    margin-bottom: 0px;
}

.btn-group:hover li:first-child:hover {
    margin-top: -1px;
    padding-top: 1px;

    margin-left: -1px;
    margin-right: -1px;
    padding-left: 6px;
    padding-right: 20px;
    //margin-bottom: -1px;
    border-radius: 2px 2px 0px 0px;
}

.btn-group:hover li:last-child:hover {
    border-radius: 0px 0px 2px 2px;
}

.i-bills .i-content-main {
    overflow: visible;
}

.i-bills .i-content-footer {
    padding-top: 10px;
    overflow: hidden;
    border: 0;
    border-top: 1px solid transparent;
    border-top: 1px solid #E6E3DC\9;
    -moz-border-image: -moz-linear-gradient(left, rgba(12, 105, 9, 0.3) 0%, rgba(133, 34, 225, 0.3) 53%, rgba(46, 161, 219, 0.3) 100%);
    -webkit-border-image: -webkit-linear-gradient(left, #3acfd5 0%, #3a4ed5 100%);
    border-image: linear-gradient(to right, rgba(12, 105, 9, 0.3) 0%, rgba(133, 34, 225, 0.3) 53%, rgba(46, 161, 219, 0.3) 100%);
    border-image-slice: 1;
}


.pop-con {
  width: 340px;
  right: 0px;
  border-radius: 2px;
  border: 1px solid #cccccc;
  z-index: 99;
  position: absolute;
  background: white;
  box-shadow: 0 0 2px 1px rgba(204, 204, 204, 0.8);
}

.pop-head {
  padding: 5px;
}
.pop-head .create-time{
  float: right;
  color: #999;
  display: inline-block;
  padding-right: 5px;
}

.pop-content {
  border-top: 1px solid #ebebeb;
}

.pop-content table{
  width: 100%;
  border-collapse: collapse;
  border-style: hidden;
}

.pop-content table th {
  background: #f7f7f7;
  padding-left: 10px;
  height: 25px;
  line-height: 25px;
  border: 1px solid #ebebeb;
}

.pop-content table th.detail-time {
  background: white;
}

.memo-pop-table td.title-td {
  width: 70px;
}

.memo-pop-table td.content-td {
  width: 280px;
  word-break: break-all;
}

.pop-content table td {
  padding-left: 10px;
  line-height: 20px;
  height: 30px;
  border: 1px solid #ebebeb;
}

.pop-content table td.ft-right,
.pop-content table th.ft-right
 {
  padding-right: 10px;
  text-align: right;
}

.fn-left-important{
  float: left!important;
}
.fn-right-important{
  float: right!important;
}
.ui-newxbox{
	outline: none;
    border-radius: 2px;
    -moz-box-shadow: 0px 0px 10px #ccc;
    -webkit-box-shadow: 0px 0px 10px #ccc;
    background: white;
    padding: 0px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
	overflow: hidden;
}
.ui-newxbox .ui-newxbox-close
{
	color: #999;
    cursor: pointer;
    display: block;
    font-family: tahoma;
    font-size: 24px;
    height: 18px;
    line-height: 14px;
    overflow: hidden;
    position: absolute;
    right: 16px;
    text-decoration: none;
    top: 10px;
    width: 18px;
    z-index: 10;
}

.ui-newxbox-content{
	background: #fff;
}
.ui-newxbox .ui-newxbox-content .ui-tipbox{
	position: relative;
    overflow: hidden;
}
.ui-tipxbox .ui-tipxbox-icon{
	width: 32px;
    height: 32px;
    position: absolute;
    top: 24px;
    left: 40px;
    text-indent: -9999px;
}
.ui-tipxbox-icon.ui-icon-error {
    background-position: -66px 0;
}
.ui-tipxbox-icon, a.xbox-close-link {
    background: url('https://i.alipayobjects.com/e/201201/2NBAbOHc4g.png') no-repeat;
}
.ui-tipxbox .ui-tipxbox-content{
	margin:30px 0 30px 87px;
}
.ui-tipxbox-content h3 {
    color: #333;
    font-size: 14px;
    font-weight: 700;
}
.ui-poptip-shadow{
    background-color: rgba(0,0,0,.05);
}
.ui-poptip-shadow .ui-poptip-container{
    border: 1px solid #b1b1b1;
    background-color: #fff;
}
.ui-poptip-arrow.ui-poptip-arrow-7{
    bottom: 1px;
    left: 17px;
    position: absolute;
}
.ui-poptip-arrow.ui-poptip-arrow-7 span{
    border-width: 6px 6px 0;
    width: 0;
    height: 0;
    border-color: hsla(0,0%,100%,0);
    border-color: transparent\0;
    _border-color: tomato;
    _filter: chroma(color=tomato);
    border-style: solid;
    border-top-color: #b1b1b1;
    top: 2px;
}
.ui-poptip-arrow.ui-poptip-arrow-7 em{
    border-width: 6px 6px 0;
    border-color: hsla(0,0%,100%,0);
    _border-color: tomato;
    _filter: chroma(color=tomato);
    border-style: solid;
    overflow: hidden;
    border-top-color: #ffffff;
    position: absolute;
    z-index: 19;
}
.icon-detail{
    cursor: pointer;
}
</style>
<script>
    seajs.use('consumeprod-record/1.1.7/knight', function() {

        var jquery = $ = knight.$,
            ConfirmBox = knight.arale.ConfirmBox,
            Xbox = knight.alipay.Xbox,
            TopTip = knight.biz.TopTip,
            PopTip = knight.alipay.PopTip,
			Tip = knight.arale.Tip,
            detailBuffer = {},
            Emoji = knight.biz.Emoji,
            con = $('#J_home-record-container');

        $(function() {

            var pop;

            con.css('position', 'relative');

            var fundDetailTip = new Tip({
              trigger: '.icon-detail-trigger',
              triggerType: 'hover',
              theme: 'white',
              effect: 'fade',
              arrowPosition: 7,
            });

            fundDetailTip.before('show', function() {
                var targetUrl = this.activeTrigger.attr('href');
                var tipContent = targetUrl ? '<a href="'+ targetUrl +'">点击查看明细</a>' : '点击查看明细';
                this.set('content', tipContent);
            });


            con.on('mouseover', '.icon-group', function(e) {

              var target = $(e.target);
              var icons = this;
              var targetType = target.data('type');
              if (!targetType || targetType === 'detail') {
                return;
              }

              // 初始化根据类型装载模版
              if (pop) {
                pop.tip.removeClass('fn-hide');
                pop.tip.find('.pop-content').addClass('fn-hide');
                pop._offset(this);
                pop.tip.find('.pop-head').html(icons.innerHTML);
              } else {
                pop = Pop(target, con, this);
              }

            })

            var Pop = function(icon, con, icons) {
              if (this instanceof Pop) {

                this.initView(icon, con, icons);
                this._offset(icons);
                this.initHoverIcon();

                return this;
              }
              return new Pop(icon, con, icons);
            }

            Pop.prototype.initView = function(icon, con, icons) {

              // 初始化内容

              var data = this._parseData(icon);

              this._initRender(data);

              // 渲染pop头部
              this.tip.find('.pop-head').html(icons.innerHTML);


            }

            Pop.prototype.hide = function() {
              this.tip.addClass('fn-hide');
            }

            Pop.prototype._offset = function(icons) {
              var target = $(icons);
              var ori = target.offset();
              ori.top -= 6;
              ori.left -= 6;
              this.tip.offset(ori);
            }

            Pop.prototype._initRender = function(data) {
              var tpl = '<div class="pop-con J_pop-con">' +
                '<div class="pop-head">' +
                '</div>' +
                '<div class="pop-content">' +
                '</div>' +
              '</div>'

              this.tip = $(tpl).appendTo(con);

            }

            Pop.prototype._updateRender = function(data) {

              var self = this;

              function handlerAjaxData(data, key, remoteURL) {
                if (data.stat == 'ok') {

                  self.tip.find('.pop-content').html(data.html);
                  // 明细加载完毕准备替换emoji
                  //注emoji
                  Emoji.render('.pop-content td.emoji-explain');
                  // 只有查询成功才缓存结果
                  if (key !== 'key') {
                    detailBuffer[remoteURL] = data;
                  }

                } else {
                  self.tip.find('.pop-content').html("系统出错");

                }


                self.tip.find('.pop-content').removeClass('fn-hide');

              }

              if (data.type == 'detail') {
                self.tip.addClass('fn-hide');

                return;

              }

              var yebTpl = '<table class="yeb-pop-table">' +
                '<tr>' +
                '<th>TITLE</th>'.replace('TITLE', data.title) +
                '</tr>' +
                '<tr>' +
                '<td class="title-td">VALUE</td>'.replace('VALUE', data.value) +
                '</tr>' +
                '</table>';

              var feeTpl = '<table class="fee-pop-table">' +
                '<tr>' +
                '<th>TITLE</th>'.replace('TITLE', data.title) +
                '</tr>' +
                '<tr>' +
                '<td class="content-td">VALUE</td>'.replace('VALUE', data.value) +
                '</tr>' +
                '</table>';

              var memoTpl = '<table class="memo-pop-table" border=1 bordercolor="#ebebeb">' +
                '<tr>' +
                '<th>分类</th>' +
                '<th>备注</th>' +
                '</tr>' +
                '<tr>' +
                '<td class="title-td">CATEGORY</td>'.replace('CATEGORY', data.category) +
                '<td class="content-td">INFO</td>'
              '</tr>' +
              '<tr>' +
              '<td class="text-muted" colspan="2">请勿备注个人敏感信息</td>' +
              '</tr>'

              var tplDic = {
                'yeb-fq': yebTpl,
                'fee': feeTpl,
                'memo': memoTpl
              }

              var entry = this.tip.find('.pop-content')
                .html(tplDic[data.type])
                .find('.content-td')
                // 防止 xss, 这里替换 emoji 表情允
                .text(data.info);
              // 渲染 Emoji 表情
              Emoji.render('.pop-content .content-td');

              this.tip.find('.pop-content').removeClass('fn-hide');

            }

            Pop.prototype._parseData = function(icon) {
              var type = icon.data('type');
              var value = icon.data('value');
              var title;

              var result = {};

              result.type = type;
              result.value = value;

              if (type == 'fee') {
                result.title = icon.data('title') || '服务费';
              } else if (type == 'yeb-fq') {
                result.title = icon.data('title') || '余额宝分期';
              } else if (type == 'memo') {
                result.category = icon.data('category') || '备注';
                result.info = icon.attr('data-info');
              }

              return result;
            }

            Pop.prototype.initHoverIcon = function() {

              var tip = this.tip;
              var self = this;

              tip.on('click', '.icon-memo', function() {

                var $bizId = $(this).data('bizid').toString();
                var targetLi = $('li[data-bizid="'+ $bizId +'"]');

                targetLi.click();
              })


              tip.on('mouseleave', function() {
                self.hide();
              })


              tip.on('mouseover', '.record-icon', function() {
                //update view
                var icon = $(this);
                var type = icon.attr('data-type');
                var data = self._parseData($(this));

                //手动埋点
                var seed = 'record_index_seed_' + type;
                window.Tracker && window.Tracker.click && window.Tracker.click(seed);

                //先隐藏正文
                self.tip.find('.pop-content').addClass('fn-hide');
                self._updateRender(data);

                //update icon
                if (!icon.hasClass('active')) {

                  var type = icon.data('type');
                  var oldIcon = tip.find('.active');
                  var oldType = oldIcon.data('type');

                  var normal = {
                    "detail": "&#xe60b;",//明细
                    "memo": "&#xe608;",//备注
                    "fee": "&#xe609;",//服务费
                    "yeb-fq": "&#xe61f;"//分期
                  }

                  var active = {
                    "detail": "&#xe61d;",//明细
                    "memo": "&#xe61a;",//备注
                    "fee": "&#xe61e;",//服务费
                    "yeb-fq": "&#xe61b;"//分期
                  }

                  oldIcon.removeClass('active');
                  oldIcon.html(normal[oldType]);
                  if (type !== 'detail') {
                    icon.addClass('active');
                    icon.html(active[type]);
                  }
                }else {
                }

              })
            }
            $('.btn-group').each(function(i, ele) {
                ele = $(ele);
                var fli = ele.find('li:first-child')
                var fliText = fli.text();

                if (fliText != '详情' && fliText !='备注' && fliText !='退款') {

                    fli.addClass('init-orange');

                    fli.parents('td')
                      .prev('td.status')
                      .find('.text-muted')
                      .css({
                        color: '#ff6600'
                      })

                    fli.on('mouseenter', function() {
                      fli.removeClass('init-orange');
                    })

                    fli.parent().on('mouseleave', function() {
                      fli.addClass('init-orange');
                    })
                }
                fli.html(fliText + "<span> &#xe612;</span>");

                fli.find('span').css({
                  "font-family": "xianrou"
                })

				function deleteFail(xboxCntSelector) {
                    var x = new Xbox({
                        content: $(xboxCntSelector).clone().removeAttr('id'),
                        classPrefix:"ui-newxbox",
                        width: 400,
                        height: 100
                    });
                    x.show();
                    $('a[data-action=no-thanks]', x.element).click(function(e) {
                        e.preventDefault();
                        x.hide();
                    });
                    x.after('hide', function() {
                        x.destroy();
                    });
                }
                ele.on('click', 'li[data-link]', function(e) {
                    var self = $(this);
                    if (self.data('action') || self.hasClass('disabled') ) {
                        return;
                    }
                    var url = $(this).data('link');
                    window.open(url, '_blank');


                })
				// 用户操作tip提示
				ele.find('li[data-tip]').each(function (i, linode) {
					var li = $(linode);
					var tip = li.data('tip');
					if(tip && tip !== '') {
						var t = new Tip({
							trigger: li,
							content: tip,
							theme: 'white',
							arrowPosition: 2,
							width: 212,
                        	delay: -1
						});
					}
				})
                // delete start
                ele.on('click', 'li[data-action="delete"]', function(e) {

                    var that = this;
                    var aDom = $(e.target);

                    var confirmtext = '<p>删除后你可在回收站还原或永久删除。</p>';
                    ConfirmBox.confirm(confirmtext, '确定要删除此记录？', function() {

                      jquery.ajax(aDom.data('link'), {
                            dataType: "jsonp",
                            timeout: 5000,
							jsonp: '_callback',
                            success: function(data) {
                                if (data.stat == 'ok') {
                                    var delTr = aDom.parents('tr');
                                    delTr.css('background-color', '#FFA18C').fadeOut(function() {
                                        delTr.remove();
                                    });
                                }else {
                                  if(data.msg){
                                    $("#J-delete-failure").find(".ui-tipxbox-explain").html(data.msg).prev("h3").removeClass("mt-30").addClass("mt-20");
                                  }
								  deleteFail("#J-delete-failure");
                                }
                            },
                            error: function(e) {
                                deleteFail("#J-delete-failure");
                            }
                        });

                    },
					function () {},
					{
            			afterShow: function() {
                            this.element.css('height', 'auto');
                            $(".ui-dialog-close",this.element).attr("seed","consume-delete-close");
                            $(".ui-dialog-button-orange",this.element).attr("seed","consume-delete-ok");
                            $(".ui-dialog-button-white",this.element).attr("seed","consume-delete-cancel");
                        },
						closeTpl: '&#xe60e;'
					}
					);
                });

                // edit-memo start
                ele.on('click', 'li[data-type="memo"]', function(e) {

                    var aDom = $(this);
                    var iframeurl = aDom.data('link') + '&ISNEW=true';

                    var x = new Xbox({
                        width: 600,
                        height: 320,
                        classPrefix: "ui-newxbox",
                        isOld: true,
                        content: iframeurl
                    })

                    x.after('show', function() {
                        x.element.find('iframe')[0].on('change:height', function(h) {
                            x.set('height', h);
                        });
                    })

                    x.show();
                })

                // cancel-peer-pay start
                function cancelPeerPayFail(xboxCntSelector) {
                    var x = new Xbox({
                        content: $(xboxCntSelector).clone().removeAttr('id'),
                        classPrefix:"ui-newxbox",
                        width: 400
                    });
                    x.on('complete:show', function() {
                        this.element.css('height', 'auto');
                    });
                    x.show();
                    x.after('hide', function() {
                        x.destroy();
                    });
                }

                ele.on('click', 'li[data-action="cancel-peer-pay"]', function(e) {
                    var that = this;
                    var target = $(this);
                    ConfirmBox.confirm('确定要取消代付？','取消代付', function() {
                        var aDom = target;
                        jquery.ajax({
							url: aDom.data('link'),
                            dataType: "jsonp",
                            timeout: 5000,
							jsonp: "_callback",
                            success: function(data) {
                                if (data.stat == 'ok') {
                                    document.location.reload();
                                } else  {
                                    //ERROR HANDLER
									cancelPeerPayFail('#J-cancel-peer-failure');
                                }
                            },
                            error: function() {
                                //ERROR HANDLER
								cancelPeerPayFail('#J-cancel-peer-failure');
                            }
                        });
                    },
					function () {},
					{
                        afterShow: function() {
                            this.element.css('height', 'auto');
                        },
                        closeTpl: '&#xe60e;'
                    })
                })


                ele.on('click', 'li[data-action="close-repay"]',function() {
                    var that = this;
                    var target = $(this);

                    ConfirmBox.confirm('确定要关闭还款？', '关闭还款', function() {
                            var aDom = target;
                            jquery.ajax(aDom.data('link'), {
                                dataType: "jsonp",
								jsonp: "_callback",
                                success: function(data) {
                                    if (data.stat == 'ok') {
                                        document.location.reload();
                                    } else {
										TopTip.show(data.msg, {type: 'error'});
                                    }
                                },
                                error: function() {
									TopTip.show("抱歉，关闭还款失败，请稍后再试。", {type: 'error'});
                                }
                            });
                    },
					 function () {},
					{
                        afterShow: function() {
                            this.element.css('height', 'auto');
                        },
                        closeTpl: '&#xe60e;'
                    });
                });

            });
        });


    });
</script>

        <style>
/*处理emoji表情
因为emoji表情字符串为unicode编码，
模板层不做长度限制
首屏渲染前会特别长*/

.other .name {
    max-width: 130px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    visibility: hidden;
}

.emoji-icon {
    width: 12px;
    height: 12px;
    top: 1px;
    position: relative;
}

.title .opposite {
    max-width: 370px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    visibility: hidden;
}

td.emoji-explain {
    padding-right:10px;
}
</style>

<script>

// 这个脚本负责渲染首屏 emoji 表情
// 动态载入的文本需要手动替换
seajs.use('consumeprod-record/1.1.7/knight', function() {
  //注销emoji
  
  var Emoji = knight.biz.Emoji;
  // 新版首页交易方、新版带有链接的标题、旧版交易方、旧版标题 消费收支明细列表
  Emoji.render('.title .opposite , .title .content , .other .name, .consume-title, td.name p.name, .trade-info .info-item .opposite,.trade-info .info-item .title ');

});
</script>    <div class="fn-hide">

        <div id="J-delete-failure">
        <div class="ui-tipxbox">
            <div class="ui-tipxbox-icon ui-icon-error">error</div>
            <div class="ui-tipxbox-content">
                <h3 class="mt-30">删除失败，请稍后再试。</h3>
                <p class="ui-tipxbox-explain"></p>
            </div>
        </div>
    </div>

        <div id="J-cancel-peer-failure">
        <div class="ui-tipxbox">
            <div class="ui-tipxbox-icon ui-icon-error">error</div>
            <div class="ui-tipxbox-content">
                <h3 class="mt-30">抱歉，取消代付失败，请稍后再试。</h3>
            </div>
        </div>
    </div>

</div>

        <!--统计、下载及图标说明-->
		    

<div class="amount-bottom">
        	<div class="action-content">
    	    		<a class="amount-links" seed="CR-statistical-bottom"  href="https://consumeprod.alipay.com:443/record/statistic.json?_input_charset=utf-8&dateRange=oneMonth&amp;endDate=2018.09.18&amp;pageNum=1&amp;beginDate=2018.08.18&amp;dateType=createDate&amp;fundFlow=all&amp;beginTime=00%3A00&amp;endTime=24%3A00&amp;tradeType=ALL&amp;status=all">
                统计查询结果
            </a>

    		<div class="amount-detail"><img style="vertical-align:middle;" src="https://i.alipayobjects.com/e/201202/2adw50Ek31.gif" width="16" height="16" alt="载入中" /></div>
    	    		<div class="fn-clear action-other  action-other-show ">
    			<div class="fn-left">
    				    				<em class="ft-bar first-bar">|</em>
    				    				    				<a class="J-download-tip mr-20" seed="CR-download-bottom" data-link="https://consumeprod.alipay.com:443/record/download.htm?_input_charset=utf-8&suffix=csv&dateRange=oneMonth&amp;endDate=2018.09.18&amp;pageNum=1&amp;beginDate=2018.08.18&amp;dateType=createDate&amp;fundFlow=all&amp;beginTime=00%3A00&amp;endTime=24%3A00&amp;tradeType=ALL&amp;status=all"><span class="record-icon icon-download"></span>下载查询结果</a>
    				

<script type="text/javascript">
document.domain=document.domain.split(".").slice(-2).join(".");

seajs.use(['alipay/xbox/1.1.5/xbox','jquery'], function(Xbox, $) {
    var example = new Xbox({
        type: 'iframe',
		width: '600px',
        trigger: '.J-download-tip'
    }).before('show',function() {
        var url = this.activeTrigger.attr('data-link');
        this.set('content', url);
    }).render();
});
</script>    				    	            <span class="iconTip">
    	                图释:
    	                <em class="ml-5"><i class="record-icon icon-detail icon-list">&#xe61d;</i>支付明细</em>
    	                <em class="ml-5"><i class="record-icon icon-memo icon-list">&#xe61a;</i>备注</em>
    	                <em class="ml-5"><i class="record-icon icon-fee icon-list">&#xe61e;</i>服务费</em>
                        <em class="ml-5"><i class="record-icon icon-yeb-fq icon-list">&#xe61b;</i>余额宝分期</em>
    	            </span>
    			</div>
    			
   
	<div class="page fn-right">   		<div class="page-link">
						1 - 10条，共235条
							<a class="page-next page-trigger" href="javascript:;" pageNum="2">下一页&gt;</a>
				<a class="page-end page-trigger" href="javascript:;" pageNum="24">尾页&gt;&gt;</a>
					</div>
	</div>
	

    			    		</div>

    	</div>
    </div>

<!-- CMS:电子账单/消费记录/new交易记录调查开始:consumeprod/record/consume_survey.vm --><!-- CMS:电子账单/消费记录/new交易记录调查结束:consumeprod/record/consume_survey.vm -->
<script>

seajs.use('consumeprod-record/1.1.7/knight', function(knight) {
    var knightObj = knight || window.knight;
    var jquery = knightObj.$,
        URI = knightObj.biz.URI;

    var cache = null;

    // 从 cache 中获取数据，否则请求 ajax
    function retrieveData(jsonUrl,success, failure) {          //https://consumeprod.alipay.com:443/record/statisticAdvanced.json
        if (cache) {
            success(cache);
        } else {
            
            jquery.get(jsonUrl, function(returnVal) {
                if (returnVal.stat == 'ok') {
                    cache = returnVal.statisticVO;
                    success(cache);
                } else {
                    failure();
                }
            });
        }
    }

    jquery(function() {
        jquery(".amount-links").bind("click",function(e){
            var requestTime = setTimeout(function(){
	        	jquery(e.target).parents("div").find(".amount-detail").append("<span class='ml-10'>数据量较大，统计需要一定时间，请稍作等待</span>");
        	},5000);
            e.preventDefault();
            jquery(e.target).parents("div.action-content").toggleClass('show-amount');
            var jsonUrl = jquery(e.target).attr("href");
            retrieveData(jsonUrl,function(data) {
                clearTimeout(requestTime);
                var text = '';
                             
                                                     text = '已支出' + data.expendCount + '笔共' + data.expendAmount + '元，待支出' + data.payableCount + '笔共' + data.payableAmount + '元 | 已收入' + data.incomeCount + '笔共' + data.incomeAmount + '元，待收入' + data.receivableCount + '笔共' + data.receivableAmount + '元';
                
                             jquery(e.target).parents("div").find(".amount-detail").html(text);

            }, function() {
                clearTimeout(requestTime);
            	jquery(e.target).parents("div").find(".amount-detail").html("<p class='ui-tiptext ui-tiptext-error ft-red'><span class='ui-tiptext-icon'></span>系统繁忙，请稍候再试</p>");
            });
        });

    });
});

</script>




    

 

    </div>
    <!--主交易记录区end-->
    <!--backToTop-->
    <div class="back-to-top invisible">
        <img class="top-img" src="https://os.alipayobjects.com/rmsportal/JfMcObAPKmMgpnM.png" />
    </div>
    <script>


        seajs.use('consumeprod-record/1.1.7/knight', function() {

            var backTopMgr = (function () {
                var $ = knight.$,
                    body = document.body,
                    delayer = null,
                    TIME = 100;
                function scrollProxy(fn){
                    $(window).on('scroll', function (){
                        clearTimeout(delayer);
                        delayer = setTimeout(fn, TIME);
                    });
                    $('.back-to-top').on('click', function () {
                        $('body').animate({
                            scrollTop: 0
                        }, 300);
                    })
                }
                function checkerVisible() {
                    var contentMarginTop = $('#container').offset().top;
                    return body.scrollTop > contentMarginTop ;
                }
                 function checkerPosition() {
                    return (body.scrollHeight - $(window).height() - body.scrollTop > 100);
                }
                function eventHandler() {
                    var backElem = $('.back-to-top');
                    checkerVisible() && backElem.removeClass("invisible") || backElem.addClass("invisible");
                    checkerPosition() && backElem.removeClass("up-bottom") || backElem.addClass("up-bottom");

                }
                return {
                    init : function () {
                        scrollProxy(eventHandler);
                        checkerVisible() && $('.back-to-top').click();
                    }
                }
            })();
            backTopMgr.init();
        });
    </script>
</div>

<!-- CMS:消费记录产品系统cms/消费记录/电子钱包下载开始:consumeprod/record/mobile_alipay.vm -->				<style type="text/css" media="screen">
		.mobile-alipay{
			position: fixed;
			_position:absolute;
			bottom: 10px;
			right:25px;
		/*width:230px;*/
			height:125px;
		}
		.mobile-alipay .mobile-alipay-trigger{
			position: absolute;
			bottom:0;
			right: 0;
		}
		.mobile-alipay-box .content-arrow{
			position: absolute;
			bottom: 15px;
			right: -7px;
			border-width: 7px 0 7px 7px;
			border-style: solid;
			border-color: #FFFFFF #FFFFFF #FFFFFF #000000;
			line-height:0;
			-ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=70)";
			filter:alpha(opacity=70);
			opacity:0.7;
		}
		.mobile-alipay .mobile-alipay-content{
			width: 210px;
			padding: 10px;
			background-color: #000;
			-ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=70)";
			filter:alpha(opacity=70);
			opacity:0.7;
			color:#dbdbdb;
			font-family:"Microsoft YaHei";
			height: 105px;
		}
		.mobile-alipay-content .content-title{
			height: 27px;
		    overflow: hidden;
		    line-height: 27px;
		}
		.mobile-alipay-content .content-title h4{
			font-size: 14px;
		    overflow: hidden;
		    width: 85px;
		}
		.mobile-alipay-content .content-title .intro{
			width: 120px;
			overflow: hidden;
		}
		.mobile-alipay .mobile-icon{
			background-image: url("https://i.alipayobjects.com/e/201307/jZmA7MtzD.png");
			background-repeat: no-repeat;
			background-position: 0 0;
			display: inline-block;
			height: 45px;
			width: 28px;
			vertical-align: middle;
		}
		.mobile-alipay .mobile-icon:hover{
			background-position: 0 -60px;
		}
		.mobile-alipay .mobile-link{
			position: absolute;
			bottom: 10px;
		    left: 10px;
		}
		.mobile-alipay .mobile-imgcode{
			position: absolute;
			bottom: 10px;
			right: 10px;
		}
		.mobile-link .mobile-link-btn{
			display: inline-block;
			border: 1px solid #d66500;
			background-color: #f57403;
			width: 90px;
			height: 23px;
			line-height: 23px;
			text-align: center;
			color: white;
			font-size: 12px;
			font-weight: bold;
			border-radius: 3px;
		}
		.mobile-link .mobile-link-btn:hover{
			color:white;
		}
		.mobile-type-img p.mobile-type{
			line-height: 21px;
		}
		.mobile-type-img p .iconfont{
			font-size: 18px;
			margin-right: 5px;
		}
	</style>
	<div id="J-mobile-alipay" class="mobile-alipay">
		<div class="mobile-alipay-trigger">
			<a class="mobile-icon J-client-alipay" href="javascript:;" title="支付宝客户端"></a>
		</div>
		<div class="mobile-alipay-box" id="mobile-alipay-box" style="display:none;">
			<div class="content-arrow"></div>
			<div class="mobile-alipay-content" id="mobile-alipay-content">
				<div class="content-title fn-clear">
					<h4 class="fn-left">支付宝客户端</h4>
					<div class="intro fn-right">随时随地掌握交易记录</div>
				</div>
				<div class="fn-clear mobile-type-img">
					<div class="fn-left">
						<p class="mobile-type"><i class="iconfont">&#xF02B;</i>Android</p>
						<p class="mobile-type"><i class="iconfont">&#xF02C;</i>iPhone</p>
					</div>
				</div>
			</div>
			<div class="mobile-link">
				<a class="mobile-link-btn" href="https://fun.alipay.com/down/index.htm?cid=5055" target="_blank">立即下载</a>
			</div>
			<div class="mobile-imgcode">
				<img src="https://i.alipayobjects.com/e/201307/jYwP8hFZn.png" class="fn-right" height="74" width="74" />
			</div>
		</div>
	</div>
	
	<script type="text/javascript">
		seajs.use(['jquery','arale/popup/1.0.2/popup'], function(jQuery,Popup) {
			jQuery(function(){
				new Popup({
			        trigger: ".J-client-alipay",
			        element: "#mobile-alipay-box",
			        align: {
			            baseXY: [ -242, -80 ]
					}
			    });
				jQuery(".J-client-alipay").click(function(e){
					e.preventDefault();
				});
			});
		});
	</script>
						<!-- CMS:消费记录产品系统cms/消费记录/电子钱包下载结束:consumeprod/record/mobile_alipay.vm -->
 
<!-- uitpl:/component/tracker.vm -->
<!-- FD:106:alipay/tracker/tracker.vm:START --><!-- FD:106:alipay/tracker/tracker.vm:785:tracker.schema:全站自动化/性能/敏感信息打点开关:START -->



<script type="text/javascript">
window.Smartracker && Smartracker.sow && Smartracker.sow();
</script>






<script type="text/javascript">

window.agp_custom_config = {
  BASE_URL: '//kcart.alipay.com/p.gif',
  TIMING_ACTION_URL: '//kcart.alipay.com/x.gif'
}

</script>
<script charset="utf-8" src="https://a.alipayobjects.com:443/g/memberAsset/securityMsg/1.0.3/index.js"></script>





<!-- FD:106:alipay/tracker/sai.vm:START --><script>
    sensScanConfig={
        ratio: 0.01,
        modules: '*',
        types: '*'
      };
</script>

<script src='https://as.alipayobjects.com/g/alipay_security/monitor-sens/1.0.1/monitor-sens.min.js'></script>
<!-- FD:106:alipay/tracker/sai.vm:END -->



<!-- FD:106:alipay/tracker/cmsbuffer.vm:START --><!-- FD:106:alipay/tracker/cmsbuffer.vm:997:cmsbuffer.schema:main-CMS全站修复:START -->















<script>
try {
  (function() {
  var logServer = 'https://magentmng.alipay.com/m.gif';
  var sample = 0.0001;
  var url = "https://a.alipayobjects.com/http-watch/1.0.7/index.js";

  // 判断比例
  if (!!window.addEventListener && Array.prototype.map && Math.random() < sample) {
    var HEAD = document.head || document.getElementsByTagName('head')[0];

    var spt = document.createElement('script');
    spt.src = url;
    HEAD.appendChild(spt);

	setTimeout(function() {
	  window.httpWatch && window.httpWatch({ sample: 1, appname: 'consumeprod-49-5672', logServer: logServer });
	}, 1000);
  }
  })();
} catch(e) {}
</script>

<!-- FD:106:alipay/tracker/cmsbuffer.vm:997:cmsbuffer.schema:main-CMS全站修复:END -->
<!-- FD:106:alipay/tracker/cmsbuffer.vm:END --><!-- FD:106:alipay/tracker/tracker.vm:785:tracker.schema:全站自动化/性能/敏感信息打点开关:END -->
<!-- FD:106:alipay/tracker/tracker.vm:END -->
<!-- FD:231:alipay/nav/versionSwitch.vm:START --><!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:START -->







<!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:END --><!-- FD:231:alipay/nav/versionSwitch.vm:END -->        </div>


<!-- /component/footCommon.vm -->

<!-- FD:231:alipay/nav/versionSwitch.vm:START --><!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:START -->







<!-- FD:231:alipay/nav/versionSwitch.vm:1743:nav/versionSwitch.schema:versionSwitch-网站改版导航新老版本切换开关:END --><!-- FD:231:alipay/nav/versionSwitch.vm:END -->



<style>
.fn-clear:after {font-size:0;}
.ui-footer {font-size: 12px; margin-top: 30px; height: 100px; line-height: 18px; background:#1e1b29; color:#808080;}
.ui-footer .ui-separator{font-weight: normal;}
.ui-footer-link a {padding: 0 3px 0 2px;}
.ui-footer a, .ui-footer-copyright .copyright a {color: #808080;}
.ui-footer a:hover, .ui-footer-copyright .copyright a:hover {color: #808080; text-decoration: none; border-bottom: 1px solid;}
.ui-footer-ctn {padding-top: 30px; text-align: center;}
.ui-footer-copyright {padding-top: 10px; background:#1e1b29;}
.ui-footer-copyright .server {color: #1e1b29;}
.ui-footer-copyright .copyright {color: #808080;}
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
      <a href="https://fun.alipay.com/certificate/jyxkz.htm" target="_blank">ICP证：沪B2-20150087</a>
  </div>
<div class="server" id="ServerNum">
  consumeprod-49-5672 &nbsp;
</div>
<!-- FD:231:alipay/foot/copyright.vm:2604:foot/copyright.schema:支付宝copyright:END --><!-- FD:231:alipay/foot/copyright.vm:END -->        </div>
    </div>
</div>
<!-- /component/footCommon.vm -->












<!-- FD:231:alipay/foot/onlineServiceNew.vm:START --><!-- FD:231:alipay/foot/onlineServiceNew.vm:2603:foot/onlineServiceNew.schema:onlineServiceNew-___新___在线客服第1块配置:START -->
    

    

    

    

    

    

    

    

    

    

    

    

    


    


    

    

    

    

    

    



    
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
                        'merchantServerConfig': 'https://gw.alipayobjects.com/os/cschannel/xXvAhTnQmiCqIYltGaYe.js',
                        'customerServerConfig': 'https://gw.alipayobjects.com/os/cschannel/eKIrsHTTgHXrEJIaDKxq.js',
			'koubeiServerConfig': 'https://gw.alipayobjects.com/os/cschannel/pQmbmblGTxzzURaFbUca.js',
			'defaultDataConfig': 'https://a.alipayobjects.com/u/js/201311/1acIoVU1Xx.js',
                        'onlineServerJS': 'https://gw.alipayobjects.com/os/rmsportal/RzgRUFdecEbUqInOXDmL.js',//云客服匹配
                        'onlineServerCSS': 'https://gw.alipayobjects.com/os/rmsportal/OoBEJPEWDpEAYzMExDNj.css'//云客服通用样式
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
        window.console && console.log && console.log(e);
        window.Tracker && Tracker.click('onlineServer-error-init-' + e);
    }
    </script>
<!-- FD:alipay-foot:alipay/foot/cliveService.vm:cliveService.schema:END -->

<!-- FD:alipay-foot:alipay/foot/cliveService.vm:END --><!-- FD:231:alipay/foot/onlineServiceNew.vm:2603:foot/onlineServiceNew.schema:onlineServiceNew-___新___在线客服第1块配置:END --><!-- FD:231:alipay/foot/onlineServiceNew.vm:END -->
<!-- FD:231:alipay/foot/onlineServiceCtr.vm:START --><!-- FD:231:alipay/foot/onlineServiceCtr.vm:2602:foot/onlineServiceCtr.schema:onlineServiceCtr-流量配置第1个区块配置:START -->
     


     


     


     


     


     


     


     


     


     


     


     


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <!-- FD:231:alipay/foot/onlineServiceCtr.vm:2602:foot/onlineServiceCtr.schema:onlineServiceCtr-流量配置第1个区块配置:END --><!-- FD:231:alipay/foot/onlineServiceCtr.vm:END -->

</body>
</html>


"""
# tt.encode('utf8').decode('utf8')
page_sel = scrapy.Selector(text=tt)
# result = page_sel.xpath('string(//*[@id="J-assets-pcredit"]/div/div/div[2]/div/p[2]/span/strong)').extract_first()
# result = page_sel.xpath('//*[@id="J_home-record-container"]/div[2]/div/div[2]/div[2]/div/text()').extract_first()

# re_list = re.findall('1 - 10条，共(\d+)条', result)
# print(result, re_list)

# python本身默认编码为unicode
# 所有编码转换时都需通过unicode
msg = "北京"
print(msg.encode(encoding="utf-8"))  # unicode编码转换为utf-8编码
print(msg.encode(encoding="utf-8").decode(encoding="utf-8"))  # unicode编码转换为utf-8编码，再转化为unicode编码
# result = page_sel.xpath('//*[@class="J-item "]').extract()
result = page_sel.xpath('//*[@id="J-item-10"]/td[2]//text()').extract()
print(len(result), result)
# for i in range(10):
# 	print(i)


# ll = ['\n\n\n                        ', '今天', '\n                  ', ' 08:49\n                    ', '\n\n ']
ll = result = page_sel.xpath('//*[@id="J-item-10"]/td[2]//text()').extract()
ll = ''.join(ll)


def delete_n(value):
	if "\n" in value:
		return value.replace("\n", "")
	else:
		return value


def delele_(value):
	return value.strip(" ")


def formate_time(value):
	if '今天' in value:
		now = time.time()
		time_array = time.localtime(now)
		day = time.strftime("%Y-%m-%d", time_array)
		times = value.split(' ')[-1]
		return day + ' ' + times
	if '昨天' in value:
		now = datetime.datetime.now()
		date = now + datetime.timedelta(days=-1)  # timedate模块时间减去一天
		date = int(time.mktime(date.timetuple()))  # timedate模块转为时间戳
		time_array = time.localtime(date)  # 时间戳转换为时间数组
		print("111", date)
		print('time_array', time_array)
		times = value.split(' ')[-1]
		day = time.strftime("%Y-%m-%d", time_array)  # 时间数据格式化
		return day + ' ' + times
	else:
		print('value的样子', value)
		if "\t" in value:
			value = value.replace("\t", "")
			value = value.strip()
		day = value.split(' ')[0]
		times = value.split(' ')[-1]
		return day + ' ' + times


ll = delete_n(ll)
print(ll)
ll = delele_(ll)
print('去除空格', ll)
ll = formate_time(ll)
print(ll)
