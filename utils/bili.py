import requests
requests.packages.urllib3.disable_warnings()


def comment(content, video = "BV1vU4y177GC"):
	Referer = "https://www.bilibili.com/video/%s/" % video
	headers = {
	'Host': "api.bilibili.com",
	'Connection': "keep-alive",
	'Content-Length': "937",
	'Accept': "application/json, text/javascript, */*; q=0.01",
	'Origin': "https://www.bilibili.com",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
	'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
	'Accept-Encoding': "gzip, deflate, br",
	'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
	'Cookie': "LIVE_BUVID=AUTO8415651727553762; rpdid=|(k|RYJYlY|m0J'ulYYuJlku~; buvid3=B4F22E96-074A-462E-A7A7-AACD0EFBEFC553933infoc; CURRENT_FNVAL=80; fingerprint3=04ae94452190fed1664c5571487ead87; buivd_fp=B4F22E96-074A-462E-A7A7-AACD0EFBEFC553933infoc; buvid_fp=B4F22E96-074A-462E-A7A7-AACD0EFBEFC553933infoc; CURRENT_QUALITY=80; fingerprint=c04f9e1d09689e7f1b1c6847478bda4a; DedeUserID=263505688; DedeUserID__ckMd5=065cdb05933d8aa3; _uuid=1A9E2A61-CBE1-BD42-687B-6C90782DC0DF12966infoc; buvid_fp_plain=B4F22E96-074A-462E-A7A7-AACD0EFBEFC553933infoc; SESSDATA=f9909fd8%2C1641561807%2C326c2%2A71; bili_jct=e6fa777ee34f02d106bd0aae7ce0643c; sid=lakaokfb; blackside_state=0; CURRENT_BLACKGAP=1; fingerprint_s=2221d2540e3eb20043eca8db51d5c548; bp_t_offset_263505688=557574660116465374; bp_video_offset_263505688=557624984252887294; bfe_id=6f285c892d9d3c1f8f020adad8bed553",
	}

	headers.update(Referer=Referer)

	url = "https://api.bilibili.com/x/v2/reply/add"

	data = {
	'oid':674777977,
	'type':1,
	'message':content,
	'plat':1,
	'ordering':'time',
	'jsonp':'jsonp',
	'csrf':'e6fa777ee34f02d106bd0aae7ce0643c',}

	s = requests.post(url,data=data,headers=headers,verify=False)

	print(s.ok)

