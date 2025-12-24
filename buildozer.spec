[app]
title = NFG Elite
package.name = nfgelite
package.domain = org.nfg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 4.0
requirements = python3,kivy==2.2.0,kivymd,pillow,android

orientation = portrait
fullscreen = 1
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.presplash_color = #000000

[buildozer]
log_level = 2
warn_on_root = 1
