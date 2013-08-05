var LiveRefresh = function(options){

	var defaults = {
		debug: false,
		debug_level: 0,
		notification_timeout: 10,
		port: 9999
	};
	
	// Process overrides
	this.options = options?options:{};
	for(key in defaults){
		if(this.options[key] == undefined){
			this.options[key] = defaults[key];
		}
	}

	// Initialize
	this.init();

}
LiveRefresh.prototype = {
	
	init: function() {
		var websocket = new WebSocket("ws://"+window.location.hostname+":"+this.options['port']);

		var self = this;
		websocket.onopen = function(event){ LiveRefresh.prototype.on_open.call(self,event); }
		websocket.onmessage = function(event){ LiveRefresh.prototype.on_message.call(self,event); }

		this.timer_el = null;
		this.refresh_date = new Date().getTime();
		this.add_timer();
		this.timer_interval = setInterval( function(){
			LiveRefresh.prototype.update_timer.call(self)
		},100);

	},
	add_timer: function(){
		document.write("<div id=\"liverefresh_timer\" style=\"position:absolute;font-size:10px;width:120px;text-align:center;top:10px;right:10px;background-color:#4A93DE;padding:10px;\"></div>")
		this.timer_el = document.getElementById("liverefresh_timer")
	},
	update_timer: function(){
		enlapsed = ((new Date().getTime() - this.refresh_date)/1000).toFixed(1);
		this.timer_el.innerHTML="Refreshed " + enlapsed + "s ago";
		this.timer_el.style.opacity= (this.options.notification_timeout-enlapsed)/this.options.notification_timeout
		if(enlapsed > this.options.notification_timeout){
			this.timer_el.parentNode.removeChild(this.timer_el)
			window.clearInterval(this.timer_interval)
		}
	},
	on_open: function(event){
		this.debug("Websocket opened")
	},
	on_message: function(event){
		this.debug("Message received: " + event.data)
		if(event.data == "refresh"){
			location.reload();
		}
	},
	debug: function(){
		if(this.options['debug'] && window.console){
			if(arguments.length == 1 || (arguments.length >= 1 && arguments[1] <= this.options['debug_level'])){
				console.log(arguments[0])
			}
		}
	}
}