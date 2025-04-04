from django.shortcuts import render

def waste_view(request):
    return render(request, "admin_panel/waste_templates/waste_list.html")
