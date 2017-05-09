#!/usr/bin/env python
# encoding: utf-8
import os
import shutil
import xml.etree.ElementTree as EleTree

import datetime

from repack import const
from repack import utils


def log(text=''):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator


class AndroidManifest(object):

    namespace = '{http://schemas.android.com/apk/res/android}'

    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = EleTree.parse(filepath)
        self.root = self.tree.getroot()

    @log('')
    def change_app(self, packagename=None, icon=None, appname=None, support_flash=True):
        if packagename is not None:
            self.root.attrib['package'] = packagename
            self.tree.write(self.filepath)
        for elem in self.root.iterfind('application'):
            if icon is not None:
                elem.attrib[self.namespace + 'icon'] = icon
            if appname is not None:
                elem.attrib[self.namespace + 'label'] = appname
            if not support_flash:
                for subelem in elem.iterfind('meta-data'):
                    if subelem.attrib[self.namespace + 'name'] == 'YYSDK_FLASH_SWITCH':
                        subelem.attrib[self.namespace + 'value'] = 'false'
            self.tree.write(self.filepath, encoding='utf-8', xml_declaration=True)


class Apk(object):

    def __init__(self, strings=None, xxhdpi=None, xhdpi=None, hdpi=None):
        """四个参数均是字典类型"""
        if strings is None:
            strings = {}
        if xxhdpi is None:
            xxhdpi = {}
        if xhdpi is None:
            xhdpi = {}
        if hdpi is None:
            hdpi = {}
        self.__strings = strings
        self.__xxhdpi = xxhdpi
        self.__xhdpi = xhdpi
        self.__hdpi = hdpi

    @staticmethod
    def repack(inputapk,
               inputaar=None,
               appname=None,
               iconname=None,
               iconpath=None,
               support_falsh=True,
               packagename=None,
               outputapk=const.outputapk):
        """ inputapk 要反编译的apk文件
            appname  重新打包后app名称
            iconname app图标在manifest文件中的名称(例如@drawable/game_reicon 或者 @mipmap/game_reicon)
            iconpath 新的app图标的存放位置
            supprot_flash 是否支持闪屏
            outputapk 重新打包后的apk文件"""

        Apk.prepare(inputapk)
        Apk.apktool_d(inputapk, const.repack_dir_apktool)

        # if inputaar is not None:
        #     utils.un_zip(inputaar, const.repack_dir_aar)
        #     if not os.path.exists(const.repack_dir_aar_libs):
        #         os.makedirs(const.repack_dir_aar_libs)
        #     if not os.path.exists(const.repack_dir_aar_dex):
        #         os.makedirs(const.repack_dir_aar_dex)
        #     if not os.path.exists(const.repack_dir_aar_smali):
        #         os.makedirs(const.repack_dir_aar_smali)
        #     shutil.copy(const.repack_dir_aar + os.sep + 'classes.jar', const.repack_dir_aar + os.sep + 'libs')
        #     for root, dirs, files in os.walk(const.repack_dir_aar_libs):
        #         for jarfile in files:
        #             if jarfile.endswith('.jar'):
        #                 temp_dex_name = const.repack_dir_aar_dex + os.sep + utils.get_file_name(jarfile) + '.dex'
        #                 Apk.jartodex(root + os.sep + jarfile, temp_dex_name)
        #                 Apk.dextosmali(temp_dex_name, const.repack_dir_aar_smali)

        # utils.xcopy(const.repack_dir_aar_smali, const.smali_dir)
        # print "d"
        # utils.xcopy(const.repack_dir_aar_res, const.res_dir)
        # utils.xcopy(const.repack_dir_aar_jni, const.lib_dir)
        # utils.xcopy(const.repack_dir_aar_assets, const.assets_dir)

        AndroidManifest(const.androidmenifest_xml).change_app(packagename, iconname, appname, support_falsh)
        if os.path.exists(iconpath):
            if not os.path.exists(const.xhdpi_dir):
                os.makedirs(const.xhdpi_dir)
            shutil.copy(iconpath, const.xhdpi_dir + os.sep + const.new_icon_name)

        Apk.apktool_b(const.repack_dir_apktool, outputapk)
        Apk.del_meta_inf(outputapk)
        Apk.sign(outputapk)
        apk = Apk.rename(outputapk)
        Apk.move(apk, const.outputdir)

    @staticmethod
    @log("准备文件夹")
    def prepare(apk):
        if not os.path.exists(const.repack_dir):
            os.makedirs(const.repack_dir)
        Apk.mkdir(const.repack_dir_apk)
        Apk.mkdir(const.repack_dir_aar)
        shutil.copy(apk, const.repack_dir_apk)
        return

    @staticmethod
    @log('反编译')
    def apktool_d(apk, output):
        utils.del_path(const.repack_dir_apktool)
        utils.execute_command("apktool d " + apk + " -o " + output)

    @staticmethod
    @log('回编译')
    def apktool_b(recompiledir, output):
        utils.execute_command("apktool b " + recompiledir + " -o " + output)

    @staticmethod
    @log('重新sign')
    def sign(apk):
        sign_cmd = "{0} -sigalg MD5withRSA -digestalg SHA1 -keystore {1} -storepass {2} {3} {4}". \
            format(const.java_home_sign,
                   const.keystore,
                   const.storepass,
                   apk,
                   const.storealias)
        utils.execute_command(sign_cmd)
        return

    @staticmethod
    @log('更改图标')
    def change_icon(iconname, iconpath, resdir):
        utils.del_path(resdir + os.sep + iconname)
        shutil.copy(iconpath, resdir)
        return

    @staticmethod
    @log('更改指定字符串')
    def change_stringxml(attrib, value, stringxml):
        tree = EleTree.parse(stringxml)
        root = tree.getroot()
        for elem in root.iter():
            if elem.attrib == attrib:
                elem.text = value
                break
        tree.write(stringxml)
        return

    @staticmethod
    @log('删除meta_inf')
    def del_meta_inf(apk):
        utils.un_zip(apk, const.repack_dir_unpack)
        utils.del_path(const.repack_dir_unpack + os.sep + "META-INF")
        utils.make_zip(const.repack_dir_unpack + os.sep, const.outputapk)
        return

    @staticmethod
    def move(apk, des):
        if not os.path.exists(des):
            os.makedirs(des)
        shutil.move(apk, des)
        return

    @staticmethod
    def rename(apk):
        newname = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".apk"
        os.rename(apk, newname)
        return newname

    @staticmethod
    def mkdir(directory):
        if os.path.exists(directory):
            utils.del_path(directory)
        os.mkdir(directory)

    @staticmethod
    @log("jar to dex")
    def jartodex(jarfile, output):
        cmd = 'java -jar ' + os.getcwd() + os.sep + 'dx.jar --dex --output=' + output + " " + jarfile
        utils.execute_command(cmd)

    @staticmethod
    @log("dex to smali")
    def dextosmali(dexfile, output):
        cmd = 'java -jar ' + os.getcwd() + os.sep + 'baksmali-2.2b4.jar d ' + dexfile + " -o " + output
        utils.execute_command(cmd)

if __name__ == '__main__':
    a = Apk()
    a.repack('/Users/nick/Desktop/H5pack/720001_yy.apk',
             '/Users/nick/Desktop/H5pack/yyplaysdklib-debug.aar',
             u'我的世界',
             '@drawable/' + const.new_icon_name,
             '/Users/nick/PycharmProjects/AndroidPack/src/res/game_reicon.png')
