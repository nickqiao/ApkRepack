#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import zipfile

from src import const

import subprocess
import shlex
import datetime
import time


def execute_command(cmdstring, cwd=None, timeout=None, shell=False):

    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096)

    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)

    return str(sub.returncode)


def sign(apkpath):
    sign_cmd = "{0} -sigalg MD5withRSA -digestalg SHA1 -keystore {1} -storepass {2} {3} {4}".\
        format('/Library/Java/JavaVirtualMachines/jdk1.8.0_112.jdk/Contents/Home/bin/jarsigner',
               const.keystore,
               const.storepass,
               apkpath,
               const.storealias)
    execute_command(sign_cmd)
    return


def del_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        pass
    return


def un_zip(file_name, des):
    z_file = zipfile.ZipFile(file_name)
    if os.path.isdir(des):
        pass
    else:
        os.mkdir(des)
    for names in z_file.namelist():
        z_file.extract(names, des)
    z_file.close()


def add_zip(add, zfile):
    f = zipfile.ZipFile(zfile, 'w', zipfile.ZIP_DEFLATED)
    f.write(add)
    f.close()


def zip_file(srcdir, zfilename):
    f = zipfile.ZipFile(zfilename, 'w', zipfile.ZIP_DEFLATED)

    for dirpath, dirnames, filenames in os.walk(srcdir):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()


def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()
    return zipf


def get_file_name(inputapk):
    name = os.path.basename(inputapk)
    return os.path.splitext(name)[0]


def xcopy(src, des):
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    if not os.path.exists(src):
        print "src dir is not exist:"
        return False
    if not os.path.exists(des):
        os.makedirs(des)
    src_file = [os.path.join(src, f) for f in os.listdir(src)]
    for source in src_file:
        if os.path.isfile(source):
            shutil.copy(source, os.path.join(des, os.path.basename(source)))
        if os.path.isdir(source):
            p, src_name = os.path.split(source)
            newdes = os.path.join(des, src_name)
            xcopy(source, newdes)
    return True
