from page_objects.PageTiktok import PageTiktok
import time
import pandas as pd

def main():
    # login with your control tiktok account
    username = "Sec1Gr1_50405" #replace with the filename of your data
    browsingList = getBrowsingList(username)
    page = PageTiktok(username,browsingList)
    page.fetch_tiktok_videos(browsingList)
    #page.iterate_through_videos()
    time.sleep(10)

def getBrowsingList(username):
    path = f"C:\\Users\\lilli\\OneDrive\\Desktop\\CS 315\\project 2\\tiktok\\test\\{username}.json"
    print(path)
    df = pd.read_json(path_or_buf=path, orient='split')
    browsingList = df['Link'].to_list()
    #print(browsingList)
    return browsingList

main()

