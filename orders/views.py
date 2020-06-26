from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderPizza, OrderSub, OrderPasta, OrderSalad, OrderDinnerPlatter, Topping, Size, PizzaName, Pizza, SubName, Sub, SubAddon, Pasta, Salad, DinnerPlatterName, DinnerPlatter


def index(request):
    # retrieve all menu data from DB and render with index.html
    context = {
        "pizza_names": PizzaName.objects.all(),
        "sizes": Size.objects.all(),
        "toppings":Topping.objects.all(),
        "toppings_count":[0,1,2,3,5],
        "subs": SubName.objects.all(),
        "subs_extra":SubAddon.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": DinnerPlatterName.objects.all()
    }
    return render(request, "orders/index.html", context=context)


def register_view(request):
    if request.method == "GET":
        # access register.html
        return render(request, "orders/register.html")

    if request.method == "POST":
        # after user submits information -> save to db
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        # user object for django ORM
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        # go back to index page
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    # user wants to log in to make order - authenticate user credentials
    if request.method == "GET":
        # access login page
        return render(request, "orders/login.html")

    if request.method == "POST":
        # when user provides info - check against User table with django/authenticate()
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # success --> go to index
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # fail --> stay on login
            return HttpResponseRedirect(reverse("login"))


def logout_view(request):
    # end user session --> go back to main menu page
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def add_to_cart(request):
    if request.method == "GET":
        # no GET access
        return HttpResponseNotAllowed()

    # get orders made by user and not sent
    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
    if order.count() == 0:
        # ^no orders found --> create new order for user
        order = Order(user=request.user)
        order.save()
    else:
        # select first order found
        order = order[0]

    # Get product data from client request
    try:
        product_class = request.POST["product_class"]
        # product_name is actually the product ID
        product_name = request.POST["product_name"]
    except (KeyError, ValueError):
        return HttpResponseBadRequest()

    # get quantity of product order
    quantity = int(request.POST["quantity"])

    # Add to order_(food) in DB i.e. save food details to order_(food) table
    #                                and link to unsent order by user
    if product_class == "DinnerPlatterName":
        order_dinner_platter = OrderDinnerPlatter(
            order=order,
            dinner_platter=DinnerPlatter.objects.get(
                name=DinnerPlatterName.objects.get(pk=int(product_name)),
                size=Size.objects.get(pk=int(request.POST["platter-size"]))
            ),
            quantity=quantity
        )
        order_dinner_platter.save()
        order.save()
    elif product_class == "Salad":
        order_salad = OrderSalad(
            order=order,
            salad=Salad.objects.get(
                name=Salad.objects.get(pk=int(product_name))
            ),
            quantity=quantity
        )
        order_salad.save()
        order.save()
    elif product_class == "Pasta":
        order_pasta = OrderPasta(
            order=order,
            pasta=Pasta.objects.get(
                name=Pasta.objects.get(pk=int(product_name))
            ),
            quantity=quantity
        )
        order_pasta.save()
        order.save()
    elif product_class == "Sub":
        order_sub = OrderSub(
            order=order,
            sub=Sub.objects.get(
                name=SubName.objects.get(pk=int(product_name)),
                size=Size.objects.get(pk=int(request.POST["sub-size"]))
            ),
            quantity=quantity
        )
        order_sub.save()
        # get toppings added to sub
        for addon_id in request.POST.get("subaddons", []).split(","):
            order_sub.sub_addons.add(
                SubAddon.objects.get(pk=int(addon_id))
            )
        order_sub.save()

        order.save()
    elif product_class == "PizzaName":
        query_size = Size.objects.get(name=request.POST["pizza_size"])
        order_pizza = OrderPizza(
            order=order,
            pizza=Pizza.objects.get(
                name=PizzaName.objects.get(pk=int(product_name)),
                size=query_size,
                toppings_count=int(request.POST["num_toppings"])
            ),
            quantity=quantity
        )
        order_pizza.save()
        # if num toppings is not plain cheese
        if int(request.POST["num_toppings"]) > 0:
            for topping_id in request.POST.get("list_toppings"):
                order_pizza.toppings.add(
                    Topping.objects.get(pk=int(topping_id))
                )
        order_pizza.save()

        order.save()
    else:
        return HttpResponseNotFound()

    return JsonResponse({
        "order_price": order.get_order_price(),
        "order_id": order.id
    })


@csrf_exempt
def remove_from_cart(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order_class = request.POST["order_class"]
    order_id = request.POST["order_id"]

    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)[0]

    class_obj = globals()[order_class]
    order_product = class_obj.objects.get(pk=order_id)
    order_product.delete(keep_parents=True)

    return JsonResponse({
        "order_price": order.get_order_price(),
        "order_id": order.id
    })


@csrf_exempt
def get_current_order_price(request):
    # client request to get users order total
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order_price = 0
    order_id = None
    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
    if order.count() > 0:
        order = order[0]
        order_price = order.get_order_price()
        order_id = order.id

    return JsonResponse({"order_price": order_price, "order_id": order_id}, safe=False)


@csrf_exempt
def confirm_order_final(request):
    # on button click --> order is sent
    if request.method == "POST":
        # select tentative orders created by current user
        order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
        if order.count() == 0:
            # no orders found - empty response and reject request
            return HttpResponseNotFound()
        else:
            # ?? Get first order ??
            order = order[0]
        # ^ selected order is now sent --> success response
        order.order_sent = True
        order.save()

        return JsonResponse({"success": True}, safe=False)
    else:
        # GET request not allowed
        return HttpResponseNotAllowed()


@csrf_exempt
def cancel_order(request):
    # delete order made by users
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
    if order.count() == 0:
        return HttpResponseNotFound()
    else:
        order = order[0]

    order.delete(keep_parents=True)

    return JsonResponse({"success": True}, safe=False)


@login_required
def order(request, order_id=None):
    # render order page
    context = {
        "order_exists": False
    }

    if order_id is None:
        order = Order.objects.filter(user__pk=request.user.id).filter(order_sent=False)
        if order.count() == 0:
            return render(request, "orders/order.html", context=context)
        else:
            order = order[0]
    else:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotFound:
            return render(request, "orders/order.html", context=context)

    context["order_exists"] = True
    context.update({
        "pizzas": OrderPizza.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "subs": OrderSub.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "pastas": OrderPasta.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "salads": OrderSalad.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "dinner_platters": OrderDinnerPlatter.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "overall_price": order.get_order_price()
    })

    if order_id is None:
        context["order_title"] = "Your current order"
        context["buttons"] = True
    else:
        context["order_title"] = f"Order #{order_id}"
        context["buttons"] = False

    return render(request, "orders/order.html", context=context)


@login_required
def orders_history(request):
    # render history page
    context = {
        "orders": []
    }

    orders = Order.objects.filter(user__pk=request.user.id).filter(order_sent=True).order_by("-created")
    context["orders"] = orders

    return render(request, "orders/orders_history.html", context=context)
