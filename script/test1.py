import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl

douyincookie = [{'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'ssid_ucp_v1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1.0.0-KGI1YjU2ZDYxNzdlZmU3ZTlmOGNjNzgyYTNjMWUxZDU4YTE3ZjI3OTAKGAj3zsDsjY0iEKyYgZsGGO8xIAw4BkD0BxoCaGwiIDI3M2FlZmNhZDNkMzU0ZTNiMDRiYTMwNWE0ZTNiZTll'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sid_ucp_v1', 'path': '/', 'secure': True, 'value': '1.0.0-KGI1YjU2ZDYxNzdlZmU3ZTlmOGNjNzgyYTNjMWUxZDU4YTE3ZjI3OTAKGAj3zsDsjY0iEKyYgZsGGO8xIAw4BkD0BxoCaGwiIDI3M2FlZmNhZDNkMzU0ZTNiMDRiYTMwNWE0ZTNiZTll'}, {'domain': '.douyin.com', 'expiry': 1698791341, 'httpOnly': True, 'name': 'odin_tt', 'path': '/', 'secure': False, 'value': 'dcacb5439d181a64c335e969f14454e34b53ecfc75241835436fac7564cf76529af0080f9de9256dfc24baff0c07542a396529eaf79f8b24ff1b2b98e62b881e'}, {'domain': '.www.douyin.com', 'httpOnly': False, 'name': 'passport_fe_beating_status', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.douyin.com', 'expiry': 1667860138, 'httpOnly': False, 'name': 'msToken', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'y8s1IAoDKGPB33VVIeLjG76cuVTxtHWHCI_h8fYKgoGhyuya__zC5dvZjVeLqDFSGc0pardUJ28H4B1T-T-9XUc_Fz6PRlZ2JXVFWH3lsPFe6IjA7G1fFb7MHXK6oII='}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sessionid_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '273aefcad3d354e3b04ba305a4e3be9e'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sid_tt', 'path': '/', 'secure': False, 'value': '273aefcad3d354e3b04ba305a4e3be9e'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'uid_tt_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '7ecec5188783033fbc81bed12e9aee93'}, {'domain': '.douyin.com', 'expiry': 1669847332, 'httpOnly': True, 'name': 'passport_auth_status_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'cb5a66e266c65e22f23afc5678017a28%2C'}, {'domain': '.douyin.com', 'expiry': 1669847332, 'httpOnly': True, 'name': 'passport_auth_status', 'path': '/', 'secure': False, 'value': 'cb5a66e266c65e22f23afc5678017a28%2C'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sid_ucp_sso_v1', 'path': '/', 'secure': True, 'value': '1.0.0-KDY1ZDU4NDllN2Q5NGI1MmNhNmQyN2M0ZDQyMmU0ZTQxZWIwZDEwNzcKHgj3zsDsjY0iEKKYgZsGGO8xIAwww7S3jAY4BkD0BxoCbHEiIGFjZjEzYmVkNWJmNjA5OTk1YmJjZWNjYzA3NTZlYjRj'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'toutiao_sso_user', 'path': '/', 'secure': False, 'value': 'acf13bed5bf609995bbceccc0756eb4c'}, {'domain': '.douyin.com', 'expiry': 1701815331, 'httpOnly': False, 'name': 'passport_assist_user', 'path': '/', 'secure': True, 'value': 'CkCnXxsEc8xWCDxPmbglFWF6iFfBUE7pN7ZD6gwJUAQCKkk_R7i2ZVtRd9CSZSxYWhrPIH1gWyEZd4miUc9bdOT5GkgKPIKT95gsNEQHfyHepd5yaoKEPr_5oamMMULE4oa2w0ILPJkelObeqGWV6L_am9ZGhTVTyXzZDpQFLuGStRD5_58NGImv1lQiAQNkIoSx'}, {'domain': '.douyin.com', 'expiry': 1677623331, 'httpOnly': True, 'name': 'n_mh', 'path': '/', 'secure': False, 'value': 'hu0Qw1k2DcT273oyIvMecbJ-iF5KmDvdsBQErWOxDMU'}, {'domain': 'www.douyin.com', 'expiry': 1667860141, 'httpOnly': False, 'name': 'msToken', 'path': '/', 'secure': False, 'value': 'foimD9EsxiACgrzlxvSPA5Pu1kaBDVpwPaDi90evbva3-YRhnAWUyvvga6AEF_eM9wCNA_Ty1Tsie19hLGpC5oUo_UoscnDgpLEYnDlzLrSe3gDZrukzvrTkGM6vQug='}, {'domain': '.douyin.com', 'expiry': 1672439317, 'httpOnly': False, 'name': 'passport_csrf_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'dc650a8e2e9f75ac2420f90d33f388b9'}, {'domain': '.douyin.com', 'expiry': 1667860146, 'httpOnly': False, 'name': 'home_can_add_dy_2_desktop', 'path': '/', 'secure': False, 'value': '%221%22'}, {'domain': '.douyin.com', 'expiry': 1667860114, 'httpOnly': False, 'name': 'strategyABtestKey', 'path': '/', 'secure': False, 'value': '1667255314.784'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'toutiao_sso_user_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'acf13bed5bf609995bbceccc0756eb4c'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sso_uid_tt_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ef31c48a8cb419ceb7d06453083fb4b4'}, {'domain': 'www.douyin.com', 'expiry': 1698791311, 'httpOnly': False, 'name': '__ac_signature', 'path': '/', 'secure': False, 'value': '_02B4Z6wo00f01NGWqVAAAIDAUZRTEo6tSUjRto3AAFcL58'}, {'domain': '.douyin.com', 'expiry': 1698359341, 'httpOnly': True, 'name': 'sid_guard', 'path': '/', 'secure': False, 'value': '273aefcad3d354e3b04ba305a4e3be9e%7C1667255340%7C5183990%7CFri%2C+30-Dec-2022+22%3A28%3A50+GMT'}, {'domain': 'www.douyin.com', 'expiry': 1672439317, 'httpOnly': False, 'name': 's_v_web_id', 'path': '/', 'secure': False, 'value': 'verify_l9xcrojd_DZr0rrxh_GkwO_4A9g_81fk_uNtLGyQawENi'}, {'domain': '.douyin.com', 'expiry': 1672439317, 'httpOnly': False, 'name': 'passport_csrf_token_default', 'path': '/', 'secure': False, 'value': 'dc650a8e2e9f75ac2420f90d33f388b9'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'ssid_ucp_sso_v1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1.0.0-KDY1ZDU4NDllN2Q5NGI1MmNhNmQyN2M0ZDQyMmU0ZTQxZWIwZDEwNzcKHgj3zsDsjY0iEKKYgZsGGO8xIAwww7S3jAY4BkD0BxoCbHEiIGFjZjEzYmVkNWJmNjA5OTk1YmJjZWNjYzA3NTZlYjRj'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sso_uid_tt', 'path': '/', 'secure': False, 'value': 'ef31c48a8cb419ceb7d06453083fb4b4'}, {'domain': 'www.douyin.com', 'expiry': 1667257111, 'httpOnly': False, 'name': '__ac_nonce', 'path': '/', 'secure': False, 'value': '063604c0e00bdf7857e04'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'sessionid', 'path': '/', 'secure': False, 'value': '273aefcad3d354e3b04ba305a4e3be9e'}, {'domain': 'www.douyin.com', 'expiry': 1667860147, 'httpOnly': False, 'name': 'tt_scid', 'path': '/', 'secure': False, 'value': 'biQ1rHzfEUY5Y0ZBlRSJQcuu92Dn88jzAihYFUFD7GgvD2bJXI49gOI-C30hRSvb17c9'}, {'domain': '.douyin.com', 'expiry': 1672439331, 'httpOnly': True, 'name': 'uid_tt', 'path': '/', 'secure': False, 'value': '7ecec5188783033fbc81bed12e9aee93'}, {'domain': '.douyin.com', 'expiry': 1698359338, 'httpOnly': True, 'name': 'ttwid', 'path': '/', 'secure': False, 'value': '1%7Ciy4jqe1wtJoEymP5CIVf3EsSBmNKmFb7NB07XLXnw7A%7C1667255311%7C56c6b01482137a1907b1362a5cd01f0383e6efb68a52cb54c971d7b74f2cdfa4'}, {'domain': 'www.douyin.com', 'expiry': 1667860122, 'httpOnly': False, 'name': 'ttcid', 'path': '/', 'secure': False, 'value': '9421ada16f6644a884a38517018a491127'}, {'domain': 'www.douyin.com', 'httpOnly': False, 'name': '', 'path': '/video', 'secure': False, 'value': 'douyin.com'}]

cookie_driver = webdriver.Chrome()
cookie_driver.get(url='https://www.douyin.com/video/7073782200499571999')
for singledict in douyincookie:
    cookie_driver.add_cookie(singledict)
time.sleep(5)
cookie_driver.refresh()
input('wait for confirm')
# time.sleep(5)

res = cookie_driver.find_elements(by=By.CLASS_NAME,value='sX7gMtFl.comment-mainContent')
print(res)
sep_res = res[0].find_elements(by=By.CLASS_NAME,value='RHiEl2d8')

try:
    reply_comment = res[0].find_elements(by=By.CLASS_NAME,value='nNNp3deF')
    reply_list = []
    for single_reply_list in reply_comment:
        delete = single_reply_list.find_element(by=By.CLASS_NAME,value='RHiEl2d8')
        sep_res.remove(delete)
except:
    pass


for i in sep_res:
    name = i.find_element(by=By.CLASS_NAME,value='Nu66P_ba.NCRZnxVF')
    comment = i.find_element(by=By.CLASS_NAME,value='YzbzCgxU').find_element(by=By.CLASS_NAME,value='Nu66P_ba.undefined')
    try:
        at_someone = i.find_element(by=By.CLASS_NAME,value='B3AsdZT9.DxCF1YBq.VQCdkeKT')
    except:
        at_someone = ''
    like = i.find_element(by=By.CLASS_NAME,value='eJuDTubq')
    time = i.find_element(by=By.CLASS_NAME,value='dn67MYhq')
    print(f'username:{name.text}\ncomment:{comment.text}')
    try:
        print(f'at_someone:{at_someone.text}')
    except:
        print('at_someone:')
    print(f'like number:{like.text}\ncomment time{time.text}\n-----------------')
input('wait to shut')
cookie_driver.close()