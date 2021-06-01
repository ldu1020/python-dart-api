from getCorpCode import get_corp_code
from dartCroller import get_rcp_no_list, get_dcm_no_list,download_excel

key_word = "삼성"
period="20150101"
page_count="4"

corp_name, corp_code  = get_corp_code(key_word=key_word)
rcp_no_list = get_rcp_no_list(corp_code,period,page_count)
dcm_no_list = get_dcm_no_list(rcp_no_list)

for rcp_no, dcm_no in zip(rcp_no_list,dcm_no_list):
    period = rcp_no[:4] + '년' + rcp_no[4:6] + '월'
    download_excel(rcp_no,dcm_no,period,corp_name)





