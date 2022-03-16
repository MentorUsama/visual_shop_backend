from visualshop.utility.request import Success,SerilizationFailed
from rest_framework.views import APIView
class GetProductByImage(APIView):
    def post(self,request,format=None):
        if 'image' not in request.FILES:
            return SerilizationFailed({"productIdList":"Please provide image"})
        print(request.FILES['image'])
        return Success("ok")
        