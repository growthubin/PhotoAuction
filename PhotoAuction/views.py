from django.shortcuts import render
from rest_framework.views import APIView


class Main(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "auction/main2.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, "auction/main2.html")


class Chapter1(APIView):
    def get(self, request):
        return render(request, "content/chapter_sunrise.html")


class Chapter2(APIView):
    def get(self, request):
        return render(request, "content/chapter_shadow.html")


class Chapter3(APIView):
    def get(self, request):
        return render(request, "content/chapter_beach.html")
