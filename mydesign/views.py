# mydesign/views.py
import json
import base64

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.files.base import ContentFile

from .models import Design


def mockup_page(request):
    return render(request, "mydesign/3ddesign.html")


def my_designs_page(request):
    
    if not request.user.is_authenticated:
        return render(request, "mydesign/my_designs.html", {"authenticated": False})
    
    return render(request, "mydesign/my_designs.html", {"authenticated": True})


def edit_design_page(request, design_id):
    
    design = get_object_or_404(Design, id=design_id)
    return render(request, "mydesign/3ddesign.html", {"design_id": design_id})


@require_http_methods(["POST"])
@csrf_protect
def save_design(request):
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    design_data = data.get("design_data")
    preview_png_dataurl = data.get("preview_png")
    product_id = data.get("product_id")
    design_id = data.get("design_id")  # برای بروزرسانی

    if not design_data or not preview_png_dataurl:
        return JsonResponse(
            {"ok": False, "error": "design_data و preview_png الزامی هستند"},
            status=400,
        )

    # DataURL -> فایل PNG
    try:
        prefix = "data:image/png;base64,"
        if not preview_png_dataurl.startswith(prefix):
            return JsonResponse({"ok": False, "error": "preview_png باید DataURL PNG باشد"}, status=400)

        base64_str = preview_png_dataurl[len(prefix):]
        image_data = base64.b64decode(base64_str)
        image_file = ContentFile(image_data, name="preview.png")
    except Exception as e:
        return JsonResponse({"ok": False, "error": f"خطا در decode PNG: {str(e)}"}, status=400)

    # بروزرسانی یا ایجاد جدید
    if design_id:
        # بروزرسانی طراحی موجود
        try:
            design = Design.objects.get(id=design_id)
            design.design_data = design_data
            design.preview_image = image_file
            if product_id is not None:
                design.product_id = product_id
            design.save()
        except Design.DoesNotExist:
            return JsonResponse({"ok": False, "error": f"Design with id {design_id} not found"}, status=404)
    else:
        # ایجاد طراحی جدید
        design = Design.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product_id=product_id,
            design_data=design_data,
            preview_image=image_file,
        )

    return JsonResponse({
        "ok": True,
        "design_id": design.id,
        "preview_url": design.preview_image.url if design.preview_image else ""
    })


def design_result(request, design_id):
    """
    صفحه نتیجه: نمایش 3D + اعمال تکسچر ذخیره شده + نمایش JSON
    """
    design = get_object_or_404(Design, id=design_id)

    context = {
        "design": design,
        "design_data_json": json.dumps(design.design_data, ensure_ascii=False, indent=2),

        # مدل سه بعدی (فعلاً ثابت؛ اگر بعداً per-product شد از DB می‌گیری)
        "model_glb_url": "/static/models/tshirt.glb",

        # تکسچر ذخیره شده (همون PNG خروجی canvas)
        "texture_png_url": design.preview_image.url if design.preview_image else "",
    }
    return render(request, "mydesign/result.html", context)


@require_http_methods(["GET"])
def get_design_api(request, design_id):
    """
    API: دریافت داده‌های طراحی ذخیره شده
    
    استفاده: GET /mydesign/api/design/<design_id>/
    
    پاسخ:
    {
      "ok": true,
      "design": {
        "id": 123,
        "design_data": {...},
        "created_at": "2024-01-01T12:00:00Z"
      }
    }
    """
    try:
        design = Design.objects.get(id=design_id)
    except Design.DoesNotExist:
        return JsonResponse(
            {"ok": False, "error": f"Design with id {design_id} not found"},
            status=404
        )

    return JsonResponse({
        "ok": True,
        "design": {
            "id": design.id,
            "design_data": design.design_data,
            "created_at": design.created_at.isoformat(),
            "updated_at": design.updated_at.isoformat()
        }
    })


@require_http_methods(["GET"])
def get_user_designs_api(request):
    """
    Stage 5.3: API endpoint to get all designs for authenticated user
    
    استفاده: GET /mydesign/api/designs/
    
    پاسخ:
    {
      "ok": true,
      "designs": [
        {
          "id": 1,
          "preview_url": "/media/designs/preview_1.png",
          "created_at": "2026-02-07T15:00:00Z",
          "updated_at": "2026-02-08T09:30:00Z"
        },
        ...
      ]
    }
    """
    # Only authenticated users can access
    if not request.user.is_authenticated:
        return JsonResponse(
            {"ok": False, "error": "Authentication required"},
            status=401
        )

    # Get all designs for this user, ordered by updated_at (newest first)
    designs = Design.objects.filter(user=request.user).order_by('-updated_at')
    
    designs_list = [
        {
            "id": design.id,
            "preview_url": design.preview_image.url if design.preview_image else "",
            "created_at": design.created_at.isoformat(),
            "updated_at": design.updated_at.isoformat()
        }
        for design in designs
    ]
    
    return JsonResponse({
        "ok": True,
        "designs": designs_list
    })
