$(function(){
    console.log("v=201706291828");
    $('#n-banner').flexslider({
        directionNav: false,
        pauseOnAction: false
    });

    var page=$("body").attr("data-page") || 0;
    switch (page){
        case "index":{
            $(document).scrollTop(0);
            $("#header").css({"position":"fixed"});
            var ulHeight = $(".footer-cooperation-list ul").height(), ultop = $(".footer-cooperation-list ul").css("margin-top");
            ultop = ultop.split("p")[0];

            var swiper = new Swiper('.swiper-container', {
                pagination: '.swiper-pagination',
                paginationClickable: true,
                direction: 'vertical',
                // 如果需要前进后退按钮
                keyboardControl: true,
                mousewheelControl: true,
                onInit: function (e) {
                    //                    $(".swiper-game .swiper-game-list li").height(Math.ceil($(".swiper-game .swiper-game-list li").width()*(43/50)));
                    //                    $(".swiper-game .swiper-game-list li img").height(Math.ceil($(".swiper-game .swiper-game-list li").width()*(43/50)));
                    $(".swiper-container").css("visibility", "visible");
                    $(".swiper-pagination").hide();
                },
                onSlideNextStart: function (e) {
                    if (e.activeIndex == 3) {
                        swiper.disableMousewheelControl();
                    }
                },
                onSlidePrevStart: function (e) {
                    swiper.enableMousewheelControl();
                },
                onSlideChangeStart: function (swiper) {
                    console.log("onSlideChangeStart");
                    if (swiper.activeIndex == 0) {
                        $(".swiper-pagination").hide();
                    } else if (swiper.activeIndex == 1) {
                        $(".swiper-pagination").show();
                    }
                },
            });

            $(document).scroll(function () {
                if ($(document).scrollTop() == 0) {
                    swiper.enableMousewheelControl();
                }
            });

            $('.flexslider').flexslider({
                animation: "slide",
                controlNav: true,
                directionNav: true
            });
            $('.share-flexslider').flexslider({
                animation: "slide",
                controlNav: true,
                directionNav: false
            });
            $(".news-left").flexslider({
                animation: "slide",
                controlNav: false,
                directionNav: true
            });

            $(".footer-cooperation-paging").on("click", ".footer-cooperation-paging-top,.footer-cooperation-paging-bottom", function (e) {
                var clickClassName = e.target.className;
                if (clickClassName == "footer-cooperation-paging-top") {
                    if (ultop != 0) {
                        $(".footer-cooperation-list ul").css({"margin-top": -(-parseInt(ultop) - 412) + "px"});
                        ultop=-(-parseInt(ultop) - 412);
                    }
                } else {
                    if (ulHeight > -parseInt(ultop) + 412) {
                        $(".footer-cooperation-list ul").css({"margin-top": -(-parseInt(ultop) + 412) + "px"})
                        ultop=-(-parseInt(ultop) + 412);
                    }
                }

            });
            break;
        }
        case "history":{
            var courseUlHeight = $(".course-swiper ul").height(),  //全部高度
                courseUltop = $(".course-swiper ul").css("margin-top").split("p")[0]; //相对高度
            $(".walk-course-main").on("click", ".footer-cooperation-paging-top,.footer-cooperation-paging-bottom", function (e) {
                var clickClassName = e.target.className;
                if (clickClassName == "footer-cooperation-paging-top") {
                    if (courseUltop != 0) {
                        $(".course-swiper ul").css({"margin-top": -(-parseInt(courseUltop) - 200) + "px"});
                        courseUltop=-(-parseInt(courseUltop) - 200);
                    }
                } else {
                    if (courseUlHeight > -parseInt(courseUltop) + 600) {
                        $(".course-swiper ul").css({"margin-top": -(-parseInt(courseUltop) + 200) + "px"})
                        courseUltop= -(-parseInt(courseUltop) + 200);
                    }
                }

            });
            break;
        }
        case "product":{
            if(typeof localStorage.clickProductId=="undefined"){ localStorage.clickProductId=",";}
            $('.game-voide-list li').click(function (event) {
                var url=$(this).find("img").attr("url"),locationurl=$(this).find("img").attr("locationurl"),video_cont="";
                var dialog_video_cont = $('<div>', {"class": "full_dialog"})
                if(locationurl==""){
                    video_cont = "<div id='dialog_video_cont'><embed name='plugin' src='"+url+"' allowFullScreen='true' quality='high' align='middle' allowScriptAccess='always' type='application/x-shockwave-flash'></embed></div>";
                }else{
                    video_cont = "<div id='dialog_video_cont'><video width='640' height='480' src="+locationurl+"'/' controls=''>您的浏览器不支持H5视频</video></div>";
                }

                var dialog_video_close_btn = $('<a>', {
                    "href": "javascript:void(0)", "html": "X", "id": "dialog_video_close_btn", "click": function (event) {
                        $('.full_dialog').remove()
                        $('#dialog_video_cont').remove()
                    }
                })
                $('body').append(dialog_video_cont).append(video_cont)
                $('#dialog_video_cont').append(dialog_video_close_btn)
            });
            $(".jp_props").on("click",function(){
                if($(this).hasClass("active")){return false; }
                var jsonObj={"catid":$(this).attr("data-catid"),"id":$(this).attr("data-id")};
                var sef=$(this);
                $.post("/index.php?m=content&c=index&f=ajaxStat" +
                    "istical", jsonObj,"","json").success(function(data){
                    if(typeof localStorage.clickProductId=="undefined"){ localStorage.clickProductId=",";}
                    sef.find(".cont-zan").html(data.zan);
                    sef.addClass("active");
                    localStorage.clickProductId+=sef.attr("data-id")+",";
                })
            });
            $(".jp_props").each(function(index){
                if(localStorage.clickProductId.indexOf(","+$(this).attr("data-id")+",") >= 0){
                    $(this).addClass("active");
                }
            });
            $('.game-voide-list li').hover(function(){
                $(this).append("<div class='img-mask'></div><div class='icon-play'></div>");
                $(this).children(".icon-play").animate({"opacity":1},50);

            },function(){
                $(this).children(".img-mask").remove();
                $(this).children(".icon-play").remove();
            });
            $.post("/index.php?m=content&c=index&f=getGameListZan",{},"","json").success(function(data){
                if(!data){ return false;}
               for(var dataKey in data){
                    $(".game-list li").find(".jp_props[data-id="+data[dataKey]["id"]+"]").find(".cont-zan").html(data[dataKey]["zan"])
               }
            });
            break;
        }
        case "life":{
            var viewSwiper = new Swiper('.view .swiper-container', {
                onSlideChangeStart: function() {
                    updateNavPosition();
                }
            })

            $('.view .arrow-left,.preview .arrow-left').on('click', function(e) {
                e.preventDefault();
                if(viewSwiper.activeIndex == 0) {
                    viewSwiper.swipeTo(viewSwiper.slides.length - 1, 1000);
                    return;
                }
                viewSwiper.swipePrev();
            })
            $('.view .arrow-right,.preview .arrow-right').on('click', function(e) {
                e.preventDefault();
                if(viewSwiper.activeIndex == viewSwiper.slides.length - 1) {
                    viewSwiper.swipeTo(0, 1000);
                    return
                }
                viewSwiper.swipeNext();
            })

            var previewSwiper = new Swiper('.preview .swiper-container', {
                visibilityFullFit: true,
                slidesPerView: 'auto',
                onlyExternal: true,
                onSlideClick: function() {
                    viewSwiper.swipeTo(previewSwiper.clickedSlideIndex);
                }
            });

            function updateNavPosition() {
                $('.preview .active-nav').removeClass('active-nav');
                var activeNav = $('.preview .swiper-slide').eq(viewSwiper.activeIndex).addClass('active-nav');
                if(!activeNav.hasClass('swiper-slide-visible')) {
                    if(activeNav.index() > previewSwiper.activeIndex) {
                        var thumbsPerNav = Math.floor(previewSwiper.width /(activeNav.width()+16)) - 1;
                        console.log(thumbsPerNav);
                        previewSwiper.swipeTo(activeNav.index() - thumbsPerNav);
                    } else {
                        previewSwiper.swipeTo(activeNav.index());
                    }
                }
            }
            break;
        }
        case "job":{
            $(".submit").on("click",function(){
                var content=$(".input-job").val();
                if(content==""){
                    alert("请填写搜索内容");
                }else{
                    location.href="/index.php?m=content&c=index&f=search&catid=41&key="+content;
                }
            })
            $(".input-job").on("keydown",function(event){
                if (event.keyCode==13){  //回车键的键值为13
                    $(".submit").trigger('click');
                }
            });
        }
    }

    function IsPC()
    {
        var userAgentInfo = navigator.userAgent;
        var Agents = new Array("Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod");
        var flag = true;
        for (var v = 0; v < Agents.length; v++) {
            if (userAgentInfo.indexOf(Agents[v]) > 0) { flag = false; break; }
        }
        return flag;
    }
});
$(function(){
	
			if (window.location.host.search('www.gzyouai.cn')>=0 || window.location.host.search('gzyouai.cn')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-8');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003001').children().text('粤公网安备 44010602003001号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003001');
			}

			else if (window.location.host.search('www.gzyouai.net')>=0 || window.location.host.search('gzyouai.net')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-9');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003002').children().text('粤公网安备 44010602003002号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003002');
			}
			else  if (window.location.host.search('www.51fytx.com')>=0 || window.location.host.search('51fytx.com')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-10');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003004').children().text('粤公网安备 44010602003004号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003004');
				
			}


			else if (window.location.host.search('www.yhzbonline.com')>=0 || window.location.host.search('yhzbonline.com')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-11');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003006').children().text('粤公网安备 44010602003006号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003006');
			}


			else if (window.location.host.search('www.fytx.cc')>=0 || window.location.host.search('fytx.cc')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-7');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003003').children().text('粤公网安备 44010602003003号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003003');
			}

			else if (window.location.host.search('game1919.com')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-3');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003007').children().text('粤公网安备 44010602003007号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003007');
			}

			 else if (window.location.host.search('game2828.com')>=0){
				$('a[href="http://www.miitbeian.gov.cn"]').children().text('粤ICP备12082062号-4');
				$('a[href^="https://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]')
				.attr('href','https://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003005').children().text('粤公网安备 44010602003005号');
				$('a[href^="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode="]').attr('href','http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44010602003005');
				
			}


});
