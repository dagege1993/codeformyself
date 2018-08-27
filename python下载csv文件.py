# coding=utf-8

from urllib import request

goog_url = 'http://kry-fintech.oss-cn-hangzhou.aliyuncs.com/citest/0020180809PM111_2877f1638a2b460fb9895c9b546be43a_810011317_JK_1_takeoutMonthlyStandard.csv?Expires=1534477520&OSSAccessKeyId=STS.NKNYVMgkkyrfVHXeSiHme72zi&Signature=UPrtPdlwJdw9UUfpVisZfUhlu1s%3D&security-token=CAISpQJ1q6Ft5B2yfSjIr4j7Euz5irRKzrCNVG7pgVM8ROJJ2PfRizz2IHxMf3FqBO8Xtfk0lW9Y6f0YlqdwUY4AQlTfKMB075lR7VsmlREGB4jng4YfgbiJREKEaXeirt2wDsz9SNTCAIDPD3nPii50x5bjaDymRCbLGJaViJlhHLt1Mw6jdmgEfu80QDFvs8gHL3DcGO%2BwOxrx%2BArqAVFvpxB3hBEji9u2ydbO7QHF3h%2BoiL0WvZW0LJmic8RnPPUOWtyujuttbfiDgmwC6AJbsal3irBJ8jeA%2FPPlWgkLsk7abLaNr4w3d1UgPJJXQfAU8KLO8tRjofHWmojNzBJAAPpYSSy3Rvr7nJOfQLn0aYdiKO2qZCSSiYqVXZ7uqBOgno%2Fk3pK9EBqAAR7KAnyy4ApL8v5oJOxUQau1IiWUUOhMwCi7bgQQgfFadCmChAF1hu1OgUa5q9EX89eQICjJENSfVT8IjEz6K8%2Bk61Q0%2BvwrFmqIztQZA%2F0XMzXOjxEX6CQ0p3FNiqb9%2F%2FekKPHRV7%2Fgt%2FdwVpOWmcDxIj%2F5pkZlD912YPqEx6en'


def download(csv_url):
	response = request.urlopen(csv_url)
	csv = response.read()
	csv = csv.decode('utf-8')
	csv_str = str(csv)
	lines = csv_str.split("\\n")
	filename = goog_url.split('?')[0].split('/')[-1]
	fw = open(filename, "w")
	for line in lines:
		fw.write(line + '\n')
	fw.close()


download(goog_url)

# goog_url = 'http://kry-fintech.oss-cn-hangzhou.aliyuncs.com/citest/0020180809PM111_2877f1638a2b460fb9895c9b546be43a_810011317_JK_1_takeoutMonthlyStandard.csv?Expires=1534477520&OSSAccessKeyId=STS.NKNYVMgkkyrfVHXeSiHme72zi&Signature=UPrtPdlwJdw9UUfpVisZfUhlu1s%3D&security-token=CAISpQJ1q6Ft5B2yfSjIr4j7Euz5irRKzrCNVG7pgVM8ROJJ2PfRizz2IHxMf3FqBO8Xtfk0lW9Y6f0YlqdwUY4AQlTfKMB075lR7VsmlREGB4jng4YfgbiJREKEaXeirt2wDsz9SNTCAIDPD3nPii50x5bjaDymRCbLGJaViJlhHLt1Mw6jdmgEfu80QDFvs8gHL3DcGO%2BwOxrx%2BArqAVFvpxB3hBEji9u2ydbO7QHF3h%2BoiL0WvZW0LJmic8RnPPUOWtyujuttbfiDgmwC6AJbsal3irBJ8jeA%2FPPlWgkLsk7abLaNr4w3d1UgPJJXQfAU8KLO8tRjofHWmojNzBJAAPpYSSy3Rvr7nJOfQLn0aYdiKO2qZCSSiYqVXZ7uqBOgno%2Fk3pK9EBqAAR7KAnyy4ApL8v5oJOxUQau1IiWUUOhMwCi7bgQQgfFadCmChAF1hu1OgUa5q9EX89eQICjJENSfVT8IjEz6K8%2Bk61Q0%2BvwrFmqIztQZA%2F0XMzXOjxEX6CQ0p3FNiqb9%2F%2FekKPHRV7%2Fgt%2FdwVpOWmcDxIj%2F5pkZlD912YPqEx6en'
# print(goog_url.split('?')[0].split('/')[-1])
