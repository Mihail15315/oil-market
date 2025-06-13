import random
from datetime import date, timedelta
from django.db import transaction
from oilmarke.models import Product, Supplier, Client, Transaction

def create_initial_data():
    from django.db import connection
    
    # Проверка кодировки соединения
    print("\nПроверка кодировки базы данных:")
    with connection.cursor() as cursor:
        cursor.execute("SHOW VARIABLES LIKE 'character_set%'")
        for row in cursor.fetchall():
            print(row)
    # Очищаем все данные
    with transaction.atomic():
        Transaction.objects.all().delete()
        Product.objects.all().delete()
        Supplier.objects.all().delete()
        Client.objects.all().delete()

        # Создаем продукты
        products = [
            Product.objects.create(name="Нефть сырая", description="Сырая нефть марки Urals"),
            Product.objects.create(name="Дизельное топливо", description="Дизельное топливо ЕВРО-5"),
            Product.objects.create(name="Бензин АИ-92", description="Бензин автомобильный АИ-92"),
            Product.objects.create(name="Бензин АИ-95", description="Бензин автомобильный АИ-95"),
            Product.objects.create(name="Мазут", description="Топочный мазут М-100"),
        ]

        # Создаем поставщиков
        suppliers = [
            Supplier.objects.create(name="Роснефть", contact_person="Иванов И.И.", phone="+79991234567", email="info@rosneft.ru"),
            Supplier.objects.create(name="Лукойл", contact_person="Петров П.П.", phone="+79992345678", email="contact@lukoil.com"),
            Supplier.objects.create(name="Газпром нефть", contact_person="Сидоров С.С.", phone="+79993456789", email="sales@gazprom-neft.ru"),
        ]

        # Создаем клиентов
        clients = [
            Client.objects.create(name="Нефтетрейд", address="Москва, ул. Нефтяная, 1", phone="+74951234567"),
            Client.objects.create(name="Топливный альянс", address="Санкт-Петербург, пр. Топливный, 10", phone="+78123456789"),
            Client.objects.create(name="Энергосбыт", address="Казань, ул. Энергетиков, 5", phone="+78431234567"),
            Client.objects.create(name="Транснефть", address="Новосибирск, ул. Транспортная, 15", phone="+73832123456"),
        ]

        # Создаем 40 транзакций
        for _ in range(40):
            Transaction.objects.create(
                product=random.choice(products),
                supplier=random.choice(suppliers),
                client=random.choice(clients),
                quantity=round(random.uniform(10, 1000), 2),
                price_per_ton=round(random.uniform(20000, 80000), 2),
                date=date.today() - timedelta(days=random.randint(1, 365)),
                payment_status=random.choice([True, False])
            )

        print(f"Создано: {Product.objects.count()} продуктов, "
              f"{Supplier.objects.count()} поставщиков, "
              f"{Client.objects.count()} клиентов, "
              f"{Transaction.objects.count()} транзакций")

# Для выполнения при прямом запуске файла
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oilmarket_project.settings')
    import django
    django.setup()
    create_initial_data()