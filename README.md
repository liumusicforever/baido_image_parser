# baido_image_parser
The simple multi-thread parser for baido image.

## Environment
* Python 2.7
* request
* BeautifulSoup
* urllib

## How To Use
* Step 1 :
    type your header in `lib/config.py` line 10 
    ```
    header={
    'accept':'',
    'accept-language':'',
    'avail-dictionary':'',
    'cache-control':'no-cache',
    'cookie':'',
    'pragma':'no-cache',
    'referer':'https://www.google.com.tw/',
    'upgrade-insecure-requests':'1',
    'user-agent':'',
    'x-client-data':''}
    ```
    **key:** You can open F12(develop mode) on Chrome and search keyword on google image , then open `Network -> Header` , get your own header
    
* Step 2 :
    Prepare your keywords , here is the `xxx_keywords.csv` format:
    ```
    1,<keyword 1 >
    2,<keyword 2 >
    3,<keyword 3 >
    4,<keyword 4 >
    ...
    ```

* Step 3 :
    Generate urls from each keywords.
    ```shell
    # arguments:
    #   -h, --help            show this help message and exit
    #   --keywords            keywords file from step 2
    #   --out_dir             output dir of urls (.txt)
    #   --limit_per_word      limit query number of each keywords

    # example:
    python keywords2urls.py --keywords ./test_keywords.csv --out_dir img_list --limit_per_word 10000
    ```
* Step 4 :
    Parse the whole urls and save to image files.
    
    ```shell
    # arguments:
    #   -h, --help            show this help message and exit
    #   --in_dir              input dir (output dir from Step 3)
    #   --out_dir             output dir of images

    # example:
    python parsing_by_list.py --in_dir ./img_list --out_dir images
    ```
    
    
    
    
    
    
    
    
    
    
