hs.registerOverlay({
	html: '<div class="closebutton" onclick="return hs.close(this)"></div>',
	position: 'top right',
	fade: 2 // fading the semi-transparent overlay looks bad in IE
});
hs.graphicsDir = '/static/highslide/graphics/';
hs.align = 'center';
hs.showCredits = false;
hs.blockRightClick = true;
hs.dimmingOpacity = 0.5;
hs.lang.fullExpandTitle = '';
hs.lang.restoreTitle = '';
hs.lang.closeTitle = '';