import scrapy

dd = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="renderer" content="webkit">
        <meta http-equiv="X-UA-COMPATIBLE" content="IE=edge,chrome=1" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
        <meta name="baidu-site-verification" content="XzDsKwXKLB" />
        <meta name="format-detection" content="telephone=no">
        <meta name="format-detection" content="address=no">
        <meta name="msvalidate.01" content="221C2BA206DD2C1D975EB3F81DE44ACD" />
        <meta name='keywords' Content='互联网创业,创业报道,融资报道,融资首发阵地,融资媒体,铅笔道,不说谎的创业媒体,发现优质创业者'>
        <meta name='description' Content='铅笔道是国内专业的创投信息服务商，为客户（投资机构、创业者等）提供创投新闻、投融资数据、研究报告等信息服务。旗下主要分为两大业务：媒体与数据。'>
        <meta property='og:type' content="website">
        <meta property='og:title' content='铅笔道'>
        <meta property='og:description' content="铅笔道是国内专业的创投信息服务商，为客户（投资机构、创业者等）提供创投新闻、投融资数据、研究报告等信息服务。旗下主要分为两大业务：媒体与数据。">
        <meta property='og:url' content='http://www.pencilnews.cn/'>
        <meta name="360-site-verification" content="c0efc5369d10fe4d647af23d4591cd87" />
        <meta name="baidu-site-verification" content="4IbCcGODwt" />
        <!-- <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" /> -->
        <title>铅笔道DATA</title>
        <!-- Add to homescreen for Safari on iOS -->
        <!-- 添加至主屏, 从主屏进入会隐藏地址栏和状态栏, 全屏(content="yes") -->
        <meta name="apple-mobile-web-app-capable" content="yes">
        <!-- 系统顶栏的颜色(content = black、white 和 black-translucent)选其一就可以 -->
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <!-- 指定标题 -->
        <meta name="apple-mobile-web-app-title" content="铅笔道">
        <!-- 指定icon, 建议PNG格式-->
        <link rel="apple-touch-icon" href="/imgs/bitmap.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/imgs/icon57x57@1x.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/imgs/icon76x76@1x.png">
        <link rel="apple-touch-icon" sizes="114 x 114" href="/imgs/icon114x114@1x.png">
        <link rel="apple-touch-icon" sizes="144 x 144" href="/imgs/icon144x144@2x.png">
        <link rel="shortcut icon" href="/imgs/shortcut.png" type="image/x-icon" />
        <link rel="icon" href="/imgs/shortcut.png" sizes="48x48" />
        <!-- 新 Bootstrap 核心 CSS 文件 -->
        <link rel="stylesheet" type="text/css" href="/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="/css/toastr.css">
        <link rel="stylesheet" type="text/css" href="/css/iconfonts.css">
        <link rel="stylesheet" type="text/css" href="/css/pay/global.css">
        <!-- //为了做宣传页手机适配加的 -->
        <!-- <link rel="stylesheet" type="text/css" href="/css/header.css"> -->
        <link rel="stylesheet" type="text/css" href="/css/pay/header-former.css">
        <link rel="stylesheet" type="text/css" href="/css/pay/footer.css">
        <link rel="stylesheet" type="text/css" href="/css/pay/sidebar.css">
        <link rel="stylesheet" type="text/css" href="/css/jPages.css">
        <link rel="stylesheet" type="text/css" href="/css/pay/detail.css">
        <script>
        var _hmt = _hmt || [];
        (function () {
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?600e3722e2f1b277d856407f27713124";
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
        })();
    </script>
    </head>
    <body data-spy="scroll" data-target="#nav-bar">
        <div class="outer-wra">
            <div style="display:none;">
                <img src="/imgs/bitmap.png" alt="">铅笔道是国内专业的创投信息服务商，为客户（投资机构、创业者等）提供创投新闻、投融资数据、研究报告等信息服务。旗下主要分为两大业务：媒体与数据。
            </div>
            <!-- 导航栏部分 -->
            <header class="">
                <!-- 顶部和LOGO -->
                <div class="container" id="pc-header-con">
                    <div class="row cate-report">
                        <div class="nav_logo">
                            <a href="/projectlist">
                </a>
                        </div>
                        <ul class="list-inline pull-left cates">
                            <li>
                                <a href="/projectlist">优选项目</a>
                            </li>
                            <li class="hot-icon">
                                <a href="/industryAnalysis">行业分析
                                    <span></span>
                                </a>
                            </li>
                            <li>
                                <a href="/workpanel#collect">工作台</a>
                            </li>
                            <li>
                                <a href="/mymessage">项目动态</a>
                            </li>
                        </ul>
                        <div class="search-log pull-right">
                            <div class="keyword-wra">
                                <span id="clicksearch">
                                    <img src="/imgs/pay/common/search2.png" alt="">
                                </span>
                                <input type="text" name="" placeholder="输入创业项目名称搜索" id="keyword">

                            </div>
                            <div class="header-notify">
                                <a href="/usercenter?cate=my-notify" class="header-notify-icon">
                                    <span class="glyphicon glyphicon-bell"></span>
                                    <span class="header-notify-badge js-header-notify-badge"></span>
                                </a>
                            </div>
                            <div class="login_sigin_con">
                                <span id="login_sign_in">登录</span>
                            </div>
                            <!-- 登录后头像 -->
                            <!-- <span id="user_vip" class="uservip"><img src="/imgs/user_vip2.png" alt=""><span>VIP已登录</span></span> -->
                            <span id="user_vip" class="uservip"></span>
                            <div id="login_on1">
                                <a id="personal_head_1" href="/usercenter?cate=basic-info-wra">
                                    <!-- <div id="show_personal"><span class="icon-mine"></span></div> -->
                                    <div id="show_personal">
                                        <img src="/imgs/defaultAva40.png" onerror="this.src='/imgs/defaultAva40.png'">
                                        <span
                                class=" triangle triangle-down"></span>
                                    </div>
                                </a>
                                <div id="personal_center_1" class="personal_center">
                                    <!-- <a href="/usercenter?cate=my-contact"><div><span class="icon-personal-center"></span>个人中心</div>
                        </a><a href="/usercenter?cate=my-certification"><div><span class="icon-zhubanren"></span>创投认证</div>
                        </a><a id="to_admin_page1" href="http://admin.pencilnews.cn"><div><span class="icon-report"></span>进入后台</div>
                        </a><a id="logout1" href="javascript:void(0)"><div><span class="icon-exit"></span>退出登录</div>
                        </a> -->
        <a href="/usercenter?cate=basic-info-wra">
            <div>个人中心</div>
        </a>
        <!-- <a href="/usercenter?cate=my-certification"><div>创投认证</div></a> -->
        <a id="to_admin_page1" href="http://admin.pencilnews.cn">
            <div>进入后台</div>
        </a>
        <!-- <div class="renew" id="renew">马上续费</div> -->
        <a id="logout1" href="javascript:void(0)">
            <div>退出登录</div>
        </a>
    </div>
</div>
<!-- 登录后头像结束 -->

</div>
<div class="clearfix"></div>
</div>
</div>
<!-- pc导航栏结束 -->
<!-- 手机端侧边导航栏 -->
<!-- <div id="slidenavbar" class="menu-wrap"><div class="slidenavbar_container"><div class="slidenavbar_main_con"><div class="slidenavbar_nav"><ul><li><a href="/projectlist">首页</a></li><li><a href="/workpanel#collect">工作台</a></li><li><a href="/mymessage">项目动态</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div> -->
<!-- 手机端侧边导航栏结束 -->
<!-- 手机上边导航 -->
<!-- <nav id="navbar" class="navbar menu-wrap-navbar"><div class="" id="mobilenavbar"><div><button type="button" id="btn_slidenavbar" class="navbar-toggle"><span class="sr-only">切换导航</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><a href="/" style="display: inline-block;width: 100px;"><img id="mobile_navbar_logo" src="/imgs/logo_without_slogan1x.png"></a><div id="slidenav_search"><div id="slidenav_input_con"><input type="text" id="keyword2"><i class="icon-search"></i><i id="search_prompt">输入创业项目名称搜索</i><img src="/imgs/cancel.png" class="cancel">
                    </div><div id="cancel_search"><p>取消</p></div>
                </div><div id="slidenav_search_con"><p id="slidenav_clicksearch"><span class="icon-search"></span></p>
                </div><div class="slidenav_clearfix"></div></div>
        </div>
    </nav> -->
<!-- 手机上边导航结束 -->


</header>
<div id="slidenavbar_cover"></div>
<div id="slidenavbar_cover2"></div>
<!--导航栏部分-->
<div class="box">
    <div class="content-header js-content-header">
        <div class="container content-project">
            <div class="projectheader clearfix js-project-header">
                <!-- <div class="project-logo"><img src="/imgs/logo.png" alt="" class="img-logo">
                </div><div class="project-content clearfix"><div class="project-name">项目名称<span class="project-buildtime">2015.04</span></div><div class="project-introduction">数字化媒体营销服务提供商</div><span class="project-industry">金融/文化娱乐</span></div><div class="project-right"><span class="project-claim">认领项目</span></div> -->

</div>
<!-- 导航栏 start -->
<div id="myfixed">
    <div id="nav-bar">
        <ul class="nav nav-bar" data-spy="affix" data-offset-top="250" data-offset-bottom="0">
            <li class="nav-bar-item">
                <a href="#project-data" class="bar-item active">项目概述</a>
            </li>
            <li class="nav-bar-item">
                <a href="#busi-data" class="bar-item">业务数据</a>
            </li>
            <!-- <li class="nav-bar-item"><a href="#industry-data" class="bar-item">行业数据</a></li> -->
            <li class="nav-bar-item">
                <a href="#team-data" class="bar-item">团队详情</a>
            </li>
            <li class="nav-bar-item">
                <a href="#round-data" class="bar-item">融资历史</a>
            </li>
            <li class="nav-bar-item">
                <a href="#commercial-data" class="bar-item">工商信息</a>
            </li>
            <li class="nav-bar-item">
                <a href="#relatednews-data" class="bar-item">相关新闻</a>
            </li>
            <li class="nav-bar-item">
                <a href="#competitor-data" class="bar-item">相关竞品</a>
            </li>
            <li class="nav-bar-item">
                <a href="#album-data" class="bar-item">所在专辑</a>
            </li>
            <li class="nav-bar-item">
                <a href="#recruit-data" class="bar-item">公司招聘</a>
            </li>
            <!-- <li class="nav-bar-item"><a href="#competitor-data" class="bar-item">商业计划</a></li> -->
            <!-- <li class="nav-bar-item"><a href="#competitor-data" class="bar-item">融资顾问</a></li> -->

        </ul>
    </div>
</div>
<!-- 导航栏 end -->

</div>
</div>
<!-- container  -->
<div class="container content-wrap js-content">
    <!-- left side  -->
    <div class="left_container">
        <div class="left-info" data-spy="affix" data-offset-top="120" data-offset-bottom="0">
            <!--<div class="project-info"><div class="img-wrap"><img src="" alt="">
                    </div><div class="project-name">笨熊智酷</div><div class="introduce">数字化媒体营销服务提供商</div><div class="industry">企业服务／企业服务／企业服务</div><div class="round-info"><div class="round-need">目标轮次：<span>A轮</span></div><div class="round-need">目标金额：<span>2500万人民币</span></div><div class="round-need">出让比例：<span>20%</span></div>
                    </div>
                </div>-->
<!--<div class="project-related" id="collect-project">
                    收藏项目
                </div><div class="project-related" id="view-bp">
                    查看BP
                </div><div class="project-related" id="get-contact" data-toggle="modal" data-target="#contactModal">
                    获取联系方式
                </div>-->
<div class="related-article">
    <div class="header">
        <span>项目相关文章</span>
        <hr>

    </div>
    <!--<div class="article-item"><a class="title" href="">
                            克己复礼的时刻加快了建设力度
                        </a><div class="article-info"><div class="from">铅笔道</div><div class="time">2012-03-04</div></div>
                    </div>-->
<!--<div class="article-item"><a class="title" href="">
                            克己复礼的时刻加快了建设力度sdkjflksa
                        </a><div class="article-info"><div class="from">36kr</div><div class="time">2012-03-04</div></div>
                    </div>-->

</div>
</div>
</div>
<!-- left side end -->
<!-- right side  -->
<div class="right_container">
    <div class="detail-wrap">
        <!-- 项目 start-->
        <div id="project-data" class="project-section project-data">
            <div class="section-title">
                        项目概述

                <span class="project-feedBack js-project-feedBack" data-key="1">纠错</span>
            </div>
            <hr>
            <div class="section-content longtitle">
                <!-- <div class="item-box"><div class="item-title">
                                市场需求：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                用户画像：
                            </div><div class="item-content">
                                小学生
                            </div></div><div class="item-box"><div class="item-title">
                                产品描述：
                            </div><div class="item-content">
                                一家在线少儿美术内容提供商，以“思维导向”的引导方式设计课程，同时以在线的形式给家长们另一种陪伴孩子的选择，家长每周匀出2小时，引导孩子学画，在亲子互动中发现孩子的点滴变化。
                            </div></div><div class="item-box"><div class="item-title">
                                产品特点：
                            </div><div class="item-content">
                                在线美术教育，自研发优质视频课程；引导方式编排课程，注重引导儿童创作；多样化、标准化课程设计模型，1v1指导跟踪式教学。
                            </div></div><div class="item-box"><div class="item-title">
                                客户画像：
                            </div><div class="item-content">
                                幼儿园、教育培训机构
                            </div></div><div class="item-box"><div class="item-title">
                                收入来源：
                            </div><div class="item-content">
                                在线美术教育，自研发优质视频课程；引导方式编排课程，注重引导儿童创作；多样化、标准化课程设计模型，1v1指导跟踪式教学。
                            </div></div><div class="item-box"><div class="item-title">
                                主攻市场：
                            </div><div class="item-content">
                                在线美术教育，自研发优质视频课程；引导方式编排课程，注重引导儿童创作；多样化、标准化课程设计模型，1v1指导跟踪式教学。
                            </div></div><div class="item-box"><div class="item-title">
                                获客方式：
                            </div><div class="item-content">
                                在线美术教育，自研发优质视频课程；引导方式编排课程，注重引导儿童创作；多样化、标准化课程设计模型，1v1指导跟踪式教学。
                            </div></div>-->

</div>
</div>
<div id="bp-data" class="project-section bp-data js-bp-data">
    <div class="section-title">
                        商业计划书

        <span class="project-feedBack js-project-feedBack" data-key="6">纠错</span>
    </div>
    <hr>
    <div class="section-content clearfix bp-section-content">
        <img src="/imgs/submit_project/pdf@2x.png" alt="" class="img-pdf">
        <div class="pdf-box">
            <div class="box-left">
                <div class="pdf-name js-pdf-name">称这里是文件名称.pdf</div>
                <!-- <div class="pdf-size">14.8M</div> -->

            </div>
            <div class="box-right js-box-right">
                <button class="get-bp" id="view-bp">点击查看</button>
                <!-- <span class="send-out-bp js-send-out-bp">发送到我的邮箱</span> -->

            </div>
        </div>
    </div>
</div>
<div id="financing-advisor-data" class="project-section financing-advisor-data js-financing-advisor-data">
    <div class="section-title">
                        融资顾问

        <span class="project-feedBack js-project-feedBack" data-key="7">纠错</span>
    </div>
    <hr>
    <div class="section-content">
        <ul class="advisor-box js-advisor-box">
            <!-- <li class="advisor-item clearfix"><img src="/imgs/submit_project/pdf@2x.png" alt="" class="img-advisor"><div class="advisor-content"><div class="left-content"><p class="name">李四</p><p class="position">IDG资本/投资经理</p></div><button class="get-contact js-get-advisor-contact" data-id="123824">联系TA</button></div>
                            </li><li class="advisor-item clearfix"><img src="/imgs/submit_project/pdf@2x.png" alt="" class="img-advisor"><div class="advisor-content"><div class="left-content"><p class="name">李四</p><p class="position">IDG资本/投资经理</p></div><button class="get-contact js-get-advisor-contact" data-id="2">联系TA</button></div>
                            </li> -->

</ul>
</div>
</div>
<div id="busi-data" class="project-section busi-data">
    <div class="section-title">
                        业务数据

        <span class="project-feedBack js-project-feedBack" data-key="3">纠错</span>
    </div>
    <hr>
    <div class="no-auth">
        <div id="no-auth1" style="display:block;">
            <p>您当前帐号为普通账号，申请成为认证用户后可查看所有项目业务数据</p>
            <!-- <button id="bp-buy" onclick="ga('send', 'event', '项目详情页', '点击跳转立即购买', '158d3fd6d2eaa07d')"><span>立即开通</span></button> -->
            <button onclick="ga('send', 'event', '项目详情页', '点击跳转立即购买', '158d3fd6d2eaa07d')">
                <a href="/datacert?from=projectdetail&id=158d3fd6d2eaa07d">
                    <span>立即认证</span>
                </a>
            </button>
            <!-- <a class="try-use" id="bp-try" onclick="ga('send', 'event', '项目详情页', '点击跳转申请试用', '158d3fd6d2eaa07d')">申请试用</a> -->
            <!-- <a class="try-use" id="bp-buy" onclick="ga('send', 'event', '项目详情页', '点击跳转立即开通', '158d3fd6d2eaa07d')">立即开通</a> -->

        </div>
        <div id="no-auth2" style="display:none;">
            <p>您提交的认证信息正在审核中...</p>
        </div>
    </div>
    <div class="section-content longtitle">
        <!-- <div class="item-box"><div class="item-title">
                                供应商数据：
                            </div><div class="item-content">
                                很显然我是一套数据，我主要来源于实体企业数据很显然我是一套数据，我主要来源于实体企业数据很显然我是一套数据，我主要来源于实体企业数据很显然我是一套数据，我主要来源于实体企业数据很显然我是一套数据，我主要来源于实体企业数据
                            </div></div><div class="item-box"><div class="item-title">
                                用户数据：
                            </div><div class="item-contentd"><div class="user-data"><div class="data-item">
                                        日新增：<span>3000</span></div><div class="data-item">
                                        日新增：<span>4333</span></div><div class="data-item">
                                        日新增：<span>sdjfkljklsd</span></div><div class="data-item">
                                        日新增：<span>344</span></div><div class="data-item">
                                        日新增：<span>3000</span></div><div class="data-item">
                                        日新增：<span>苏打粉可圣诞节疯狂了临时决定了疯狂的是</span></div><div class="data-item">
                                        日新增：<span>3000</span></div>
                                </div>
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                财务数据：
                            </div><div class="item-content"><div class="user-data"><div class="data-item">
                                        日新增：<span>3000</span></div><div class="data-item">
                                        日新增：<span>4333</span></div><div class="data-item">
                                        日新增：<span>sdjfkljklsd</span></div><div class="data-item">
                                        日新增：<span>344</span></div><div class="data-item">
                                        日新增：<span>3000</span></div><div class="data-item">
                                        日新增：<span>苏打粉可圣诞节疯狂了临时决定了疯狂的是</span></div><div class="data-item">
                                        日新增：<span>3000</span></div>
                                </div>
                            </div>
                        </div> -->

</div>
<div id="avgBtn" class="average-button"></div>
</div>
<div id="industry-data" class="project-section industry-data">
    <div class="section-title">
                        行业数据

        <span class="project-feedBack js-project-feedBack" data-key="4">纠错</span>
    </div>
    <hr>
    <div class="section-content longtitle">
        <!-- <div class="item-box"><div class="item-title">
                                市场规模：
                            </div><div class="item-content">
                                格局什么什么去判断这块饼有多大。判断依据具体都是些什么？
                            </div></div><div class="item-box"><div class="item-title">
                                用户规模：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                客户规模：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                国外对标目标：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                主要竞争对手：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                我方优势：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                我方劣势：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                未来目标：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div> -->

</div>
</div>
<div id="team-data" class="project-section team-data">
    <div class="section-title">
                        团队详情

        <span class="project-feedBack js-project-feedBack" data-key="2">纠错</span>
    </div>
    <hr>
    <div class="section-content longtitle ">
        <!-- <div class="item-box"><div class="item-title">
                                团队构成：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                团队优势：
                            </div><div class="item-content">
                                1. 培训费用与教育水平不匹配，费用严重偏高；<br> 2.线下教育机构，画室美术老师的美术水平参差不齐，比较混乱； <br> 3.机构画室以小班，大班的形式开课，美术老师很难抓每一个学生，逐渐演变为只抓头部学生；
                                <br> 4.学生画的作品，大多数并非个人全程作画，更多是老师帮忙画
                            </div>
                        </div><div class="item-box"><div class="item-title">
                                创始人团队是如何认识的：
                            </div><div class="item-content">
                                培训费用与教育水平不匹配，费用严重偏高；
                            </div></div><div class="item-box"><div class="item-title">
                                创业前是否有共事经验：
                            </div><div class="item-content">
                                培训费用与教育水平不匹配，费用严重偏高；
                            </div></div><div class="item-box"><div class="core-team-title">
                                核心成员信息：
                            </div><div class="core-team"><div class="person-head"><div class="img-wrap">
                                        梁
                                    </div></div><div class="person-info"><div class="person-name">梁山伯 | CEO兼创始人</div><div class="person-graduate">毕业于清华大学</div><div class="former-info">原公司：<span class="former-company">网易科技</span>原公司职位：<span class="fromer-position">运营总监</span></div><div class="person-introduce">
                                        刘延兵，天泓光电创始人。连续创业者，2006年开始专注环境、环保与健康领域，2012年带领团队投入负离子技术的研究、开发和应用，先后获得PCT、美国、日本、中国等国内外30余项专利。
                                    </div></div>
                            </div><div class="core-team"><div class="person-head"><div class="img-wrap">
                                        梁
                                    </div></div><div class="person-info"><div class="person-name">梁山伯 | CEO兼创始人</div><div class="person-graduate">毕业于清华大学</div><div class="former-info">原公司：<span class="former-company">网易科技</span>原公司职位：<span class="fromer-position">运营总监</span></div><div class="person-introduce">
                                        刘延兵，天泓光电创始人。连续创业者，2006年开始专注环境、环保与健康领域，2012年带领团队投入负离子技术的研究、开发和应用，先后获得PCT、美国、日本、中国等国内外30余项专利。
                                    </div></div>
                            </div>
                        </div> -->

</div>
</div>
<div id="round-data" class="project-section round-data">
    <div class="section-title">
                        融资历史

        <span class="project-feedBack js-project-feedBack" data-key="5">纠错</span>
    </div>
    <hr>
    <div class="section-content">
        <div class="round-bar">
            <div class="round-bar-item col-1">时间轴</div>
            <div class="round-bar-item col-2">融资类型</div>
            <div class="round-bar-item col-3">融资币种</div>
            <div class="round-bar-item col-4">融资金额</div>
            <div class="round-bar-item col-5">投资机构</div>
            <div class="round-bar-item col-6">FA</div>
            <div class="round-bar-item col-7">估值</div>
        </div>
        <!-- <div class="round-info"><div class="round-info-item col-1">2016.19</div><div class="round-info-item col-2">A轮</div><div class="round-info-item col-3">人民币</div><div class="round-info-item col-4">300万</div><div class="round-info-item col-5">阿里巴巴</div><div class="round-info-item col-6">不想</div><div class="round-info-item col-7">200万</div></div> -->


    </div>
</div>
<div id="commercial-data" class="project-section commercial-data">
    <div class="section-title">
                        工商信息

        <span class="project-feedBack js-project-feedBack" data-key="8">纠错</span>
    </div>
    <hr>
    <!-- <div class="section-content"><div class="item-box"><div class="item-title">
                                公司名称：
                            </div><div class="item-content">
                                长春天泓光电技术有限公司
                            </div></div><div class="item-box"><div class="item-title">
                                法人代表：
                            </div><div class="item-content">
                                薛之谦
                            </div></div><div class="item-box"><div class="item-title">
                                成立时间：
                            </div><div class="item-content">
                                2012-03-04
                            </div></div><div class="item-box"><div class="item-title">
                                注册资本：
                            </div><div class="item-content">
                                300万
                            </div></div>

                    </div> -->
<!-- <table><tr><th>股东</th><th>持股比例</th><th>认缴出资日期</th><th>股东类型</th></tr><tr><td></td><td></td><td></td><td></td></tr>
                    </table> -->

</div>
<div id="relatednews-data" class="project-section relatednews-data js-relatednews-data">
    <div class="section-title">
                        相关新闻
                    </div>
    <hr>
    <div class="section-content">
        <ul class="newslists" id="articles_list_container">
            <!-- <li class="news-item clearfix"><img src="/imgs/submit_project/pdf@2x.png" alt="" class="news-img"><div class="content-box"><p class="news-title">新宜资本马占田：消费领域是个大赛道 所以创业者容易迷路</p><p class="news-build-time">2018-09-12 铅笔道</p></div>
                            </li><li class="news-item"><div class="content-box"><p class="news-title">新宜资本马占田：消费领域是个大赛道 所以创业者容易迷路</p><p class="news-build-time">2018-09-12 铅笔道</p></div>
                            </li><li class="news-item"><img src="/imgs/submit_project/pdf@2x.png" alt="" class="news-img"><div class="content-box"><p class="news-title">新宜资本马占田：消费领域是个大赛道 所以创业者容易迷路</p><p class="news-build-time">2018-09-12 铅笔道</p></div>
                            </li> -->

</ul>
<!-- 分页信息 -->
<div class="articles_pages_container" id="articles_pages_container">
    <div class="articles_page js-articles-page">

                            </div>
    <!-- <div class="page-jump-container"><input class="page-jump-input" id="page-jump-input" type="text" placeholder="页码"><button class="page-jump-btn" id="page-jump-btn">跳转</button></div> -->

</div>
<div class="getmore-btn-box js-getmore-btn-box">
    <span class="get-more js-get-more">查看更多</span>
</div>
</div>
</div>
<div id="competitor-data" class="project-section competitor-data">
    <div class="section-title">
                        相关竞品
                    </div>
    <hr>
    <div class="section-content">
        <div class="competitor-bar">
            <div class="competitor-bar-item col-co-1">项目</div>
            <div class="competitor-bar-item col-co-2">当前轮次</div>
            <div class="competitor-bar-item col-co-3">地区</div>
            <div class="competitor-bar-item col-co-4">行业</div>
        </div>
        <div class="competitor-info">
            <div class="competitor-info-item col-co-1">
                <div class="competitor-base-info">
                    <div class="competitor-logo">
                        <div class="img-wrap">
                            <a target="_blank" href="/projectdetail/9c56d823f2fe0624?from=competitive_project_list">
                                <img src="https://odonohz90.qnssl.com/FoKjkAyj0zqVCFjCy58XsQHiRT_V" width="50" alt="">

                            </a>
                        </div>
                    </div>
                    <div class="competitor-title">
                        <a target="_blank" href="/projectdetail/9c56d823f2fe0624?from=competitive_project_list">
                            <div class="competitor-name">摩西机器人 </div>
                        </a>
                        <p class="competitor-desc">工业机器人研产商</p>
                    </div>
                </div>
            </div>
            <div class="competitor-info-item col-co-2">战略融资</div>
            <div class="competitor-info-item col-co-3">重庆</div>
            <div class="competitor-info-item col-co-4">人工智能</div>
        </div>
        <div class="competitor-info">
            <div class="competitor-info-item col-co-1">
                <div class="competitor-base-info">
                    <div class="competitor-logo">
                        <div class="img-wrap">
                            <a target="_blank" href="/projectdetail/f02d3e669f98c9dc?from=competitive_project_list">
                                <img src="https://odonohz90.qnssl.com/FgkKByMf74kkeQTC5h6b3xPTZgFF" width="50" alt="">

                            </a>
                        </div>
                    </div>
                    <div class="competitor-title">
                        <a target="_blank" href="/projectdetail/f02d3e669f98c9dc?from=competitive_project_list">
                            <div class="competitor-name">图灵机器人Turing OS</div>
                        </a>
                        <p class="competitor-desc">一家个性化智能机器人平台</p>
                    </div>
                </div>
            </div>
            <div class="competitor-info-item col-co-2">收购并购</div>
            <div class="competitor-info-item col-co-3">北京</div>
            <div class="competitor-info-item col-co-4">企业服务/人工智能</div>
        </div>
        <div class="competitor-info">
            <div class="competitor-info-item col-co-1">
                <div class="competitor-base-info">
                    <div class="competitor-logo">
                        <div class="img-wrap">
                            <a target="_blank" href="/projectdetail/2988efe094f9caee?from=competitive_project_list">
                                <img src="https://odonohz90.qnssl.com/FtW55DGEIBgyYziEkghX0xqgNXqz" width="50" alt="">

                            </a>
                        </div>
                    </div>
                    <div class="competitor-title">
                        <a target="_blank" href="/projectdetail/2988efe094f9caee?from=competitive_project_list">
                            <div class="competitor-name">物灵科技</div>
                        </a>
                        <p class="competitor-desc">生活服务类机器人研发商</p>
                    </div>
                </div>
            </div>
            <div class="competitor-info-item col-co-2">Pre-A轮</div>
            <div class="competitor-info-item col-co-3">北京</div>
            <div class="competitor-info-item col-co-4">人工智能</div>
        </div>
        <div class="competitor-info">
            <div class="competitor-info-item col-co-1">
                <div class="competitor-base-info">
                    <div class="competitor-logo">
                        <div class="img-wrap">
                            <a target="_blank" href="/projectdetail/8a5a5d6fe99d21b9?from=competitive_project_list">
                                <img src="https://odonohz90.qnssl.com/FojDZHgQmF9Tb1Moz_UNbIslSo_G" width="50" alt="">

                            </a>
                        </div>
                    </div>
                    <div class="competitor-title">
                        <a target="_blank" href="/projectdetail/8a5a5d6fe99d21b9?from=competitive_project_list">
                            <div class="competitor-name">来福谐波</div>
                        </a>
                        <p class="competitor-desc">机器人高精密谐波减速器生产商</p>
                    </div>
                </div>
            </div>
            <div class="competitor-info-item col-co-2">B轮</div>
            <div class="competitor-info-item col-co-3">暂无</div>
            <div class="competitor-info-item col-co-4">人工智能</div>
        </div>
        <div class="competitor-info">
            <div class="competitor-info-item col-co-1">
                <div class="competitor-base-info">
                    <div class="competitor-logo">
                        <div class="img-wrap">
                            <a target="_blank" href="/projectdetail/3570cadbf07414dc?from=competitive_project_list">
                                <img src="https://odonohz90.qnssl.com/FobCtUR4HdKxN1dKmSMzNmFel2Pr" width="50" alt="">

                            </a>
                        </div>
                    </div>
                    <div class="competitor-title">
                        <a target="_blank" href="/projectdetail/3570cadbf07414dc?from=competitive_project_list">
                            <div class="competitor-name">中设机器人</div>
                        </a>
                        <p class="competitor-desc">智能工业机器人研发商</p>
                    </div>
                </div>
            </div>
            <div class="competitor-info-item col-co-2">新三板</div>
            <div class="competitor-info-item col-co-3">广州</div>
            <div class="competitor-info-item col-co-4">人工智能</div>
        </div>
        <div class="competitor-info">
            <div class="competitor-info-item col-co-1">
                <div class="competitor-base-info">
                    <div class="competitor-logo">
                        <div class="img-wrap">
                            <a target="_blank" href="/projectdetail/c8703014049bf9d5?from=competitive_project_list">
                                <img src="https://odonohz90.qnssl.com/FgXfshW_8577TMhXiZRnGw7KufJD" width="50" alt="">

                            </a>
                        </div>
                    </div>
                    <div class="competitor-title">
                        <a target="_blank" href="/projectdetail/c8703014049bf9d5?from=competitive_project_list">
                            <div class="competitor-name">机器之心</div>
                        </a>
                        <p class="competitor-desc">专注于人工智能、机器人等领域的科技媒体</p>
                    </div>
                </div>
            </div>
            <div class="competitor-info-item col-co-2">A轮</div>
            <div class="competitor-info-item col-co-3">北京</div>
            <div class="competitor-info-item col-co-4">企业服务</div>
        </div>
    </div>
</div>
<div id="album-data" class="project-section album-data js-album-data">
    <div class="section-title">
                        所在专辑
                    </div>
    <hr>
    <div class="section-content ">
        <ul class="albumlist row clearfix" id="album_list_container">
            <!-- <li class="album-item col-md-4"><p class="title">2018年最热的十大项目2018年最热的十大项目2018年最热的十大项目2018年最热的十大项目2018年最热的十大项目2018年最热的十大项目2018年最热的十大项目2018年最热的十大项目</p><p class="albumDetail"><span>共10个项目</span><span>2018-09-12</span></p><img src="/imgs/submit_project/pdf@2x.png" alt="" class="album-img">
                            </li><li class="album-item col-md-4"><p class="title">2018年最热的十大项目</p><p class="albumDetail"><span>共10个项目</span><span>2018-09-12</span></p><img src="/imgs/submit_project/pdf@2x.png" alt="" class="album-img">
                            </li><li class="album-item col-md-4"><p class="title">2018年最热的十大项目</p><p class="albumDetail"><span>共10个项目</span><span>2018-09-12</span></p><img src="/imgs/submit_project/pdf@2x.png" alt="" class="album-img">
                            </li> -->

</ul>
<div class="customBtns js-customBtns">
    <span class="arrowPrev"></span>
    <span class="arrowNext"></span>
</div>
<div class="js-album-pages" style="display: none"></div>
</div>
</div>
<div id="recruit-data" class="project-section recruit-data js-recruit-data">
    <div class="section-title">
                        公司招聘
                    </div>
    <hr>
    <div class="section-content">
        <div class="competitor-bar">
            <div class="competitor-bar-item col-co-1">职位</div>
            <div class="competitor-bar-item col-co-2">城市</div>
            <div class="competitor-bar-item col-co-3">薪资</div>
            <div class="competitor-bar-item col-co-4">发布时间</div>
        </div>
        <div class="recruit-info-box" id="recruit_list_container">
            <!-- <div class="competitor-info recruit-info"><div class="competitor-info-item col-co-1">前端开发工程师</div><div class="competitor-info-item col-co-2">北京</div><div class="competitor-info-item col-co-3">10/20k</div><div class="competitor-info-item col-co-4">2018-09-12</div></div><div class="competitor-info recruit-info"><div class="competitor-info-item col-co-1">前端开发工程师</div><div class="competitor-info-item col-co-2">北京</div><div class="competitor-info-item col-co-3">10/20k</div><div class="competitor-info-item col-co-4">2018-09-12</div></div><div class="competitor-info recruit-info"><div class="competitor-info-item col-co-1">前端开发工程师</div><div class="competitor-info-item col-co-2">北京</div><div class="competitor-info-item col-co-3">10/20k</div><div class="competitor-info-item col-co-4">2018-09-12</div></div> -->

</div>
<!-- 分页信息 -->
<div class="articles_pages_container js-recruit-pages-container">
    <div class="articles_page js-recruit-page">

                            </div>
</div>
<div class="getmore-btn-box js-recruit-getmore-box">
    <span class="get-more js-recruit-getmore">查看更多</span>
    <!-- <span class="get-more">没有更多了</span> -->

</div>
</div>
</div>
<!-- 项目 end -->

</div>
</div>
<!-- right side end -->

</div>
<!-- container end  -->
<div class="content-footer content-footer-fixed js-content-footer">
    <div class="footer-btn-box js-footer-btn">
        <!-- <span class="btn-related" id="get-contact">获取联系方式</span><span class="btn-fllow" id="collect-project">关注项目</span> -->

    </div>
</div>
</div>
<!-- modal -->
<div class="modal fade" id="contactModal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="contact-info">
                <div class="person-head-img">

                </div>
                <div class="project-name">
                    项目名字
                </div>
                <div class="project-intro">
                    1句话介绍项目。
                </div>
                <div class="contact-info-content">
                    <div class="person-info">
                        <div class="title">姓名：</div>
                        <div class="content">李刚</div>
                    </div>
                    <div class="person-info">
                        <div class="title">微信：</div>
                        <div class="content">1234567845678</div>
                    </div>
                    <div class="person-info">
                        <div class="title">电话：</div>
                        <div class="content">3456789</div>
                    </div>
                </div>
            </div>
        </div>
        <!-- /.modal-content -->

    </div>
    <!-- /.modal-dialog -->
</div>
<!-- /.modal -->
<!-- 提醒付费modal -->
<div class="modal fade" id="noAuthModal" role="dialog" tabindex="-1">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body no" style="display: block;">
                <p>现在认证投资人，即刻享受30天VIP权限，项目业务数据更为直观，联系方式轻松获取</p>
            </div>
            <div class="modal-body ok" style="display:none;text-align: center;margin-bottom: 30px;">
                <p>您提交的认证信息正在审核中...</p>
            </div>
            <div class="modal-footer no">
                <!-- <button type="button" id="bp-buy" onclick="ga('send', 'event', '项目详情页', '点击跳转立即购买', '158d3fd6d2eaa07d')" class="btn btn-primary"><span>立即开通</span></button> -->
                <button type="button" onclick="ga('send', 'event', '项目详情页', '点击跳转立即认证', '158d3fd6d2eaa07d')" class="btn btn-primary">
                    <a href="http://pencilnews.mikecrm.com/sLO7ZTK" target="_blank">
                        <span>立即认证</span>
                    </a>
                </button>
                <!-- <a id="bp-try" onclick="ga('send', 'event', '项目详情页', '点击跳转申请试用', '158d3fd6d2eaa07d')" style="display: block; text-decoration: underline; color: #4f84ca; margin-top: 15px;cursor:pointer;">申请试用</a> -->
                <a id="bp-buy" onclick="ga('send', 'event', '项目详情页', '点击跳转立即购买', '158d3fd6d2eaa07d')" style="display: block; text-decoration: underline; color: #4f84ca; margin-top: 15px;cursor:pointer;">立即开通</a>
            </div>
        </div>
        <!-- /.modal-content -->

    </div>
    <!-- /.modal-dialog -->
</div>
<!-- 提醒付费modal结束 -->
<!--业务数据平均数展示modal  -->
<div class="modal fade" id="showBusiDataAvg" role="dialog" tabindex="-1">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
            </div>
            <div class="modal-body">

            </div>
            <div class="modal-footer">

            </div>
        </div>
        <!-- /.modal-content -->

    </div>
    <!-- /.modal-dialog -->
</div>
<!--业务数据平均数展示modal结束  -->
<!--融资需求平均数展示modal  -->
<div class="modal fade" id="showRoundDataAvg" role="dialog" tabindex="-1">
    <div class="modal-dialog" role="document">
        <div class="modal-content">

        </div>
        <!-- /.modal-content -->

    </div>
    <!-- /.modal-dialog -->
</div>
<!--融资需求平均数展示modal结束  -->
<!--  确认委托弹框  -->
<div class="modal entrustment-modal js-entrustment-modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p></p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span class="btn-lf">取消</span>
                    <span class="btn-rt">确认委托</span>
                </div>
                <p class="footer-title"></p>
                <!-- <p class="footer-title">您本周剩余使用次数<span class="start">0</span>次，寻找失败会退还您的使用次数</p> -->

            </div>
        </div>
    </div>
</div>
<!--  委托成功提示框  -->
<div class="modal" id="confirm_modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>委托成功！</p>
                <p>委托结果会有铅笔道工作人员与您对接</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span id="comfirm-btn" class="btn-rt">确 认</span>
                </div>
                <p class="footer-title"></p>
            </div>
        </div>
    </div>
</div>
<!--  认领项目提示框  -->
<div class="modal" id="claim_confirm_modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>您已经认领/提交过项目了！</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span id="claim-comfirm-btn" class="btn-rt">确 认</span>
                </div>
                <p class="footer-title"></p>
                <!-- <p class="footer-title">您本周剩余使用次数<span class="end">0</span>次，寻找失败会退还您的使用次数</p> -->

            </div>
        </div>
    </div>
</div>
<!-- 获取联系方式相关弹窗 -->
<div class="modal pre-add-contact js-pre-add-contact" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>您当前帐号尚未认证，不具备查看权限 请您完成认证后再使用</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span class="btn-lf">取消</span>
                    <span class="btn-rt">前往认证</span>
                </div>
                <p class="footer-title"></p>
            </div>
        </div>
    </div>
</div>
<!-- 查看bp相关弹窗 -->
<div class="modal pre-add-bp js-pre-add-bp" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>您当前帐号尚未认证，不具备查看权限 请您完成认证后再使用</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span class="btn-lf">取消</span>
                    <span class="btn-rt">前往认证</span>
                </div>
                <p class="footer-title"></p>
            </div>
        </div>
    </div>
</div>
<!-- 查看BP确认框 -->
<div class="modal pre-add-bp js-check-bp" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>查看BP详情，让您更深度的了解项目</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span class="btn-rt">
                        <a href='https://www.pencilnews.cn' target='_blank'>确认查看</a>
                    </span>
                </div>
                <p class="footer-title"></p>
            </div>
        </div>
    </div>
</div>
<!-- 提交项目反馈modal -->
<div class="modal projectFeedback_modal js-projectFeedback-modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span id="img_close" class="img"></span>
            </div>
            <div class="modal-body">
                <div class="title">此项目已入铅笔道前端展示库，不可以直接修改哦~如有信息不符请反馈：</div>
                <textarea name="market_demand" placeholder="请输入正确的信息，工作人员将及时核对处理"></textarea>
            </div>
            <div class="modal-footer">
                <div class="feedback-btn">提交反馈</div>
            </div>
        </div>
    </div>
</div>
<!-- 提交项目反馈(商业计划书bp)modal -->
<div class="modal projectFeedback_modal js-projectFeedback-bp-modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span id="img_close" class="img"></span>
            </div>
            <div class="modal-body">
                <div class="title">此项目已入铅笔道前端展示库，不可以直接修改哦~如有信息不符请反馈：</div>
                <div class="add_feedback_bp">
                    <div class="upload_bp">
                        <div class="img">
                            <span class="img-span"></span>
                        </div>
                        <div class="file-box"></div>
                        <div class="bp_name js-bp-name"></div>
                        <div class="btn-box">
                            <div class="btn-span" id="feedback_upload_bp_father">选择文件

                                <input type="file" name="bp_file" class="js-upload-bp" accept="application/pdf">

                            </div>
                        </div>
                        <p class="subtitle">目前仅支持PDF格式且文件小于10M</p>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <div class="feedback-btn">提交反馈</div>
            </div>
        </div>
    </div>
</div>
<!-- 反馈成功提示框 -->
<div class="modal entrustment-modal" id="feedback_confirm_modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>反馈成功，我们会尽快处理你的请求</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn">
                    <span class="btn-rt">关闭</span>
                </div>
                <p class="footer-title"></p>
                <!-- <p class="footer-title">您本周剩余使用次数<span class="start">0</span>次，寻找失败会退还您的使用次数</p> -->

            </div>
        </div>
    </div>
</div>
<!-- 主页部分结束 -->
<!-- 登录弹出层 -->
<!-- 登录弹出层 -->
<!------------------------------------------>
<div class="login_form_con" id="regist_container">
    <!-- top -->
    <div class="login_form_close_img">
        <img src="/imgs/close_black.png">

    </div>
    <div class="login_form_top">
        <!-- left -->
        <div class="login_form_left pull-left">
            <div class="login_form_title">
                <h3>欢迎来到铅笔道</h3>
            </div>
            <div class="login_form_pc">
                <div class="login_form_input login_form_phonenum">
                    <div class="login_form_areacode">
                        <div>+86</div>
                    </div>
                    <input id="phone_number" type="text" placeholder="手机号">

                </div>
                <div class="login_form_input">
                    <input id="cert" type="text" placeholder="请输入6位验证码">
                    <button class="login_form_verify" id="get_cert_btn">
                        获取验证码
                    </button>
                </div>
                <!-- <div class="login_form_input"><input id="pwd" type="password" placeholder="请设置密码">
                </div> -->
                <div class="login_form_checkbox login_form_forget_con">
                    <div>
                        <span class="light_grey" id="btn_sign_in">密码登录</span>
                    </div>
                    <!-- <div class="pull-right"><div class="login_form_forget" id="forgetpw">忘记密码</div></div> -->

                </div>
                <div class="clearfix"></div>
                <div class="login_form_input">
                    <div class="login_form_btn" id="register">
                        进入
                    </div>
                </div>
                <div class="login_form_left_bottom">
                    <div class="login_form_third_title">其他方式登录：</div>
                    <div class="login_form_third_pic wechat_qrcode_login">
                        <img src="/imgs/m_login_wechat_g.png">

                    </div>
                </div>
                <div class="login-policy">
                    未注册手机自动注册并同意

                    <a href="/privacy" target="_blank">《隐私条款及用户协议》</a>
                </div>
            </div>
        </div>
    </div>
    <!-- bottom -->
    <div class="download-qrcode-handle-open">
        下载铅笔道APP
    </div>
</div>
<div class="login_form_con" id="login_container">
    <div class="login_form_close_img">
        <img src="/imgs/close_black.png">

    </div>
    <!-- top -->
    <div class="login_form_top">
        <!-- left -->
        <div class="login_form_left pull-left">
            <div class="login_form_title">
                <h3>欢迎来到铅笔道</h3>
            </div>
            <div class="login_form_pc">
                <div class="login_form_input">
                    <input id="username" type="text" placeholder="请输入注册的手机号码">

                </div>
                <div class="login_form_input">
                    <input id="password" type="password" placeholder="请输入您的密码">

                </div>
                <div class="login_form_checkbox login_form_forget_con">
                    <div>
                        <span class="light_grey" id="btn_sign_up">验证码登录</span>
                    </div>
                    <div class="pull-right">
                        <div class="login_form_forget" id="forgetpw">忘记密码</div>
                    </div>
                </div>
                <div class="clearfix"></div>
                <div class="login_form_input">
                    <div class="login_form_btn" id="login_button">
                        进入
                    </div>
                </div>
                <div class="login_form_left_bottom">
                    <div class="login_form_third_title">其他方式登录：</div>
                    <div class="login_form_third_pic wechat_qrcode_login">
                        <img src="/imgs/m_login_wechat_g.png">

                    </div>
                </div>
                <div class="login-policy">
                    未注册手机自动注册并同意

                    <a href="/privacy" target="_blank">《隐私条款及用户协议》</a>
                </div>
            </div>
        </div>
    </div>
    <!-- bottom -->
    <div class="download-qrcode-handle-open">
        下载铅笔道APP
    </div>
</div>
<div class="login_form_con" id="forget_pwd_container">
    <div class="login_form_close_img">
        <img src="/imgs/close_black.png">

    </div>
    <!-- top -->
    <div class="login_form_top">
        <div id="btn_sign_in_2" class="login_form_back">
            <div>
                <img src="/imgs/back_to_login.png">

            </div>
            <div>
                返回账号密码登录
            </div>
        </div>
        <!-- left -->
        <div class="login_form_left pull-left">
            <div class="login_form_title">
                <h3>密码找回</h3>
            </div>
            <div class="login_form_pc">
                <div class="login_form_input">
                    <input id="forget_phone_number" type="text" placeholder="请输入手机号">

                </div>
                <div class="login_form_input">
                    <input id="forget_cert" type="text" placeholder="请输入6位验证码">
                    <button class="login_form_verify" id="forget_get_cert_btn">
                        获取验证码
                    </button>
                </div>
                <div class="login_form_input">
                    <input id="forget_pwd" type="password" placeholder="请设置新密码">

                </div>
                <div class="clearfix"></div>
                <div class="login_form_input">
                    <div class="login_form_btn" id="resetpwd">
                        保存
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- bottom -->
    <div class="download-qrcode-handle-open">
        下载铅笔道APP
    </div>
</div>
<div id="download-qrcode">
    <div class="download-qrcode-wrap">
        <div class="qrcode-title">
            下载铅笔道APP
        </div>
        <div class="download-qrcode-img-wrap">
            <img src="/imgs/app_qrcode.png" alt="">

        </div>
    </div>
    <div class="download-qrcode-handle-close">
        关闭二维码
    </div>
</div>
<div class="login_bg_mask" id="login_bg"></div>
<!-- 登录弹出层 -->
<!-- 登录弹出层结束 -->
<!-- footer部分和置顶挂件 -->
<!-- footer -->
<footer id="main-footer">
    <div class="container">
        <div class="footer-contact">
            <div class="row">
                <div class="col-md-3 hidden-sm hidden-xs ">
                    <a href="/" title="铅笔道-发现优质创业者">
                        <img src="/imgs/new_logo.png" alt="铅笔道 发现优质创业者" class="img-responsive">

                    </a>
                </div>
                <div class="col-md-6  col-sm-12 ">
                    <ul class="footer-menu">
                        <li>
                            <a href="/submit_project">求报道</a>
                        </li>
                        <li>
                            <a href="/report">我要爆料</a>
                        </li>
                        <li>
                            <a href="/join">加入我们</a>
                        </li>
                        <li>
                            <a href="/copyright">版权声明</a>
                        </li>
                        <li>
                            <a href="/about">关于我们</a>
                        </li>
                        <li>
                            <a href="/contact">联系我们</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="copyright">
            <p>© COPYRIGHT 2015-2018 铅笔道 All Rights Reserved. 京ICP备15043184号.</p>
        </div>
    </div>
    <!-- <div class="innerPageAdd"></div> -->
</footer>
<!-- 置顶 微信 微博 -->
<ul class="to-top card">
    <li id="topArrow">
        <a class="icon-top"></a>
    </li>
    <li>
        <a class="icon-wechat2"></a>
    </li>
    <li>
        <a href="http://service.weibo.com/share/share.php?url=&title=pencilnews铅笔道官网" target="_blank" class="icon-sina_nobg"></a>
    </li>
    <li class="service">
        <a class="icon-service">
        </a>
        <div >
            <span class="icon-tel"></span>
            <span>010-82169084</span>
        </div>
    </li>
</ul>
<!-- 微信二维码 -->
<div class="qr-wra">
    <div class="qrcode card">
        <h3>
              分享到微信

            <i class="fa fa-times pull-right"></i>
        </h3>
        <!-- <img src="imgs/qrcode.png" alt="" class="img-responsive"> -->
        <div id="qr-div"></div>
        <div>打开微信，点击底部的“发现”，使用 “扫一扫” 即可登录</div>
    </div>
</div>
<!-- 置顶 微信 微博结束 -->
<!-- footer部分和置顶挂件 -->

</div>
<div class="util-loading">
    <div class="spinner">
        <div class="rect1"></div>
        <div class="rect2"></div>
        <div class="rect3"></div>
        <div class="rect4"></div>
        <div class="rect5"></div>
    </div>
</div>
<!-- 退出登录提示弹框（样式在header里） start -->
<div class="modal logoout-modal js-logoout-modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <span class="img"></span>
            </div>
            <div class="modal-body">
                <p>铅笔道为您带来最真实项目信息与最全面的创投报道，您确定要退出吗？</p>
            </div>
            <div class="modal-footer">
                <div class="my-btn comfirm-btn">
                    <span class="btn-lf">取消</span>
                    <span class="btn-rt">确定</span>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- 退出登录提示弹框（样式在header里） end -->
<!-- scripts -->
<script type="text/javascript" src="/js/lib/jquery-3.0.0.min.js"></script>
<script type="text/javascript" src="/js/lib/bootstrap.js"></script>
<script type="text/javascript" src="/js/lib/jstorage.min.js"></script>
<script type="text/javascript" src="/js/lib/TweenLite.min.js"></script>
<script type="text/javascript" src="/js/lib/CSSPlugin.min.js"></script>
<script type="text/javascript" src="/js/lib/jquery.qrcode.js"></script>
<script type="text/javascript" src="/js/lib/qrcode.js"></script>
<script type="text/javascript" src="/js/lib/jbase64.js"></script>
<script type="text/javascript" src="/js/lib/md5.min.js"></script>
<script type="text/javascript" src="/js/packer.js"></script>
<script src="https://lkme.cc/js/linkedme.min.js"></script>
<script>
        linkedme.init("c5f497861496f7fcca455a97f2451a90", {
            type: "live"
        }, null);
    </script>
<script src="/js/lib/classie.js"></script>
<script type="text/javascript" src="/js/lib/toastr.js"></script>
<!-- <script src="/js/slidenavbar.js"></script> -->
<!-- 自己的js -->
<script src="/js/util.js"></script>
<script src="/js/pay/util.js"></script>
<!-- <script src="/js/header.js"></script> -->
<script src="/js/pay/header.js"></script>
<script src="/js/pay/sidebar.js"></script>
<!-- <script async src="https://qiyukf.com/script/8b74d43d413f23caab25a362d79a0bde.js"></script> -->
<!-- 加载js -->
<script type="text/javascript" src="/js/lib/jquery.history.js"></script>
<script>
    var nav_order = "";
    var projectid = '158d3fd6d2eaa07d';
    var competitors = '[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]';
    var is_unexample = true;
    if (projectid == '8b5fabf6d83adc4d') {
        is_unexample = false;
    }
    // var projectContent = '';
    UTL.checkUaToMobile(M_URL + location.pathname.substr(1))
</script>
<script type="text/javascript" src="/js/lib/jPages.js"></script>
<script type="text/javascript" src="/js/plupload/plupload.full.min.js"></script>
<script type="text/javascript" src="/js/lib/qiniu.v2.min.js"></script>
<script type="text/javascript" src="/js/uploadFile.js"></script>
<script type="text/javascript" src="/js/pay/projectdetail.js"></script>
<!-- 采用mockjs模拟数据 -->
<!-- <script type="text/javascript" src="/js/mockjs/dist/mock.js"></script> -->
<!-- <script type="text/javascript" src="/js/mockData/projectDetail.js"></script> -->
<script type="text/javascript">
    $(document).ready(function () {
        // 判断是否为IE浏览器
        if (!+[1, ]) {
            PROD.init();
            if (competitors.length == 0) {
                $('.nav-bar-item').eq(6).hide()
            }
        } else {
            $(window).on('pageshow', function () {
                PROD.init();
                if (competitors.length == 0) {
                    $('.nav-bar-item').eq(6).hide()
                }
            });
        }
    })
</script>
<!-- 神策sdk -->
<script>
        (function (para) {
            var n = para.name;
            window['sensorsDataAnalytic201505'] = n;
            window[n] = {
                _q: [],
                para: para
            };
        })({
            sdk_url: '/js/lib/sensorsdata.min.js',
            heatmap_url: '/js/lib/heatmap.min.js',
            name: 'sa',
            server_url: is_master ?
                'https://pencilnews.cloud.sensorsdata.cn:4006/sa?token=9953a0eaf83dbce3&project=production' : 'https://pencilnews.cloud.sensorsdata.cn:4006/sa?token=9953a0eaf83dbce3',
            show_log: !is_master
        })
    </script>
<script src="/js/lib/sensorsdata.min.js"></script>
<script>
        if ($.jStorage.get('localUid')) {
            sa.login($.jStorage.get('localUid'));
        }
        sa.quick('autoTrack');
        var sa_datas = sa.getPresetProperties();
        var sa_obj = {
            device_id: sa_datas._distinct_id,
            screen_width: sa_datas.$screen_width,
            screen_height: sa_datas.$screen_height
        }
        // 将设配ID、屏幕宽高存入cookie中
        setCookie('sa_obj', JSON.stringify(sa_obj))
        var localToken = $.jStorage.get('localToken');
        setCookie('token', localToken);
    </script>
<!-- 神策sdk end-->
<script>
        (function (i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r;
            i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date();
            a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
            a.async = 1;
            a.src = g;
            m.parentNode.insertBefore(a, m)
        })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

        ga('create', 'UA-498196-15', 'auto');
        ga('require', 'linkid');
        ga('send', 'pageview');

        (function () {
            var bp = document.createElement('script');
            var curProtocol = window.location.protocol.split(':')[0];
            if (curProtocol === 'https') {
                bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
            } else {
                bp.src = 'http://push.zhanzhang.baidu.com/push.js';
            }
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(bp, s);
        })();
        (function () {
            var token = $.jStorage.get("localToken");
            if (token) {
                var name = $.jStorage.get("localUsername");
                var uid = $.jStorage.get("localUid");
                var certType = $.jStorage.get("localCertType") == 2 ? '投资人' : '未认证投资人';
                var hasPay = $.jStorage.get("localPayState");
                if (hasPay == 1) {
                    ga('set', 'userId', name + uid + '付费用户');
                } else {
                    ga('set', 'userId', name + uid + certType);
                }
            }
        })()

        sidebar();
        header();
        // UTL.checkUaToMobile(M_URL + location.pathname.substr(1))
    </script>
<!-- <script src="https://s95.cnzz.com/z_stat.php?id=1261729730&web_id=1261729730" language="JavaScript"></script> -->
</body>
</html>

'''
competing_product = scrapy.Selector(text=dd)
competing_product = competing_product.xpath('//*[@class="competitor-name"]//text()').extract()
print(''.join(competing_product))
