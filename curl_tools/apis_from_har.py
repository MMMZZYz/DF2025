# Auto-generated API functions

import requests

# 方法用途：orderbill保存操作
def orderbill_save_do(session):
    url = "https://shop.dianplus.cn/rs/drp/orderbill/save.do"
    headers = {'Host': 'shop.dianplus.cn', 'Connection': 'keep-alive', 'Content-Length': '1764', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"', 'sec-ch-ua-mobile': '?0', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Traceid': '100864-8ed718b0-470a-41b8-be6b-4b38c105ff88-1745229310958', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://shop.dianplus.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://shop.dianplus.cn/?module=170&menu=17020', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    data = {'opType': 'ADD', 'senderInfo': '{"linkman":"丹枫","mobile":"15938796766","detailAddress":"yunhua联营仓库001地址","provinceCode":"350000","cityCode":"350100","areaCode":"350102","province":"福建省","city":"福州市","area":"鼓楼区"}', 'receiverInfo': '{"linkman":"一级丹枫","mobile":"15938111111","detailAddress":"丹枫一级仓库","provinceCode":"110000","cityCode":"110100","areaCode":"110102","province":"北京","city":"北京市","area":"西城区"}', 'upBillId': '', 'upBillCode': '', 'inChannelId': '1024377522764124160', 'inChannelName': '新新丹枫一级渠道A', 'inChannelCode': 'dfqd001', 'inChannelPath': 'R/10010/980069', 'inChannelLevel': '3', 'inStorageId': '1024378688629657601', 'inStorageName': '新丹枫一级仓库', 'inStorageCode': 'dfck001A', 'inStoragePath': '', 'inStorageLevel': '', 'outChannelId': '10010', 'outChannelName': '总部渠道', 'outChannelCode': 'DJ01', 'outChannelPath': 'R/10010', 'outChannelLevel': '2', 'outStorageId': '433618099434958849', 'outStorageName': 'yunhua联营仓库001', 'outStorageCode': '0010001', 'outStoragePath': '', 'outStorageLevel': '', 'billDate': '2025-04-21', 'strategyTypeId': '1036660618590965761', 'strategyTypeName': '丹枫策略', 'bizType': '', 'expectArrivalDate': '', 'childBrandId': '', 'childBrandName': '', 'billYear': '', 'billSeason': '', 'billRemark': '', 'depositRatio': ''}
    return session.post(url, headers=headers, data=data)

# 方法用途：orderbillitemmodify单据num操作
def orderbillitem_modify_bill_num_do(session):
    url = "https://shop.dianplus.cn/rs/drp/orderbillitem/modify_bill_num.do"
    headers = {'Host': 'shop.dianplus.cn', 'Connection': 'keep-alive', 'Content-Length': '118', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"', 'sec-ch-ua-mobile': '?0', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Traceid': '100864-509f341b-00a5-4a0e-8cf7-b11889afe428-1745229315606', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://shop.dianplus.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://shop.dianplus.cn/?module=170&menu=17020', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    data = {'billId': '1213778547585315840', 'content': '[{"skuId":"1211351383215186944","num":1}]', 'accumulate': 'true'}
    return session.post(url, headers=headers, data=data)


# 方法用途：orderbillsubmit操作
def orderbill_submit_do(session):
    url = "https://shop.dianplus.cn/rs/drp/orderbill/submit.do"
    headers = {'Host': 'shop.dianplus.cn', 'Connection': 'keep-alive', 'Content-Length': '40', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"', 'sec-ch-ua-mobile': '?0', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Traceid': '100864-3537680d-6f2c-4ce1-97ca-eb59e3eee4ef-1745229322606', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://shop.dianplus.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://shop.dianplus.cn/?module=170&menu=17020', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    data = {'billId': '1213778547585315840', 'brandId': '10010'}
    return session.post(url, headers=headers, data=data)