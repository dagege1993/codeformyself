import re

import requests
import scrapy

ll = '''
<!DOCTYPE html>
<html>

<body id="main">

<div id="react">
    <div class="page index" data-reactroot="">
        <div class="op-area">
            <div class="choose-by-province"><h3 class="l-attr">按省份选择:</h3>
                <div class="choose-wrap">
                    <div class="province-choose">省份<i class="iconfont icon-downarrow"></i>
                        <div class="mt-provinces undefined"><p>省份</p>
                            <div class="provinces-wrapper clearfix"></div>
                        </div>
                    </div>
                    <div class="city-choose ">城市<i class="iconfont icon-downarrow"></i>
                        <div class="mt-cities undefined"><p>城市</p>
                            <div class="cities-wrapper clearfix"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="search"><h3 class="l-attr">直接搜索：</h3><input type="text" placeholder="请输入城市中文或拼音"
                                                                    class="search-text" value=""/></div>
        </div>
        <div class="citylist"><h3 class="l-attr">热门城市：</h3>
            <p class="r-info"><a href="//bj.meituan.com" class="link city">北京</a><a href="//sh.meituan.com"
                                                                                    class="link city">上海</a><a
                    href="//gz.meituan.com" class="link city">广州</a><a href="//sz.meituan.com"
                                                                       class="link city">深圳</a><a
                    href="//tj.meituan.com" class="link city">天津</a><a href="//xa.meituan.com"
                                                                       class="link city">西安</a><a
                    href="//cq.meituan.com" class="link city">重庆</a><a href="//hz.meituan.com"
                                                                       class="link city">杭州</a><a
                    href="//nj.meituan.com" class="link city">南京</a><a href="//wh.meituan.com"
                                                                       class="link city">武汉</a><a
                    href="//cd.meituan.com" class="link city">成都</a></p></div>
        <div class="alphabet"><h3 class="l-attr">按拼音首字母选择：</h3>
            <p class="r-info"><span class="letter">A</span><span class="letter">B</span><span
                    class="letter">C</span><span class="letter">D</span><span class="letter">E</span><span
                    class="letter">F</span><span class="letter">G</span><span class="letter">H</span><span
                    class="letter">J</span><span class="letter">K</span><span class="letter">L</span><span
                    class="letter">M</span><span class="letter">N</span><span class="letter">P</span><span
                    class="letter">Q</span><span class="letter">R</span><span class="letter">S</span><span
                    class="letter">T</span><span class="letter">W</span><span class="letter">X</span><span
                    class="letter">Y</span><span class="letter">Z</span></p></div>
        <div class="alphabet-city-area">
            <div class="city-area" id="city-A"><span class="city-label">A</span><span class="cities"><a
                    href="//as.meituan.com" class="link city ">鞍山</a><a href="//anqing.meituan.com" class="link city ">安庆</a><a
                    href="//ay.meituan.com" class="link city ">安阳</a><a href="//anshun.meituan.com" class="link city ">安顺</a><a
                    href="//ankang.meituan.com" class="link city ">安康</a><a href="//aq.meituan.com" class="link city ">安丘</a><a
                    href="//anyue.meituan.com" class="link city ">安岳</a><a href="//anlushi.meituan.com"
                                                                           class="link city ">安陆市</a><a
                    href="//aks.meituan.com" class="link city ">阿克苏</a><a href="//anzhouqu.meituan.com"
                                                                          class="link city ">安州区</a><a
                    href="//atushishi.meituan.com" class="link city ">阿图什市</a><a href="//aj.meituan.com"
                                                                                 class="link city ">安吉</a><a
                    href="//als.meituan.com" class="link city ">阿拉善盟</a><a href="//arongqi.meituan.com"
                                                                           class="link city ">阿荣旗</a><a
                    href="//anping.meituan.com" class="link city ">安平</a><a href="//anxi.meituan.com"
                                                                            class="link city ">安溪</a><a
                    href="//anning.meituan.com" class="link city ">安宁</a><a href="//anhua.meituan.com"
                                                                            class="link city ">安化</a><a
                    href="//alaer.meituan.com" class="link city ">阿拉尔</a><a href="//anfu.meituan.com"
                                                                            class="link city ">安福</a><a
                    href="//aletaishi.meituan.com" class="link city ">阿勒泰市</a><a href="//achengqu.meituan.com"
                                                                                 class="link city ">阿城区</a><a
                    href="//am.meituan.com" class="link city ">澳门</a><a href="//alt.meituan.com"
                                                                        class="link city ">阿勒泰</a><a
                    href="//al.meituan.com" class="link city ">阿里</a><a href="//ab.meituan.com"
                                                                        class="link city ">阿坝</a></span></div>
            <div class="city-area" id="city-B"><span class="city-label">B</span><span class="cities"><a
                    href="//bj.meituan.com" class="link city sa-city">北京</a><a href="//bt.meituan.com"
                                                                               class="link city ">包头</a><a
                    href="//bd.meituan.com" class="link city ">保定</a><a href="//bengbu.meituan.com" class="link city ">蚌埠</a><a
                    href="//bozhou.meituan.com" class="link city ">亳州</a><a href="//bz.meituan.com" class="link city ">滨州</a><a
                    href="//baoji.meituan.com" class="link city ">宝鸡</a><a href="//bc.meituan.com"
                                                                           class="link city ">白城</a><a
                    href="//hbbazhou.meituan.com" class="link city ">霸州</a><a href="//byne.meituan.com"
                                                                              class="link city ">巴彦淖尔</a><a
                    href="//bh.meituan.com" class="link city ">北海</a><a href="//baise.meituan.com"
                                                                        class="link city ">百色</a><a
                    href="//bazhong.meituan.com" class="link city ">巴中</a><a href="//bijie.meituan.com"
                                                                             class="link city ">毕节</a><a
                    href="//bs.meituan.com" class="link city ">保山</a><a href="//benxi.meituan.com"
                                                                        class="link city ">本溪</a><a
                    href="//by.meituan.com" class="link city ">白银</a><a href="//baishan.meituan.com" class="link city ">白山</a><a
                    href="//bishan.meituan.com" class="link city ">璧山</a><a href="//baiquanxian.meituan.com"
                                                                            class="link city ">拜泉县</a><a
                    href="//baichengxian.meituan.com" class="link city ">拜城县</a><a href="//baoying.meituan.com"
                                                                                   class="link city ">宝应</a><a
                    href="//beiliu.meituan.com" class="link city ">北流</a><a href="//boai.meituan.com"
                                                                            class="link city ">博爱</a><a
                    href="//bachuxian.meituan.com" class="link city ">巴楚县</a><a href="//baofeng.meituan.com"
                                                                                class="link city ">宝丰</a><a
                    href="//boxing.meituan.com" class="link city ">博兴</a><a href="//biyang.meituan.com"
                                                                            class="link city ">泌阳</a><a
                    href="//binxian.meituan.com" class="link city ">彬县</a><a href="//bayanxian.meituan.com"
                                                                             class="link city ">巴彦县</a><a
                    href="//boshan.meituan.com" class="link city ">博山</a><a href="//binyang.meituan.com"
                                                                            class="link city ">宾阳</a><a
                    href="//botou.meituan.com" class="link city ">泊头市</a><a href="//boluoxian.meituan.com"
                                                                            class="link city ">博罗县</a><a
                    href="//bobaixian.meituan.com" class="link city ">博白县</a><a href="//beizhenshi.meituan.com"
                                                                                class="link city ">北镇市</a><a
                    href="//beianshi.meituan.com" class="link city ">北安市</a><a href="//binhai.meituan.com"
                                                                               class="link city ">滨海</a><a
                    href="//beipei.meituan.com" class="link city ">北碚</a><a href="//betl.meituan.com"
                                                                            class="link city ">博尔塔拉</a><a
                    href="//baz.meituan.com" class="link city ">巴州</a></span></div>
            <div class="city-area" id="city-C"><span class="city-label">C</span><span class="cities"><a
                    href="//cq.meituan.com" class="link city sa-city">重庆</a><a href="//cd.meituan.com"
                                                                               class="link city sa-city">成都</a><a
                    href="//cz.meituan.com" class="link city ">常州</a><a href="//chs.meituan.com"
                                                                        class="link city ">长沙</a><a
                    href="//cc.meituan.com" class="link city ">长春</a><a href="//cangzhou.meituan.com"
                                                                        class="link city ">沧州</a><a
                    href="//changzhi.meituan.com" class="link city ">长治</a><a href="//chifeng.meituan.com"
                                                                              class="link city ">赤峰</a><a
                    href="//cixi.meituan.com" class="link city ">慈溪</a><a href="//chuzhou.meituan.com"
                                                                          class="link city ">滁州</a><a
                    href="//changshu.meituan.com" class="link city ">常熟</a><a href="//changde.meituan.com"
                                                                              class="link city ">常德</a><a
                    href="//chengde.meituan.com" class="link city ">承德</a><a href="//chenzhou.meituan.com"
                                                                             class="link city ">郴州</a><a
                    href="//chaozhou.meituan.com" class="link city ">潮州</a><a href="//conghua.meituan.com"
                                                                              class="link city ">从化</a><a
                    href="//ch.meituan.com" class="link city ">巢湖</a><a href="//cy.meituan.com"
                                                                        class="link city ">朝阳</a><a
                    href="//chx.meituan.com" class="link city ">长兴</a><a href="//changyi.meituan.com"
                                                                         class="link city ">昌邑</a><a
                    href="//cangnan.meituan.com" class="link city ">苍南</a><a href="//cg.meituan.com" class="link city ">长葛</a><a
                    href="//chizhou.meituan.com" class="link city ">池州</a><a href="//chengjiangxian.meituan.com"
                                                                             class="link city ">澄江县</a><a
                    href="//changle.meituan.com" class="link city ">长乐</a><a href="//changji.meituan.com"
                                                                             class="link city ">昌吉</a><a
                    href="//cmx.meituan.com" class="link city ">澄迈县</a><a href="//chongzuo.meituan.com"
                                                                          class="link city ">崇左</a><a
                    href="//cx.meituan.com" class="link city ">楚雄</a><a href="//cb.meituan.com"
                                                                        class="link city ">赤壁</a><a
                    href="//ca.meituan.com" class="link city ">淳安</a><a href="//chengdexian.meituan.com"
                                                                        class="link city ">承德县</a><a
                    href="//changlecl.meituan.com" class="link city ">昌乐</a><a href="//caofeidian.meituan.com"
                                                                               class="link city ">曹妃甸</a><a
                    href="//cixian.meituan.com" class="link city ">磁县</a><a href="//changyuan.meituan.com"
                                                                            class="link city ">长垣</a><a
                    href="//chengan.meituan.com" class="link city ">成安</a><a href="//changli.meituan.com"
                                                                             class="link city ">昌黎</a><a
                    href="//cenxi.meituan.com" class="link city ">岑溪</a><a href="//chiping.meituan.com"
                                                                           class="link city ">茌平</a><a
                    href="//caoxian.meituan.com" class="link city ">曹县</a><a href="//chenggu.meituan.com"
                                                                             class="link city ">城固</a><a
                    href="//changting.meituan.com" class="link city ">长汀</a><a href="//chaoan.meituan.com"
                                                                               class="link city ">潮安</a><a
                    href="//changshou.meituan.com" class="link city ">长寿</a><a href="//changshan.meituan.com"
                                                                               class="link city ">常山</a><a
                    href="//chishui.meituan.com" class="link city ">赤水</a><a href="//cili.meituan.com"
                                                                             class="link city ">慈利</a><a
                    href="//changningshi.meituan.com" class="link city ">常宁市</a><a href="//chalingxian.meituan.com"
                                                                                   class="link city ">茶陵</a><a
                    href="//changfengxian.meituan.com" class="link city ">长丰县</a><a href="//cangxixian.meituan.com"
                                                                                    class="link city ">苍溪县</a><a
                    href="//changqingqu.meituan.com" class="link city ">长清区</a><a href="//chongmingqu.meituan.com"
                                                                                  class="link city ">崇明区</a><a
                    href="//chengwuxian.meituan.com" class="link city ">成武县</a><a href="//chongzhou.meituan.com"
                                                                                  class="link city ">崇州</a><a
                    href="//changdu.meituan.com" class="link city ">昌都</a></span></div>
            <div class="city-area" id="city-D"><span class="city-label">D</span><span class="cities"><a
                    href="//dl.meituan.com" class="link city ">大连</a><a href="//dg.meituan.com"
                                                                        class="link city ">东莞</a><a
                    href="//dt.meituan.com" class="link city ">大同</a><a href="//dq.meituan.com"
                                                                        class="link city ">大庆</a><a
                    href="//dandong.meituan.com" class="link city ">丹东</a><a href="//dy.meituan.com" class="link city ">东营</a><a
                    href="//dz.meituan.com" class="link city ">德州</a><a href="//deyang.meituan.com" class="link city ">德阳</a><a
                    href="//dazhou.meituan.com" class="link city ">达州</a><a href="//dx.meituan.com" class="link city ">定西</a><a
                    href="//dengzhou.meituan.com" class="link city ">邓州</a><a href="//dongyang.meituan.com"
                                                                              class="link city ">东阳</a><a
                    href="//df.meituan.com" class="link city ">大丰</a><a href="//dongtai.meituan.com" class="link city ">东台</a><a
                    href="//dengfeng.meituan.com" class="link city ">登封</a><a href="//danzhou.meituan.com"
                                                                              class="link city ">儋州</a><a
                    href="//djy.meituan.com" class="link city ">都江堰</a><a href="//dsq.meituan.com" class="link city ">大石桥</a><a
                    href="//dali.meituan.com" class="link city ">大理</a><a href="//danyang.meituan.com"
                                                                          class="link city ">丹阳</a><a
                    href="//dangyang.meituan.com" class="link city ">当阳</a><a href="//donggang.meituan.com"
                                                                              class="link city ">东港</a><a
                    href="//dongkengzhen.meituan.com" class="link city ">东坑镇</a><a href="//dingyuanxian.meituan.com"
                                                                                   class="link city ">定远县</a><a
                    href="//dazuqu.meituan.com" class="link city ">大足区</a><a href="//deqing.meituan.com"
                                                                             class="link city ">德清</a><a
                    href="//daye.meituan.com" class="link city ">大冶</a><a href="//dongxing.meituan.com"
                                                                          class="link city ">东兴</a><a
                    href="//dbs.meituan.com" class="link city ">调兵山</a><a href="//dawuxia.meituan.com"
                                                                          class="link city ">大悟县</a><a
                    href="//dehuishi.meituan.com" class="link city ">德惠市</a><a href="//datongshi.meituan.com"
                                                                               class="link city ">大通</a><a
                    href="//dongfang.meituan.com" class="link city ">东方</a><a href="//dongping.meituan.com"
                                                                              class="link city ">东平</a><a
                    href="//dianbai.meituan.com" class="link city ">电白</a><a href="//donghai.meituan.com"
                                                                             class="link city ">东海</a><a
                    href="//dingzhou.meituan.com" class="link city ">定州</a><a href="//dancheng.meituan.com"
                                                                              class="link city ">郸城</a><a
                    href="//dalixian.meituan.com" class="link city ">大荔</a><a href="//dalateqi.meituan.com"
                                                                              class="link city ">达拉特旗</a><a
                    href="//dazhu.meituan.com" class="link city ">大竹</a><a href="//dawa.meituan.com" class="link city ">大洼</a><a
                    href="//dayi.meituan.com" class="link city ">大邑</a><a href="//dangshan.meituan.com"
                                                                          class="link city ">砀山</a><a
                    href="//dunhua.meituan.com" class="link city ">敦化</a><a href="//dongguang.meituan.com"
                                                                            class="link city ">东光</a><a
                    href="//daoxian.meituan.com" class="link city ">道县</a><a href="//daanshi.meituan.com"
                                                                             class="link city ">大安市</a><a
                    href="//dinganxian.meituan.com" class="link city ">定安县</a><a href="//dianjiang.meituan.com"
                                                                                 class="link city ">垫江</a><a
                    href="//dongmingxian.meituan.com" class="link city ">东明县</a><a href="//dingtaoqu.meituan.com"
                                                                                   class="link city ">定陶区</a><a
                    href="//dingbianxian.meituan.com" class="link city ">定边县</a><a href="//dachangzizhixian.meituan.com"
                                                                                   class="link city ">大厂回族自治县</a><a
                    href="//dengta.meituan.com" class="link city ">灯塔</a><a href="//dunhuang.meituan.com"
                                                                            class="link city ">敦煌</a><a
                    href="//diqing.meituan.com" class="link city ">迪庆</a><a href="//dh.meituan.com" class="link city ">德宏</a><a
                    href="//dxal.meituan.com" class="link city ">大兴安岭</a></span></div>
            <div class="city-area" id="city-E"><span class="city-label">E</span><span class="cities"><a
                    href="//erds.meituan.com" class="link city ">鄂尔多斯</a><a href="//ez.meituan.com" class="link city ">鄂州</a><a
                    href="//es.meituan.com" class="link city ">恩施</a><a href="//enping.meituan.com" class="link city ">恩平</a><a
                    href="//ems.meituan.com" class="link city ">峨眉山</a><a href="//eminxian.meituan.com"
                                                                          class="link city ">额敏县</a><a
                    href="//eegn.meituan.com" class="link city ">额尔古纳</a></span></div>
            <div class="city-area" id="city-F"><span class="city-label">F</span><span class="cities"><a
                    href="//fz.meituan.com" class="link city ">福州</a><a href="//fs.meituan.com"
                                                                        class="link city ">佛山</a><a
                    href="//fy.meituan.com" class="link city ">阜阳</a><a href="//fuz.meituan.com"
                                                                        class="link city ">抚州</a><a
                    href="//fushun.meituan.com" class="link city ">抚顺</a><a href="//fx.meituan.com" class="link city ">阜新</a><a
                    href="//fl.meituan.com" class="link city ">涪陵</a><a href="//fuqing.meituan.com" class="link city ">福清</a><a
                    href="//fenghua.meituan.com" class="link city ">奉化</a><a href="//fc.meituan.com" class="link city ">肥城</a><a
                    href="//fuyangfy.meituan.com" class="link city ">富阳</a><a href="//fn.meituan.com"
                                                                              class="link city ">阜宁</a><a
                    href="//fcg.meituan.com" class="link city ">防城港</a><a href="//fuminxian.meituan.com"
                                                                          class="link city ">富民</a><a
                    href="//fengcheng.meituan.com" class="link city ">凤城</a><a href="//fenyang.meituan.com"
                                                                               class="link city ">汾阳</a><a
                    href="//fukang.meituan.com" class="link city ">阜康</a><a href="//fch.meituan.com" class="link city ">丰城</a><a
                    href="//fanxian.meituan.com" class="link city ">范县</a><a href="//fanchang.meituan.com"
                                                                             class="link city ">繁昌</a><a
                    href="//feixiang.meituan.com" class="link city ">肥乡区</a><a href="//fengqiu.meituan.com"
                                                                               class="link city ">封丘</a><a
                    href="//fufeng.meituan.com" class="link city ">扶风</a><a href="//fh.meituan.com" class="link city ">凤凰</a><a
                    href="//fusong.meituan.com" class="link city ">抚松</a><a href="//fushunxian.meituan.com"
                                                                            class="link city ">富顺</a><a
                    href="//feixian.meituan.com" class="link city ">费县</a><a href="//fogang.meituan.com"
                                                                             class="link city ">佛冈</a><a
                    href="//fengning.meituan.com" class="link city ">丰宁</a><a href="//fugou.meituan.com"
                                                                              class="link city ">扶沟</a><a
                    href="//fengtai.meituan.com" class="link city ">凤台</a><a href="//fengxin.meituan.com"
                                                                             class="link city ">奉新</a><a
                    href="//fangcheng.meituan.com" class="link city ">方城</a><a href="//fuyuanxian.meituan.com"
                                                                               class="link city ">富源县</a><a
                    href="//fenyi.meituan.com" class="link city ">分宜</a><a href="//fusuixian.meituan.com"
                                                                           class="link city ">扶绥县</a><a
                    href="//feixixian.meituan.com" class="link city ">肥西县</a><a href="//fanzhixian.meituan.com"
                                                                                class="link city ">繁峙县</a><a
                    href="//fengxiangxian.meituan.com" class="link city ">凤翔县</a><a href="//fuan.meituan.com"
                                                                                    class="link city ">福安</a><a
                    href="//fudingshi.meituan.com" class="link city ">福鼎市</a><a href="//fuguxian.meituan.com"
                                                                                class="link city ">府谷县</a><a
                    href="//fengjie.meituan.com" class="link city ">奉节</a><a href="//fengdu.meituan.com"
                                                                             class="link city ">丰都</a><a
                    href="//feidongxian.meituan.com" class="link city ">肥东县</a><a href="//fengxian.meituan.com"
                                                                                  class="link city ">丰县</a></span></div>
            <div class="city-area" id="city-G"><span class="city-label">G</span><span class="cities"><a
                    href="//gz.meituan.com" class="link city sa-city">广州</a><a href="//gy.meituan.com"
                                                                               class="link city ">贵阳</a><a
                    href="//ganzhou.meituan.com" class="link city ">赣州</a><a href="//gg.meituan.com" class="link city ">贵港</a><a
                    href="//gl.meituan.com" class="link city ">桂林</a><a href="//guangyuan.meituan.com"
                                                                        class="link city ">广元</a><a
                    href="//ga.meituan.com" class="link city ">广安</a><a href="//gaozhou.meituan.com" class="link city ">高州</a><a
                    href="//gbd.meituan.com" class="link city ">高碑店</a><a href="//gm.meituan.com"
                                                                          class="link city ">高密</a><a
                    href="//gongyishi.meituan.com" class="link city ">巩义</a><a href="//gaoyou.meituan.com"
                                                                               class="link city ">高邮</a><a
                    href="//gr.meituan.com" class="link city ">广饶</a><a href="//guanxian.meituan.com"
                                                                        class="link city ">固安县</a><a
                    href="//gp.meituan.com" class="link city ">桂平</a><a href="//gzl.meituan.com"
                                                                        class="link city ">公主岭</a><a
                    href="//guangshanxian.meituan.com" class="link city ">光山县</a><a href="//gh.meituan.com"
                                                                                    class="link city ">广汉</a><a
                    href="//gc.meituan.com" class="link city ">藁城</a><a href="//gaoping.meituan.com" class="link city ">高平</a><a
                    href="//guangze.meituan.com" class="link city ">光泽</a><a href="//gj.meituan.com" class="link city ">个旧</a><a
                    href="//gushixian.meituan.com" class="link city ">固始县</a><a href="//gaizhou.meituan.com"
                                                                                class="link city ">盖州</a><a
                    href="//gujiao.meituan.com" class="link city ">古交</a><a href="//geermu.meituan.com"
                                                                            class="link city ">格尔木</a><a
                    href="//guyuan.meituan.com" class="link city ">固原</a><a href="//guanyun.meituan.com"
                                                                            class="link city ">灌云</a><a
                    href="//guannan.meituan.com" class="link city ">灌南</a><a href="//ganyu.meituan.com"
                                                                             class="link city ">赣榆</a><a
                    href="//gaoan.meituan.com" class="link city ">高安</a><a href="//guangde.meituan.com"
                                                                           class="link city ">广德</a><a
                    href="//gongqingcheng.meituan.com" class="link city ">共青城</a><a href="//gaoyang.meituan.com"
                                                                                    class="link city ">高阳</a><a
                    href="//gaoling.meituan.com" class="link city ">高陵</a><a href="//gongan.meituan.com"
                                                                             class="link city ">公安</a><a
                    href="//gulangyu.meituan.com" class="link city ">鼓浪屿</a><a href="//ganzi.meituan.com"
                                                                               class="link city ">甘孜</a><a
                    href="//gn.meituan.com" class="link city ">甘南</a><a href="//guoluo.meituan.com" class="link city ">果洛</a><a
                    href="//gaoxiong.meituan.com" class="link city ">高雄</a></span></div>
            <div class="city-area" id="city-H"><span class="city-label">H</span><span class="cities"><a
                    href="//hz.meituan.com" class="link city sa-city">杭州</a><a href="//hf.meituan.com"
                                                                               class="link city ">合肥</a><a
                    href="//hrb.meituan.com" class="link city ">哈尔滨</a><a href="//hy.meituan.com"
                                                                          class="link city ">衡阳</a><a
                    href="//hd.meituan.com" class="link city ">邯郸</a><a href="//huizhou.meituan.com" class="link city ">惠州</a><a
                    href="//hu.meituan.com" class="link city ">呼和浩特</a><a href="//haikou.meituan.com"
                                                                          class="link city ">海口</a><a
                    href="//huzhou.meituan.com" class="link city ">湖州</a><a href="//ha.meituan.com" class="link city ">淮安</a><a
                    href="//hn.meituan.com" class="link city ">淮南</a><a href="//heze.meituan.com"
                                                                        class="link city ">菏泽</a><a
                    href="//hshi.meituan.com" class="link city ">黄石</a><a href="//hg.meituan.com"
                                                                          class="link city ">黄冈</a><a
                    href="//hh.meituan.com" class="link city ">怀化</a><a href="//hs.meituan.com"
                                                                        class="link city ">衡水</a><a
                    href="//hld.meituan.com" class="link city ">葫芦岛</a><a href="//hc.meituan.com"
                                                                          class="link city ">河池</a><a
                    href="//huangshan.meituan.com" class="link city ">黄山</a><a href="//hlbe.meituan.com"
                                                                               class="link city ">呼伦贝尔</a><a
                    href="//heihe.meituan.com" class="link city ">黑河</a><a href="//hb.meituan.com"
                                                                           class="link city ">鹤壁</a><a
                    href="//heyuan.meituan.com" class="link city ">河源</a><a href="//hezhou.meituan.com"
                                                                            class="link city ">贺州</a><a
                    href="//hegang.meituan.com" class="link city ">鹤岗</a><a href="//honghe.meituan.com"
                                                                            class="link city ">红河</a><a
                    href="//hanzhong.meituan.com" class="link city ">汉中</a><a href="//haining.meituan.com"
                                                                              class="link city ">海宁</a><a
                    href="//huidong.meituan.com" class="link city ">惠东</a><a href="//huiyang.meituan.com"
                                                                             class="link city ">惠阳</a><a
                    href="//haicheng.meituan.com" class="link city ">海城</a><a href="//hm.meituan.com"
                                                                              class="link city ">海门</a><a
                    href="//haiyang.meituan.com" class="link city ">海阳</a><a href="//huaibei.meituan.com"
                                                                             class="link city ">淮北</a><a
                    href="//haian.meituan.com" class="link city ">海安</a><a href="//huazhou.meituan.com"
                                                                           class="link city ">化州</a><a
                    href="//hechuan.meituan.com" class="link city ">合川</a><a href="//hengdian.meituan.com"
                                                                             class="link city ">横店</a><a
                    href="//haidong.meituan.com" class="link city ">海东</a><a href="//heshan.meituan.com"
                                                                             class="link city ">鹤山</a><a
                    href="//huadian.meituan.com" class="link city ">桦甸</a><a href="//huachuanxian.meituan.com"
                                                                             class="link city ">桦川县</a><a
                    href="//huanglingxian.meituan.com" class="link city ">黄陵县</a><a href="//huayin.meituan.com"
                                                                                    class="link city ">华阴</a><a
                    href="//huanxian.meituan.com" class="link city ">环县</a><a href="//houma.meituan.com"
                                                                              class="link city ">侯马</a><a
                    href="//hejiangxian.meituan.com" class="link city ">合江县</a><a href="//hami.meituan.com"
                                                                                  class="link city ">哈密</a><a
                    href="//huozhou.meituan.com" class="link city ">霍州</a><a href="//huanghua.meituan.com"
                                                                             class="link city ">黄骅</a><a
                    href="//hailunshi.meituan.com" class="link city ">海伦市</a><a href="//hl.meituan.com"
                                                                                class="link city ">海林</a><a
                    href="//hannanqu.meituan.com" class="link city ">汉南区</a><a href="//helanxian.meituan.com"
                                                                               class="link city ">贺兰县</a><a
                    href="//haiyan.meituan.com" class="link city ">海盐</a><a href="//hengshanqu.meituan.com"
                                                                            class="link city ">横山区</a><a
                    href="//huaiyang.meituan.com" class="link city ">淮阳</a><a href="//hanyin.meituan.com"
                                                                              class="link city ">汉阴</a><a
                    href="//hanshan.meituan.com" class="link city ">含山</a><a href="//hexian.meituan.com"
                                                                             class="link city ">和县</a><a
                    href="//huxian.meituan.com" class="link city ">户县</a><a href="//huixian.meituan.com"
                                                                            class="link city ">辉县</a><a
                    href="//huairen.meituan.com" class="link city ">怀仁</a><a href="//huaxian.meituan.com"
                                                                             class="link city ">滑县</a><a
                    href="//huian.meituan.com" class="link city ">惠安</a><a href="//hancheng.meituan.com"
                                                                           class="link city ">韩城</a><a
                    href="//huarong.meituan.com" class="link city ">华容</a><a href="//huating.meituan.com"
                                                                             class="link city ">华亭</a><a
                    href="//hongtong.meituan.com" class="link city ">洪洞</a><a href="//hekou.meituan.com"
                                                                              class="link city ">河口</a><a
                    href="//huinan.meituan.com" class="link city ">辉南</a><a href="//honghu.meituan.com"
                                                                            class="link city ">洪湖</a><a
                    href="//haicang.meituan.com" class="link city ">海沧</a><a href="//huoqiu.meituan.com"
                                                                             class="link city ">霍邱</a><a
                    href="//hunchun.meituan.com" class="link city ">珲春</a><a href="//huaining.meituan.com"
                                                                             class="link city ">怀宁</a><a
                    href="//huaiyuanxian.meituan.com" class="link city ">怀远县</a><a href="//huizexian.meituan.com"
                                                                                   class="link city ">会泽县</a><a
                    href="//hejianshi.meituan.com" class="link city ">河间市</a><a href="//hepuxian.meituan.com"
                                                                                class="link city ">合浦县</a><a
                    href="//hengyangxian.meituan.com" class="link city ">衡阳县</a><a href="//hengshanxian.meituan.com"
                                                                                   class="link city ">衡山县</a><a
                    href="//hengdongxian.meituan.com" class="link city ">衡东县</a><a href="//huangchuanxian.meituan.com"
                                                                                   class="link city ">潢川县</a><a
                    href="//hj.meituan.com" class="link city ">河津</a><a href="//hengchun.meituan.com"
                                                                        class="link city ">恒春</a><a
                    href="//hualian.meituan.com" class="link city ">花莲</a><a href="//ht.meituan.com" class="link city ">和田</a><a
                    href="//hx.meituan.com" class="link city ">海西</a><a href="//hnz.meituan.com"
                                                                        class="link city ">海南州</a><a
                    href="//huangnan.meituan.com" class="link city ">黄南</a><a href="//haibei.meituan.com"
                                                                              class="link city ">海北</a><a
                    href="//hk.meituan.com" class="link city ">香港</a></span></div>
            <div class="city-area" id="city-J"><span class="city-label">J</span><span class="cities"><a
                    href="//jn.meituan.com" class="link city ">济南</a><a href="//jining.meituan.com" class="link city ">济宁</a><a
                    href="//jiangyin.meituan.com" class="link city ">江阴</a><a href="//jl.meituan.com"
                                                                              class="link city ">吉林</a><a
                    href="//jm.meituan.com" class="link city ">江门</a><a href="//jx.meituan.com"
                                                                        class="link city ">嘉兴</a><a
                    href="//jh.meituan.com" class="link city ">金华</a><a href="//jingzhou.meituan.com"
                                                                        class="link city ">荆州</a><a
                    href="//jingmen.meituan.com" class="link city ">荆门</a><a href="//jinzhou.meituan.com"
                                                                             class="link city ">锦州</a><a
                    href="//jms.meituan.com" class="link city ">佳木斯</a><a href="//jy.meituan.com"
                                                                          class="link city ">揭阳</a><a
                    href="//jj.meituan.com" class="link city ">九江</a><a href="//jiaozuo.meituan.com" class="link city ">焦作</a><a
                    href="//jinjiang.meituan.com" class="link city ">晋江市</a><a href="//jincheng.meituan.com"
                                                                               class="link city ">晋城</a><a
                    href="//jz.meituan.com" class="link city ">晋中</a><a href="//jimo.meituan.com"
                                                                        class="link city ">即墨</a><a
                    href="//jdz.meituan.com" class="link city ">景德镇</a><a href="//jiangdu.meituan.com"
                                                                          class="link city ">江都</a><a
                    href="//jq.meituan.com" class="link city ">酒泉</a><a href="//ja.meituan.com"
                                                                        class="link city ">吉安</a><a
                    href="//jixi.meituan.com" class="link city ">鸡西</a><a href="//jiyuan.meituan.com"
                                                                          class="link city ">济源</a><a
                    href="//jingjiang.meituan.com" class="link city ">靖江</a><a href="//jintan.meituan.com"
                                                                               class="link city ">金坛</a><a
                    href="//jiaozhou.meituan.com" class="link city ">胶州</a><a href="//jr.meituan.com"
                                                                              class="link city ">句容</a><a
                    href="//js.meituan.com" class="link city ">嘉善</a><a href="//jiangyou.meituan.com"
                                                                        class="link city ">江油</a><a
                    href="//jiangshan.meituan.com" class="link city ">江山</a><a href="//jianhu.meituan.com"
                                                                               class="link city ">建湖</a><a
                    href="//jinzhoushi.meituan.com" class="link city ">晋州</a><a href="//jiutai.meituan.com"
                                                                                class="link city ">九台</a><a
                    href="//jd.meituan.com" class="link city ">建德</a><a href="//jianyang.meituan.com"
                                                                        class="link city ">简阳</a><a
                    href="//jiexiu.meituan.com" class="link city ">介休</a><a href="//jyg.meituan.com" class="link city ">嘉峪关</a><a
                    href="//jianshi.meituan.com" class="link city ">集安</a><a href="//jingguxian.meituan.com"
                                                                             class="link city ">景谷</a><a
                    href="//jingxixian.meituan.com" class="link city ">靖西市</a><a href="//jiaohe.meituan.com"
                                                                                 class="link city ">蛟河</a><a
                    href="//jianyangjy.meituan.com" class="link city ">建阳</a><a href="//jiaxian.meituan.com"
                                                                                class="link city ">郏县</a><a
                    href="//jintang.meituan.com" class="link city ">金堂</a><a href="//jianli.meituan.com"
                                                                             class="link city ">监利</a><a
                    href="//jiangjin.meituan.com" class="link city ">江津</a><a href="//juye.meituan.com"
                                                                              class="link city ">巨野</a><a
                    href="//jiaxiang.meituan.com" class="link city ">嘉祥</a><a href="//jinxiang.meituan.com"
                                                                              class="link city ">金乡</a><a
                    href="//jinyun.meituan.com" class="link city ">缙云</a><a href="//jingshan.meituan.com"
                                                                            class="link city ">京山</a><a
                    href="//jinghexian.meituan.com" class="link city ">精河县</a><a href="//junan.meituan.com"
                                                                                 class="link city ">莒南</a><a
                    href="//jinchang.meituan.com" class="link city ">金昌</a><a href="//jinhu.meituan.com"
                                                                              class="link city ">金湖</a><a
                    href="//jimei.meituan.com" class="link city ">集美</a><a href="//jinsha.meituan.com"
                                                                           class="link city ">金沙</a><a
                    href="//jingxian.meituan.com" class="link city ">泾县</a><a href="//jianxian.meituan.com"
                                                                              class="link city ">吉安县</a><a
                    href="//jishuixian.meituan.com" class="link city ">吉水县</a><a href="//jiangchuanxian.meituan.com"
                                                                                 class="link city ">江川县</a><a
                    href="//jianghuayaozuziz.meituan.com" class="link city ">江华瑶族自治县</a><a
                    href="//jinningxian.meituan.com" class="link city ">晋宁区</a><a href="//jiangyong.meituan.com"
                                                                                  class="link city ">江永</a><a
                    href="//jianshuixian.meituan.com" class="link city ">建水县</a><a href="//juanchengxian.meituan.com"
                                                                                   class="link city ">鄄城县</a><a
                    href="//jingbian.meituan.com" class="link city ">靖边</a><a href="//jiayuxian.meituan.com"
                                                                              class="link city ">嘉鱼县</a><a
                    href="//jzqixian.meituan.com" class="link city ">祁县</a><a href="//jingdongyizuzizh.meituan.com"
                                                                              class="link city ">景东彝族自治县</a><a
                    href="//jgs.meituan.com" class="link city ">井冈山</a><a href="//jiayi.meituan.com" class="link city ">嘉义市</a><a
                    href="//jilong.meituan.com" class="link city ">基隆</a><a href="//jzg.meituan.com" class="link city ">九寨沟</a></span>
            </div>
            <div class="city-area" id="city-K"><span class="city-label">K</span><span class="cities"><a
                    href="//km.meituan.com" class="link city ">昆明</a><a href="//kunshan.meituan.com" class="link city ">昆山</a><a
                    href="//kaifeng.meituan.com" class="link city ">开封</a><a href="//klmy.meituan.com"
                                                                             class="link city ">克拉玛依</a><a
                    href="//kaihua.meituan.com" class="link city ">开化</a><a href="//kp.meituan.com" class="link city ">开平</a><a
                    href="//krl.meituan.com" class="link city ">库尔勒</a><a href="//kaiyang.meituan.com"
                                                                          class="link city ">开阳</a><a
                    href="//kt.meituan.com" class="link city ">奎屯</a><a href="//kangxian.meituan.com"
                                                                        class="link city ">康县</a><a
                    href="//kaizhouqu.meituan.com" class="link city ">开州区</a><a href="//kenli.meituan.com"
                                                                                class="link city ">垦利</a><a
                    href="//kuancheng.meituan.com" class="link city ">宽城</a><a href="//kuche.meituan.com"
                                                                               class="link city ">库车</a><a
                    href="//kl.meituan.com" class="link city ">凯里</a><a href="//ks.meituan.com"
                                                                        class="link city ">喀什地区</a><a
                    href="//kz.meituan.com" class="link city ">克州</a><a href="//kending.meituan.com" class="link city ">垦丁</a></span>
            </div>
            <div class="city-area" id="city-L"><span class="city-label">L</span><span class="cities"><a
                    href="//lyg.meituan.com" class="link city ">连云港</a><a href="//linyi.meituan.com" class="link city ">临沂</a><a
                    href="//luoyang.meituan.com" class="link city ">洛阳</a><a href="//liuzhou.meituan.com"
                                                                             class="link city ">柳州</a><a
                    href="//lz.meituan.com" class="link city ">兰州</a><a href="//lc.meituan.com"
                                                                        class="link city ">聊城</a><a
                    href="//lf.meituan.com" class="link city ">廊坊</a><a href="//liaoyang.meituan.com"
                                                                        class="link city ">辽阳</a><a
                    href="//lishui.meituan.com" class="link city ">丽水</a><a href="//la.meituan.com" class="link city ">六安</a><a
                    href="//ls.meituan.com" class="link city ">乐山</a><a href="//lasa.meituan.com"
                                                                        class="link city ">拉萨</a><a
                    href="//ly.meituan.com" class="link city ">龙岩</a><a href="//linfen.meituan.com" class="link city ">临汾</a><a
                    href="//linzhou.meituan.com" class="link city ">林州</a><a href="//lb.meituan.com" class="link city ">来宾</a><a
                    href="//luzhou.meituan.com" class="link city ">泸州</a><a href="//liaoyuan.meituan.com"
                                                                            class="link city ">辽源</a><a
                    href="//lvliang.meituan.com" class="link city ">吕梁</a><a href="//lps.meituan.com"
                                                                             class="link city ">六盘水</a><a
                    href="//lj.meituan.com" class="link city ">丽江</a><a href="//lw.meituan.com"
                                                                        class="link city ">莱芜</a><a
                    href="//luohe.meituan.com" class="link city ">漯河</a><a href="//liyang.meituan.com"
                                                                           class="link city ">溧阳</a><a
                    href="//linhai.meituan.com" class="link city ">临海</a><a href="//lx.meituan.com" class="link city ">兰溪</a><a
                    href="//lk.meituan.com" class="link city ">龙口</a><a href="//leiyang.meituan.com" class="link city ">耒阳</a><a
                    href="//laizhou.meituan.com" class="link city ">莱州</a><a href="//linan.meituan.com"
                                                                             class="link city ">临安</a><a
                    href="//laiyang.meituan.com" class="link city ">莱阳</a><a href="//lufeng.meituan.com"
                                                                             class="link city ">陆丰</a><a
                    href="//liuyang.meituan.com" class="link city ">浏阳</a><a href="//lianjiang.meituan.com"
                                                                             class="link city ">廉江</a><a
                    href="//ld.meituan.com" class="link city ">娄底</a><a href="//liangshan.meituan.com"
                                                                        class="link city ">凉山</a><a
                    href="//linquanxian.meituan.com" class="link city ">临泉县</a><a href="//lincang.meituan.com"
                                                                                  class="link city ">临沧</a><a
                    href="//luchuanxian.meituan.com" class="link city ">陆川县</a><a href="//lingbao.meituan.com"
                                                                                  class="link city ">灵宝</a><a
                    href="//lsj.meituan.com" class="link city ">冷水江</a><a href="//ll.meituan.com"
                                                                          class="link city ">乐陵</a><a
                    href="//linxia.meituan.com" class="link city ">临夏</a><a href="//lh.meituan.com" class="link city ">龙海</a><a
                    href="//liling.meituan.com" class="link city ">醴陵</a><a href="//laixi.meituan.com"
                                                                            class="link city ">莱西</a><a
                    href="//lechang.meituan.com" class="link city ">乐昌</a><a href="//lp.meituan.com" class="link city ">乐平</a><a
                    href="//langzhong.meituan.com" class="link city ">阆中</a><a href="//luquan.meituan.com"
                                                                               class="link city ">鹿泉</a><a
                    href="//lichuan.meituan.com" class="link city ">利川</a><a href="//lhk.meituan.com"
                                                                             class="link city ">老河口</a><a
                    href="//linghai.meituan.com" class="link city ">凌海</a><a href="//luannan.meituan.com"
                                                                             class="link city ">滦南</a><a
                    href="//lingshan.meituan.com" class="link city ">灵山</a><a href="//lianzhou.meituan.com"
                                                                              class="link city ">连州</a><a
                    href="//luquanxian.meituan.com" class="link city ">禄劝彝族苗族自治县</a><a href="//linjiang.meituan.com"
                                                                                       class="link city ">临江</a><a
                    href="//lianjiangxian.meituan.com" class="link city ">连江</a><a href="//linqu.meituan.com"
                                                                                   class="link city ">临朐</a><a
                    href="//laoting.meituan.com" class="link city ">乐亭</a><a href="//luanxian.meituan.com"
                                                                             class="link city ">滦县</a><a
                    href="//luancheng.meituan.com" class="link city ">栾城</a><a href="//lushanls.meituan.com"
                                                                               class="link city ">鲁山</a><a
                    href="//lingshi.meituan.com" class="link city ">灵石</a><a href="//linzhang.meituan.com"
                                                                             class="link city ">临漳</a><a
                    href="//lintong.meituan.com" class="link city ">临潼</a><a href="//lantian.meituan.com"
                                                                             class="link city ">蓝田</a><a
                    href="//lq.meituan.com" class="link city ">临清</a><a href="//longchang.meituan.com"
                                                                        class="link city ">隆昌市</a><a
                    href="//luyi.meituan.com" class="link city ">鹿邑</a><a href="//liuhe.meituan.com" class="link city ">柳河</a><a
                    href="//linyixian.meituan.com" class="link city ">临猗</a><a href="//liangshanxian.meituan.com"
                                                                               class="link city ">梁山</a><a
                    href="//lijin.meituan.com" class="link city ">利津</a><a href="//linyily.meituan.com"
                                                                           class="link city ">临邑</a><a
                    href="//longquan.meituan.com" class="link city ">龙泉</a><a href="//lingchuan.meituan.com"
                                                                              class="link city ">陵川</a><a
                    href="//longyao.meituan.com" class="link city ">隆尧</a><a href="//leizhou.meituan.com"
                                                                             class="link city ">雷州</a><a
                    href="//luanchuan.meituan.com" class="link city ">栾川</a><a href="//longyou.meituan.com"
                                                                               class="link city ">龙游</a><a
                    href="//lanling.meituan.com" class="link city ">兰陵</a><a href="//linshu.meituan.com"
                                                                             class="link city ">临沭</a><a
                    href="//lianshui.meituan.com" class="link city ">涟水</a><a href="//lixian.meituan.com"
                                                                              class="link city ">澧县</a><a
                    href="//liaozhong.meituan.com" class="link city ">辽中</a><a href="//luopingxian.meituan.com"
                                                                               class="link city ">罗平县</a><a
                    href="//lianyuanshi.meituan.com" class="link city ">涟源市</a><a href="//lujiangxian.meituan.com"
                                                                                  class="link city ">庐江县</a><a
                    href="//linying.meituan.com" class="link city ">临颍</a><a href="//lanshan.meituan.com"
                                                                             class="link city ">蓝山</a><a
                    href="//longhui.meituan.com" class="link city ">隆回</a><a href="//luxi.meituan.com"
                                                                             class="link city ">芦溪</a><a
                    href="//lushixian.meituan.com" class="link city ">卢氏县</a><a href="//longhuaxian.meituan.com"
                                                                                class="link city ">隆化县</a><a
                    href="//luoningxian.meituan.com" class="link city ">洛宁</a><a href="//lankaoxian.meituan.com"
                                                                                 class="link city ">兰考县</a><a
                    href="//linli.meituan.com" class="link city ">临澧</a><a href="//lixin.meituan.com"
                                                                           class="link city ">利辛</a><a
                    href="//lingqiuxian.meituan.com" class="link city ">灵丘县</a><a href="//lufengxian.meituan.com"
                                                                                  class="link city ">禄丰县</a><a
                    href="//lishuiqu.meituan.com" class="link city ">溧水区</a><a href="//luxian.meituan.com"
                                                                               class="link city ">泸县</a><a
                    href="//luochuanxian.meituan.com" class="link city ">洛川县</a><a href="//luodingshi.meituan.com"
                                                                                   class="link city ">罗定市</a><a
                    href="//ledong.meituan.com" class="link city ">乐东</a><a href="//liangping.meituan.com"
                                                                            class="link city ">梁平</a><a
                    href="//lingaoxian.meituan.com" class="link city ">临高县</a><a href="//luoyuanxian.meituan.com"
                                                                                 class="link city ">罗源县</a><a
                    href="//lingshui.meituan.com" class="link city ">陵水</a><a href="//ln.meituan.com"
                                                                              class="link city ">陇南</a><a
                    href="//linzhi.meituan.com" class="link city ">林芝</a></span></div>
            <div class="city-area" id="city-M"><span class="city-label">M</span><span class="cities"><a
                    href="//my.meituan.com" class="link city ">绵阳</a><a href="//mdj.meituan.com"
                                                                        class="link city ">牡丹江</a><a
                    href="//mas.meituan.com" class="link city ">马鞍山</a><a href="//mm.meituan.com"
                                                                          class="link city ">茂名</a><a
                    href="//mz.meituan.com" class="link city ">梅州</a><a href="//ms.meituan.com"
                                                                        class="link city ">眉山</a><a
                    href="//mzl.meituan.com" class="link city ">满洲里</a><a href="//mhk.meituan.com" class="link city ">梅河口</a><a
                    href="//ml.meituan.com" class="link city ">汨罗</a><a href="//mg.meituan.com"
                                                                        class="link city ">明光</a><a
                    href="//mc.meituan.com" class="link city ">麻城</a><a href="//mengzhou.meituan.com"
                                                                        class="link city ">孟州</a><a
                    href="//mingshuixian.meituan.com" class="link city ">明水县</a><a href="//mishan.meituan.com"
                                                                                   class="link city ">密山</a><a
                    href="//muping.meituan.com" class="link city ">牟平</a><a href="//meixian.meituan.com"
                                                                            class="link city ">眉县</a><a
                    href="//minquan.meituan.com" class="link city ">民权</a><a href="//mianchi.meituan.com"
                                                                             class="link city ">渑池</a><a
                    href="//mianzhu.meituan.com" class="link city ">绵竹</a><a href="//mengyin.meituan.com"
                                                                             class="link city ">蒙阴</a><a
                    href="//mengzishi.meituan.com" class="link city ">蒙自市</a><a href="//mengcheng.meituan.com"
                                                                                class="link city ">蒙城</a><a
                    href="//menglaxian.meituan.com" class="link city ">勐腊县</a><a href="//miyixian.meituan.com"
                                                                                 class="link city ">米易县</a><a
                    href="//minhouxian.meituan.com" class="link city ">闽侯县</a><a href="//mengjin.meituan.com"
                                                                                 class="link city ">孟津</a><a
                    href="//mh.meituan.com" class="link city ">漠河</a><a href="//mingwangxing.meituan.com"
                                                                        class="link city ">冥王星</a><a
                    href="//miaoli.meituan.com" class="link city ">苗栗</a></span></div>
            <div class="city-area" id="city-N"><span class="city-label">N</span><span class="cities"><a
                    href="//nj.meituan.com" class="link city sa-city">南京</a><a href="//nb.meituan.com"
                                                                               class="link city ">宁波</a><a
                    href="//nn.meituan.com" class="link city ">南宁</a><a href="//nc.meituan.com"
                                                                        class="link city ">南昌</a><a
                    href="//nt.meituan.com" class="link city ">南通</a><a href="//ny.meituan.com"
                                                                        class="link city ">南阳</a><a
                    href="//nd.meituan.com" class="link city ">宁德</a><a href="//nanchong.meituan.com"
                                                                        class="link city ">南充</a><a
                    href="//np.meituan.com" class="link city ">南平</a><a href="//scnj.meituan.com"
                                                                        class="link city ">内江</a><a
                    href="//nh.meituan.com" class="link city ">宁海</a><a href="//na.meituan.com"
                                                                        class="link city ">南安</a><a
                    href="//nanchuan.meituan.com" class="link city ">南川</a><a href="//nx.meituan.com"
                                                                              class="link city ">宁乡</a><a
                    href="//ns.meituan.com" class="link city ">南沙</a><a href="//ningyuanxian.meituan.com"
                                                                        class="link city ">宁远县</a><a
                    href="//nehe.meituan.com" class="link city ">讷河</a><a href="//nanxiong.meituan.com"
                                                                          class="link city ">南雄</a><a
                    href="//nenjiangxian.meituan.com" class="link city ">嫩江县</a><a href="//nanle.meituan.com"
                                                                                   class="link city ">南乐</a><a
                    href="//nanling.meituan.com" class="link city ">南陵</a><a href="//ningyang.meituan.com"
                                                                             class="link city ">宁阳</a><a
                    href="//ningguo.meituan.com" class="link city ">宁国</a><a href="//ningjin.meituan.com"
                                                                             class="link city ">宁晋</a><a
                    href="//ningjinnj.meituan.com" class="link city ">宁津</a><a href="//neiqiu.meituan.com"
                                                                               class="link city ">内丘</a><a
                    href="//nangong.meituan.com" class="link city ">南宫</a><a href="//neihuang.meituan.com"
                                                                             class="link city ">内黄</a><a
                    href="//nanhe.meituan.com" class="link city ">南和</a><a href="//nanbuxian.meituan.com"
                                                                           class="link city ">南部县</a><a
                    href="//nanpixian.meituan.com" class="link city ">南皮县</a><a href="//ninglingxian.meituan.com"
                                                                                class="link city ">宁陵</a><a
                    href="//nanzhengxian.meituan.com" class="link city ">南郑区</a><a href="//ninglangyizuzizh.meituan.com"
                                                                                   class="link city ">宁蒗彝族自治县</a><a
                    href="//nq.meituan.com" class="link city ">那曲</a><a href="//nujiang.meituan.com" class="link city ">怒江</a><a
                    href="//nantou.meituan.com" class="link city ">南投</a></span></div>
            <div class="city-area" id="city-P"><span class="city-label">P</span><span class="cities"><a
                    href="//pt.meituan.com" class="link city ">莆田</a><a href="//pj.meituan.com"
                                                                        class="link city ">盘锦</a><a
                    href="//pds.meituan.com" class="link city ">平顶山</a><a href="//puyang.meituan.com"
                                                                          class="link city ">濮阳</a><a
                    href="//panzhihua.meituan.com" class="link city ">攀枝花</a><a href="//pe.meituan.com"
                                                                                class="link city ">普洱</a><a
                    href="//pl.meituan.com" class="link city ">平凉</a><a href="//pz.meituan.com"
                                                                        class="link city ">邳州</a><a
                    href="//px.meituan.com" class="link city ">萍乡</a><a href="//pn.meituan.com"
                                                                        class="link city ">普宁</a><a
                    href="//pd.meituan.com" class="link city ">平度</a><a href="//pengzhou.meituan.com"
                                                                        class="link city ">彭州</a><a
                    href="//penglai.meituan.com" class="link city ">蓬莱</a><a href="//pingyang.meituan.com"
                                                                             class="link city ">平阳</a><a
                    href="//peixian.meituan.com" class="link city ">沛县</a><a href="//ph.meituan.com" class="link city ">平湖</a><a
                    href="//pujiang.meituan.com" class="link city ">浦江</a><a href="//panshi.meituan.com"
                                                                             class="link city ">磐石</a><a
                    href="//pingyuan.meituan.com" class="link city ">平原</a><a href="//pulandian.meituan.com"
                                                                              class="link city ">普兰店</a><a
                    href="//poyang.meituan.com" class="link city ">鄱阳</a><a href="//pucheng.meituan.com"
                                                                            class="link city ">蒲城</a><a
                    href="//panxian.meituan.com" class="link city ">盘州市</a><a href="//pingjiang.meituan.com"
                                                                              class="link city ">平江</a><a
                    href="//puyangxian.meituan.com" class="link city ">濮阳县</a><a href="//pingshan.meituan.com"
                                                                                 class="link city ">平山</a><a
                    href="//pingquan.meituan.com" class="link city ">平泉市</a><a href="//pingyi.meituan.com"
                                                                               class="link city ">平邑</a><a
                    href="//pingyu.meituan.com" class="link city ">平舆</a><a href="//pengshuizizhixia.meituan.com"
                                                                            class="link city ">彭水苗族土家族自治县</a><a
                    href="//pingyao.meituan.com" class="link city ">平遥</a><a href="//pingguo.meituan.com"
                                                                             class="link city ">平果</a><a
                    href="//pingluoxian.meituan.com" class="link city ">平罗县</a><a href="//pingyinxian.meituan.com"
                                                                                  class="link city ">平阴县</a><a
                    href="//pingluxian.meituan.com" class="link city ">平陆县</a><a href="//pingchangxian.meituan.com"
                                                                                 class="link city ">平昌县</a><a
                    href="//pingnanxian.meituan.com" class="link city ">平南县</a><a href="//pingtan.meituan.com"
                                                                                  class="link city ">平潭</a><a
                    href="//penghu.meituan.com" class="link city ">澎湖</a></span></div>
            <div class="city-area" id="city-Q"><span class="city-label">Q</span><span class="cities"><a
                    href="//qd.meituan.com" class="link city ">青岛</a><a href="//qhd.meituan.com"
                                                                        class="link city ">秦皇岛</a><a
                    href="//qz.meituan.com" class="link city ">泉州</a><a href="//qj.meituan.com"
                                                                        class="link city ">曲靖</a><a
                    href="//quzhou.meituan.com" class="link city ">衢州</a><a href="//qingyuan.meituan.com"
                                                                            class="link city ">清远</a><a
                    href="//qqhr.meituan.com" class="link city ">齐齐哈尔</a><a href="//qinzhou.meituan.com"
                                                                            class="link city ">钦州</a><a
                    href="//qth.meituan.com" class="link city ">七台河</a><a href="//qingyang.meituan.com"
                                                                          class="link city ">庆阳</a><a
                    href="//qa.meituan.com" class="link city ">迁安</a><a href="//qingzhou.meituan.com"
                                                                        class="link city ">青州</a><a
                    href="//qidong.meituan.com" class="link city ">启东</a><a href="//qianjiang.meituan.com"
                                                                            class="link city ">潜江</a><a
                    href="//qdn.meituan.com" class="link city ">黔东南</a><a href="//qxn.meituan.com" class="link city ">黔西南</a><a
                    href="//qishizhen.meituan.com" class="link city ">企石镇</a><a href="//qh.meituan.com"
                                                                                class="link city ">琼海</a><a
                    href="//qy.meituan.com" class="link city ">沁阳</a><a href="//ql.meituan.com"
                                                                        class="link city ">邛崃</a><a
                    href="//qihe.meituan.com" class="link city ">齐河</a><a href="//qn.meituan.com"
                                                                          class="link city ">黔南</a><a
                    href="//qixian.meituan.com" class="link city ">淇县</a><a href="//quanjiao.meituan.com"
                                                                            class="link city ">全椒</a><a
                    href="//qixia.meituan.com" class="link city ">栖霞</a><a href="//qingtian.meituan.com"
                                                                           class="link city ">青田</a><a
                    href="//qinghe.meituan.com" class="link city ">清河</a><a href="//qingyun.meituan.com"
                                                                            class="link city ">庆云</a><a
                    href="//qianshan.meituan.com" class="link city ">潜山</a><a href="//qingxian.meituan.com"
                                                                              class="link city ">青县</a><a
                    href="//qidongxian.meituan.com" class="link city ">祁东县</a><a href="//qinganxian.meituan.com"
                                                                                 class="link city ">庆安县</a><a
                    href="//qixiankaifeng.meituan.com" class="link city ">杞县</a><a href="//qinggangxian.meituan.com"
                                                                                   class="link city ">青冈县</a><a
                    href="//qishanxian.meituan.com" class="link city ">岐山县</a><a href="//qiongzhong.meituan.com"
                                                                                 class="link city ">琼中</a><a
                    href="//qingyangxian.meituan.com" class="link city ">青阳县</a><a href="//qingzhen.meituan.com"
                                                                                   class="link city ">清镇</a><a
                    href="//qijiang.meituan.com" class="link city ">綦江</a><a href="//qingxu.meituan.com"
                                                                             class="link city ">清徐</a><a
                    href="//qianxixian.meituan.com" class="link city ">迁西县</a><a href="//qingfeng.meituan.com"
                                                                                 class="link city ">清丰</a></span></div>
            <div class="city-area" id="city-R"><span class="city-label">R</span><span class="cities"><a
                    href="//rizhao.meituan.com" class="link city ">日照</a><a href="//ruian.meituan.com"
                                                                            class="link city ">瑞安</a><a
                    href="//rc.meituan.com" class="link city ">荣成</a><a href="//rs.meituan.com"
                                                                        class="link city ">乳山</a><a
                    href="//rg.meituan.com" class="link city ">如皋</a><a href="//rz.meituan.com"
                                                                        class="link city ">汝州</a><a
                    href="//rudong.meituan.com" class="link city ">如东</a><a href="//rh.meituan.com" class="link city ">仁怀</a><a
                    href="//rj.meituan.com" class="link city ">瑞金</a><a href="//rongchangqu.meituan.com"
                                                                        class="link city ">荣昌区</a><a
                    href="//renshou.meituan.com" class="link city ">仁寿</a><a href="//renqiu.meituan.com"
                                                                             class="link city ">任丘</a><a
                    href="//ruyang.meituan.com" class="link city ">汝阳</a><a href="//ruili.meituan.com"
                                                                            class="link city ">瑞丽</a><a
                    href="//renxian.meituan.com" class="link city ">任县</a><a href="//ruchengxian.meituan.com"
                                                                             class="link city ">汝城县</a><a
                    href="//rongxian.meituan.com" class="link city ">容县</a><a href="//ruichang.meituan.com"
                                                                              class="link city ">瑞昌</a><a
                    href="//rkz.meituan.com" class="link city ">日喀则</a></span></div>
            <div class="city-area" id="city-S"><span class="city-label">S</span><span class="cities"><a
                    href="//sh.meituan.com" class="link city sa-city">上海</a><a href="//sz.meituan.com"
                                                                               class="link city sa-city">深圳</a><a
                    href="//sjz.meituan.com" class="link city ">石家庄</a><a href="//su.meituan.com"
                                                                          class="link city ">苏州</a><a
                    href="//sy.meituan.com" class="link city ">沈阳</a><a href="//sanya.meituan.com"
                                                                        class="link city ">三亚</a><a
                    href="//st.meituan.com" class="link city ">汕头</a><a href="//sx.meituan.com"
                                                                        class="link city ">绍兴</a><a
                    href="//songyuan.meituan.com" class="link city ">松原</a><a href="//sg.meituan.com"
                                                                              class="link city ">韶关</a><a
                    href="//shaoyang.meituan.com" class="link city ">邵阳</a><a href="//suqian.meituan.com"
                                                                              class="link city ">宿迁</a><a
                    href="//shiyan.meituan.com" class="link city ">十堰</a><a href="//suzhousz.meituan.com"
                                                                            class="link city ">宿州</a><a
                    href="//sd.meituan.com" class="link city ">顺德</a><a href="//sr.meituan.com"
                                                                        class="link city ">上饶</a><a
                    href="//sq.meituan.com" class="link city ">商丘</a><a href="//shz.meituan.com"
                                                                        class="link city ">石河子</a><a
                    href="//smx.meituan.com" class="link city ">三门峡</a><a href="//suizhou.meituan.com"
                                                                          class="link city ">随州</a><a
                    href="//suihua.meituan.com" class="link city ">绥化</a><a href="//sys.meituan.com" class="link city ">双鸭山</a><a
                    href="//sw.meituan.com" class="link city ">汕尾</a><a href="//suining.meituan.com" class="link city ">遂宁</a><a
                    href="//sl.meituan.com" class="link city ">商洛</a><a href="//szs.meituan.com"
                                                                        class="link city ">石嘴山</a><a
                    href="//sp.meituan.com" class="link city ">四平</a><a href="//sm.meituan.com"
                                                                        class="link city ">三明</a><a
                    href="//ss.meituan.com" class="link city ">石狮</a><a href="//shangyu.meituan.com" class="link city ">上虞</a><a
                    href="//shouguang.meituan.com" class="link city ">寿光</a><a href="//shengzhou.meituan.com"
                                                                               class="link city ">嵊州</a><a
                    href="//shuyang.meituan.com" class="link city ">沭阳</a><a href="//sheyang.meituan.com"
                                                                             class="link city ">射阳</a><a
                    href="//sanhe.meituan.com" class="link city ">三河</a><a href="//shuozhou.meituan.com"
                                                                           class="link city ">朔州</a><a
                    href="//shucheng.meituan.com" class="link city ">舒城</a><a href="//shaya.meituan.com"
                                                                              class="link city ">沙雅</a><a
                    href="//suiping.meituan.com" class="link city ">遂平</a><a href="//shuangcheng.meituan.com"
                                                                             class="link city ">双城</a><a
                    href="//shaoshan.meituan.com" class="link city ">韶山</a><a href="//shahe.meituan.com"
                                                                              class="link city ">沙河</a><a
                    href="//sihui.meituan.com" class="link city ">四会</a><a href="//songzi.meituan.com"
                                                                           class="link city ">松滋</a><a
                    href="//shulan.meituan.com" class="link city ">舒兰</a><a href="//shaodong.meituan.com"
                                                                            class="link city ">邵东</a><a
                    href="//suixian.meituan.com" class="link city ">睢县</a><a href="//siyang.meituan.com"
                                                                             class="link city ">泗阳</a><a
                    href="//shawan.meituan.com" class="link city ">沙湾</a><a href="//shilinxian.meituan.com"
                                                                            class="link city ">石林彝族自治县</a><a
                    href="//shenmu.meituan.com" class="link city ">神木市</a><a href="//suizhong.meituan.com"
                                                                             class="link city ">绥中</a><a
                    href="//shanggao.meituan.com" class="link city ">上高</a><a href="//shiquan.meituan.com"
                                                                              class="link city ">石泉</a><a
                    href="//sihong.meituan.com" class="link city ">泗洪</a><a href="//shanxian.meituan.com"
                                                                            class="link city ">单县</a><a
                    href="//shenqiu.meituan.com" class="link city ">沈丘</a><a href="//sanmen.meituan.com"
                                                                             class="link city ">三门</a><a
                    href="//suiningxian.meituan.com" class="link city ">睢宁</a><a href="//shangcai.meituan.com"
                                                                                 class="link city ">上蔡</a><a
                    href="//suichang.meituan.com" class="link city ">遂昌</a><a href="//shidao.meituan.com"
                                                                              class="link city ">石岛</a><a
                    href="//shifang.meituan.com" class="link city ">什邡</a><a href="//shanghang.meituan.com"
                                                                             class="link city ">上杭</a><a
                    href="//songxian.meituan.com" class="link city ">嵩县</a><a href="//songmingxian.meituan.com"
                                                                              class="link city ">嵩明县</a><a
                    href="//shehong.meituan.com" class="link city ">射洪</a><a href="//shanghe.meituan.com"
                                                                             class="link city ">商河</a><a
                    href="//sishui.meituan.com" class="link city ">泗水</a><a href="//sheqi.meituan.com"
                                                                            class="link city ">社旗</a><a
                    href="//sixian.meituan.com" class="link city ">泗县</a><a href="//shenzhoushi.meituan.com"
                                                                            class="link city ">深州市</a><a
                    href="//shanglinxian.meituan.com" class="link city ">上林县</a><a href="//shangshuixian.meituan.com"
                                                                                   class="link city ">商水县</a><a
                    href="//shuangfeng.meituan.com" class="link city ">双峰</a><a href="//suichuan.meituan.com"
                                                                                class="link city ">遂川</a><a
                    href="//shangli.meituan.com" class="link city ">上栗</a><a href="//shachexian.meituan.com"
                                                                             class="link city ">莎车县</a><a
                    href="//suningxian.meituan.com" class="link city ">肃宁县</a><a href="//shangchengxian.meituan.com"
                                                                                 class="link city ">商城县</a><a
                    href="//sangzhi.meituan.com" class="link city ">桑植</a><a href="//shimen.meituan.com"
                                                                             class="link city ">石门</a><a
                    href="//shanshanxian.meituan.com" class="link city ">鄯善县</a><a href="//suidexian.meituan.com"
                                                                                   class="link city ">绥德县</a><a
                    href="//shaxian.meituan.com" class="link city ">沙县</a><a href="//shenzexian.meituan.com"
                                                                             class="link city ">深泽县</a><a
                    href="//shizhu.meituan.com" class="link city ">石柱</a><a href="//shaowu.meituan.com"
                                                                            class="link city ">邵武</a><a
                    href="//shouxian.meituan.com" class="link city ">寿县</a><a href="//santaixian.meituan.com"
                                                                              class="link city ">三台县</a><a
                    href="//shandanxian.meituan.com" class="link city ">山丹县</a><a href="//shanzhouqu.meituan.com"
                                                                                  class="link city ">陕州区</a><a
                    href="//suiningxiansnx.meituan.com" class="link city ">绥宁县</a><a href="//shexian.meituan.com"
                                                                                     class="link city ">涉县</a><a
                    href="//sqs.meituan.com" class="link city ">三清山</a><a href="//snj.meituan.com" class="link city ">神农架</a><a
                    href="//sn.meituan.com" class="link city ">山南</a><a href="//sanx.meituan.com"
                                                                        class="link city ">三峡</a></span></div>
            <div class="city-area" id="city-T"><span class="city-label">T</span><span class="cities"><a
                    href="//tj.meituan.com" class="link city sa-city">天津</a><a href="//ty.meituan.com"
                                                                               class="link city ">太原</a><a
                    href="//taizhou.meituan.com" class="link city ">泰州</a><a href="//tz.meituan.com" class="link city ">台州</a><a
                    href="//ts.meituan.com" class="link city ">唐山</a><a href="//ta.meituan.com"
                                                                        class="link city ">泰安</a><a
                    href="//tx.meituan.com" class="link city ">桐乡</a><a href="//taicang.meituan.com" class="link city ">太仓</a><a
                    href="//tianshui.meituan.com" class="link city ">天水</a><a href="//tr.meituan.com"
                                                                              class="link city ">铜仁</a><a
                    href="//th.meituan.com" class="link city ">通化</a><a href="//tl.meituan.com"
                                                                        class="link city ">铁岭</a><a
                    href="//tongling.meituan.com" class="link city ">铜陵</a><a href="//tongliao.meituan.com"
                                                                              class="link city ">通辽</a><a
                    href="//taishan.meituan.com" class="link city ">台山</a><a href="//taixing.meituan.com"
                                                                             class="link city ">泰兴</a><a
                    href="//tengzhou.meituan.com" class="link city ">滕州</a><a href="//tm.meituan.com"
                                                                              class="link city ">天门</a><a
                    href="//tianchang.meituan.com" class="link city ">天长</a><a href="//tc.meituan.com"
                                                                               class="link city ">铜川</a><a
                    href="//taiwan.meituan.com" class="link city ">台湾</a><a href="//tunchangxian.meituan.com"
                                                                            class="link city ">屯昌县</a><a
                    href="//tonglu.meituan.com" class="link city ">桐庐</a><a href="//tonghexian.meituan.com"
                                                                            class="link city ">通河县</a><a
                    href="//tachengshi.meituan.com" class="link city ">塔城市</a><a href="//tn.meituan.com"
                                                                                 class="link city ">洮南</a><a
                    href="//tongcheng.meituan.com" class="link city ">桐城</a><a href="//tongxinxian.meituan.com"
                                                                               class="link city ">同心县</a><a
                    href="//tongjiangxian.meituan.com" class="link city ">通江县</a><a href="//tanghe.meituan.com"
                                                                                    class="link city ">唐河</a><a
                    href="//tongyuxian.meituan.com" class="link city ">通榆县</a><a href="//taiqian.meituan.com"
                                                                                 class="link city ">台前</a><a
                    href="//taihe.meituan.com" class="link city ">太和</a><a href="//tiantai.meituan.com"
                                                                           class="link city ">天台</a><a
                    href="//taigu.meituan.com" class="link city ">太谷</a><a href="//tengxian.meituan.com"
                                                                           class="link city ">藤县</a><a
                    href="//tangyin.meituan.com" class="link city ">汤阴</a><a href="//tmtyq.meituan.com"
                                                                             class="link city ">土默特右旗</a><a
                    href="//tancheng.meituan.com" class="link city ">郯城</a><a href="//tongliang.meituan.com"
                                                                              class="link city ">铜梁</a><a
                    href="//tongan.meituan.com" class="link city ">同安</a><a href="//taoyuanxian.meituan.com"
                                                                            class="link city ">桃源</a><a
                    href="//taihexian.meituan.com" class="link city ">泰和县</a><a href="//tonggu.meituan.com"
                                                                                class="link city ">铜鼓</a><a
                    href="//tiandongxian.meituan.com" class="link city ">田东县</a><a href="//taikangxian.meituan.com"
                                                                                   class="link city ">太康县</a><a
                    href="//tongxuxian.meituan.com" class="link city ">通许县</a><a href="//tonghaixian.meituan.com"
                                                                                 class="link city ">通海县</a><a
                    href="//taoyuan.meituan.com" class="link city ">桃园</a><a href="//taidong.meituan.com"
                                                                             class="link city ">台东</a><a
                    href="//taizhong.meituan.com" class="link city ">台中</a><a href="//tengchong.meituan.com"
                                                                              class="link city ">腾冲</a><a
                    href="//tb.meituan.com" class="link city ">台北</a><a href="//tac.meituan.com"
                                                                        class="link city ">塔城</a><a
                    href="//tlf.meituan.com" class="link city ">吐鲁番</a><a href="//tainan.meituan.com"
                                                                          class="link city ">台南</a></span></div>
            <div class="city-area" id="city-W"><span class="city-label">W</span><span class="cities"><a
                    href="//wh.meituan.com" class="link city sa-city">武汉</a><a href="//wx.meituan.com"
                                                                               class="link city ">无锡</a><a
                    href="//wz.meituan.com" class="link city ">温州</a><a href="//wf.meituan.com"
                                                                        class="link city ">潍坊</a><a
                    href="//weihai.meituan.com" class="link city ">威海</a><a href="//wuhu.meituan.com"
                                                                            class="link city ">芜湖</a><a
                    href="//xj.meituan.com" class="link city ">乌鲁木齐</a><a href="//wn.meituan.com"
                                                                          class="link city ">渭南</a><a
                    href="//wj.meituan.com" class="link city ">吴江</a><a href="//wenling.meituan.com" class="link city ">温岭</a><a
                    href="//wuhai.meituan.com" class="link city ">乌海</a><a href="//wanzhou.meituan.com"
                                                                           class="link city ">万州</a><a
                    href="//wuzhou.meituan.com" class="link city ">梧州</a><a href="//wuan.meituan.com"
                                                                            class="link city ">武安</a><a
                    href="//wlcb.meituan.com" class="link city ">乌兰察布</a><a href="//wd.meituan.com" class="link city ">文登</a><a
                    href="//wc.meituan.com" class="link city ">吴川</a><a href="//wafangdian.meituan.com"
                                                                        class="link city ">瓦房店</a><a
                    href="//wuwei.meituan.com" class="link city ">武威</a><a href="//wy.meituan.com"
                                                                           class="link city ">婺源</a><a
                    href="//wugangshi.meituan.com" class="link city ">武冈市</a><a href="//wuzhong.meituan.com"
                                                                                class="link city ">吴忠</a><a
                    href="//wangkuixian.meituan.com" class="link city ">望奎县</a><a href="//wys.meituan.com"
                                                                                  class="link city ">武夷山</a><a
                    href="//wenchang.meituan.com" class="link city ">文昌</a><a href="//wuxue.meituan.com"
                                                                              class="link city ">武穴</a><a
                    href="//wanning.meituan.com" class="link city ">万宁</a><a href="//wg.meituan.com" class="link city ">舞钢</a><a
                    href="//wuding.meituan.com" class="link city ">武定</a><a href="//wuzhi.meituan.com"
                                                                            class="link city ">武陟</a><a
                    href="//wusu.meituan.com" class="link city ">乌苏</a><a href="//wuweiww.meituan.com"
                                                                          class="link city ">无为</a><a
                    href="//wuhuxian.meituan.com" class="link city ">芜湖县</a><a href="//weihui.meituan.com"
                                                                               class="link city ">卫辉</a><a
                    href="//wltqq.meituan.com" class="link city ">乌拉特前旗</a><a href="//weishan.meituan.com"
                                                                              class="link city ">微山</a><a
                    href="//wenshang.meituan.com" class="link city ">汶上</a><a href="//wucheng.meituan.com"
                                                                              class="link city ">武城</a><a
                    href="//weichang.meituan.com" class="link city ">围场</a><a href="//ws.meituan.com"
                                                                              class="link city ">文山</a><a
                    href="//wuyi.meituan.com" class="link city ">武义</a><a href="//wuming.meituan.com"
                                                                          class="link city ">武鸣</a><a
                    href="//weining.meituan.com" class="link city ">威宁</a><a href="//wuyang.meituan.com"
                                                                             class="link city ">舞阳</a><a
                    href="//wuji.meituan.com" class="link city ">无极</a><a href="//wanrong.meituan.com"
                                                                          class="link city ">万荣</a><a
                    href="//wanzai.meituan.com" class="link city ">万载</a><a href="//weixian.meituan.com"
                                                                            class="link city ">威县</a><a
                    href="//wupingxian.meituan.com" class="link city ">武平县</a><a href="//weishixian.meituan.com"
                                                                                 class="link city ">尉氏县</a><a
                    href="//wulongxian.meituan.com" class="link city ">武隆县</a><a href="//wuchangshi.meituan.com"
                                                                                 class="link city ">五常市</a><a
                    href="//wangcangxian.meituan.com" class="link city ">旺苍县</a><a href="//wenxian.meituan.com"
                                                                                   class="link city ">温县</a><a
                    href="//wuzhen.meituan.com" class="link city ">乌镇</a><a href="//wds.meituan.com" class="link city ">武当山</a></span>
            </div>
            <div class="city-area" id="city-X"><span class="city-label">X</span><span class="cities"><a
                    href="//xa.meituan.com" class="link city sa-city">西安</a><a href="//xm.meituan.com"
                                                                               class="link city ">厦门</a><a
                    href="//xz.meituan.com" class="link city ">徐州</a><a href="//xf.meituan.com"
                                                                        class="link city ">襄阳</a><a
                    href="//xiangtan.meituan.com" class="link city ">湘潭</a><a href="//xn.meituan.com"
                                                                              class="link city ">西宁</a><a
                    href="//xuancheng.meituan.com" class="link city ">宣城</a><a href="//xianyang.meituan.com"
                                                                               class="link city ">咸阳</a><a
                    href="//xc.meituan.com" class="link city ">许昌</a><a href="//xy.meituan.com"
                                                                        class="link city ">信阳</a><a
                    href="//xt.meituan.com" class="link city ">邢台</a><a href="//xiaogan.meituan.com" class="link city ">孝感</a><a
                    href="//xx.meituan.com" class="link city ">新乡</a><a href="//xintai.meituan.com" class="link city ">新泰</a><a
                    href="//xianning.meituan.com" class="link city ">咸宁</a><a href="//xinyu.meituan.com"
                                                                              class="link city ">新余</a><a
                    href="//xan.meituan.com" class="link city ">兴安盟</a><a href="//xiantao.meituan.com"
                                                                          class="link city ">仙桃</a><a
                    href="//xh.meituan.com" class="link city ">兴化</a><a href="//bn.meituan.com"
                                                                        class="link city ">西双版纳</a><a
                    href="//xinji.meituan.com" class="link city ">辛集</a><a href="//xinyi.meituan.com"
                                                                           class="link city ">新沂</a><a
                    href="//xinzheng.meituan.com" class="link city ">新郑</a><a href="//xinmi.meituan.com"
                                                                              class="link city ">新密</a><a
                    href="//xinzhou.meituan.com" class="link city ">忻州</a><a href="//xinyixy.meituan.com"
                                                                             class="link city ">信宜</a><a
                    href="//xiegangzhen.meituan.com" class="link city ">谢岗镇</a><a href="//xiaoxian.meituan.com"
                                                                                  class="link city ">萧县</a><a
                    href="//xlgl.meituan.com" class="link city ">锡林郭勒</a><a href="//xiangxi.meituan.com"
                                                                            class="link city ">湘西</a><a
                    href="//xingyang.meituan.com" class="link city ">荥阳</a><a href="//xixian.meituan.com"
                                                                              class="link city ">息县</a><a
                    href="//xingning.meituan.com" class="link city ">兴宁</a><a href="//xinmin.meituan.com"
                                                                              class="link city ">新民</a><a
                    href="//xiangcheng.meituan.com" class="link city ">项城</a><a href="//xiaoyi.meituan.com"
                                                                                class="link city ">孝义</a><a
                    href="//xiangxiang.meituan.com" class="link city ">湘乡</a><a href="//xingcheng.meituan.com"
                                                                                class="link city ">兴城</a><a
                    href="//xp.meituan.com" class="link city ">兴平</a><a href="//xiangshan.meituan.com"
                                                                        class="link city ">象山</a><a
                    href="//xw.meituan.com" class="link city ">修武</a><a href="//xiaochangxian.meituan.com"
                                                                        class="link city ">孝昌县</a><a
                    href="//xunyangxian.meituan.com" class="link city ">旬阳县</a><a href="//xiangyin.meituan.com"
                                                                                  class="link city ">湘阴</a><a
                    href="//xiangshui.meituan.com" class="link city ">响水</a><a href="//xinhua.meituan.com"
                                                                               class="link city ">新化</a><a
                    href="//xianju.meituan.com" class="link city ">仙居</a><a href="//xiangyuan.meituan.com"
                                                                            class="link city ">襄垣</a><a
                    href="//xuanwei.meituan.com" class="link city ">宣威</a><a href="//xiapu.meituan.com"
                                                                             class="link city ">霞浦</a><a
                    href="//xinan.meituan.com" class="link city ">新安</a><a href="//xinxiangxian.meituan.com"
                                                                           class="link city ">新乡县</a><a
                    href="//xuyi.meituan.com" class="link city ">盱眙</a><a href="//xuwen.meituan.com" class="link city ">徐闻</a><a
                    href="//xiayi.meituan.com" class="link city ">夏邑</a><a href="//xunxian.meituan.com"
                                                                           class="link city ">浚县</a><a
                    href="//xixiang.meituan.com" class="link city ">西乡</a><a href="//xiping.meituan.com"
                                                                             class="link city ">西平</a><a
                    href="//xinle.meituan.com" class="link city ">新乐</a><a href="//xinchang.meituan.com"
                                                                           class="link city ">新昌</a><a
                    href="//xuecheng.meituan.com" class="link city ">薛城</a><a href="//xihua.meituan.com"
                                                                              class="link city ">西华</a><a
                    href="//xishui.meituan.com" class="link city ">浠水</a><a href="//xianghe.meituan.com"
                                                                            class="link city ">香河</a><a
                    href="//xinfeng.meituan.com" class="link city ">信丰</a><a href="//xincai.meituan.com"
                                                                             class="link city ">新蔡</a><a
                    href="//xupu.meituan.com" class="link city ">溆浦</a><a href="//xichuan.meituan.com"
                                                                          class="link city ">淅川</a><a
                    href="//xingan.meituan.com" class="link city ">新干</a><a href="//xingguoxian.meituan.com"
                                                                            class="link city ">兴国县</a><a
                    href="//xintian.meituan.com" class="link city ">新田</a><a href="//xunwuxian.meituan.com"
                                                                             class="link city ">寻乌县</a><a
                    href="//xiangyunxian.meituan.com" class="link city ">祥云县</a><a href="//xiangchengxian.meituan.com"
                                                                                   class="link city ">襄城县</a><a
                    href="//xinning.meituan.com" class="link city ">新宁</a><a href="//xianxian.meituan.com"
                                                                             class="link city ">献县</a><a
                    href="//xinzhouqu.meituan.com" class="link city ">新洲区</a><a href="//xiushantujiazumi.meituan.com"
                                                                                class="link city ">秀山土家族苗族自治县</a><a
                    href="//xinye.meituan.com" class="link city ">新野</a><a href="//xianyouxian.meituan.com"
                                                                           class="link city ">仙游县</a><a
                    href="//xinjinxian.meituan.com" class="link city ">新津县</a><a href="//xiajin.meituan.com"
                                                                                 class="link city ">夏津</a><a
                    href="//xinzhushi.meituan.com" class="link city ">新竹市</a><a href="//xinbei.meituan.com"
                                                                                class="link city ">新北</a><a
                    href="//xitang.meituan.com" class="link city ">西塘</a><a href="//xgll.meituan.com"
                                                                            class="link city ">香格里拉</a></span></div>
            <div class="city-area" id="city-Y"><span class="city-label">Y</span><span class="cities"><a
                    href="//yt.meituan.com" class="link city ">烟台</a><a href="//yz.meituan.com"
                                                                        class="link city ">扬州</a><a
                    href="//yinchuan.meituan.com" class="link city ">银川</a><a href="//yancheng.meituan.com"
                                                                              class="link city ">盐城</a><a
                    href="//yy.meituan.com" class="link city ">岳阳</a><a href="//yc.meituan.com"
                                                                        class="link city ">宜昌</a><a
                    href="//yk.meituan.com" class="link city ">营口</a><a href="//yichun.meituan.com" class="link city ">宜春</a><a
                    href="//yj.meituan.com" class="link city ">阳江</a><a href="//yuncheng.meituan.com"
                                                                        class="link city ">运城</a><a
                    href="//yb.meituan.com" class="link city ">宜宾</a><a href="//yl.meituan.com"
                                                                        class="link city ">榆林</a><a
                    href="//yiyang.meituan.com" class="link city ">益阳</a><a href="//yiwu.meituan.com"
                                                                            class="link city ">义乌</a><a
                    href="//yixing.meituan.com" class="link city ">宜兴</a><a href="//yuyao.meituan.com"
                                                                            class="link city ">余姚</a><a
                    href="//yueqing.meituan.com" class="link city ">乐清</a><a href="//yulin.meituan.com"
                                                                             class="link city ">玉林</a><a
                    href="//yongzhou.meituan.com" class="link city ">永州</a><a href="//yongchuan.meituan.com"
                                                                              class="link city ">永川</a><a
                    href="//yf.meituan.com" class="link city ">云浮</a><a href="//yanzhou.meituan.com" class="link city ">兖州</a><a
                    href="//yingtan.meituan.com" class="link city ">鹰潭</a><a href="//yongkang.meituan.com"
                                                                             class="link city ">永康</a><a
                    href="//yanbian.meituan.com" class="link city ">延边</a><a href="//yq.meituan.com" class="link city ">阳泉</a><a
                    href="//yd.meituan.com" class="link city ">英德</a><a href="//yizheng.meituan.com" class="link city ">仪征</a><a
                    href="//yongcheng.meituan.com" class="link city ">永城</a><a href="//yuzhou.meituan.com"
                                                                               class="link city ">禹州</a><a
                    href="//yn.meituan.com" class="link city ">伊宁</a><a href="//yanan.meituan.com"
                                                                        class="link city ">延安</a><a
                    href="//yx.meituan.com" class="link city ">玉溪</a><a href="//yichuan.meituan.com" class="link city ">伊川</a><a
                    href="//yuxian.meituan.com" class="link city ">盂县</a><a href="//yanshi.meituan.com"
                                                                            class="link city ">偃师</a><a
                    href="//yangzhong.meituan.com" class="link city ">扬中</a><a href="//yiliangxian.meituan.com"
                                                                               class="link city ">宜良县</a><a
                    href="//yongji.meituan.com" class="link city ">永济</a><a href="//yucheng.meituan.com"
                                                                            class="link city ">禹城</a><a
                    href="//yongjiaxian.meituan.com" class="link city ">永嘉县</a><a href="//yangshuo.meituan.com"
                                                                                  class="link city ">阳朔</a><a
                    href="//yicheng.meituan.com" class="link city ">宜城</a><a href="//yp.meituan.com" class="link city ">原平</a><a
                    href="//yutianxian.meituan.com" class="link city ">玉田县</a><a href="//yuanjiang.meituan.com"
                                                                                 class="link city ">沅江</a><a
                    href="//yh.meituan.com" class="link city ">玉环市</a><a href="//yimashi.meituan.com"
                                                                         class="link city ">义马市</a><a
                    href="//ya.meituan.com" class="link city ">雅安</a><a href="//yongnian.meituan.com"
                                                                        class="link city ">永年</a><a
                    href="//yangcheng.meituan.com" class="link city ">阳城</a><a href="//yunyang.meituan.com"
                                                                               class="link city ">云阳</a><a
                    href="//yexian.meituan.com" class="link city ">叶县</a><a href="//yixian.meituan.com"
                                                                            class="link city ">易县</a><a
                    href="//yiyangyy.meituan.com" class="link city ">宜阳</a><a href="//yanliang.meituan.com"
                                                                              class="link city ">阎良</a><a
                    href="//yuanyang.meituan.com" class="link city ">原阳</a><a href="//yuchengxian.meituan.com"
                                                                              class="link city ">虞城</a><a
                    href="//yushan.meituan.com" class="link city ">玉山</a><a href="//yanggu.meituan.com"
                                                                            class="link city ">阳谷</a><a
                    href="//yunchengxian.meituan.com" class="link city ">郓城</a><a href="//yjhlq.meituan.com"
                                                                                  class="link city ">伊金霍洛旗</a><a
                    href="//yangling.meituan.com" class="link city ">杨凌</a><a href="//yishui.meituan.com"
                                                                              class="link city ">沂水</a><a
                    href="//yinan.meituan.com" class="link city ">沂南</a><a href="//yudu.meituan.com" class="link city ">于都</a><a
                    href="//yifeng.meituan.com" class="link city ">宜丰</a><a href="//yingshanxian.meituan.com"
                                                                            class="link city ">营山县</a><a
                    href="//yongan.meituan.com" class="link city ">永安</a><a href="//yanling.meituan.com"
                                                                            class="link city ">鄢陵</a><a
                    href="//yongfeng.meituan.com" class="link city ">永丰</a><a href="//yongxin.meituan.com"
                                                                              class="link city ">永新</a><a
                    href="//yongxingxian.meituan.com" class="link city ">永兴县</a><a href="//youxian.meituan.com"
                                                                                   class="link city ">攸县</a><a
                    href="//yongshunxian.meituan.com" class="link city ">永顺县</a><a href="//yuminxian.meituan.com"
                                                                                   class="link city ">裕民县</a><a
                    href="//youyangtujiazumi.meituan.com" class="link city ">酉阳土家族苗族自治县</a><a
                    href="//yingxian.meituan.com" class="link city ">应县</a><a href="//yangshanxian.meituan.com"
                                                                              class="link city ">阳山县</a><a
                    href="//yushushi.meituan.com" class="link city ">榆树市</a><a href="//yuanlingxian.meituan.com"
                                                                               class="link city ">沅陵县</a><a
                    href="//yongdengxian.meituan.com" class="link city ">永登县</a><a href="//yutaixian.meituan.com"
                                                                                   class="link city ">鱼台县</a><a
                    href="//yizhoushi.meituan.com" class="link city ">宜州区</a><a href="//yidu.meituan.com"
                                                                                class="link city ">宜都</a><a
                    href="//yilan.meituan.com" class="link city ">宜兰</a><a href="//yili.meituan.com" class="link city ">伊犁</a><a
                    href="//ys.meituan.com" class="link city ">玉树</a><a href="//yich.meituan.com"
                                                                        class="link city ">伊春</a></span></div>
            <div class="city-area" id="city-Z"><span class="city-label">Z</span><span class="cities"><a
                    href="//zz.meituan.com" class="link city ">郑州</a><a href="//zb.meituan.com"
                                                                        class="link city ">淄博</a><a
                    href="//zs.meituan.com" class="link city ">中山</a><a href="//zhanjiang.meituan.com"
                                                                        class="link city ">湛江</a><a
                    href="//zj.meituan.com" class="link city ">镇江</a><a href="//zhuzhou.meituan.com" class="link city ">株洲</a><a
                    href="//zh.meituan.com" class="link city ">珠海</a><a href="//zaozhuang.meituan.com"
                                                                        class="link city ">枣庄</a><a
                    href="//zhangzhou.meituan.com" class="link city ">漳州</a><a href="//zmd.meituan.com"
                                                                               class="link city ">驻马店</a><a
                    href="//zhoushan.meituan.com" class="link city ">舟山</a><a href="//zjk.meituan.com"
                                                                              class="link city ">张家口</a><a
                    href="//zq.meituan.com" class="link city ">肇庆</a><a href="//zunyi.meituan.com"
                                                                        class="link city ">遵义</a><a
                    href="//zjg.meituan.com" class="link city ">张家港</a><a href="//zhuji.meituan.com" class="link city ">诸暨</a><a
                    href="//zk.meituan.com" class="link city ">周口</a><a href="//zhucheng.meituan.com"
                                                                        class="link city ">诸城</a><a
                    href="//zt.meituan.com" class="link city ">昭通</a><a href="//zhangye.meituan.com" class="link city ">张掖</a><a
                    href="//zoucheng.meituan.com" class="link city ">邹城</a><a href="//zjj.meituan.com"
                                                                              class="link city ">张家界</a><a
                    href="//zhuozhou.meituan.com" class="link city ">涿州</a><a href="//zhangqiu.meituan.com"
                                                                              class="link city ">章丘区</a><a
                    href="//zg.meituan.com" class="link city ">自贡</a><a href="//zaoyang.meituan.com" class="link city ">枣阳</a><a
                    href="//zunhua.meituan.com" class="link city ">遵化</a><a href="//zy.meituan.com" class="link city ">资阳</a><a
                    href="//zhuanghe.meituan.com" class="link city ">庄河</a><a href="//zhaoyuan.meituan.com"
                                                                              class="link city ">招远</a><a
                    href="//zhungeerqi.meituan.com" class="link city ">准格尔旗</a><a href="//zp.meituan.com"
                                                                                  class="link city ">邹平</a><a
                    href="//zhenxiongxian.meituan.com" class="link city ">镇雄县</a><a href="//zhijiang.meituan.com"
                                                                                    class="link city ">枝江</a><a
                    href="//zhangpu.meituan.com" class="link city ">漳浦</a><a href="//zhangshu.meituan.com"
                                                                             class="link city ">樟树</a><a
                    href="//zhongjiangxian.meituan.com" class="link city ">中江县</a><a href="//zhengding.meituan.com"
                                                                                     class="link city ">正定</a><a
                    href="//zhongmou.meituan.com" class="link city ">中牟</a><a href="//zw.meituan.com"
                                                                              class="link city ">中卫</a><a
                    href="//zhaoxian.meituan.com" class="link city ">赵县</a><a href="//zhecheng.meituan.com"
                                                                              class="link city ">柘城</a><a
                    href="//zx.meituan.com" class="link city ">钟祥</a><a href="//zhouzhi.meituan.com" class="link city ">周至</a><a
                    href="//zhijiangtongzu.meituan.com" class="link city ">芷江</a><a href="//zhijin.meituan.com"
                                                                                    class="link city ">织金</a><a
                    href="//zhangping.meituan.com" class="link city ">漳平</a><a href="//zixingshi.meituan.com"
                                                                               class="link city ">资兴市</a><a
                    href="//zhalantunshi.meituan.com" class="link city ">扎兰屯市</a><a href="//zhongxian.meituan.com"
                                                                                    class="link city ">忠县</a><a
                    href="//zherong.meituan.com" class="link city ">柘荣</a><a href="//zhongningxian.meituan.com"
                                                                             class="link city ">中宁县</a><a
                    href="//zhanghua.meituan.com" class="link city ">彰化</a><a href="//zhouzhuang.meituan.com"
                                                                              class="link city ">周庄</a></span></div>
        </div>
    </div>
</div>

</body>
</html>

'''

result = re.findall('href="(.*?)"', ll)


# print(result)


def get_url_list():
	response = requests.get('https://www.meituan.com/changecity/')
	page_sel = scrapy.Selector(text=response.text)
	result = page_sel.xpath('//*[@id="react"]//@href').extract()
	# print(result)
	return list(set(result)).remove('//bj.meituan.com')


print('返回结果', get_url_list())
