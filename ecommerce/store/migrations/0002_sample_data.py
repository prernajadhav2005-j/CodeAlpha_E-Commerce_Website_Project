from django.db import migrations

def add_products(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')

    electronics = Category.objects.get(name='Electronics')

    Product.objects.get_or_create(
        name='Smartphone',
        category=electronics,
        price=15000,
        stock=10,
        description='Android Phone',
        image='products/iphone.jpg'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_products),
    ]
