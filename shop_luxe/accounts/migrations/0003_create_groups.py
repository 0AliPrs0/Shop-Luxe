from django.db import migrations

def create_user_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='Customers')
    Group.objects.create(name='Sellers')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_groups_alter_user_user_permissions'), 
    ]

    operations = [
        migrations.RunPython(create_user_groups),
    ]