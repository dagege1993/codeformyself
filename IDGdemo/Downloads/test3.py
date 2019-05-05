response_test = """
orgame : "1",
	apkName : "com.tencent.mobileqq",
	apkCode : "980",
	appId : "6633",
	appName: "QQ",
	iconUrl:"https://pp.myapp.com/ma_icon/0/icon_6633_1545382196/96",
	appScore:"",
	downTimes:"8699114395",
	downUrl:"https://imtt.dd.qq.com/16891/B82FD7E2F759060B05E2D486364BE1D0.apk?fsname=com.tencent.mobileqq_7.9.5_980.apk&csr=1bbd",
	tipsUpDown:"false"

"""
import re

result = re.findall('downTimes:"(\d+)",', response_test)
print(result.pop())
