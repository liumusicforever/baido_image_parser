import sys
import os
import json
import argparse
import requests
import time

import csv
import urllib

from lib.utils import mkdirs
from lib.decode_objurl import DecodeObjUrl
from lib.config import *

example_text = '''example:
python keywords2urls.py --keywords ./test_keywords.csv --out_dir img_list --limit_per_word 10000
'''



def argparer():
    parser = argparse.ArgumentParser( epilog=example_text,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--keywords', required=True, dest="keywords", type=str, help="the csv file path")
    parser.add_argument('--out_dir', required=True, dest="out_dir", type=str, help="out_dir")
    parser.add_argument('--limit_per_word', required=True, dest="limit_per_word", type=int, help="per word limit num")
    
    args = parser.parse_args()

    return args

def get_page_urls(pagenum,keyword):
    '''
    Parameter : 
        pagenum : pagenum of each pagenum
        keyword : search keyword
    Return :
        url_list : list of urls
    '''
    url_list = []
    url = search_url+"&pn="+str(pagenum)+"&word="+keyword+"&queryWord="+keyword
    
    # got page meta
    try:
        response = requests.get(url,headers=header)
        stat = response.status_code
        content = unicode(response.content, errors='ignore')
        web_source = json.loads(content)
    except Exception as e:
        return []
    
    page_data=web_source['data']

    
    for img_num,img_data in enumerate(page_data):
        if img_num >= len(page_data)-1 : continue
        url = DecodeObjUrl(img_data['objURL'])+'\n'
        url_list.append(url)
    return url_list

def get_keywords_urls(keyword , out_dir , limit):
    page_num = 0
    
    mkdirs(out_dir)
    out_path = os.path.join(out_dir , keyword + '.txt')

    hash_word = urllib.quote(keyword)
    
    while page_num < limit:
        url_list = get_page_urls(page_num,hash_word)
        save_per_page_img_url(url_list , out_path)
        page_num += 50
        if len(url_list)== 0: break
        time.sleep(1)
        
    return page_num

def save_per_page_img_url(url_list , path):
    with open(path,'a') as fs:
        for url in url_list:
            fs.write(url)

def main():
    args = argparer()
    query_list = list(csv.reader(open(args.keywords)))

    total_img = 0
    for i,(key_id , keyword) in enumerate(query_list):
        print ('processing keyword : {}/{} , total_img : {}'.format(
                i,
                len(query_list),
                total_img))
        num_img = get_keywords_urls(keyword , 
                    out_dir = args.out_dir,
                    limit = args.limit_per_word)
        total_img += num_img
        
        
    
if __name__ == "__main__":
    main()