import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
from django.conf import settings
from .models import *
from django.db.models import Q
import matplotlib.pyplot as plt
from urllib.parse import quote
def product_list(request):
    """Список продуктов с поиском и фильтрацией"""
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    
    # Поиск по названию
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    # Сортировка
    products = products.order_by(sort_by)
    
    return render(request, 'oilmarket/product_list.html', {
        'products': products,
        'search_query': search_query,
        'sort_by': sort_by
    })

def transactions_report(request):
    # Генерируем имя файла с датой и временем
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Отчет_по_сделкам_{current_datetime}.pdf"
    encoded_filename = quote(filename)
    # Регистрируем русский шрифт
    font_path = os.path.join(settings.BASE_DIR, 'oilmarke', 'fonts', 'arial.ttf')
    pdfmetrics.registerFont(TTFont('Arial', font_path))
    
    transactions = Transaction.objects.all().order_by('-date')[:10]
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFont("Arial", 12)
    
    # Заголовок
    p.drawString(50, height-50, "Отчет по последним сделкам")
    p.line(50, height-60, width-50, height-60)
    
    # Данные сделок
    y = height-100
    for t in transactions:
        # Форматируем строку
        line = (
            f"{t.date.strftime('%Y-%m-%d')}: "
            f"{t.product.name} - "
            f"{t.quantity:.2f}т × "
            f"{t.price_per_ton:.2f}₽ = "
            f"{t.total_price():.2f}₽ "
            f"({'Оплачено' if t.payment_status else 'Не оплачено'})"
        )
        
        p.drawString(50, y, line)
        y -= 25
        if y < 50:
            p.showPage()
            y = height-50
            p.setFont("Arial", 12) 
    
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
    return response

def sales_chart(request):
    """График продаж по продуктам"""
    products = Product.objects.all()
    product_names = [p.name for p in products]
    total_sales = [sum(t.quantity for t in Transaction.objects.filter(product=p)) for p in products]
    
    plt.figure(figsize=(10, 6))
    plt.bar(product_names, total_sales)
    plt.title('Объем продаж по продуктам')
    plt.xlabel('Продукт')
    plt.ylabel('Количество (тонн)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')