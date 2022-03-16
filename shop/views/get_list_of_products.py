from rest_framework.views import APIView
from visualshop.utility.request import Success,SerilizationFailed
# getting models
from shop.models.Product import Product
from shop.serialization import ProductSerializer

class GetListOfProducts(APIView):
    def post(self, request, format=None):
        data = request.data
        if not "productIdList" in data.keys():
            return SerilizationFailed({"productIdList":"Please Provide The List Of Product To Fetch"})
        products=Product.objects.filter(id__in=data['productIdList'])
        serializer=ProductSerializer(products,many=True,context={'request': request})
        return Success(serializer.data)