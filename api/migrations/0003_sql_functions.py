from django.db import migrations
from pathlib import Path

def load_sql():
    sql_dir = Path(__file__).resolve().parent.parent / "sql"
    full_sql = ""
    for file in sql_dir.glob("*.sql"):
        with open(file, "r", encoding="utf-8") as f:
            full_sql += f.read() + "\n"
    return full_sql

class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_create_sql_functions"),
    ]

    operations = [
        migrations.RunSQL(
            sql=load_sql(),
            reverse_sql="",   # nemáme způsob revertovat funkce
        )
    ]
