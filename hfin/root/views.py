from django.shortcuts import render


def render_income_page(request):
    """Рендер на страницу приветствия."""
    return render(request, 'common.html')
