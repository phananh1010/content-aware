all split.sh files receives filename as argument. The file contains list of videos to be processed (instead of using folders like before)
to create such filelist, execute this command:
for f in /home/u9167/content_aware/data/YOUTUBE_data/videos/7/*.mp4; do printf "${f}\n" >> filelist/7.txt; done
Then, in the qsub script, specify the number, the script will look to the filelist folder and find the file with name match the provided number.
