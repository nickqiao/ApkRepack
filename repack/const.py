#!/usr/bin/env python
# encoding: utf-8
import os
import tempfile


# 配置java环境变量,这个是本机的jarsigner文件位置
java_home_sign = '/Library/Java/JavaVirtualMachines/jdk1.8.0_112.jdk/Contents/Home/bin/jarsigner'

# 重新打包的apk输出路径
outputdir = "/Users/nick/Desktop/H5output"
outputapk = "/Users/nick/Desktop/H5output/new.apk"
new_icon_name = 'game_reicon'

# 需要配置签名的参数
keystore = u''
storealias = u''
storepass = u''

# 反编译过程中用到的路径
cache_dir = tempfile.gettempdir()
# os.path.join() may not handle unicode well
repack_dir = cache_dir + os.sep + 'repack'
repack_dir_apk = repack_dir + os.sep + 'source'   # 源文件位置
repack_dir_unpack = repack_dir + os.sep + 'unpack'  # unzip解压位置

# aar文件解压之后的位置
repack_dir_aar = repack_dir + os.sep + 'aar'
repack_dir_aar_libs = repack_dir_aar + os.sep + 'libs'
repack_dir_aar_dex = repack_dir_aar + os.sep + 'dex'
repack_dir_aar_smali = repack_dir_aar + os.sep + 'smali'
repack_dir_aar_res = repack_dir_aar + os.sep + 'res'
repack_dir_aar_jni = repack_dir_aar + os.sep + 'jni'
repack_dir_aar_assets = repack_dir_aar + os.sep + 'assets'

# apk经过apktool反编译之后的各个文件位置
repack_dir_apktool = repack_dir + os.sep + "apktool"  # 经过apktool反编译后的文件位置
androidmenifest_xml = repack_dir_apktool + os.sep + "AndroidManifest.xml"
lib_dir = repack_dir_apktool + os.sep + 'lib'
smali_dir = repack_dir_apktool + os.sep + 'smali'
assets_dir = repack_dir_apktool + os.sep + 'assets'
res_dir = repack_dir_apktool + os.sep + 'res'
string_xml = res_dir + os.sep + 'values' + os.sep + 'strings.xml'
xxhdpi_dir = res_dir + os.sep + 'drawable-xxhdpi-v4'
xhdpi_dir = res_dir + os.sep + 'drawable-xhdpi-v4'
hdpi_dir = res_dir + os.sep + 'drawable-hdpi-v4'



