Live Refresh
============

Live Refresh is a [Sublime Text 3](http://www.sublimetext.com/3) plugin that automatically refreshes websites after a file is saved.

Installation
------------

1. Using Sublime [Package Control](http://wbond.net/sublime_packages/package_control/installation) *this doesn't work yet*:

  * Press `ctrl+shift+p`(Windows, Linux) or `cmd+shift+p`(OS X).
  * Type install, then press enter with Package Control: Install Package selected.
  * Type Live Refresh, then press enter with the Live Refresh plugin selected.

2. Add the following code to the website you want to refresh:

```html
<script type="text/javascript" src="js/liverefresh.js"></script>
<script> LiveRefresh() </script>
```
