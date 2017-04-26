from django.shortcuts import render


def test_view(request):
    context = {

    }
    return render(request, 'talent/main.html', context)


def detail_view(request):
    context = {

    }
    return render(request, 'talent/detail.html', context)
