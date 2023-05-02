from django import forms


class BidForm(forms.Form):
    product_name = forms.CharField()
    bid_price = forms.IntegerField(min_value=5000, step_size=1000)
    bidder_name = forms.CharField(max_length=7)  # 입찰자 이름
    bidder_phone = forms.CharField(max_length=11)  # 핸드폰 번호
    bidder_email = forms.EmailField()  # 이메일
    agree = forms.CheckboxInput()  # 개인정보 수집 동의
