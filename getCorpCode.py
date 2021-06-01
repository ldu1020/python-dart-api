
import pandas as pd
import re
import inquirer



def get_corp_code(data_type = 'kospi', key_word ='.'):
    url = 'https://kind.krx.co.kr/corpgeneral/corpList.do' 
    data = None
    if data_type == 'kosdaq':
        data = pd.read_html(url+"?method=download&marketType=kosdaqMkt")[0] #2
    else:
        data = pd.read_html(url+"?method=download&marketType=stockMkt")[0] #3
    data = data.rename(columns={'회사명': 'name', '종목코드': 'code'})
    data = data[['name', 'code']]
    data['code'] = data.code.map('{:06d}'.format)

    r = re.compile(r'.*({}).*'.format(key_word))
    filtered = data['name'].apply(lambda x: bool(r.match(x)))

    questions = [
    inquirer.List('corp',
                message="목록중에 회사를 선택하세요(Enter)",
                choices=[item[0] + item[1] for item in data[filtered].to_numpy()],
            ),
    ]   
    answers = inquirer.prompt(questions)

    selected_name = answers['corp'][:-6]
    selected_code = answers['corp'][-6:]

    return (selected_name, selected_code)