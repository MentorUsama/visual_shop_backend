from torchvision import models
from PIL import Image
import torch
from visualshop.settings import STATIC_ROOT
from shop.core.utility.transform_image import transform
def get_model_result(image):
    # Getting the pretrained model
    alexnet = models.alexnet(pretrained=True)
    # getting the uploaded image
    img=Image.open(image)
    # transforming the image
    img_t = transform(img)
    # evaluation
    batch_t = torch.unsqueeze(img_t, 0)
    alexnet.eval()
    out = alexnet(batch_t)
    # Getting the label of the output
    url = STATIC_ROOT + "/imagenet_classes.txt"
    classes=[]
    with open(url) as f:
        # classes = [line.strip() for line in f.readlines()]
        for line in f.readlines():
            full_line=line.strip()
            label=full_line.split(',',1)[1]
            classes.append(label.strip())
    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)
    all_matches=[(classes[idx], percentage[idx].item()) for idx in indices[0][:5]] 
    return all_matches