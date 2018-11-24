from selenium import webdriver
import time


"""
在selenium中重复请求网页时，不要关闭退出driver，
会导致session不一致，或者造成其他的请求异常
"""
class WangyiyunSpider():
    """
    实现了获取小分类的歌单信息
    """
    def __init__(self):
        self.start_url = "https://music.163.com/#/discover/playlist"
        self.driver = webdriver.Chrome()
        # self.headers = {'Connection': 'close',}
        

    def get_s_cate_list(self): # 获取小分类信息、包含链接
        self.driver.switch_to.frame("contentFrame")
        self.driver.find_element_by_xpath('.//div[@class="u-title f-cb"]//a').click() # 点击“选择分类” 
        b_cate_list = self.driver.find_elements_by_xpath('.//div[@id="cateListBox"]//dl[@class="f-cb"]') # 大分类的列表

        cate_list = []
        for b_cate in b_cate_list: # 获取各个大分类的div
            b_cate_title = b_cate.find_element_by_xpath('./dt').text # 大分类的名字
            s_cate_list = b_cate.find_elements_by_xpath('.//dd/a') # 大分类中小分类的列表
            
            for s_cate in s_cate_list: # 便利大分类中的小分类a标签
                item = {}
                item['b_cate_title'] = b_cate_title
                item['s_cate_title'] = s_cate.text
                item['s_cate_url'] = s_cate.get_attribute("href")
                cate_list.append(item)
                # 直接跳转到小分类，再去遍历原来的元素是行不通的
        return cate_list


                # self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
                # li_lists = self.driver.find_elements_by_xpath('.//ul[@class="m-cvrlst f-cb"]/li') #歌单列表
                # for li in li_lists:
                #     title = li.driver.find_element_by_xpath('./div[@class="u-cover u-cover-1"]/a').get_attribute("title")
                #     print(title)


    def get_music_list_info(self, s_cate_list):
        # 获取各个小分类页面的信息
        for s_cate in s_cate_list:
            s_cate_url = s_cate["s_cate_url"] # 获取小分类链接
            print(s_cate_url)
            self.driver.get(s_cate_url)
            time.sleep(2) # 等待页面加载
            self.driver.switch_to.frame("contentFrame")
            li_lists = self.driver.find_elements_by_xpath('.//ul[@class="m-cvrlst f-cb"]/li') #歌单列表
            song_lists = []
            for li in li_lists: # 获取歌单的信息
                item = {}
                item['cate'] = s_cate["s_cate_title"]
                item['title'] = li.find_element_by_xpath('./div[@class="u-cover u-cover-1"]/a').get_attribute("title")
                item['song_list_url'] = li.find_element_by_xpath('./div[@class="u-cover u-cover-1"]/a').get_attribute("href")
                print(item)
                song_lists.append(item)









    def run(self):
        # 发送请求,获取相应
        self.driver.get(self.start_url)
        # 提取小分类数据
        s_cate_list = self.get_s_cate_list()
        
        for cate in s_cate_list:
            print(cate)
        #遍历小分类的链接，提取详情页
        time.sleep(1)
        self.get_music_list_info(s_cate_list)
        # 提取下一页数据


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
