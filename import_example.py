## Deep leanring
import torch.nn as nn
from  torch.utils.data import Dataset,DataLoader
import torch
import torchvision

# Data agumentation
import albumentations as A
from albumentations.pytorch import ToTensorV2


# Machine learning
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import QuantileTransformer
from xgboost import XGBClassifier
from catboost import CatBoostClassifier,CatBoostRegressor, Pool, EShapCalcType, EFeaturesSelectionAlgorithm
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from imblearn.over_sampling import KMeansSMOTE,SMOTE,SVMSMOTE
from imblearn.under_sampling import EditedNearestNeighbours


import pandas as pd
import numpy as np
import cv2

# 畫圖
import matplotlib.pyplot as plt
import seaborn as sns

# 進度條
from tqdm.notebook import tqdm

from time import sleep
import warnings

from glob import glob
import os,sys

#sys.path.append('../input/coolshan-coding-utils')
#from confusion_matrix_pretty_print import pp_matrix_from_data
#from logger import Logger
#from model_instance import ModelInstance
warnings.filterwarnings("ignore")