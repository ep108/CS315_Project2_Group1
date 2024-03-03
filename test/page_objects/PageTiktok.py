from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By # contains operators for the type of search we want to do
import time
from seleniumbase import BaseCase
from random import randint
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import html
import re
import numpy as np
import csv
from datetime import datetime
import os.path

"""
1 batch = the number of posts available on page before scrolling down and loading more.
"""

class PageTiktok(BaseCase): #inherit BaseCase
    chromebrowser = webdriver.Chrome()
    actions = ActionChains(chromebrowser)

    def __init__(self,username,browsingList):
        self.username = username
        self.current_time = datetime.now().strftime("%m-%d-%H-%M")
        self.video_list = []
        self.browsingList = browsingList
        self.currentInfo = {}

    def info_videos(self, videoList):
        '''
        When given a list of video divs, return a summary of each video
        [{'index': 1, 'video': web_element, 'hashtag': [], 'author': 'author_name', 'likes': 123}, ...]
        '''
        summary = []
        for index, video in enumerate(videoList):
            author = self.get_author(video)
            likes = self.get_stats(video,0)
            comments = self.get_stats(video,1)
            shares = self.get_stats(video,2)
            saves = self.get_stats(video,3)
            hashtag = self.get_hashtag(video)
            music = self.get_music(video)
            batch_number = self.batch_num
            summary.append({'batch': batch_number, 'index': index, 'music': music, 'video': video, 'hashtag': hashtag, 'author': author, 'likes': likes, 'comments': comments, 'shares':shares, 'saves': saves, 'video_id': id})

            return summary
        
    def info_video(self, video):
        '''
        When given a list of video divs, return a summary of each video
        [{'index': 1, 'video': web_element, 'hashtag': [], 'author': 'author_name', 'likes': 123}, ...]
        '''
        author = self.get_author(video)
        likes = self.get_stats(video,0)
        comments = self.get_stats(video,1)
        shares = self.get_stats(video,2)
        saves = self.get_stats(video,3)
        hashtag = self.get_hashtag(video)
        music = self.get_music(video)
        batch_number = self.batch_num
        return {'batch': batch_number, 'music': music, 'video': video, 'hashtag': hashtag, 'author': author, 'likes': likes, 'comments': comments, 'shares':shares, 'saves': saves, 'video_id': id}
        
    def get_author(self, video):
        try:
            author_element = video.find_element(By.XPATH, ".//*[@class='css-1k5oywg-H3AuthorTitle emt6k1z0']")
            return author_element.text if author_element else None
        except NoSuchElementException:
            print("Author element not found.")
            return None

    def get_stats(self, video, target):
        #id: xgwrapper-0-7315931231986666798
        try:
            like_button = video.find_elements(By.XPATH, ".//*[@class='css-1ok4pbl-ButtonActionItem e1hk3hf90']")[target]
            like_text = like_button.get_attribute('aria-label')
            
            # Extract numerical value using regex
            match = re.search(r'(\d+\.\d+|\d+)([KM])?', like_text)
            if match:
                # Check if suffix (K or M) is present
                if match.group(2) == 'K':
                    likes = float(match.group(1)) * 1000  # Convert K to actual number
                elif match.group(2) == 'M':
                    likes = float(match.group(1)) * 1000000  # Convert M to actual number
                else:
                    likes = float(match.group(1))
                return int(likes)
            else:
                return 0

        except (NoSuchElementException, ValueError):
            print(f"Unable to retrieve the number of target:{target}")
            return -1


    def get_hashtag(self, video):
        try:
            hashtag_list = video.find_elements(By.XPATH, './/*[@class="ejg0rhn6 css-g8ml1x-StyledLink-StyledCommonLink er1vbsz0"]')
            if hashtag_list:
                return [hashtag.get_attribute('href').split('/')[-1] for hashtag in hashtag_list]
            else:
                return []
        except NoSuchElementException:
            print("Hashtag element not found.")
            return []
        
    def get_music(self, video):
        try:
            music_info = video.find_element(By.XPATH, ".//*[@class='css-pvx3oa-DivMusicText epjbyn3']")
            music_text = music_info.text if music_info else None

            if music_text:
                return music_text
            else:
                return None
        except (NoSuchElementException, ValueError):
            print("Unable to retrieve the number of music")
            return -1
        
    def fetch_tiktok_videos(self,browsingList):
        """
        open tiktok, provide time for manual log in
        """ 
        try: 
            self.chromebrowser.get('https://www.tiktok.com/en/') #link to login page

            time.sleep(40)

            results = []
            for url in browsingList[:10]:
                self.chromebrowser.get(url)
                #html_source = self.chromebrowser.page_source
                try: 
                    self.currentInfo = self.info_video(self.chromebrowser)
                    print(self.currentInfo)
                except:
                    pass
                results.append(self.currentInfo)

            self.write_to_csv(results, "all_videos.csv")
        except Exception as e:
            print("An error occurred:", str(e))


    def iterate_through_videos(self):
        """
        Like posts in current batch after updating, then move on to the next batch
        """
        current_batch_info = self.info_videos(self.video_list)
        self.write_to_csv(current_batch_info, "all_videos.csv")  # all videos on page             

    def write_to_csv(self, data, filename):
        """
        Write data to a CSV file
        """

        csv_file_path = f"./data/{self.username}_{self.current_time}_{filename}"

        file_exists = os.path.isfile(csv_file_path) # checks if file exists already
        
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['index', 'music', 'hashtag', 'author', 'likes','comments','shares','saves']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader() #writes header only once

            for video_info in data:
                writer.writerow({
                    'index': video_info['index'],
                    'music': video_info['music'],
                    #'video': video_info['video'],
                    'hashtag': ', '.join(video_info['hashtag']),  # Convert list to comma-separated string
                    'author': video_info['author'],
                    'likes': video_info['likes'],
                    'comments': video_info['comments'],
                    'shares': video_info['shares'],
                    'saves': video_info['saves'],
                })
  
    




        
