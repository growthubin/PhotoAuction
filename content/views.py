from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Product, Bid
import json
from django.core.mail import EmailMessage


# Create your views here.
class Main(APIView):
    def get(self, request):
        product_list = Product.objects.all()  # Product의 모든 데이터를 가져오겠다

        content = {'products': product_list}
        return render(request, "auction/main2.html", context=content)


class SearchResult(APIView):
    def get(self, request):
        query = None
        product = None

        # 사용자가 입력한 kw 중에 같은 거 있으면(filter) 보내주기
        if 'kw' in request.GET:
            query = request.GET.get('kw')
            product = Product.objects.all().filter(
                Q(product_name__icontains=query)
            )

            # 추후, 원래 있던 content_product DB에 상세  이미지 (단독컷 2개, 단체컷 하나) 추가할 예정
            # db를 하나 더 쌓을 수도...(Model)
            return render(request, "content/product_detail.html", context=dict(products=product))

        # else:
        # message: 검색 결과가 없습니다


# POST /submit/
class PostForm(APIView):
    def post(self, request):
        json_object = json.loads(request.body)
        product = Product.objects.filter(product_name=json_object["product_name"])

        product_name = json_object.get("product_name")
        bidder_name = json_object.get('bidder_name')
        bid_price = json_object.get('bid_price')
        bidder_phone = json_object.get('bidder_phone')
        bidder_email = json_object.get('bidder_email')

        # Product의 current price와 비교했을 때, bid_price가 더 크면 Bid 업데이트
        if json_object.get('bid_price') > product[0].current_price:
            bid_list = Bid.objects.create(
                product_name=product_name,
                bidder_name=bidder_name,
                bid_price=bid_price,
                bidder_phone=bidder_phone,
                bidder_email=bidder_email
            )
            bid_list.save()
            send_email(bidder_email,bidder_name,product_name,bid_price)
            print('이메일 발송')

            # 현재 가격 업데이트
            for product1 in product:
                # 즉시구매를 했거나 입찰가가 최대에 도달한 경우
                if bid_price == product1.buy_now:
                    product1.sold = True
                    product1.current_price = 0
                    product1.save()

                    print(product1.product_name, ' 즉시 구매 ', product1.sold, ' 판매 완료')

                # 일반적인 입찰
                else:
                    product1.current_price = bid_price
                    product1.save()

                    print(product1.product_name, ' 현재 가격 갱신 ', product1.current_price, '원')

        return HttpResponse(status=200)  # html에 뿌리기 위한 return


def send_email(email, bidder_name, product_name, bid_price):
    email = EmailMessage(
        '사진 경매 입찰 내역',  # 이메일 제목
        '안녕하세요, {0}님\n\n입찰 내역 안내드립니다\n작품명: {1}\n입찰가: {2} \n\n감사합니다\n박수빈 드림 '
        '\n@su.napshot\nhttp://www.photoauction.site'.format(bidder_name, product_name, bid_price),  # 내용
        to=[email],  # 받는 이메일
    )
    email.send()
