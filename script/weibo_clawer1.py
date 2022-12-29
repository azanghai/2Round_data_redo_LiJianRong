import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl


def get_weibo_cookie():
    cookie_driver = webdriver.Chrome()
    cookie_driver.get(url='https://m.weibo.cn/detail/4499476460497308')
    time.sleep(5)
    cookie_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    input('press enter after login')
    cookies = cookie_driver.get_cookies()
    file_name = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    with open(f'../raw_data/weibo_raw_data/weibo_cookie/{file_name}.txt', 'w') as f:
        f.write(str(cookies))
    print(cookies)
    print(type(cookies))
    # print(cookies[0])
    # print(type(cookies[0]))
    # print(str(cookies))
    # print(str(cookies[0]))
    cookie_driver.close()
    return cookies


def weibo_comment_clawer(weiboid, weibocookie, like_number):
    # set_user_cookie was acquired from previous action
    # weibocookie = {'domain': '.weibo.cn', 'expiry': 1667227174, 'httpOnly': False, 'name': 'MLOGIN', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.weibo.cn', 'expiry': 1698759572, 'httpOnly': True, 'name': 'SUB', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '_2A25OW6BDDeRhGeNM7FAX-SfPzzWIHXVtp8ALrDV6PUJbktAKLXHFkW1NSesQgybbepw0EE4CmMChq7W0ghd64Tjl'}, {'domain': '.weibo.cn', 'httpOnly': True, 'name': 'WEIBOCN_FROM', 'path': '/', 'secure': False, 'value': '1110006030'}, {'domain': '.m.weibo.cn', 'expiry': 1698759520, 'httpOnly': False, 'name': 'FPTOKEN', 'path': '/', 'secure': False, 'value': '30$MdZ60r46+Tpj+6trHWibC/IXhM6KPC66kpG6Gw4G+uRxVp1SKFhwqWgk3zkVlMMlEFsNeuRheQ6E1ry+V/LfiZkirEfZUDY+jo0k1zH8Kd38rxx911uZVqL/I/Hg/hCroP9DyfZTLSiKJ3A3KsJTe9XhPFe9OlfHkZ+sEvHl59ItA72HTYkGu+qjeOIGPMMRdadoXrvqNLMN5Wcqa3PR8KS1sf9+n4G7jgJNXPGyDjvvxWx69qeAulzM2fTLZpB6M/7NybibfR2se+czlVlFS3O8ZxHUk8kpxPOxbKWCjNelmTvjcf3mUpqD9z2qMgXdJjuHnQtWEuLsjQS75JqIOYB6WYdBEtUqTGzMpwpLY1NlkCtuGa3DOo4+n8JUTowD|wQNbmrKCrjUVyep0P/i/a8d3tRRqD5codjl07X4jHkY=|10|9a510e7e0e217478c9f00ae22dbe97be'}, {'domain': '.weibo.cn', 'expiry': 1667224174, 'httpOnly': True, 'name': 'M_WEIBOCN_PARAMS', 'path': '/', 'secure': False, 'value': 'oid%3D4499476460497308%26luicode%3D20000061%26lfid%3D4499476460497308%26uicode%3D20000061%26fid%3D4499476460497308'}, {'domain': '.weibo.cn', 'expiry': 1701783520, 'httpOnly': False, 'name': '__bid_n', 'path': '/', 'secure': False, 'value': '1842e440286d5377954207'}, {'domain': '.m.weibo.cn', 'expiry': 1667224774, 'httpOnly': False, 'name': 'XSRF-TOKEN', 'path': '/', 'secure': False, 'value': '452db3'}, {'domain': '.weibo.cn', 'httpOnly': False, 'name': 'SSOLoginState', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1667223571'}, {'domain': '.weibo.cn', 'expiry': 1698759572, 'httpOnly': False, 'name': 'SUBP', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWviwglwWW76Tz5oCwh4lhh5NHD95QfeoMESo.4e0B4Ws4DqcjKi--RiK.NiKysTCH8SC-4SEHW15tt'}, {'domain': '.weibo.cn', 'expiry': 1667232001, 'httpOnly': False, 'name': '_T_WM', 'path': '/', 'secure': False, 'value': '72196962777'}
    # initiate chrome driver
    driver = webdriver.Chrome()
    Url = f'https://m.weibo.cn/detail/{weiboid}'
    driver.get(url=Url)
    for singledict in weibocookie:
        driver.add_cookie(singledict)
    print('Cookie add successfully, refresh now')
    driver.refresh()
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # the value parameter included date and like number, parameter needs updated value, use function instead of variable
    like_check = driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')

    # a loop to find and decide when to stop scroll
    redo_count = 0
    while True:

        # next two line used for debugging
        # for a in driver.find_elements(by=By.CLASS_NAME,value='lite-bot.m-text-cut'):
        # print(a.text.split('\n'))

        # use try because program shall raise an error when there is no like value
        try:
            if int(driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')[-1].text.split('\n')[-1]) < int(
                    like_number):
                break
            else:
                # find the last comment and scroll
                iframe = driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')[-1]
                ActionChains(driver) \
                    .scroll_to_element(iframe) \
                    .perform()
                # sleep 5 second to avoid being blocked
                time.sleep(5)
        except:
            break
    while True:
        # print('small 200')
        if len(driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')) < 200:
            # find the last comment and scroll
            iframe = driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')[-1]
            ActionChains(driver) \
                .scroll_to_element(iframe) \
                .perform()
            redo_count = redo_count + 1
            time.sleep(5)
            # sleep 5 second to avoid being blocked
        elif redo_count > 20:
            break
        else:
            break

    print('finding complete, start to save data')
    # once complete, save data to res variable
    res = driver.find_elements(by=By.CLASS_NAME, value='m-box-col.m-box-dir.m-box-center.lite-line')
    wb = openpyxl.Workbook()
    destfile = f'../raw_data/weibo_raw_data/weibo_data/weibo_{weiboid}_{str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))}.xlsx'
    ws1 = wb.active
    countnum = 1
    for single_data in res:
        for data in single_data.text.split('\n'):
            ws1.cell(countnum, single_data.text.split('\n').index(data) + 1).value = data
        countnum = countnum + 1
    # print(i.get_attribute('innerHTML'))
    wb.save(filename=destfile)
    print(f'saving datafor weibo{weiboid} complete!')
    driver.close()


if __name__ == '__main__':
    # get_cookie = get_weibo_cookie()
    get_cookie = [
        {'domain': '.weibo.cn', 'expiry': 1672063506, 'httpOnly': True, 'name': 'M_WEIBOCN_PARAMS', 'path': '/', 'secure': False, 'value': 'oid%3D4499476460497308%26luicode%3D20000061%26lfid%3D4499476460497308%26uicode%3D20000061%26fid%3D4499476460497308'}, {'domain': '.m.weibo.cn', 'expiry': 1672064106, 'httpOnly': False, 'name': 'XSRF-TOKEN', 'path': '/', 'secure': False, 'value': 'c14c45'},
        {'domain': '.weibo.cn', 'expiry': 1672066506, 'httpOnly': False, 'name': 'MLOGIN', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.weibo.cn', 'expiry': 1672070401, 'httpOnly': False, 'name': '_T_WM', 'path': '/', 'secure': False, 'value': '82755656215'}, {'domain': '.weibo.cn', 'httpOnly': True, 'name': 'WEIBOCN_FROM', 'path': '/', 'secure': False, 'value': '1110006030'},
        {'domain': '.weibo.cn', 'expiry': 1703598906, 'httpOnly': True, 'name': 'SUB', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '_2A25OrdfpDeRhGeRL71MQ9SzPzzmIHXVqUfmhrDV6PUJbkdANLWLnkW1NUwSjJWAfhckfsZg24DgpQ9eC3HPTaPpZ'}, {'domain': '.weibo.cn', 'expiry': 1672063193, 'httpOnly': True, 'name': 'loginScene', 'path': '/', 'secure': False, 'value': '102003'},
        {'domain': '.weibo.cn', 'expiry': 1706622877, 'httpOnly': False, 'name': '__xaf_fpstarttimer__', 'path': '/', 'secure': False, 'value': '1672062877742'}, {'domain': '.weibo.cn', 'expiry': 1706622877, 'httpOnly': False, 'name': '__xaf_thstime__', 'path': '/', 'secure': False, 'value': '1672062877883'},
        {'domain': '.weibo.cn', 'expiry': 1672149277, 'httpOnly': False, 'name': '__xaf_ths__', 'path': '/', 'secure': False, 'value': '{"data":{"0":1,"1":43200,"2":60},"id":"6179a2ce-5e16-4e2a-b481-763e72edd518"}'}, {'domain': '.weibo.cn', 'expiry': 1706622878, 'httpOnly': False, 'name': '__xaf_fptokentimer__', 'path': '/', 'secure': False, 'value': '1672062878107'},
        {'domain': '.weibo.cn', 'expiry': 1706622878, 'httpOnly': False, 'name': 'FPTOKEN', 'path': '/', 'secure': False, 'value': 'E9aRdMnxpmFTeMWwFnZlsl2PAnm05Oi1W3TbnLyjQaeam/5hW2NT2Ha5jm5ZZpq/HpZAc+Xf66G29nOf+8Z7oBnV1vqX/BNYqqQCxt3MQrYeEOb6uZSsEKu6zQqQ8F4Na+zJfMxHhNTutUWFoQQnlN7rS9uQXj9SpVZyDlnbkiDQ6i9T9R8Na2CCmqyiwVC3Ccx/3AvfCLWV9eoFwlaBOpXCdoY5mgVVNjxMF2uGTXohqa8S9KYdwuZ4wIVA/qzw5GupWVsV9jZuipaUHBczO5ltN7oYW1jhhemN+0l42EEBxXXAEmX5UtJroKcldtZb2pK46vSbmCYX0VL/9DlE+FYu0ilFj+QzCr+zSQBxUY74bfhOOjM2NVjPmd5iun0bMqnWbZUH38LeOdtYsujOlhqZ3vlPvJkirPOGozwB+Vvw12X0NROyyE8cS2DcJFpt|UtacBJRs68cExVZYa+42ztBUrRdl1twbH1l+fHVXrDo=|10|e378cea8ab7bc434ed4ce7166af8c25d'},
        {'domain': '.weibo.cn', 'expiry': 1706622907, 'httpOnly': False, 'name': '__bid_n', 'path': '/', 'secure': False, 'value': '1854eb6bfd4fb3ffff4207'}, {'domain': '.weibo.cn', 'expiry': 1706622877, 'httpOnly': False, 'name': 'FEID', 'path': '/', 'secure': False, 'value': 'v10-fe2d17a31d0aced8e6e5d85ff5e033ed8a518d56'}]
    weibo_ID_list = [4448352072484155]
    for weiboid in weibo_ID_list:
        weibo_comment_clawer(weiboid=weiboid, weibocookie=get_cookie, like_number=50)
