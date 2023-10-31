from django.http import HttpResponse
from django.shortcuts import render
from .models import Services
from datetime import date
from django.shortcuts import get_object_or_404

# data = {'data': {'orders': [
#     {'id': 1, 'title': 'Декларирование товаров', 'img': 'https://akket.com/wp-content/uploads/2020/06/Posylki-s-AliExpress-tamozhnya-Sroki-0.jpg', 'text': 'Товары для личного пользования не превышающие 10000 ервро и весом не более 10 кг',
#      'type': '  Товар', 'price': 3000},
#     {'id': 2, 'title': 'Декларирование ценностей', 'img': 'https://telegra.ph/file/14b9b1e38c22490781f20.jpg',
#      'text': ' Перемещение культурных ценностей физическими лицами через таможенную границу Перечень культурных ценностей, документов национальных архивных фондов и оригиналов архивных документов, подлежащих контролю при перемещении через таможенную границу Российской Федерации, определен разделом 2.20 Единого перечня товаров, к которым применяются запреты или ограничения на ввоз или вывоз государствами – членами ЕАЭС в торговле с третьими странами (далее – Единый перечень) утвержденного Решением Коллегии Евразийской экономической комиссии от 21 апреля 2015 года № 30', 'type': 'Ценности', 'price': 100000},
#     {'id': 3, 'title': 'Декларирование валют', 'img': 'https://catherineasquithgallery.com/uploads/posts/2023-02/1676587612_catherineasquithgallery-com-p-dengi-na-zelenom-fone-33.jpg', 'text': ' Со 2 марта 2022 года временно запрещено вывозить валюту свыше 10 тыс. долл. США. Соответствующий Указ Президента РФ опубликован 1 марта 2022 года. Согласно документу со 2 марта 2022 года запрещено вывозить из РФ наличную иностранную валюту и денежные инструменты в иностранной валюте в сумме, превышающей эквивалент 10 тыс. долл. США и рассчитанной по официальному курсу ЦБ РФ, установленному на дату вывоза.',
#      'type': 'Деньги', 'price': 2000},
#     {'id': 4, 'title': 'Декларирование транспортных средств', 'img': 'https://rostov.explorer-russia.ru/gallery/auto/modification/1962.jpg', 'text': 'Согласно ст. 260 ТК ЕАЭС транспортные средства для личного пользования (за исключением ТС, зарегистрированных в странах ЕАЭС), перемещаемые через таможенную границу ЕАЭС любым способом, для целей выпуска в свободное обращение подлежат таможенному декларированию. Таможенное декларирование товаров для личного пользования, производится с использованием пассажирской таможенной декларации (ПТД).',
#      'type': 'Транспорт', 'price': 3000},
#     {'id': 5, 'title': 'Декларирование медицинских товаров', 'img': 'https://pronikotin.ru/wp-content/uploads/2023/06/0-17.jpg', 'text': 'Медицинская аппаратура и лекарственные средства.',
#      'type': 'Мед товары', 'prcie': 1200}
# ]}}


def GetOrders(request):
    services = Services.objects.all()
    try:
        input_text = request.GET['text']
        if input_text:
            services = services.filter(name__icontains=input_text)
        return render(request, 'orders.html', {'data': {'orders': services}})
    except:
        return render(request, 'orders.html', {'data': {'orders': services}})

def GetOrder(request, id):
    obj=get_object_or_404(Services, pk=id)
    return render(request, 'order.html', {'obj':obj})