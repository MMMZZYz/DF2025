# testcases/test_drp_api.py
from utils.request_util import request_with_allure

from apis.drp_api import (
    orderapplybill_save_do,
    orderapplybillitem_modify_item_list_do,
    orderapplybill_submit_do,
)

def test_drp_order_flow(session):
    # 第一步：保存申请单
    save_resp = orderapplybill_save_do(session)
    bill_id = save_resp.json()["resultObject"]["billId"]
    assert bill_id is not None
    

    # 第二步：添加明细
    item_resp = orderapplybillitem_modify_item_list_do(session, billId=bill_id)
    assert item_resp.status_code == 200

    # 第三步：提交申请单
    submit_resp = orderapplybill_submit_do(session, billId=bill_id)
    assert submit_resp.status_code == 200
