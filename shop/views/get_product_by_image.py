from rest_framework.views import APIView
from torch import classes
# model related imports
from shop.core.utility.get_model_result import get_model_result
from visualshop.utility.request import SerilizationFailed,Success,NotFound,unAuthrized
from shop.models.Features import Features
from shop.serialization import FeatureSerializer
from shop.serialization import ProductSerializer
from shop.models.Product import Product



class GetProductByImage(APIView):
    def post(self,request,format=None):
        if 'image' not in request.FILES:
            return SerilizationFailed({"productIdList":"Please provide image"})
        
        # Getting all the features of the image with percentage greater then 50 (note: data is sorted by max percent first)
        features_detected=get_model_result(request.FILES['image'])  
        print(features_detected)
        if len(features_detected)==0:
            return NotFound({"message":"Unable to detect any features from the image"})

        # Getting the label of the feature detected from the image
        features_detected_labels=[]
        for feature_detected in features_detected:
            features_detected_labels.append(feature_detected[0])

        # Getting all the features according to the labels
        saved_features=Features.objects.filter(feature__in=features_detected_labels).order_by('feature')
        if saved_features.count()==0:
            return NotFound({"message":"No product found with the given feature"})
        saved_features_serialized=FeatureSerializer(saved_features,many=True)
        saved_features_serialized_data=saved_features_serialized.data

        # Sort the features according to the best match label
        saved_features_serialized_data_sorted=[]
        for features_detected_label in features_detected_labels:
            for data in saved_features_serialized_data:
                if data['feature'] == features_detected_label:
                    saved_features_serialized_data_sorted.append(data)

        saved_features_serialized_data_sorted_unique=[]
        products_id_found=[]
        for saved_feature in saved_features_serialized_data_sorted:
            if saved_feature['productId'] not in products_id_found:
                saved_features_serialized_data_sorted_unique.append(saved_feature)
                products_id_found.append(saved_feature['productId'])

        # Getting the products
        products=Product.objects.filter(id__in=products_id_found)
        products_serailizer=ProductSerializer(products,many=True,context={'request': request})
        products_serailizer_data=products_serailizer.data
        products_serailizer_data_sorted=[]

        # sorting the prodct for the best match first
        for product_id in products_id_found:
            for product_serailizer_data in products_serailizer_data:
                if product_serailizer_data['id']==product_id:
                    products_serailizer_data_sorted.append(product_serailizer_data)
                    break

        return Success(data={'features':saved_features_serialized_data_sorted_unique,'products':products_serailizer_data_sorted})
        