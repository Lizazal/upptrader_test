from django.db import models
from django.urls import reverse, NoReverseMatch

# меню
class Menu(models.Model):
    # название меню
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# элементы меню
class MenuItem(models.Model):
    # название пункта меню
    name = models.CharField(max_length=100)
    # URL
    url = models.CharField(max_length=200, blank=True, null=True)
    # named URL
    named_url = models.CharField(max_length=200, blank=True, null=True)
    # внешний ключ, ссылка на меню
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    # внешний ключ, сслылка на родительский пункт меню
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # функция для возврата ссылки на пункт меню
    def get_url(self):
        # если шаблона для страницы не существует, то переход на страницу ошибки
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return reverse('page_not_found')
        elif self.url:
            return self.url
        return reverse('page_not_found')