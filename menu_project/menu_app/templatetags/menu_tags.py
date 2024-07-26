from django import template
from menu_app.models import Menu
from django.template.loader import render_to_string

# создание экземпляра библиотеки шаблонов
register = template.Library()

# регистрация функции как простого тега, принимающего контекст
@register.simple_tag(takes_context=True)
# отрисовка меню
def draw_menu(context, menu_name):
    # извлекает объект запроса из контекста
    request = context['request']
    # попытка получить меню с заданным именем из бд
    try:
        menu = Menu.objects.prefetch_related('items__children').get(name=menu_name)
    # иначе вернуть пустую строку
    except Menu.DoesNotExist:
        return ""

    # загрузка всех пунктов меню
    menu_items = menu.items.all()
    # переменная для хранения активного пункта меню
    active_item = None
    # устанавливаем нужный элемент как активный
    for item in menu_items:
        if request.path == item.get_url():
            active_item = item
            break

    # функция для определения активного элемента
    def is_active_or_parent(item, active_item):
        if item == active_item:
            return True
        return any(is_active_or_parent(child, active_item) for child in item.children.all())

    # построения дерева меню
    def build_tree(items, parent=None):
        tree = []
        for item in items:
            # если родитель элемента совпадает с текущим родителем, добавляем элемент и его дочерние элементы в дерево
            if item.parent == parent:
                children = build_tree(items, item)
                tree.append((item, children))
        return tree

    # вызов построения дерева
    menu_tree = build_tree(menu_items)

    # рендер шаблона меню с контекстом: имя меню, дерево меню, активный элемент
    return render_to_string('menu/menu.html', {
        'menu_name': menu_name,
        'menu_tree': menu_tree,
        'active_item': active_item
    })
