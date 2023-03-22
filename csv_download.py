
# coding: utf-8
import pandas as pd
import io
import requests
url="https://github.com/xiaomidangjia/middle_crypto/blob/main/base_information.csv"
s=requests.get(url).content
squirrel=pd.read_csv(io.StringIO(s.decode('utf-8')))
squirrel.to_csv("base_information.csv")

