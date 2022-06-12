#!/usr/bin/env python
#
# This scritps to compile rk3399-roc-pc kernel-5.17
#
# Author:  Robin.J
# Date:    2019-11-18


import os
import os.path
import sys
import time
import logging

logger = logging.getLogger(__name__)

def help():
    print("Please input ./build.py [param]:")
    print("[param]:")
    print("         [build_uboot]: full compile kernel.")
    print("         [clean]: make clean.")

def set_env():
    """Set Build enviroment.

    """
    arch = os.popen("echo $ARCH")
    arch_value = arch.read()
    print("Current ARCH = " + '\033[1;32m' + arch_value + '\033[0m')
    arch.close()
    cross_comp = os.popen("echo $CROSS_COMPILE")
    cross_comp_value = cross_comp.read()
    print("Current CROSS_COMPILE = " + '\033[1;32m' +cross_comp_value + '\033[0m')
    cross_comp.close()
    if arch_value == "" and cross_comp_value == "":
        os.system("chmod a+x setenv.sh")
        os.system("source setenv.sh")
    elif arch_value == "arm64" or cross_comp_value == "aarch64-linux-gnu-":
        sys.exit(1)

def build_uboot(command_one):
    """build uboot

       rk3399-roc-pc
    """
    if "build_uboot" == command_one:
        os.system("make roc-rk3399-pc_defconfig")
        print("===============" + '\033[1;33m' + "Start Build Uboot" + '\033[0m' + "===============")
        ret = os.system("make -j32  2>&1 | tee build.log")
        #./make.sh trust
        #./make.sh uboot
        #./make.sh loader
        ret = os.system("./make.sh trust")
        ret = os.system("./make.sh uboot")
        ret = os.system("./make.sh loader")
        if ret == 0:
            print("Compile Finished !!!")
        print("===============" + '\033[1;33m' + "End Build Uboot" + '\033[0m' + "===============")
    elif "clean" == command_one:
        finish_1 = os.system("make clean")
        finish_2 = os.system("make mrproper")
        if finish_1 == 0 and finish_2 == 0:
            print("Clean Finish !!!")
    else:
        logger.error("Unknown command  name %s", command_one)
        sys.exit(1)


def main(argv):
    if len(argv) != 1:
        help()
        sys.exit(1)
    set_env()
    build_uboot(argv[0])


if __name__ == '__main__':
        main(sys.argv[1:])
