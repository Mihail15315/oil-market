from django.db import models

class Product(models.Model):
    """Тип нефтепродукта"""
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    """Поставщик"""
    name = models.CharField(max_length=200, verbose_name="Название компании")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.CharField(max_length=100, verbose_name="Email")
    
    def __str__(self):
        return self.name

class Client(models.Model):
    """Покупатель"""
    name = models.CharField(max_length=200, verbose_name="Название компании")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Транзакция продажи"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Поставщик")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Покупатель")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество (тонн)")
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за тонну")
    date = models.DateField(verbose_name="Дата сделки")
    payment_status = models.BooleanField(default=False, verbose_name="Оплачено")
    
    def total_price(self):
        return self.quantity * self.price_per_ton
    
    def __str__(self):
        return f"Сделка #{self.id} - {self.product}"