from django.shortcuts import render

def property_view(request):
    return render(request, "admin_panel/property_templates/property_list.html")