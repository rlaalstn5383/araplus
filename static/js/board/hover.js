(function (a) { a.fn.hovercard = function (b) { var c = { width: 300, openOnLeft: false, openOnTop: false, cardImgSrc: "", detailsHTML: "", showCustomCard: false, customCardJSON: {}, customDataUrl: "", background: "#ffffff", delay: 0, autoAdjust: true, onHoverIn: function () { }, onHoverOut: function () { } }; var b = a.extend(c, b); if (a("#css-hovercard").length <= 0) { var d = '<style id="css-hovercard" type="text/css">' + ".hc-preview { position: relative; display:inline; }" + ".hc-name { font-weight:bold; position:relative; display:inline-block; }" + ".hc-details { left:-10px; margin-right:80px; text-align:left; font-family:Sans-serif !important; font-size:12px !important; color:#666 !important; line-height:1.5em; border:solid 1px #ddd; position:absolute;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;top:-10px;padding:2em 10px 10px;-moz-box-shadow:5px 5px 5px #888;-webkit-box-shadow:5px 5px 5px #888;box-shadow:5px 5px 5px #888;display:none;}" + ".hc-pic { width:70px; margin-top:-1em; float:right;  }" + ".hc-details-open-left { left: auto; right:-10px; text-align:right; margin-left:80px; margin-right:0; } " + ".hc-details-open-left > .hc-pic { float:left; } " + ".hc-details-open-top { bottom:-10px; top:auto; padding: 10px 10px 2em;} " + ".hc-details-open-top > .hc-pic { margin-top:10px; float:right;  }" + ".hc-details .s-action{ position: absolute; top:8px; right:5px; } " + ".hc-details .s-card-pad{ border-top: solid 1px #eee; margin-top:10px; padding-top:10px; overflow:hidden; } " + ".hc-details-open-top .s-card-pad { border:none; border-bottom: solid 1px #eee; margin-top:0;padding-top:0; margin-bottom:10px;padding-bottom:10px; }" + ".hc-details .s-card .s-strong{ font-weight:bold; color: #555; } " + ".hc-details .s-img{ float: left; margin-right: 10px; max-width: 70px;} " + ".hc-details .s-name{ color:#222; font-weight:bold;} " + ".hc-details .s-loc{ float:left;}" + ".hc-details-open-left .s-loc{ float:right;} " + ".hc-details .s-href{ clear:both; float:left;} " + ".hc-details .s-desc{ float:left; font-family: Georgia; font-style: italic; margin-top:5px;width:100%;} " + ".hc-details .s-username{ text-decoration:none;} " + ".hc-details .s-stats { display:block; float:left; margin-top:5px; clear:both; padding:0px;}" + ".hc-details ul.s-stats li{ list-style:none; float:left; display:block; padding:0px 10px !important; border-left:solid 1px #eaeaea;} " + ".hc-details ul.s-stats li:first-child{ border:none; padding-left:0 !important;} " + ".hc-details .s-count { font-weight: bold;} " + '.</style>")'; a(d).appendTo("head") } return this.each(function () { function g(c, d, e, g) { var h, i, j, k, l; switch (c) { case "custom": { i = d, h = function (a) { return '<div class="s-card s-card-pad">' + (a.image ? '<img class="s-img" src=' + a.image + " />" : "") + (a.name ? '<label class="s-name">' + a.name + " </label><br/>" : "") + (a.link ? '<a class="s-loc" href="' + a.link + '">' + a.link + "</a><br/>" : "") + (a.bio ? '<p class="s-desc">' + a.bio + "</p>" : "") + (a.website ? '<p class="s-desc"><span class="s-strong">Web:</span><br/><a href="' + a.website + '">' + a.website + "</a></p>" : "") + (a.email ? '<p class="s-desc"><span class="s-strong">Email:</span><br/><a href="' + a.email + '">' + a.email + "</a></p>" : "") + "</div>" }; k = "Loading..."; l = "Sorry, no data found."; j = function () { } } break; default: { } break } if (a.isEmptyObject(g)) { a.ajax({ url: i, type: "GET", dataType: "jsonp", timeout: 4e3, beforeSend: function () { e.find(".s-message").remove(); e.append('<p class="s-message">' + k + "</p>") }, success: function (a) { if (a.length <= 0) { e.find(".s-message").html(l) } else { e.find(".s-message").remove(); e.prepend(h(a)); f(e.closest(".hc-preview")); e.stop(true, true).delay(b.delay).fadeIn(); j(a) } }, error: function (a, b, c) { e.find(".s-message").html(l) } }) } else { e.prepend(h(g)) } } function f(a) { var c = a.find(".hc-details").eq(0); var d = a[0].getBoundingClientRect(); var e = d.top - 20; var f = d.left + 35 + c.width(); var g = d.top + 35 + c.height(); var h = d.top - 10; if (b.openOnLeft || b.autoAdjust && f > window.innerWidth) { c.addClass("hc-details-open-left") } else { c.removeClass("hc-details-open-left") } if (b.openOnTop || b.autoAdjust && g > window.innerHeight) { c.addClass("hc-details-open-top") } else { c.removeClass("hc-details-open-top") } } var c = a(this); c.wrap('<div class="hc-preview" />'); c.addClass("hc-name"); var d = ""; if (b.cardImgSrc.length > 0) { d = '<img class="hc-pic" src="' + b.cardImgSrc + '" />' } var e = '<div class="hc-details" >' + d + b.detailsHTML + "</div>"; c.after(e); c.siblings(".hc-details").eq(0).css({ width: b.width, background: b.background }); c.closest(".hc-preview").hover(function () { var d = a(this); f(d); d.css("zIndex", "200"); c.css("zIndex", "100").find(".hc-details").css("zIndex", "50"); var e = d.find(".hc-details").eq(0); e.stop(true, true).delay(b.delay).fadeIn(); if (typeof b.onHoverIn == "function") { if (b.showCustomCard && e.find(".s-card").length <= 0) { var h = b.customDataUrl; if (typeof c.attr("data-hovercard") == "undefined") { } else if (c.attr("data-hovercard").length > 0) { h = c.attr("data-hovercard") } g("custom", h, e, b.customCardJSON) } b.onHoverIn.call(this) } }, function () { $this = a(this); $this.find(".hc-details").eq(0).stop(true, true).fadeOut(300, function () { $this.css("zIndex", "0"); c.css("zIndex", "0").find(".hc-details").css("zIndex", "0"); if (typeof b.onHoverOut == "function") { b.onHoverOut.call(this) } }) }); }) } })(jQuery)