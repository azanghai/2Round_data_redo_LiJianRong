import time

import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_weibo_cookie():
    cookie_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
        if redo_count > 20:
            break

        elif len(driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')) < 200:
            # find the last comment and scroll
            iframe = driver.find_elements(by=By.CLASS_NAME, value='lite-bot.m-text-cut')[-1]
            ActionChains(driver) \
                .scroll_to_element(iframe) \
                .perform()
            redo_count = redo_count + 1
            time.sleep(5)
            # sleep 5 second to avoid being blocked

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
        {'domain': '.weibo.cn', 'expiry': 1668182400, 'httpOnly': False, 'name': '_T_WM', 'path': '/', 'secure': False,
         'value': '17473971605'},
        {'domain': '.weibo.cn', 'expiry': 1699717150, 'httpOnly': True, 'name': 'SUB', 'path': '/', 'sameSite': 'None',
         'secure': True,
         'value': '_2A25OahzODeRhGeRL71MQ9SzPzzmIHXVtlKSGrDV6PUJbkdAKLVnQkW1NUwSjJXj1i7KoYvCmrEhkEIEULfJEp0o6'},
        {'domain': '.weibo.cn', 'expiry': 1668184750, 'httpOnly': False, 'name': 'MLOGIN', 'path': '/', 'secure': False,
         'value': '1'},
        {'domain': '.weibo.cn', 'expiry': 1668181165, 'httpOnly': True, 'name': 'mweibo_short_token', 'path': '/',
         'secure': False, 'value': 'c2b3384c55'},
        {'domain': '.weibo.cn', 'expiry': 1668181442, 'httpOnly': True, 'name': 'loginScene', 'path': '/',
         'secure': False, 'value': '102003'},
        {'domain': '.m.weibo.cn', 'expiry': 1699717119, 'httpOnly': False, 'name': 'FPTOKEN', 'path': '/',
         'secure': False,
         'value': '30$3QmnzozkP/lRG2q1ec1GJg9rc+deA5zs7qaIs9AUgmM2lR5fx11Nu662TevAEWsswKicOSjOdxFFU9yTiDRbkfWhDwxv14cYAtjUn7AzqHaOpQugMREIwW91wnVXL+wLkjl48M8EQ3ncDNTQs7aV9XpqMn6akNYUmMqHoPyn3Q/SGZOGcv2d0YtOSmaD76gl3E3GMKTZJfLSdCUuOF+e3zyyNlm26xF0JIrMBzvDprSD4e3DADPre3apV4qjke08w1Kg/8amFpUorBpMc3PE3XCeKVhq0PaMXhclHm4UzTtorhaVZSyOAV81kBEDLevWNYn+FS6u0xmGO/mzOy68qUgcqSrhYRgdyVogS0eCv/i5dM6xF76/0yq8aqA860YodXr/SlBRMN0UK6+K3fhOQ5/PzPNnseLmqgUE/f+ojUU=|0Yt+kshimX1M5WprP7fctXjLT1IBkFaUgW9UIEXGrbg=|10|b377b763ee40607e3dffbd9c70e91e1b'},
        {'domain': '.weibo.cn', 'expiry': 1668181750, 'httpOnly': True, 'name': 'M_WEIBOCN_PARAMS', 'path': '/',
         'secure': False,
         'value': 'oid%3D4499476460497308%26luicode%3D20000061%26lfid%3D4499476460497308%26uicode%3D20000061%26fid%3D4499476460497308'},
        {'domain': '.m.weibo.cn', 'expiry': 1668182350, 'httpOnly': False, 'name': 'XSRF-TOKEN', 'path': '/',
         'secure': False, 'value': '4a84ea'},
        {'domain': '.weibo.cn', 'expiry': 1702741150, 'httpOnly': False, 'name': '__bid_n', 'path': '/',
         'secure': False, 'value': '1846757d2d3615e7cf4207'},
        {'domain': '.weibo.cn', 'httpOnly': True, 'name': 'WEIBOCN_FROM', 'path': '/', 'secure': False,
         'value': '1110006030'}]
    weibo_ID_list = [4448352072484155]
    for weiboid in weibo_ID_list:
        weibo_comment_clawer(weiboid=weiboid, weibocookie=get_cookie, like_number=50)
