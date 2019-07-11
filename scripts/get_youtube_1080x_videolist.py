#TODO: list all video that has 1080x1920 resolutions
#INPUT: csv files contain videos in train dataset. Source: https://research.google.com/youtube-bb/
#OUTPUT: list of video id which has resolution 1080x1920
import pandas as pd
import numpy as np
import requests

HOME = '/home/u9167/content_aware/data/YOUTUBE_data/'
#get list of all youtube id
df = pd.DataFrame.from_csv(HOME + 'yt_bb_detection_train.csv')
#now extract youtube id_list
col1 = df.iloc[:,0]
id_list = sorted(list(set(col1.keys())))
np.random.seed(0)#so that next time we can repeat this experiement
np.random.shuffle(id_list)

#crawl the website, search for 1920x1080 videos only
#    then, output the video ID into file
print 'begin crawling'
with open(HOME + 'youtube_1080_vidlist.txt', 'a') as f:
    url_template="http://www.youtube.com/watch?v={}"
    for idx, vid in enumerate(id_list[87200:]):
        if idx % 100 == 0:
            print 'processing {}\t{}'.format(idx, vid)
        url = url_template.format(vid)
        r = requests.get(url=url)
        pos = r.content.find('1920x1080')
        if pos >=0: 
            print vid
            print r.content[pos:pos+200]
            print '-----'
            f.writelines('{}\n'.format(vid))
            f.flush()
