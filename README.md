Live Refresh
============

Live Refresh is a [Sublime Text 2](http://www.sublimetext.com) and [3](http://www.sublimetext.com/3) plugin that automatically refreshes websites after a file is saved.

Installation
------------

1. Using Sublime [Package Control](http://wbond.net/sublime_packages/package_control/installation) __*this doesn't work yet*__:

  a) Press `ctrl+shift+p`(Windows, Linux) or `cmd+shift+p`(OS X).
  
  b) Type install, then press enter with Package Control: Install Package selected.
  
  c) Type Live Refresh, then press enter with the Live Refresh plugin selected.

2. Add the following code to the website you want to refresh:
```html
<script type="text/javascript" src="js/liverefresh.js"></script>
<script> LiveRefresh() </script>
```

Settings
--------

Its important to note that for the plugin to work correctly, the port setting has to match in both the Sublime Text plugin settings, and in the JavaScript settings.

### JavaScript

The default options are:
```javascript
var defaults = {
 	debug: false,
		debug_level: 0,
		notification_timeout: 10,
		port: 9999
	};
```

The can be overriden by calling the constructor with a literal object like this:

```javascript
LiveRefresh({debug: true,debug_level: 1,port: 8081});
```

### Sublime Text Plugin

The plugin configuration can be found in the file `LiveRefresh.sublime-settings`

TODO
----

* Add filters for multiple websites being editted at the same time
* Add compiler support for generated files (less)





