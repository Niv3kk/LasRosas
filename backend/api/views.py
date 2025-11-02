# backend/api/views.py
from django.http import JsonResponse
from django.db import connection

def health(request):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1;")
            row = cur.fetchone()
        return JsonResponse({"ok": True, "db": "connected", "select_1": row[0]})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
