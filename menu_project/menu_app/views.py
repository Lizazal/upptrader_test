from django.shortcuts import render
from django.template import TemplateDoesNotExist
from .models import MenuItem

# рендер главной страницы с меню
def home(request):
    # загружает все пункты меню из бд
    menu_items = MenuItem.objects.all()
    return render(request, 'home.html', {'menu_items': menu_items})

# рендер страницы, если она существует, либо страницы ошибки
def generic_view(request, path=None):
    template_name = path
    try:
        return render(request, f'{template_name}.html')
    except TemplateDoesNotExist:
        return render(request, 'page_not_found.html')
    
# рендер страницы ошибки
def page_not_found(request):
    return render(request, 'page_not_found.html')