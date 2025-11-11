from django.db import migrations
from pathlib import Path

def create_sql_functions(apps, schema_editor):
    sql_dir = Path(__file__).resolve().parent.parent / 'sql'
    for sql_file in sql_dir.glob('*.sql'):
        with open(sql_file) as f:
            sql = f.read()
        schema_editor.execute(sql)

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_sql_functions),
    ]
