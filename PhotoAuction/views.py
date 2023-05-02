from django.shortcuts import render
from rest_framework.views import APIView


class Main(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "auction/main.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, "auction/main.html")


class Detail(APIView):
    def get(self, request):
        print("상세페이지 GET")
        return render(request, "content/product_detail.html")

    def post(self, request):
        print("상세페이지에서 POST")
        return render(request, "content/product_detail.html")