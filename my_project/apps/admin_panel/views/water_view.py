from django.shortcuts import render

def water_view(request):
    return render(request, "admin_panel/water_templates/water_list.html")