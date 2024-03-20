# CS315_Project2_Group1
**Authors:** Lillie, Edith, Daisy, Ashley, Lucia, Adelle.  
**Purpose:** This repo contains the scripts we used to collect and analyze real user data from TikTok along with the results of the analysis. This is part CS 315 Section 1 Group 1's second project of the semester. 

[zipped tiktok-data folder](https://drive.google.com/file/d/1Xi5Xc6EpJAIaz6FzF7N_deLFyhUIDoGD/view?usp=sharing) which contains the pyktok folder and a pyktok-test.py file for using the pyktok library.

**File:** pyktok-collect.py  
Purpose: takes user data from TikTok and calls on the pyktok library to generate a csv file. This file was given to us to use and then modified to fit our data format. Authors: Eni Mustafaraj and Johanna Lee.

**File:** pyktok.py  
Purpose: library used to collect metadata from a TikTok URL. Altered from the original authors to continue collecting when given an invalid link. [Original author linked here](https://github.com/dfreelon/pyktok).  

**Folder:** user_data  
Purpose: Holds csv of the video browsing history with TikTok URLs and date watched for 3 users. The anonymous identifiers used for the users are the 5-digit code at the end of the file name (10824, 50405, 12345).   

Files:  
  * Sec1Gr1_10824.json
  * Sec1Gr1_12345.json
  * Sec1Gr1_50405.json

**Folder:** pyktok-results
Purpose: Hold the csv files of TikTok video metadata collected using the pyktok library. Multiple people collected data for the video browsing history from three accounts. Because of this, there are at least two files of pyktok data for each account. The number at the end of the filename is the data collection attempt number. The pyktok data that we used for our analysis portion of the project have "full" at the end of the filename.

Files:
  * Sec1Gr1_10824.json
  * Sec1Gr1_12345.json
  * Sec1Gr1_50405.json

**Folder:** analysis  
Purpose: Holds the python code and data files resulting from our analysis.

Subfolders:  
  * articles_csv
    * Purpose: list of NYT articles for certain days.
  * nyt_data
    * Purpose: articles collected by NYT API.
  * filter_data
    * Purpose: for each user, the results of filtering the videos by crowdsourced news hashtags and accounts.
  * cosine_results
    * Purpose: for each user, the results of cosine similarity analysis between TikTok metadata and NYT articles.  

Files:  
  * "Week 7 Lecture Code.ipynb"
  * analyze_cosine_similartiy.ipynb
  * analyze_followers.py
  * applying_cosine_similarity.ipynb
  * articles_to_csv.py
  * clustering.ipynb
  * project2-filterdata.ipynb
  * project2-timeseries.ipynb
  * using_nyt_api.py

