import json
import pyktok as pyk
import sys
import pandas as pd

#### COLLECT DATA
# python pyktok-collect.py Sec1Gr1_XXXXX.json results_XXXXX.csv

def collect_metadata(inputFile, outputFile):
    """Call pyktok with a list of URLs to collect post metadata.
    """

    try:
        # with open(inputFile) as fin:
        #     data = json.load(fin)
        df = pd.read_json(path_or_buf=inputFile, orient='split')
    except FileNotFoundError:
        print(f"File '{inputFile}' couldn't be found.")
        return 
    
    try:
        # urls = [entry['Link'] for entry in data['data']]
        urls = df['Link'].to_list()
        # print(len(urls))
    except:
        print("There is something wrong with the data format.")
        return
    
    pyk.specify_browser('firefox')
    pyk.save_tiktok_multi_urls(urls,  # list of URLs to visit
                               False, # don't save videos   
                		       outputFile, # csv file
                		       5) # max time sleep
    
if __name__ == "__main__":
    _, fin, fout = sys.argv
    collect_metadata(fin, fout)