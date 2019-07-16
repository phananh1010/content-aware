#class names are string to link class id between dataset
AIRPLANE = 'airplane'
BICYCLE = 'bicycle'
BIRD = 'bird'
BUS = 'bus'
CAR = 'car'
CAT = 'domestic_cat'
MOTORCYCLE = 'motorcycle'
SHEEP = 'sheep'
TRAIN = "train"
DOG = 'dog'
WATERCRAFT = 'watercraft'
PERSON = 'person'
HORSE = 'horse'
POTTEDPLANT = 'potted_plant'
COW = 'cow'

#class structure constant, this is the class existed in VOC, which will be used in our system
CLASS_INDEX = ['N/A', AIRPLANE, BICYCLE, BIRD, BUS, CAR, CAT, MOTORCYCLE, SHEEP, TRAIN, DOG, WATERCRAFT, PERSON, HORSE, POTTEDPLANT, COW]
CLASS_LIST = {AIRPLANE, BICYCLE, BIRD, BUS, CAR, CAT, MOTORCYCLE, SHEEP, TRAIN, DOG, WATERCRAFT, PERSON, HORSE, POTTEDPLANT, COW}
CLASS_DICT = {AIRPLANE:1, BICYCLE:2, BIRD:3, BUS:4, CAR:5, CAT:6, MOTORCYCLE:7, SHEEP:8, TRAIN:9, DOG:10, WATERCRAFT:11, PERSON:12, HORSE:13, POTTEDPLANT:14, COW:15}

#BBOX MATCHING RESULT CONSTANT
BBOX_MATCH_FN = 'false_negative'
BBOX_MATCH_TP = 'true_positive'
BBOX_MATCH_FP = 'false_positive'

#IOU THRESHOLD
THRESHOLD_IOU = .5
THRESHOLD_CONFIDENCE = 0.3

VID_CLASS_DICT = {
                    'n02691156': AIRPLANE,
                    'n02419796': "antelope",
                    'n02131653': "bear",
                    'n02834778': BICYCLE,
                    'n01503061': BIRD,
                    'n02924116': BUS,
                    'n02958343': CAR,
                    'n02402425': "cattle",
                    'n02084071': DOG,
                    'n02121808': CAT,
                    'n02503517': "elephant",
                    'n02118333': "fox",
                    'n02510455': "giant_panda",
                    'n02342885': "hamster",
                    'n02374451': "horse",
                    'n02129165': "lion",
                    'n01674464': "lizard",
                    'n02484322': "monkey",
                    'n03790512': MOTORCYCLE,
                    'n02324045': "rabbit",
                    'n02509815': "red_panda",
                    'n02411705': SHEEP,
                    'n01726692': "snake",
                    'n02355227': "squirrel",
                    'n02129604': "tiger",
                    'n04468005': TRAIN,
                    'n01662784': "turtle",
                    'n04530566': WATERCRAFT,
                    'n02062744': "whale",
                    'n02391049': "zebra"}

VOC_CLASS_DICT = {0: "background",
              1: AIRPLANE,
              2: BICYCLE,
              3: BIRD,
              4: WATERCRAFT,
              5: "bottle",
              6: BUS,
              7: CAR,
              8: CAT,
              9: "chair",
              10: COW,
              11: "diningtable",
              12: DOG,
              13: HORSE,
              14: MOTORCYCLE,
              15: PERSON,
              16: "pottedplant",
              17: SHEEP,
              18: "sofa",
              19: TRAIN,
              20: "tvmonitor"
}

YOUTUBE_CLASS_DICT = {0: PERSON, 1: BIRD, 2: BICYCLE, 3: WATERCRAFT, 4: BUS, 5: 'bear', 6: COW, 7: CAT, 8: 'giraffe', 9: POTTEDPLANT, 10: HORSE, 11: MOTORCYCLE, 12: 'knife', 13: AIRPLANE, 14: 'skateboard', 15: TRAIN, 16: 'truck', 17: 'zebra', 18: 'toilet', 19: DOG, 20: 'elephant', 21: 'umbrella', 23: CAR}

RESOLUTION_LIST=(1080, 1080, 1080, 1080, 1080, 1080, 1080, 720, 720, 720, 720, 720, 720, 720, 480, 480, 480, 480, 480, 480, 360, 360, 360, 360, 360, 240, 240, 240, 240, 144, 144, 144)
BITRATE_LIST=('2048k', '1024k', '512k', '256k', '128k', '64k', '32k', '2048k', '1024k', '512k', '256k', '128k', '64k', '32k', '1024k', '512k', '256k', '128k', '64k', '32k', '512k', '256k', '128k', '64k', '32k', '256k', '128k', '64k', '32k', '128k', '64k', '32k')
NO_RESOLUTION_LEVELS = len(RESOLUTION_LIST)

##############################END OF DATA DECLARATION####################

######ENVIRONMENT DECLARATION#######
DIRPATH_HOME = '/home/u9167/content_aware'

FILEPATH_IMAGENET_ANNOTATION = './imagenet_labels'                     #raw annotation IMAGE_NET VID
FILEPATH_SSD_WEIGHT = './ssd/weights/ssd300_mAP_77.43_v2.pth'          #model weight ssd 300x300
FILEPATH_LOG_VIDEOMETAINFO = './data/VID_data/log_allvid_metainfo.txt' #videos metainfo (HxW, bitrate, filename)
FILEPATH_VID_DIRTOKEN_DICT = './data/VID_data/vid_dirtoken_dict'

DIRPATH_VID_FRAMES = './data/VID_data/scaled/'
DIRPATH_VID_mAP_LINES = './data/VID_data/'

DIRPATH_SCRIPTS = DIRPATH_HOME + '/' + 'scripts'
DIRPATH_DATA = DIRPATH_HOME + '/' + 'data'
DIRPATH_YOUTUBE_DATA = DIRPATH_DATA + '/' + 'YOUTUBE_data'
DIRPATH_YOUTUBE_VIDEOS = DIRPATH_YOUTUBE_DATA + '/' + 'videos'

FILEPATH_SCRIPTS_GETINFO = DIRPATH_SCRIPTS + '/' + 'get_info.sh'

FILEPATH_YOUTUBE_RAWANNOCSV = DIRPATH_YOUTUBE_DATA + '/' + 'yt_bb_detection_train_filtered.pkl.gz'
FILEPATH_YOUTUBE_YANNODICT = DIRPATH_YOUTUBE_DATA + '/' + 'yanno_dict'
#meta info about raw videos
FILEPATH_YOUTUBE_VID_METAINFO = DIRPATH_YOUTUBE_DATA + '/' + 'vid_metainfo.txt'
#meta info about segment in different bitrate & resolutions
FILEPATH_YOUTUBE_SEGMENT_METAINFO = DIRPATH_YOUTUBE_DATA + '/' + 'segment_metainfo.txt' 
#prediction results for each videos in the segment
FILEPATH_YOUTUBE_SEGMENT_PREDRESULT = DIRPATH_YOUTUBE_DATA + '/' + 'segment_predresult.txt' 


FILETEMPLATE_mAP_LINES = 'mAP_line_{}'
FILETEMPLATE_FRAMEID = '{0:06d}'