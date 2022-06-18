from rest_framework.views import APIView
# model related imports
from visualshop.utility.request import Success,SerilizationFailed
# model realted imports
import torch
from torchvision import transforms
from PIL import Image
import torchvision
import os
import joblib
import torch.utils.data as data
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
# model related utility
from visualshop.utility.model_config import *
from visualshop.utility.model_utility import *


class Test(APIView):
    def post(self, request, format=None):
        # Getting image
        if 'image' not in request.FILES:
            return SerilizationFailed({"image":["Please provide image"]})
        image=request.FILES['image']

        # Extracting Feature
        deep_feats, color_feats, labels = load_feat_db()
        if(deep_feats.size == 0 or color_feats.size == 0):
            return SerilizationFailed({"message": "Unable To Load Any Feature"})
        
        # Extractig Feature
        extractor = load_test_model()
        f = dump_single_feature(image, extractor)
        if any(list(map(lambda x: x is None, f))):
            return SerilizationFailed({"message": "Unable To fetch any feature from given image"})

        # clf = load_kmeans_model()
        # result = naive_query(f, deep_feats, color_feats, labels, 5)
        # result_kmeans = kmeans_query(clf, f, deep_feats, color_feats, labels, 5)
        return Success(data={"result": "will test soon"})
