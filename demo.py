# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import json

"""
歌单信息的爬取
"""
song_lists = [{'cate': '华语', 'title': '虽然每天吵吵闹闹，但我从没想过离开你', 'song_list_url': 'https://music.163.com/playlist?id=2520646277'}, {'cate': '华语', 'title': '［人声哼唱］你的内心比表面看起来更孤独', 'song_list_url': 'https://music.163.com/playlist?id=2395345565'}, {'cate': '华语', 'title': '在青春的交叉路口 谁成为了你的牵绊', 'song_list_url': 'https://music.163.com/playlist?id=2507689955'}]



class WangyiyunSpider():
    """
    实现了获取小分类的歌单信息
    """
    def __init__(self):
        self.start_url = "https://music.163.com/#/discover/playlist"
        self.driver = webdriver.Chrome()





    def get_playlist_info(self, song_lists): # 获取歌单详情信息
        song_list_info = []

        for songlist in song_lists: # 遍历歌单
            songlist_url = songlist["song_list_url"] # 获取歌单url
            self.driver.get(songlist_url)
            time.sleep(1) # 等待页面加载
            self.driver.switch_to.frame("contentFrame")
            
            item = {} # 存储歌单信息
            item['歌单名'] = songlist['title']
            item['链接'] = songlist['song_list_url']

            item['创建人'] = self.driver.find_element_by_xpath('.//div[@class="user f-cb"]/span[@class="name"]/a').text
            item['介绍'] = self.driver.find_element_by_xpath('.//p[@id="album-desc-more"]').text
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
        playlist_info = self.get_playlist_info(song_lists)
        print(playlist_info)
        with open('data.json', 'w', ) as f:
            f.write(json.dumps(playlist_info, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    wangyi = WangyiyunSpider()
    wangyi.run()