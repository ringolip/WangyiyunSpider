from selenium import webdriver
import time
import json

"""
提取了详情页的数据
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


    def get_musiclist(self, s_cate_list):

        song_lists = [] # 存储歌单

        # 获取各个小分类页面的信息
        for s_cate in s_cate_list:
            s_cate_url = s_cate["s_cate_url"] # 获取小分类链接
            print(s_cate_url)
            self.driver.get(s_cate_url)
            time.sleep(1) # 等待页面加载
            self.driver.switch_to.frame("contentFrame")
            li_lists = self.driver.find_elements_by_xpath('.//ul[@class="m-cvrlst f-cb"]/li') #歌单列表

            
            for li in li_lists: # 获取歌单的信息
                item = {}
                item['cate'] = s_cate["s_cate_title"]
                item['title'] = li.find_element_by_xpath('./div[@class="u-cover u-cover-1"]/a').get_attribute("title")
                item['song_list_url'] = li.find_element_by_xpath('./div[@class="u-cover u-cover-1"]/a').get_attribute("href")
                print(item)
                song_lists.append(item)

        # 写入歌单信息        
        with open('playlists.json', 'w', ) as f:
            f.write(json.dumps(song_lists, indent=4, ensure_ascii=False))

        return song_lists


    def get_playlist_info(self, song_lists): # 获取歌单详情信息
        song_list_info = []

        for songlist in song_lists: # 遍历歌单
            songlist_url = songlist["song_list_url"] # 获取歌单url
            self.driver.get(songlist_url)
            
            self.driver.switch_to.frame("contentFrame")
            
            item = {} # 存储歌单信息
            item['歌单名'] = songlist['title']
            item['链接'] = songlist['song_list_url']

            item['创建人'] = self.driver.find_element_by_xpath('.//div[@class="user f-cb"]/span[@class="name"]/a').text
            # item['介绍'] = self.driver.find_element_by_xpath('.//p[@id="album-desc-more"]').text
            song_list = self.driver.find_elements_by_xpath('.//table[@class="m-table "]/tbody/tr')

            songs = [] # 存储歌单中歌曲信息
            for song in song_list:
                song_item = {} # 每首歌的信息
                song_item['歌曲名'] = song.find_element_by_xpath('.//span[@class="txt"]//b').get_attribute("title")
                song_item['歌曲链接'] = song.find_element_by_xpath('.//span[@class="txt"]//a').get_attribute('href')
                songs.append(song_item)
            item['歌曲'] = songs

            print(item)
            song_list_info.append(item)
        return song_list_info



    def run(self):
        # 发送请求,获取相应
        self.driver.get(self.start_url)
        # 提取小分类数据
        s_cate_list = self.get_s_cate_list()
        
        for cate in s_cate_list:
            print(cate)
        # 遍历小分类的链接，提取详情页
        # time.sleep(1)
        song_lists = self.get_musiclist(s_cate_list)
        # 遍历歌单，提取歌单数据
        playlist_info = self.get_playlist_info(song_lists)

        print(playlist_info)
        # 储存歌单信息
        with open('playlists_info.json', 'w', ) as f:
            f.write(json.dumps(playlist_info, indent=4, ensure_ascii=False))



if __name__ == "__main__":
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
