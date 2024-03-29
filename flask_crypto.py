
# coding: utf-8

import json
import base64
from flask import Flask, request
import requests
import numpy as np
import pandas as pd
import csv

app = Flask(__name__)


@app.route("/middle_crypto_pre", methods=['post'])
def middle_crypto_pre():
    date = request.form.get('date')
    type_ = request.form.get('type')
    crypto = request.form.get('crypto')
    api_key_value = request.form.get('api_key')
    order_value = request.form.get('order_value')
    ip_addr = request.remote_addr
    print(ip_addr)

    # 读取一个表，判断api_key 是不是在有效期内，有效的下单金额是多少
    p = []
    with open("/root/middle_crypto/base_information.csv", 'r', encoding="UTF-8") as fr:
        reader = csv.reader(fr)
        for index, line in enumerate(reader):
            if index == 0:
                continue
            p.append(line)
    res_data = pd.DataFrame(p)
    res_data['api_key'] = res_data.iloc[:,0]
    res_data['end_date'] = res_data.iloc[:,1]
    res_data['api_type'] = res_data.iloc[:,3]
    res_data['ip_addr'] = res_data.iloc[:,6]

    api_key_judge = res_data[(res_data.api_key==api_key_value) & (res_data.ip_addr==ip_addr)]

    if len(api_key_judge) == 0:
        # 无效api，返回的都是不下单
        res_dict = {'value':'no_api','today_price':0,'up_close_date':0,'up_start_price':0,'zuigao':0}
        ans_str = json.dumps(res_dict)
    else:
        # 判断api是不是试用的，是不是在有效期
        api_key_judge = api_key_judge.reset_index()
        api_type = api_key_judge['api_type'][0]
        end_date = api_key_judge['end_date'][0]
        # 已经超时，返回不下单
        if pd.to_datetime(date) > pd.to_datetime(end_date):
            res_dict = {'value':'exit_date','today_price':0,'up_close_date':0,'up_start_price':0,'zuigao':0}
            ans_str = json.dumps(res_dict)
         # 试用期的api，不能超过200u
        elif api_type == 'shiyong' and int(order_value) >= 2200:
            res_dict = {'value':'exit_value','today_price':0,'up_close_date':0,'up_start_price':0,'zuigao':0}
            ans_str = json.dumps(res_dict)
        elif api_type == 'zhengshi' and int(order_value) >= 22000:
            res_dict = {'value':'exit_value','today_price':0,'up_close_date':0,'up_start_price':0,'zuigao':0}
            ans_str = json.dumps(res_dict)
        else:
            print(type_,date,crypto)
            w = 0
            while  w == 0:
                #调用接口  
                try:
                    test_data_1 = {
                        "type": type_,
                        "date": date,
                        "crypto":crypto
                        }
                    req_url = "http://8.219.61.64:80/crypto_pre"
                    r = requests.post(req_url, data=test_data_1)
                    api_res = r.content.decode('utf-8')
                    api_res = json.loads(api_res)
                    r_value = api_res['value']
                    today_price = api_res['today_price']
                    up_close_date = str(api_res['up_close_date'])[0:10]
                    up_start_price = float(api_res['up_start_price'])
                    up_zuigao = int(api_res['zuigao'])
                    #print(r_value,today_price,up_close_date,up_start_price)
                    w = 1
                except:
                    w = 0

            res_dict = {'value':r_value,'today_price':today_price,'up_close_date':up_close_date,'up_start_price':up_start_price,'zuigao':up_zuigao}
            ans_str = json.dumps(res_dict)

    return ans_str

if __name__ == '__main__':
    app.run("0.0.0.0", port=80)


