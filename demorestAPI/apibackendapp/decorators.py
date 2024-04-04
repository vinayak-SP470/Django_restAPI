from functools import wraps
from django.http import JsonResponse
import json

def validate_required_fields(required_fields):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                try:
                    post_data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON data'}, status=400)

                missing_fields = [field for field in required_fields if field not in post_data]
                if missing_fields:
                    return JsonResponse({'error': f'Required field(s) "{", ".join(missing_fields)}" is missing'}, status=400)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator