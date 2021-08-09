from django.shortcuts import redirect, render
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    if request.method == "POST":
        quantity_from_form = int(request.POST["quantity"])
        try:
            product = Product.objects.get(id=request.POST["product.id"])
            price_from_form = float(product.price)
        except:
            return redirect("/")
        total_charge = quantity_from_form * price_from_form
        if "cantidad" in request.session:
            request.session["cantidad"] += quantity_from_form
            request.session["gasto"] += price_from_form
        else:
            request.session["cantidad"] = quantity_from_form
            request.session["gasto"] = price_from_form
        request.session["total"] = total_charge
        context = {
            "cantidad" : request.session["cantidad"],
            "gasto" : request.session["gasto"],
            "total" : request.session["total"],
        }
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        return redirect("/checkout")
    elif request.method == "GET":
        context = {
            "cantidad" : request.session["cantidad"],
            "gasto" : request.session["gasto"],
            "total" : request.session["total"],
        }
        return render(request, "store/checkout.html", context)
