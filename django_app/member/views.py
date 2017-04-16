from allauth.account.views import login
from django.shortcuts import render


# @login_required
def login_view(request):
    if request.method == 'POST':
        # POST 요청으로 넘겨받은 아이디/패스워드로 토큰을 받아온다.
        # data = {
        #     'username': request.POST['username'],
        #     'password': request.POST['password']
        # }
        # url = 'http://localhost:8000/api/member/token-auth/'
        # response = requests.post(url, data=data)
        # response_json = response.json()
        print('login')
        login(request)

        return render(request, 'member/success.html')
    return render(request, 'member/login.html')


def my_page_view(request):
    context = {

    }
    return render(request, 'member/my_page.html', context)
