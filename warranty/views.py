from datetime import date, datetime
from django.shortcuts import render, redirect
from .models import SearchHistory, WarrantyCard
from .erp_service import get_warranty_items
import qrcode
from io import BytesIO
import base64



def search_invoice(request):
    if request.method == "POST":

        invoice = request.POST.get("invoice")
        SearchHistory.objects.create(invoice_no=invoice)
        items = get_warranty_items(invoice)
        
        return render(request, "result.html", {
            "items": items,
            "invoice": invoice
        })

    return render(request, "search.html")


def history(request):
    history = SearchHistory.objects.order_by("-searched_at")[:100]

    return render(request, "history.html", {
        "history": history
    })

def clear_history(request):
    SearchHistory.objects.all().delete()
    
    return redirect("/history/")

def print_warranty(request, invoice):
    items = get_warranty_items(invoice)
    card = WarrantyCard.objects.filter(invoice_no=invoice).last()
    
    qr_data= f"http://192.168.0.105:8000/verify/{invoice} "
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    customer_name = ""
    customer_phone = ""

    if card:
        customer_name = card.customer_name
        customer_phone = card.customer_phone

    return render(request, "print.html", {
        "items": items,
        "invoice": invoice,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "qr":qr_base64
    })

def save_customer(request):
    if request.method == "POST":
        invoice = request.POST.get("invoice")
        name = request.POST.get("customer_name")
        phone = request.POST.get("customer_phone")

        WarrantyCard.objects.get_or_create(
            invoice_no=invoice,
            defaults={
                "customer_name": name,
                "customer_phone": phone
            }
        )

        return redirect(f"/print/{invoice}/")

def warranty_cards(request):
    invoice = request.GET.get("invoice")
    cards = WarrantyCard.objects.all()

    if invoice:
        cards = cards.filter(invoice_no__icontains=invoice)

    cards = cards.order_by("-printed_at")[:200]
    
    return render(request,"warranty_cards.html",{
        "cards":cards
    })

def view_result(request, invoice):
    items = get_warranty_items(invoice)

    return render(request, "result.html", {
        "items": items,
        "invoice": invoice,
    })
    
def verify_warranty(request, invoice):

    items = get_warranty_items(invoice)

    today = date.today()

    for i in items:

        expiry = i["expiry"]
        try:
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        except ValueError:
            expiry_date = None
            i["status"] = "Invalid Date"
            continue

        if expiry_date >= today:
            i["status"] = "Valid"
        else:
            i["status"] = "Expired"

    return render(request,"verify.html",{

        "items":items,
        "invoice":invoice

    })