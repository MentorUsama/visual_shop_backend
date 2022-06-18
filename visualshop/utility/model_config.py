from visualshop.settings import STATIC_ROOT

NUM_WORKERS = 0
DUMPED_MODEL = "low_resolution_model.tar"
DATASET_BASE = STATIC_ROOT
CROP_SIZE = 224
INTER_DIM = 512
CATEGORIES = 20
COLOR_TOP_N = 10
ENABLE_TRIPLET_WITH_COSINE = False  # Buggy when backward...
COLOR_WEIGHT = 0.1
DISTANCE_METRIC = ('euclidean', 'euclidean')
FREEZE_PARAM = False