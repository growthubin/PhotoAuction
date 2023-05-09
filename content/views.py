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
            return render(request, "content/product_detail2.html", context=dict(products=product))

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

        # 현재 가격 업데이트
        for product1 in product:
            # 즉시구매인 경우
            if bid_price == product1.buy_now:
                product1.sold = True
                product1.current_price = 0
                product1.save()

                # 기존의 입찰자에게 메일 보내기
                send_others(product, bid_price, "판매종료")

                # 입찰 당사자에게 메일
                send_email(bidder_email, bidder_name, product_name, bid_price, "즉시 구매")
                print('이메일 발송')

                print(product1.product_name, ' 즉시 구매 ', product1.sold, ' 판매 완료')

            # 일반적인 입찰(script에서 유효성 검사 끝냄)
            elif bid_price > 0:
                product1.current_price = bid_price
                product1.save()

                # 기존의 입찰자에게 메일 보내기
                send_others(product, bid_price, "입찰")

                # 입찰 당사자에게 메일
                send_email(bidder_email, bidder_name, product_name, bid_price, "입찰")
                print('이메일 발송')

                print(product1.product_name, ' 현재 가격 갱신 ', product1.current_price, '원')

            elif bid_price == 0:
                email_to_noti = EmailMessage(
                    '[메일알림] 작품 가격 알림 신청이 완료되었습니다',  # 이메일 제목
                    '안녕하세요, \n\n작품의 가격이 갱신되었을 때 메일드립니다\n\n작품명: {0} \n\n감사합니다\n박수빈 드림 '
                    '\n@su.napshot\nhttp://www.photoauction.site'.format(product_name),  # 내용
                    to=[bidder_email],  # 받는 이메일
                )

                email_to_noti.send()
                print('메일 알림 신청')

        # DB에 입찰 내역 저장
        bid_list = Bid.objects.create(
            product_name=product_name,
            bidder_name=bidder_name,
            bid_price=bid_price,
            bidder_phone=bidder_phone,
            bidder_email=bidder_email
        )
        bid_list.save()

        return HttpResponse(status=200)  # html에 뿌리기 위한 return


def send_email(email, bidder_name, product_name, bid_price, buy_option):
    email = EmailMessage(
        '[{0}내역] 사진 경매 {0} 내역'.format(buy_option),  # 이메일 제목
        '안녕하세요, {1}님\n\n{0} 내역 안내드립니다\n작품명: {2}\n{0}가: {3} \n\n낙찰 시 2~3일 내로 연락드립니다.\n감사합니다\n박수빈 드림 '
        '\n@su.napshot\nhttp://www.photoauction.site'.format(buy_option, bidder_name, product_name, bid_price),  # 내용
        to=[email],  # 받는 이메일
    )
    email.send()


def send_others(product_info, bid_price, message):
    product_name = product_info[0].product_name  # 입찰된 작품명 불러오기
    bids = Bid.objects.filter(product_name=product_name)  # 입찰 내역에서 해당하는 작품명으로 필터링

    # 기존에 입찰내역이 있으면
    if len(bids) > 0:
        if message == "입찰":
            for bid in bids:
                email_to_others = EmailMessage(
                    '[가격갱신] 입찰하셨던 작품의 가격이 갱신되었습니다',  # 이메일 제목
                    '안녕하세요, \n\n입찰하셨던 작품의 가격이 갱신되었음을 안내드립니다\n\n작품명: {0}\n갱신가: {1} \n\n감사합니다\n박수빈 드림 '
                    '\n@su.napshot\nhttp://www.photoauction.site'.format(product_name, bid_price),  # 내용
                    to=[bid.bidder_email],  # 받는 이메일
                )

                email_to_others.send()
                print('가격갱신 메일 발송')

        elif message == "판매종료":
            for bid in bids:
                email_to_others = EmailMessage(
                    '[판매종료] 입찰하셨던 작품이 판매 종료되었습니다',  # 이메일 제목
                    '안녕하세요, \n\n입찰하셨던 작품의 판매가 종료되었음을 안내드립니다\n\n작품명: {0}\n\n감사합니다\n박수빈 드림 '
                    '\n@su.napshot\nhttp://www.photoauction.site'.format(product_name),  # 내용
                    to=[bid.bidder_email],  # 받는 이메일
                )

                email_to_others.send()
                print('경매종료 메일 발송')

    else:
        print('첫 입찰')  # 첫 입찰이니까 아무한테도 안 보내도 됨
