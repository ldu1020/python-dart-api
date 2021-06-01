import requests
from io import BytesIO
import pandas as pd
import re
import os


api_key = os.environ.get('DART_API_KEY')
apiBase = "https://opendart.fss.or.kr/api"
dartPageBase = "http://dart.fss.or.kr"
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}


def get_rcp_no_list (corp_code,period,page_count):
    reportUrl = apiBase + f"/list.xml?crtfc_key={api_key}" + "&sort=date&sort_mth=asc" + "&corp_code={corp_code}&bgn_de={period}&pblntf_ty=A&page_count={page_count}".format(corp_code=corp_code,period=period,page_count=page_count)
    page_source = requests.get(reportUrl,headers=headers).content.decode('utf-8')
    rgx_for_rcp_no = r'<rcept_no>(.*?)</rcept_no>'
    rcp_no_list = re.findall(rgx_for_rcp_no,page_source)
    return rcp_no_list

def get_dcm_no_list(rcp_no_list):
    dcm_no_list = []
    for rcp_no in rcp_no_list:
        get_report_page_url = dartPageBase + "/dsaf001/main.do?rcpNo={}".format(rcp_no)
        page_source = requests.get(get_report_page_url).content.decode('utf-8')
        rgx_for_dcm_no = r"viewDoc\('{rcp_no}', '(.*?)'".format(rcp_no = rcp_no)
        data = re.findall(rgx_for_dcm_no,page_source)
        dcm_no_list.append(data[0])
    return dcm_no_list

def make_source_url (rcpNo,dcmNo,eleId,offset,length,dtd):
    sourceLink = '/report/viewer.do?rcpNo={rcpNo}&dcmNo={dcmNo}&eleId={eleId}&offset={offset}&length={length}&dtd={dtd}'.format(rcpNo=rcpNo,dcmNo=dcmNo,eleId=eleId,offset=offset,length=length,dtd=dtd)
    url = dartPageBase + sourceLink
    return url

def get_source_url_by_title(rcp_no,title_rgx=""):
    get_report_page_url = dartPageBase + "/dsaf001/main.do?rcpNo={}".format(rcp_no)
    page_source = requests.get(get_report_page_url).content.decode('utf-8')

    rgx_for_get_title = '.*?' +  title_rgx + '.*?' if title_rgx else '.*?'

    rgx_for_query = r"new Tree.TreeNode[{{(]*\s*text: \"({rgx})\",[\s\w\:\"\,\{{\(\)]*viewDoc\('(.*?)', '(.*?)', '(.*?)', '(.*?)', '(.*?)', '(.*?)'\);}}".format(rgx=rgx_for_get_title)
    query_values_list = re.findall(rgx_for_query,page_source)
    source_url_list = []

    for title,rcpNo,dcmNo,eleId,offset,length,dtd in query_values_list:
        url = make_source_url(rcpNo,dcmNo,eleId,offset,length,dtd)
        source_url_list.append({'title':title,'url':url})

    return source_url_list



def download_excel(rcp_no,dcm_no,period,company):
    url = dartPageBase + '/pdf/download/excel.do?rcp_no={}&dcm_no={}&lang=ko'.format(rcp_no,dcm_no)
    res = requests.get(url,headers=headers)
    table = BytesIO(res.content)

    sheet_names = pd.ExcelFile(table).sheet_names
    file_name = period + company +'.xlsx'

    if not os.path.exists(f'./{company}'):
        os.mkdir(f'./{company}')
        
    writer = pd.ExcelWriter(f'./{company}/' + file_name, engine='xlsxwriter')



    for sheet_name in sheet_names:
        data = pd.read_excel(table,sheet_name=sheet_name)
        data.to_excel(writer, sheet_name=sheet_name) 

    writer.save()
