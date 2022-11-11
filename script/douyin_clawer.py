import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl

def get_douyin_cookie():
    cookie_driver = webdriver.Chrome()
    cookie_driver.get(url='https://www.douyin.com/video/7094445702536760590')
    time.sleep(5)
    cookie_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    input('press enter after login')
    cookies = cookie_driver.get_cookies()
    file_name = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    with open(f'../raw_data/douyin_raw_data/douyin_cookie/{file_name}.txt', 'w') as f:
        f.write(str(cookies))
    print(cookies)
    print(type(cookies))
    # print(cookies[0])
    # print(type(cookies[0]))
    # print(str(cookies))
    # print(str(cookies[0]))
    cookie_driver.close()
    return cookies

def douyin_comment_clawer(douyinid,
                          douyincookie,
                          likenumber,
                          like_class_value,
                          time_class_name,
                          name_class_name,
                          comment_area_class_name,
                          block_class_name,
                          reply_comment_class_name,
                          comment_first,
                          comment_second,
                          at_someone_class):
    driver = webdriver.Chrome()
    Url = f'https://www.douyin.com/video/{douyinid}'
    driver.get(url=Url)
    for singledict in douyincookie:
        driver.add_cookie(singledict)
    print('Cookie add successfully, refresh now')
    driver.refresh()
    input('press enter to continue')
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    while True:
        try:
            if int(driver.find_elements(by=By.CLASS_NAME,value=like_class_value)[-1].text) < int(likenumber):
                break
            else:
                iframe = driver.find_elements(by=By.CLASS_NAME, value=like_class_value)[-1]
                ActionChains(driver) \
                    .scroll_to_element(iframe) \
                    .perform()
                # sleep 5 second to avoid being blocked
                time.sleep(5)
        except:
            break
    print('finding complete, begin to save data')

    redo_count = 0
    while True:
        res = driver.find_elements(by=By.CLASS_NAME,value=comment_area_class_name)
        print(res)
        sep_res = res[0].find_elements(by=By.CLASS_NAME, value=block_class_name)

        try:
            reply_comment = res[0].find_elements(by=By.CLASS_NAME, value=reply_comment_class_name)
            reply_list = []
            for single_reply_list in reply_comment:
                delete = single_reply_list.find_element(by=By.CLASS_NAME, value=block_class_name)
                sep_res.remove(delete)
        except:
            pass

        if len(sep_res)>200:
            break
        else:
            iframe = driver.find_elements(by=By.CLASS_NAME, value=like_class_value)[-1]
            ActionChains(driver) \
                .scroll_to_element(iframe) \
                .perform()
            # sleep 5 second to avoid being blocked
            time.sleep(5)
            redo_count = redo_count+1
        if redo_count>20:
            break

    wb = openpyxl.Workbook()
    destfile = f'../raw_data/douyin_raw_data/douyin_data/douyin_{douyinid}_{str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))}.xlsx'
    ws1 = wb.active
    row_control = 1
    for i in sep_res:
        name = i.find_element(by=By.CLASS_NAME, value=name_class_name)
        ws1.cell(row_control,1).value = name.text
        comment = i.find_element(by=By.CLASS_NAME, value=comment_first).find_element(by=By.CLASS_NAME,
                                                                                  value=comment_second)
        ws1.cell(row_control,2).value = comment.text
        try:
            at_someone = i.find_element(by=By.CLASS_NAME, value=at_someone_class)
        except:
            at_someone = 'Null'
        try:
            ws1.cell(row_control,3).value = at_someone.text
        except:
            ws1.cell(row_control,3).value = at_someone
        like = i.find_element(by=By.CLASS_NAME, value=like_class_value)
        ws1.cell(row_control,4).value = like.text
        comment_time = i.find_element(by=By.CLASS_NAME, value=time_class_name)
        ws1.cell(row_control, 5).value = comment_time.text
        print(f'username:{name.text}\ncomment:{comment.text}')
        try:
            print(f'at_someone:{at_someone.text}')
        except:
            print('at_someone:')
        print(f'like number:{like.text}\ncomment time{comment_time.text}\n-----------------')
        row_control = row_control+1
    wb.save(filename=destfile)
    driver.close()

if __name__ == '__main__':
    # get_douyin_cookie()
    douyincookie =
    douyin_comment_clawer(douyinid=7073782200499571999,
                          douyincookie=douyincookie,
                          likenumber=50,
                          comment_area_class_name='sX7gMtFl.comment-mainContent',
                          like_class_value='eJuDTubq',
                          block_class_name='RHiEl2d8',
                          reply_comment_class_name = 'nNNp3deF',
                          name_class_name='Nu66P_ba.NCRZnxVF',
                          comment_first='YzbzCgxU',
                          comment_second='Nu66P_ba.undefined',
                          at_someone_class='B3AsdZT9.DxCF1YBq.VQCdkeKT',
                          time_class_name='dn67MYhq')
