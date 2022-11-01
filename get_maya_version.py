#coding=utf-8
import sys, os

if (int(sys.version_info.major)) == 2:
    import _winreg as winreg
elif (int(sys.version_info.major)) == 3:
    import winreg

def get_maya_ver():
    subDir = r'SOFTWARE\Autodesk\Maya'
    regRoot = winreg.HKEY_LOCAL_MACHINE
    keyHandle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subDir)
    count = winreg.QueryInfoKey(keyHandle)[0]
    result = []
    for i in range(count):

        subKeyName = winreg.EnumKey(keyHandle, i)
        subDir_2 = r'%s\%s' % (subDir, subKeyName)
        # print(subDir_2)
        keyHandle_2 = winreg.OpenKey(regRoot, subDir_2)
        count2 = winreg.QueryInfoKey(keyHandle_2)[1]
        result2 = []
        for j in range(count2):
            name, value, type = winreg.EnumValue(keyHandle_2, j)
            if name == "UpdateVersion":
                result2.append(u"maya{}".format(value))
                # print(name, value, type) # 打印[0]是判断上面对应的名称，[1]目前的文件夹，[2]下面的子项1代表有0代表没
                _string = 'SOFTWARE\Autodesk\Maya\%s\Setup\InstallPath' % value
                # print(_string)# 打印出新的注册表路径
                handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _string)
                location, type = winreg.QueryValueEx(handle, "MAYA_INSTALL_LOCATION")# 获取相对应的地址和类型
                # print(location)# 打印出maya程序的目录地址
                result2.append(u"{}".format(location))

            if result2:
                result.append(result2)

    # print(result)
    return result