ttt = """
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>城市选择</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
	<link rel="stylesheet" href="/static/resource/index/css/index.css" />

</head>
<body>

	<div class="head">
		<div class="head-top">
			<!--<p class="head-top-logo"></p>-->
			<p class="head-top-number Js-city-count"></p>
		</div>
		<div class="head-search Js-search-bar"><input type="text" class="Js-search-input" placeholder="快速搜索城市"></div>
	</div>

	<div class="no-content">暂无搜索内容</div><!-- 无搜索结果内容 -->

	<div>
		<div class="whole-city Js-locate-content" style="display:none;">
			<h3>目前定位城市</h3>
			<ul class="city-con Js-locate-city">
				<!--<li>北京</li>-->
			</ul>
		</div>
		<div class="whole-city">
			<h3>门店所在城市</h3>
			<ul class="city-con Js-city-list">
				<!--<li>北京</li>-->
			</ul>
		</div>
	</div>

        <script src="/static/resource/common/js/jquery.min.js"></script>
        <script src="//res.wx.qq.com/open/js/jweixin-1.2.0.js"></script>
        <script>
            var controller = {
                cityList: {},
                
                init: function(json){
                    var cityList = JSON.parse(json);
                    if (!cityList) {
                        return false;
                    }
                    
                    this.cityList = cityList;
                    this.showLocateCity();
                    this.showCity(this.cityList);
                    this.bindEvents();
                },
                showLocateCity: function(){
                    var locateCityInfo = sessionStorage.getItem('locateCityInfo');
                    if (locateCityInfo) {
                        locateCityInfo = JSON.parse(locateCityInfo);
                        $('.Js-locate-city').html('<li city_id="'+locateCityInfo.id+'">'+locateCityInfo.name+'</li>')
                        $('.Js-locate-content').show();
                    }
                },
                showCity: function(cityList){
                    $('.Js-city-list').empty();
                    for (i in cityList) {
                        var item = cityList[i];
                        var tpl = '<li city_id="'+item.id+'">'+item.name+'</li>';
                        $('.Js-city-list').append(tpl);
                    }
                    $('.Js-city-count').text('共' + cityList.length + '个城市')
                },
                select: function(ev){
                    var t = $(ev.currentTarget);
                    
                    var cityInfo = {
                        id: t.attr('city_id'),
                        name: t.text()
                    };
                    
                    window.sessionStorage.cityInfo = JSON.stringify(cityInfo);
                    
                    window.location=document.referrer;
                },
                search: function(ev){
                    var self  = this;
                    var t = $(ev.currentTarget);
                    clearTimeout(this.timer);
                    this.timer = setTimeout(function(){
                        var keyword = $('.Js-search-input').val();
                        if (keyword) {
                            var cityList = [];
                            for (i in self.cityList) {
                                var city = self.cityList[i];
                                if (city.name.indexOf(keyword) != -1) {
                                    cityList.push(city);
                                }
                            }
                            
                            if (cityList.length > 0) {
                                self.showCity(cityList);
                            }
                        } else {
                            self.showCity(self.cityList);
                        }
                    }, 200);
                },
                bindEvents: function(){
                    $('.Js-city-list,.Js-locate-city').delegate('li', 'click', $.proxy(this, 'select'));
                    
                    $('.Js-search-bar').on('input change', '.Js-search-input', $.proxy(this, 'search'));
                }
            };
            
            controller.init('[{"id":"110100","name":"\u5317\u4eac\u5e02"},{"id":"310100","name":"\u4e0a\u6d77\u5e02"},{"id":"120100","name":"\u5929\u6d25\u5e02"},{"id":"610100","name":"\u897f\u5b89\u5e02"},{"id":"440100","name":"\u5e7f\u5dde\u5e02"},{"id":"440300","name":"\u6df1\u5733\u5e02"},{"id":"440600","name":"\u4f5b\u5c71\u5e02"},{"id":"441900","name":"\u4e1c\u839e\u5e02"},{"id":"350200","name":"\u53a6\u95e8\u5e02"},{"id":"350100","name":"\u798f\u5dde\u5e02"},{"id":"440400","name":"\u73e0\u6d77\u5e02"},{"id":"441300","name":"\u60e0\u5dde\u5e02"},{"id":"150200","name":"\u5305\u5934\u5e02"},{"id":"150600","name":"\u9102\u5c14\u591a\u65af\u5e02"},{"id":"320100","name":"\u5357\u4eac\u5e02"},{"id":"340100","name":"\u5408\u80a5\u5e02"},{"id":"420100","name":"\u6b66\u6c49\u5e02"},{"id":"410100","name":"\u90d1\u5dde\u5e02"},{"id":"510100","name":"\u6210\u90fd\u5e02"},{"id":"150100","name":"\u547c\u548c\u6d69\u7279\u5e02"},{"id":"330100","name":"\u676d\u5dde\u5e02"},{"id":"320500","name":"\u82cf\u5dde\u5e02"},{"id":"320200","name":"\u65e0\u9521\u5e02"},{"id":"370200","name":"\u9752\u5c9b\u5e02"},{"id":"320600","name":"\u5357\u901a\u5e02"},{"id":"320400","name":"\u5e38\u5dde\u5e02"},{"id":"321100","name":"\u9547\u6c5f\u5e02"},{"id":"330200","name":"\u5b81\u6ce2\u5e02"},{"id":"330300","name":"\u6e29\u5dde\u5e02"},{"id":"210200","name":"\u5927\u8fde\u5e02"},{"id":"210100","name":"\u6c88\u9633\u5e02"},{"id":"321000","name":"\u626c\u5dde\u5e02"},{"id":"430100","name":"\u957f\u6c99\u5e02"},{"id":"340200","name":"\u829c\u6e56\u5e02"},{"id":"500100","name":"\u91cd\u5e86\u5e02"},{"id":"320300","name":"\u5f90\u5dde\u5e02"},{"id":"442000","name":"\u4e2d\u5c71\u5e02"},{"id":"350500","name":"\u6cc9\u5dde\u5e02"},{"id":"370100","name":"\u6d4e\u5357\u5e02"},{"id":"220100","name":"\u957f\u6625\u5e02"},{"id":"330400","name":"\u5609\u5174\u5e02"},{"id":"370600","name":"\u70df\u53f0\u5e02"},{"id":"130200","name":"\u5510\u5c71\u5e02"},{"id":"520100","name":"\u8d35\u9633\u5e02"},{"id":"530100","name":"\u6606\u660e\u5e02"},{"id":"130100","name":"\u77f3\u5bb6\u5e84\u5e02"},{"id":"140106","name":"\u592a\u539f\u5e02"},{"id":"130400","name":"\u90af\u90f8\u5e02"},{"id":"440700","name":"\u6c5f\u95e8\u5e02"},{"id":"430300","name":"\u6e58\u6f6d\u5e02"},{"id":"450100","name":"\u5357\u5b81\u5e02"},{"id":"440600","name":"\u4f5b\u5c71\u5e02"},{"id":"330600","name":"\u7ecd\u5174\u5e02"},{"id":"420500","name":"\u5b9c\u660c\u5e02"},{"id":"320900","name":"\u76d0\u57ce\u5e02"},{"id":"371300","name":"\u4e34\u6c82\u5e02"},{"id":"620100","name":"\u5170\u5dde\u5e02"}]');
        </script>
    
    <script>
        (function(){
            $.ajax({
                url: '/wechat/getJsSign',
                type: 'post',
                async:true,
                data: {
                    url: encodeURIComponent(window.location.href)
                },
                dataType: 'json',
                success: function(res){
                    if (res.code == 200) {
                        var data = res.data;
                        wx.config({
                            beta: true, // 必填，开启内测接口调用，注入wx.invoke和wx.on方法
                            debug: false,//如果在测试环境可以设置为true，会在控制台输出分享信息；
                            appId:data.appId, // 必填，公众号的唯一标识
                            timestamp:data.timestamp , // 必填，生成签名的时间戳
                            nonceStr:data.nonceStr, // 必填，生成签名的随机串
                            signature:data.signature,// 必填
                            jsApiList: [
                                'onMenuShareTimeline',
                                'onMenuShareAppMessage',
                                'hideMenuItems',
                                'hideAllNonBaseMenuItem',
                                'showMenuItems',
                                'scanQRCode'
                            ] // 必填
                        });
                    }
                }
            });

            wx.ready(function(){
                var shareData = {
                    title: '西贝莜面村',
                    link:  'https://store.xibei.com.cn',
                    imgUrl: 'https://store.xibei.com.cn/static/resource/index/images/logos.jpg',
                    desc: '西贝门店列表'
                };
                // 隐藏所有非基础按钮接口
                wx.hideAllNonBaseMenuItem();
                wx.showMenuItems({
                    menuList:["menuItem:share:timeline", "menuItem:share:appMessage"]
                });
                wx.onMenuShareTimeline(shareData);
                wx.onMenuShareAppMessage(shareData);
            });
        }());
    </script>
</body>
</html>
"""
import re

result = re.findall(
    """controller.init\((.*)\);""", ttt)
tt = result[0]
tt = tt.replace("'", "")
lists = eval(tt)
# lists = list(tt)
print(dir(lists))
print(type(lists))
for i in lists:
    print(i)
