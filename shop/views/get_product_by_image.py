from visualshop.utility.request import Success,SerilizationFailed
from rest_framework.views import APIView
# model related imports
from shop.core.utility.get_model_result import get_model_result



class GetProductByImage(APIView):
    def post(self,request,format=None):
        if 'image' not in request.FILES:
            return SerilizationFailed({"productIdList":"Please provide image"})
        result=get_model_result(request.FILES['image'])    
        return Success(result)
        