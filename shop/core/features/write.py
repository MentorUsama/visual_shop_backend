# from shop.models.Features import Features
# def bulk_create(features,image_id,product_id):
#     objects = []
#     for feature in features:
#         objects.append(
#             Features(
#                 feature=feature[0],
#                 percentage=float(feature[1]),
#                 imageId=image_id,
#                 productId=product_id
#             ))
#     Features.objects.bulk_create(objects)