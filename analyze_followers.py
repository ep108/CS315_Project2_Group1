import json
import os
from collections import defaultdict
import pandas as pd

def createdata(fileName):
    #get data from a json file
    data = json.load(open(fileName, encoding="utf8"))
    return data

def getfollowers(data):
    # get list of dictionaries, representing accounts followed
    followers = data['Activity']['Following List']['Following']
    return followers

def followerlist(followers):
    # create a list of accounts followed
    follower_list = []
    for ii in followers:
        current_dict = ii
        follower = current_dict["UserName"]
        follower_list.append(follower)
    return follower_list

def getnewslist(fileName):
    # get news accounts from class CSV file
    df = pd.read_csv(fileName)
    news_list = df['Username'].tolist()
    return news_list

def checkoverlap(follower_list, news_list):
    # check overlap between follower list and news accounts
    overlap = 0
    for ii in follower_list:
        if ii in news_list:
            #print(ii)
            overlap += 1
    return overlap

def findalloverlap(fileName, newsFileName):
    # automate entire overlap check process
    data = createdata(fileName)
    followers = getfollowers(data)
    follower_list = followerlist(followers)
    newslist = getnewslist(newsFileName)
    totaloverlap = checkoverlap(follower_list, newslist)
    return totaloverlap

def getnumfollowed(fileName):
    data = createdata(ii)
    followers = getfollowers(data)
    numfollow = len(followers)
    return numfollow

def createDataFrame(fileList, newsFile):
    filelist = fileList
    followlist = []
    overlaplist = []
    
    for ii in filelist:
        numfollow = getnumfollowed(ii)
        followlist.append(numfollow)
        
        numoverlap = findalloverlap(ii, newsFile)
        overlaplist.append(numoverlap)
        
    overlapFrame = pd.DataFrame(
        {'Account' : filelist,
         'Total Followers':followlist,
         'News Accounts':overlaplist})
    return(overlapFrame)

fileList = ['C:/Users/Lucia/Desktop/Capstone/user_data2.json', "C:/Users/Lucia/Downloads/user_data.json"] #INSERT YOUR OWN FILE NAMES TO RUN

print(createDataFrame(fileList, 'C:/Users/Lucia/OneDrive/CS 315/List of News Accounts (both sections) - news accounts.csv')) #INSERT YOUR OWN UPDATED NEWS FILE TO RUN

##WILL ADD CODE TO VISUALIZE OVERLAP
