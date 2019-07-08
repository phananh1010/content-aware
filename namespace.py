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

#class structure constant, this is the class existed in VOC, which will be used in our system
CLASS_LIST = {AIRPLANE, BICYCLE, BIRD, BUS, CAR, CAT, MOTORCYCLE, SHEEP, TRAIN, DOG}
CLASS_DICT = {AIRPLANE:1, BICYCLE:2, BIRD:3, BUS:4, CAR:5, CAT:6, MOTORCYCLE:7, SHEEP:8, TRAIN:9, DOG:10}

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
              10: "cow",
              11: "diningtable",
              12: DOG,
              13: "horse",
              14: MOTORCYCLE,
              15: "person",
              16: "pottedplant",
              17: SHEEP,
              18: "sofa",
              19: TRAIN,
              20: "tvmonitor"
}

YOUTUBE_CLASS_DICT = {0: 'person', 1: BIRD, 2: BICYCLE, 3: WATERCRAFT, 4: BUS, 5: 'bear', 6: 'cow', 7: CAT, 8: 'giraffe', 9: 'potted plant', 10: 'horse', 11: MOTORCYCLE, 12: 'knife', 13: AIRPLANE, 14: 'skateboard', 15: TRAIN, 16: 'truck', 17: 'zebra', 18: 'toilet', 19: DOG, 20: 'elephant', 21: 'umbrella', 23: CAR}

FILEPATH_IMAGENET_ANNOTATION = './imagenet_labels'                     #raw annotation IMAGE_NET VID
FILEPATH_SSD_WEIGHT = './ssd/weights/ssd300_mAP_77.43_v2.pth'          #model weight ssd 300x300
FILEPATH_LOG_VIDEOMETAINFO = './data/VID_data/log_allvid_metainfo.txt' #videos metainfo (HxW, bitrate, filename)
FILEPATH_VID_DIRTOKEN_DICT = './data/VID_data/vid_dirtoken_dict'

DIRPATH_VID_FRAMES = './data/VID_data/scaled/'
DIRPATH_VID_mAP_LINES = './data/VID_data/'

FILETEMPLATE_mAP_LINES = 'mAP_line_{}'