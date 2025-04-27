#订货申请单
import requests
from utils.request_util import request_with_allure
# 方法用途：orderapplybill保存操作
def orderapplybill_save_do(session, **kwargs):
    url = "https://shop.dianplus.cn/rs/drp/orderapplybill/save.do"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'bizType': '1',
        'senderInfo': '{"linkman":"丹枫","mobile":"15938796766","detailAddress":"yunhua联营仓库001地址","provinceCode":"350000","cityCode":"350100","areaCode":"350102","province":"福建省","city":"福州市","area":"鼓楼区"}',
        'receiverInfo': '{"linkman":"一级丹枫","mobile":"15938111111","detailAddress":"丹枫一级仓库","provinceCode":"110000","cityCode":"110100","areaCode":"110102","province":"北京","city":"北京市","area":"西城区"}',
        'inChannelId': '1024377522764124160',
        'inChannelName': '新新丹枫一级渠道A',
        'inChannelCode': 'dfqd001',
        'inChannelPath': 'R/10010/980069',
        'inStorageId': '1024378688629657601',
        'inStorageName': '新丹枫一级仓库',
        'inStorageCode': 'dfck001A',
        'outChannelId': '10010',
        'outChannelName': '总部渠道',
        'outChannelCode': 'DJ01',
        'outChannelPath': 'R/10010',
        'outStorageId': '433618099434958849',
        'outStorageName': 'yunhua联营仓库001',
        'outStorageCode': '0010001',
        'strategyTypeId': '692123186275295232',
        'strategyTypeName': '茉莉策略001',
        'billDate': '2025-04-21',
    }
    data.update(kwargs)
    response = request_with_allure('POST', url, session=session, headers=headers, data=data)
    return response
# 方法用途：orderapplybillitemmodifyitem列表操作
def orderapplybillitem_modify_item_list_do(session, billId, num=1):
    url = "https://shop.dianplus.cn/rs/drp/orderapplybillitem/modify_item_list.do"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {'billId': billId, 'content': '[{"skuId":"1211351383215186944","num":1}]', 'accumulate': 'true'}

    response = request_with_allure('POST', url, session=session, headers=headers, data=data)
    return response
# 方法用途：orderapplybillsubmit操作
def orderapplybill_submit_do(session, billId):
    url = "https://shop.dianplus.cn/rs/drp/orderapplybill/submit.do"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'billId': billId,
        'requestId': '8c7bb2a3-3a49-4b68-85ee-cdaa094a1505',
    }
    response = request_with_allure('POST', url, session=session, headers=headers, data=data)
    return response

#订货单

# 方法用途：orderbill保存操作
def orderbill_save_do(session):
    url = "https://shop.dianplus.cn/rs/drp/orderbill/save.do"
    headers = {'Host': 'shop.dianplus.cn', 'Connection': 'keep-alive', 'Content-Length': '1764', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"', 'sec-ch-ua-mobile': '?0', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Traceid': '100864-8ed718b0-470a-41b8-be6b-4b38c105ff88-1745229310958', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://shop.dianplus.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://shop.dianplus.cn/?module=170&menu=17020', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    data = {'opType': 'ADD', 'senderInfo': '{"linkman":"丹枫","mobile":"15938796766","detailAddress":"yunhua联营仓库001地址","provinceCode":"350000","cityCode":"350100","areaCode":"350102","province":"福建省","city":"福州市","area":"鼓楼区"}', 'receiverInfo': '{"linkman":"一级丹枫","mobile":"15938111111","detailAddress":"丹枫一级仓库","provinceCode":"110000","cityCode":"110100","areaCode":"110102","province":"北京","city":"北京市","area":"西城区"}', 'upBillId': '', 'upBillCode': '', 'inChannelId': '1024377522764124160', 'inChannelName': '新新丹枫一级渠道A', 'inChannelCode': 'dfqd001', 'inChannelPath': 'R/10010/980069', 'inChannelLevel': '3', 'inStorageId': '1024378688629657601', 'inStorageName': '新丹枫一级仓库', 'inStorageCode': 'dfck001A', 'inStoragePath': '', 'inStorageLevel': '', 'outChannelId': '10010', 'outChannelName': '总部渠道', 'outChannelCode': 'DJ01', 'outChannelPath': 'R/10010', 'outChannelLevel': '2', 'outStorageId': '433618099434958849', 'outStorageName': 'yunhua联营仓库001', 'outStorageCode': '0010001', 'outStoragePath': '', 'outStorageLevel': '', 'billDate': '2025-04-21', 'strategyTypeId': '1036660618590965761', 'strategyTypeName': '丹枫策略', 'bizType': '', 'expectArrivalDate': '', 'childBrandId': '', 'childBrandName': '', 'billYear': '', 'billSeason': '', 'billRemark': '', 'depositRatio': ''}
    response = request_with_allure('POST', url, session=session, headers=headers, data=data)
    return response

# 方法用途：orderbillitemmodify单据num操作
def orderbillitem_modify_bill_num_do(session,billId):
    url = "https://shop.dianplus.cn/rs/drp/orderbillitem/modify_bill_num.do"
    headers = {'Host': 'shop.dianplus.cn', 'Connection': 'keep-alive', 'Content-Length': '118', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"', 'sec-ch-ua-mobile': '?0', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Traceid': '100864-509f341b-00a5-4a0e-8cf7-b11889afe428-1745229315606', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://shop.dianplus.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://shop.dianplus.cn/?module=170&menu=17020', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    data = {'billId': billId, 'content': '[{"skuId":"1211351383215186944","num":1}]', 'accumulate': 'true'}
    response = request_with_allure('POST', url, session=session, headers=headers, data=data)
    return response

# 方法用途：orderbillsubmit操作
def orderbill_submit_do(session,billId):
    url = "https://shop.dianplus.cn/rs/drp/orderbill/submit.do"
    headers = {'Host': 'shop.dianplus.cn', 'Connection': 'keep-alive', 'Content-Length': '40', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"', 'sec-ch-ua-mobile': '?0', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Traceid': '100864-3537680d-6f2c-4ce1-97ca-eb59e3eee4ef-1745229322606', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://shop.dianplus.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://shop.dianplus.cn/?module=170&menu=17020', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    data = {'billId': billId, 'brandId': '10010'}
    response = request_with_allure('POST', url, session=session, headers=headers, data=data)
    return response