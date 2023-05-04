from django.db import models


# 상품 기본 정보
class Product(models.Model):
    image = models.TextField()  # 사진 파일 이름
    product_name = models.TextField()  # 작품 이름
    product_size = models.TextField()  # 사진 사이즈 A3 A2
    buy_now = models.IntegerField()  # 즉시 구매가
    current_price = models.IntegerField()  # 현재 최고 입찰가
    frame = models.TextField(default="X")  # 액자 유무
    sold = models.TextField(default=False)  # 판매 여부


# 입찰 정보
class Bid(models.Model):
    bidded_at = models.DateTimeField(auto_now_add=True)  # 입찰 시각
    product_name = models.TextField()  # 작품 이름
    bid_price = models.IntegerField()  # 입찰가
    bidder_name = models.TextField()  # 입찰자 이름
    bidder_phone = models.TextField(max_length=11)  # 핸드폰 번호
    bidder_email = models.EmailField()  # 이메일

