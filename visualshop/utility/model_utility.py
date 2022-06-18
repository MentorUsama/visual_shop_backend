from visualshop.settings import BASE_DIR
from visualshop.utility.model_config import *
from PIL import Image
import os
import torch.utils.data as data
import random
import numpy as np
import torch
from torch.autograd import Variable
import joblib
import torch.nn as nn
from torchvision import transforms
import torch.nn.functional as F


import torch
import torchvision
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

data_transform_test = transforms.Compose([
    # transforms.Scale(CROP_SIZE),
    transforms.Resize(CROP_SIZE),
    transforms.CenterCrop(CROP_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


class Fashion_attr_prediction(data.Dataset):
    def __init__(self, type="train", transform=None, target_transform=None, crop=False, img_path=None):
        self.transform = transform
        self.target_transform = target_transform
        self.crop = crop
        # type_all = ["train", "test", "all", "triplet", "single"]
        self.type = type
        if type == "single":
            self.img_path = img_path
            return
        self.train_list = []
        self.train_dict = {i: [] for i in range(CATEGORIES)}
        self.test_list = []
        self.all_list = []
        self.bbox = dict()
        self.anno = dict()
        self.read_partition_category()
        self.read_bbox()

    def __len__(self):
        if self.type == "all":
            return len(self.all_list)
        elif self.type == "train":
            return len(self.train_list)
        elif self.type == "test":
            return len(self.test_list)
        else:
            return 1

    def read_partition_category(self):
        list_eval_partition = os.path.join(
            DATASET_BASE, r'Eval', r'list_eval_partition.txt')
        list_category_img = os.path.join(
            DATASET_BASE, r'Anno', r'list_category_img.txt')
        partition_pairs = self.read_lines(list_eval_partition)
        category_img_pairs = self.read_lines(list_category_img)
        for k, v in category_img_pairs:
            v = int(v)
            if v <= 20:
                self.anno[k] = v - 1
        for k, v in partition_pairs:
            if k in self.anno:
                if v == "train":
                    self.train_list.append(k)
                    self.train_dict[self.anno[k]].append(k)
                else:
                    # Test and Val
                    self.test_list.append(k)
        self.all_list = self.test_list + self.train_list
        random.shuffle(self.train_list)
        random.shuffle(self.test_list)
        random.shuffle(self.all_list)

    def read_bbox(self):
        list_bbox = os.path.join(DATASET_BASE, r'Anno', r'list_bbox.txt')
        pairs = self.read_lines(list_bbox)
        for k, x1, y1, x2, y2 in pairs:
            self.bbox[k] = [x1, y1, x2, y2]

    def read_lines(self, path):
        with open(path) as fin:
            lines = fin.readlines()[2:]
            lines = list(filter(lambda x: len(x) > 0, lines))
            pairs = list(map(lambda x: x.strip().split(), lines))
        return pairs

    def read_crop(self, img_path):
        img_full_path = os.path.join(DATASET_BASE, img_path)
        with open(img_full_path, 'rb') as f:
            with Image.open(f) as img:
                img = img.convert('RGB')
        if self.crop:
            x1, y1, x2, y2 = self.bbox[img_path]
            if x1 < x2 <= img.size[0] and y1 < y2 <= img.size[1]:
                img = img.crop((x1, y1, x2, y2))
        return img

    def __getitem__(self, index):
        if self.type == "triplet":
            img_path = self.train_list[index]
            target = self.anno[img_path]
            img_p = random.choice(self.train_dict[target])
            img_n = random.choice(self.train_dict[random.choice(
                list(filter(lambda x: x != target, range(20))))])
            img = self.read_crop(img_path)
            img_p = self.read_crop(img_p)
            img_n = self.read_crop(img_n)
            if self.transform is not None:
                img = self.transform(img)
                img_p = self.transform(img_p)
                img_n = self.transform(img_n)
            return img, img_p, img_n

        if self.type == "single":
            img_path = self.img_path
            img = self.read_crop(img_path)
            if self.transform is not None:
                img = self.transform(img)
            return img

        if self.type == "all":
            img_path = self.all_list[index]
        elif self.type == "train":
            img_path = self.train_list[index]
        else:
            img_path = self.test_list[index]
        target = self.anno[img_path]
        img = self.read_crop(img_path)

        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, img_path if self.type == "all" else target


def load_kmeans_model():
    clf_model_path = os.path.join(DATASET_BASE, 'kmeans.m')
    clf = joblib.load(clf_model_path)
    return clf


def load_feat_db():
    feat_all = os.path.join(DATASET_BASE,'all_feat.npy')
    feat_list = os.path.join(DATASET_BASE,'all_feat.list')
    color_feat = os.path.join(DATASET_BASE,'all_color_feat.npy')
    if not os.path.isfile(feat_list) or not os.path.isfile(feat_all) or not os.path.isfile(color_feat):
        print("No feature db file! Please run feature_extractor.py first.")
        return
    deep_feats = np.load(feat_all)
    color_feats = np.load(color_feat)
    with open(feat_list) as f:
        labels = list(map(lambda x: x.strip(), f.readlines()))
    return deep_feats, color_feats, labels


def dump_single_feature(img_path, extractor):
    paths = [img_path, os.path.join(DATASET_BASE, img_path), os.path.join(
        DATASET_BASE, 'in_shop', img_path)]
    for i in paths:
        if not os.path.isfile(i):
            continue
        single_loader = torch.utils.data.DataLoader(
            Fashion_attr_prediction(
                type="single", img_path=i, transform=data_transform_test),
            batch_size=1, num_workers=NUM_WORKERS, pin_memory=True
        )
        data = list(single_loader)[0]
        data = Variable(data)
        deep_feat, color_feat = extractor(data)
        deep_feat = deep_feat[0].squeeze()
        color_feat = color_feat[0]
        return deep_feat, color_feat
    return None


def dump_single_feature(img_path, extractor):
    paths = [img_path, os.path.join(DATASET_BASE, img_path), os.path.join(
        DATASET_BASE, 'in_shop', img_path)]
    print("===========================",paths)
    for i in paths:
        if not os.path.isfile(i):
            continue
        single_loader = torch.utils.data.DataLoader(
            Fashion_attr_prediction(
                type="single", img_path=i, transform=data_transform_test),
            batch_size=1, num_workers=NUM_WORKERS, pin_memory=True
        )
        data = list(single_loader)[0]
        data = Variable(data)
        deep_feat, color_feat = extractor(data)
        deep_feat = deep_feat[0].squeeze()
        color_feat = color_feat[0]
        return deep_feat, color_feat
    return None


def load_model(path=None):
    full = path
    for i in [path, full]:
        if os.path.isfile(i):
            return torch.load(i, map_location=torch.device('cpu'))
    return None


class f_model(nn.Module):
    '''
    input: N * 3 * 224 * 224
    output: N * num_classes, N * inter_dim, N * C' * 7 * 7
    '''

    def __init__(self, freeze_param=False, inter_dim=INTER_DIM, num_classes=CATEGORIES, model_path=None):
        super(f_model, self).__init__()
        self.backbone = torchvision.models.resnet50(pretrained=True)
        state_dict = self.backbone.state_dict()
        num_features = self.backbone.fc.in_features
        self.backbone = nn.Sequential(*list(self.backbone.children())[:-2])
        model_dict = self.backbone.state_dict()
        model_dict.update(
            {k: v for k, v in state_dict.items() if k in model_dict})
        self.backbone.load_state_dict(model_dict)
        if freeze_param:
            for param in self.backbone.parameters():
                param.requires_grad = False

        self.avg_pooling = nn.AvgPool2d(7, stride=1)
        self.fc = nn.Linear(num_features, inter_dim)
        self.fc2 = nn.Linear(inter_dim, num_classes)
        state = load_model(model_path)
        if state:
            new_state = self.state_dict()
            new_state.update(
                {k: v for k, v in state.items() if k in new_state})
            self.load_state_dict(new_state)

    def forward(self, x):
        x = self.backbone(x)
        pooled = self.avg_pooling(x)
        inter_out = self.fc(pooled.view(pooled.size(0), -1))
        out = self.fc2(inter_out)
        return out, inter_out, x


class c_model(nn.Module):
    '''
    input: N * C * 224 * 224
    output: N * C * 7 * 7
    '''

    def __init__(self, pooling_size=32):
        super(c_model, self).__init__()
        self.pooling = nn.AvgPool2d(pooling_size)

    def forward(self, x):
        return self.pooling(x)


class p_model(nn.Module):
    '''
    input: N * C * W * H
    output: N * 1 * W * H
    '''

    def __init__(self):
        super(p_model, self).__init__()

    def forward(self, x):
        n, c, w, h = x.size()
        x = x.view(n, c, w * h).permute(0, 2, 1)
        pooled = F.avg_pool1d(x, c)
        return pooled.view(n, 1, w, h)

class FeatureExtractor(nn.Module):
    def __init__(self, deep_module, color_module, pooling_module):
        super(FeatureExtractor, self).__init__()
        self.deep_module = deep_module
        self.color_module = color_module
        self.pooling_module = pooling_module
        self.deep_module.eval()
        self.color_module.eval()
        self.pooling_module.eval()

    def forward(self, x):
        cls, feat, conv_out = self.deep_module(x)
        color = self.color_module(x).cpu().data.numpy()  # N * C * 7 * 7
        weight = self.pooling_module(conv_out).cpu().data.numpy()  # N * 1 * 7 * 7
        result = []
        for i in range(cls.size(0)):
            weight_n = weight[i].reshape(-1)
            idx = np.argpartition(weight_n, -COLOR_TOP_N)[-COLOR_TOP_N:][::-1]
            color_n = color[i].reshape(color.shape[1], -1)
            color_selected = color_n[:, idx].reshape(-1)
            result.append(color_selected)
        return feat.cpu().data.numpy(), result

def load_test_model():
    if not os.path.isfile(DUMPED_MODEL) and not os.path.isfile(os.path.join(DATASET_BASE,DUMPED_MODEL)):
        print("No trained model file!")
        return
    main_model = f_model(model_path=DUMPED_MODEL)
    color_model = c_model()
    pooling_model = p_model()
    extractor = FeatureExtractor(main_model, color_model, pooling_model)
    return extractor


def naive_query(features, deep_feats, color_feats, labels, retrieval_top_n=5):
    results = get_deep_color_top_n(features, deep_feats, color_feats, labels, retrieval_top_n)
    return results

def get_deep_color_top_n(features, deep_feats, color_feats, labels, retrieval_top_n=5):
    deep_scores = get_similarity(features[0], deep_feats, DISTANCE_METRIC[0])
    color_scores = get_similarity(features[1], color_feats, DISTANCE_METRIC[1])
    results = get_top_n(deep_scores + color_scores * COLOR_WEIGHT, labels, retrieval_top_n)
    return results

def get_deep_color_top_n(features, deep_feats, color_feats, labels, retrieval_top_n=5):
    deep_scores = get_similarity(features[0], deep_feats, DISTANCE_METRIC[0])
    color_scores = get_similarity(features[1], color_feats, DISTANCE_METRIC[1])
    results = get_top_n(deep_scores + color_scores * COLOR_WEIGHT, labels, retrieval_top_n)
    return results


def get_similarity(feature, feats, metric='cosine'):
    dist = -cdist(np.expand_dims(feature, axis=0), feats, metric)[0]
    return dist

def get_top_n(dist, labels, retrieval_top_n):
    ind = np.argpartition(dist, -retrieval_top_n)[-retrieval_top_n:][::-1]
    ret = list(zip([labels[i] for i in ind], dist[ind]))
    ret = sorted(ret, key=lambda x: x[1], reverse=True)
    return ret

def kmeans_query(clf, features, deep_feats, color_feats, labels, retrieval_top_n=5):
    label = clf.predict(features[0].reshape(1, features[0].shape[0]))
    ind = np.where(clf.labels_ == label)
    d_feats = deep_feats[ind]
    c_feats = color_feats[ind]
    n_labels = list(np.array(labels)[ind])
    results = get_deep_color_top_n(features, d_feats, c_feats, n_labels, retrieval_top_n)
    return results
