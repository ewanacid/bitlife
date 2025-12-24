[app]
title = BitLife Phoenix
package.name = bitlifegen3
package.domain = org.nfg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 3.5
# CRITICAL: kivymd and pillow are required for the UI to render
requirements = python3,kivy==2.2.0,kivymd,pillow,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.presplash_color = #000000
[buildozer]
log_level = 2
warn_on_root = 1
