from selenium import webdriver
import time
"""
实现了遍历大分类小分类
"""

class WangyiyunSpider():
    def __init__(self):
        self.start_url = "https://music.163.com/#/discover/playlist"
        self.driver = webdriver.Chrome()
        

    def get_cate_list(self):
        self.driver.switch_to.frame("contentFrame")
        self.driver.find_element_by_xpath('.//div[@class="u-title f-cb"]//a').click() # 点击“选择分类” 
        b_cate_list = self.driver.find_elements_by_xpath('.//div[@id="cateListBox"]//dl[@class="f-cb"]') # 大分类的列表
        # test_data = self.driver.find_element_by_xpath('.//div[@id="cateListBox"]//dl[@class="f-cb"]')
        # print(test_data)
        cate_list = []
        for b_cate in b_cate_list: # 获取各个大分类的div
            
            s_cate_list = b_cate.find_elements_by_xpath('.//dd/a') # 大分类中小分类的列表
            
            for s_cate in s_cate_list: # 便利大分类中的小分类a标签
                item = {}
                item['s_cate_title'] = s_cate.text
                item['s_cate_url'] = s_cate.get_attribute("href")
                print(item['s_cate_title'])
                cate_list.append(item)



        return cate_list


    def run(self):
        # - 1. 确定url
        # 发送请求,获取相应
        self.driver.get(self.start_url)
        # 提取数据,提取下一页数据
        cate_list = self.get_cate_list()
        self.driver.quit()
        # - 1. 返回
        print(cate_list)


wangyi = WangyiyunSpider()
wangyi.run()
# driver.get("http://www.baidu.com/")
# driver.save_screenshot("长城.png")
# 定位和操作：
# driver.find_element_by_id(“kw”).send_keys(“长城”)
# driver.find_element_by_id("su").click()
# 查看请求信息：
# driver.page_source
# driver.get_cookies()
# driver.current_url
# 退出
# driver.close() #退出当前页面
# driver.quit()  #退出浏览器
