import csv
import urllib2
import urllib
import os
import Queue
import argparse
from threading import Thread
import time

from lib.config import random_header
from lib.utils import mkdirs

example_text = '''example:

python parsing_by_list.py --in_dir ./img_list --out_dir images

'''





def argparer():
    parser = argparse.ArgumentParser( epilog=example_text,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--in_dir', required=True, dest="in_dir", type=str, help="input dir ")
    parser.add_argument('--out_dir', required=True, dest="out_dir", type=str, help="out_dir")
    
    args = parser.parse_args()

    return args

# something ugly global vars
args = argparer()
OutputDir = args.out_dir
header = random_header
filtersize = 110000
Image_download_count = 0
terminate = False
q = Queue.Queue()


def download_page_by_url(url):
    global Image_download_count
    image_type = 'img'
    try:
        req = urllib2.Request(url, headers=header)
        raw_img = urllib2.urlopen(req).read()
        filesize = raw_img.__sizeof__()
        print 'file size : ',filesize
        if filesize > filtersize:
            filename = image_type + "_"+ str(Image_download_count)
            Image_download_count += 1
            print 'downloaded : '+filename + ' : ' + url
            mkdirs(OutputDir)
            f = open(os.path.join(OutputDir,filename+".jpg"), 'wb')
            f.write(raw_img)
            f.close()
    except Exception as e:
        print "could not load : "+url
        print e
    
        
def grab_data_from_queue():
    global terminate
    while not q.empty() and not terminate: # check that the queue isn't empty
        image_url = q.get() # print the item from the queue
        try_count = 0
        try:
            #print 'load : ',image_url
            download_page_by_url(image_url)
        except:
            print '>failed : ',image_url
            time.sleep(2)
    print "task end!"
    q.task_done() # specify that you are done with the item


def main():
    
    global terminate

    in_files = [os.path.join(args.in_dir,i) 
            for i in os.listdir(args.in_dir) if '.txt' in i]
    

    image_list =[] 
    for imglistpath in in_files:
        image_list += list(csv.reader(open(imglistpath)))

    

    
    for photo in image_list:
        q.put(photo[0]) 

    jobs = []
    for i in range(20): # aka number of threads
        t1 = Thread(target = grab_data_from_queue) # target is the above function
        jobs.append(t1)

    # Start the processes (i.e. calculate the random number lists)		
    for j in jobs:
        j.start()

    #Listening KeyboardInterrupt
    while not terminate:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            terminate = True
    # Ensure all of the processes have finished
    for j in jobs:
        j.join()
        
    
if __name__ == "__main__":
    main()