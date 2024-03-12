import os
import sys
import requests
import pandas as pd
import datetime

def get_articles_by_date(date,key):
    '''Given a date in YYYY-MM-DD format and a NYT API key, returns articles
    that were published on that date as a dictionary.'''
    try:
        dt = datetime.datetime.strptime(date,'%Y-%m-%d')
    except ValueError:
        print(ValueError)
    
    url = f'https://api.nytimes.com/svc/archive/v1/{dt.year}/{dt.month}.json?api-key={key}'
    data = requests.get(url)

    if data.status_code == 200: 
        print("Successful get request.")
        try:
            documents = data.json()['response']['docs']
            print(f"{len(documents)} documents found for {dt.year}-{dt.month}.")
        except:
            documents = {}
            print("Data not in expected format.")
    else: 
        print("Unsuccessful get request.")
        return []

    # Filter articles by specified day
    articles = [doc for doc in documents if date in doc['pub_date']]#[:10] == date]
    print(f'{len(articles)} documents found for {date}.')
    return articles

def concat_keywords(keywords_list):
    '''concatenates keywords from keywords_list with semicolons'''
    all_keywords = ""
    for dct in keywords_list:
        keyword = dct['value']
        all_keywords += keyword + ';'
    return all_keywords[:-1]

def create_flat_dct(article):
    '''Given a article (nested dictionary), returns a flat dictionary of keys
    that are relevant for analysis.'''
    str_val_keys = ['abstract','lead_paragraph','pub_date','document_type',
                    'section_name','type_of_material']
    dct = {}
    for key in str_val_keys:
        dct[key] = article[key]

    dct['headline'] = article['headline']['main']
    dct['keywords'] = concat_keywords(article['keywords'])
    return dct

def create_df(articles,date,write_csv=True):
    '''
    Takes a list of articles, gets the relevant data for each article, 
    saves the data as a df, writes it to a csv file, and returns the df.
    Takes optional parameter write_csv. By default, writes csv of articles
    from given date to a csv file.
    '''
    # Create list of flattened dictionaries
    flat_articles = []
    for article in articles:
        flat_articles.append(create_flat_dct(article))

    df = pd.DataFrame(flat_articles)

    # Save as csv
    filename = f'{date}-articles.csv'
    if articles == None:
        print(f'There were no articles passed in for {date}.')
    elif write_csv:
        if filename in os.listdir(f'{os.getcwd()}/nyt_data'):
            print(f'File {filename} already exists')
        else:
            df.to_csv(f'{os.getcwd()}/nyt_data/{filename}')
            print(f'Saving new file: {filename}')
    else:
        print(f'\'write_csv\' set to False. Not saving: {filename}')
    
    return df

def check_exists(date):
    '''
    Checks whether a csv file with cleaned articles exists in folder.
    Returns True if it does, False otherwise
    '''
    filename = f'{date}-articles.csv'
    if filename in os.listdir():
        return True
    return False


if __name__ == "__main__":
    print('Creating cleaned articles csv files using NYT API')
    date = sys.argv[1]
    key = '1DFmIMxxqdYl8wJBPqAFxtHkimk86Qtn'
    filename = f'{date}-articles.csv' 

    # Check whether file exists
    file_exists = check_exists(date)
    if not file_exists:
        articles = get_articles_by_date(date,key) # get the articles
        create_df(articles,date) # convert articles to csv
    else:
        print(f'{filename} alreadey exists')

    df = pd.read_csv(filename) # load csv into df
    filtered = df['pub_date'].str.contains(date) # filters articles by date
    print(len(filtered))
    

    



    