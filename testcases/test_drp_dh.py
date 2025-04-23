# testcases/test_drp_api.py

from apis.drp_api import (
    orderbill_save_do,
    orderbillitem_modify_bill_num_do,
    orderbill_submit_do,
)

def test_drp_order_flow(session):
    # 第一步：保存订货单
    save_resp = orderbill_save_do(session)
    bill_id = save_resp.json()["resultObject"]["billId"]
    print(bill_id)
    assert bill_id is not None

    # 第二步：添加明细
    item_resp = orderbillitem_modify_bill_num_do(session, billId=bill_id)
    assert item_resp.status_code == 200

    # 第三步：提交订货单
    submit_resp = orderbill_submit_do(session, billId=bill_id)
    assert submit_resp.status_code == 200
