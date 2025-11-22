import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voluntariado.settings')
import django
django.setup()

from django.urls import get_resolver


def list_urls(patterns, prefix=''):
    for p in patterns:
        try:
            pat = str(p.pattern)
        except Exception:
            pat = str(p)
        if hasattr(p, 'url_patterns'):
            list_urls(p.url_patterns, prefix + pat)
        else:
            name = getattr(p, 'name', '')
            print(f"{prefix}{pat}  -> name='{name}'")


if __name__ == '__main__':
    resolver = get_resolver()
    list_urls(resolver.url_patterns)
