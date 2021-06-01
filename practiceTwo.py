import pandas as pd
from dartCroller import get_rcp_no_list, get_source_url_by_title
from getCorpCode import get_corp_code

key_word = "카카오"
period="20150101"
page_count="1"

corp_name, corp_code  = get_corp_code(key_word=key_word,data_type="kosdaq")
# 293490 카카오 게임즈

rcp_no_list = get_rcp_no_list(corp_code,period,page_count)
data = get_source_url_by_title(rcp_no_list[0],'4. 재무제표')

data = pd.read_html(data[0]['url'])
print(data)







