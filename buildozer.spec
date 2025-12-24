[app]
title = BitLife 3000
package.name = bitlife3000
package.domain = org.nfg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 30.0.0
# CRITICAL: Added plyer for vibration, pillow for images
requirements = python3,kivy==2.2.0,kivymd,pillow,android,plyer
orientation = portrait
fullscreen = 0
# CRITICAL: Permissions for vibration and storage
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,VIBRATE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.presplash_color = #000000
[buildozer]
log_level = 2
warn_on_root = 1
