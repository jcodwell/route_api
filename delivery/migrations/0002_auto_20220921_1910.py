# Generated by Django 3.2.15 on 2022-09-21 19:10

from django.db import migrations


def load_initial_data(apps, schema_editor):
   
    order_model = apps.get_model('delivery', 'Order')
    order_model.objects.create (order_time="2022-01-11T01:00:00Z", 
                               address="Home", 
                               lat=37.308941481697225, 
                               lng=-122.00122455940141, 
                               home=True, 
                               delivered=False
        )
    

class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
         migrations.RunPython(load_initial_data)
    ]
