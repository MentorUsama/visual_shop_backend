from visualshop.utility.request import Success,SerilizationFailed
from rest_framework.views import APIView
import os
from visualshop.settings import STATIC_ROOT

# model related imports
from torchvision import models
from PIL import Image
import torch
from shop.core.utility.transform_image import transform



class GetProductByImage(APIView):
    def post(self,request,format=None):
        if 'image' not in request.FILES:
            return SerilizationFailed({"productIdList":"Please provide image"})
        # Getting the pretrained model
        alexnet = models.alexnet(pretrained=True)
        # getting the uploaded image
        img=Image.open(request.FILES['image'])
        # transforming the image
        img_t = transform(img)
        # evaluation
        batch_t = torch.unsqueeze(img_t, 0)
        alexnet.eval()
        out = alexnet(batch_t)
        # Getting the label of the output
        url = STATIC_ROOT + "/imagenet_classes.txt"
        with open(url) as f:
            classes = [line.strip() for line in f.readlines()]
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

        best_match=classes[index[0]], percentage[index[0]].item()
        _, indices = torch.sort(out, descending=True)
        all_matches=[(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]          
        result={
            'all_match':all_matches,
            'best_matches':best_match
        }
        return Success(result)
        