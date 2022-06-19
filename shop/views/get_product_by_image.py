from rest_framework.views import APIView
# model related imports
from visualshop.utility.request import Success,SerilizationFailed
from visualshop.settings import STATIC_URL,BASE_DIR
from django.core.files.storage import FileSystemStorage
import uuid
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


class GetProductByImage(APIView):
    def post(self, request, format=None):
        # Getting image
        if 'image' not in request.FILES:
            return SerilizationFailed({"image":["Please provide image"]})
        image=request.FILES['image']
        filename = str(uuid.uuid4())
        image.name=filename


        path = os.path.join(BASE_DIR,"static","images",filename)
        fs = FileSystemStorage()
        image_url = fs.save(path, image)

        # Extracting Feature
        deep_feats, color_feats, labels = load_feat_db()
        if(len(deep_feats) == 0 or len(color_feats) == 0) or len(labels)==0:
            return SerilizationFailed({"message": "Unable To Load Any Feature"})
        
        # Extractig Feature
        extractor = load_test_model()
        f = dump_single_feature(image_url, extractor)
        if any(list(map(lambda x: x is None, f))):
            return SerilizationFailed({"message": "Unable To fetch any feature from given image"})

        # Finding The Product With Similar Feature
        number_of_products=len(deep_feats) if len(deep_feats)<5 else 5
        query_results = naive_query(f, deep_feats, color_feats, labels, number_of_products)
        # clf = load_kmeans_model()
        # result = kmeans_query(clf, f, deep_feats, color_feats, labels, 5)
        if len(query_results)==0:
            return SerilizationFailed({"message": "No Related Product Found In Database"})

        # Getting product and image id
        new_query_result=[]
        for query_result in query_results:
            splited_image=query_result[0].split()
            splited_image.append(query_result[1])
            new_query_result.append(splited_image)
        return Success(data={"result": "will test soon"})
