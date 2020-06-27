from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("order", views.order, name="order"),
    path("order/<int:order_id>", views.order, name="order"),
    path("orders-history", views.orders_history, name="orders_history"),

    path("add-to-cart", views.add_to_cart),
    path("remove-from-cart", views.remove_from_cart),

    path("get-current-order-price", views.get_current_order_price),
    path("confirm-order-final", views.confirm_order_final),
    path("cancel-order", views.cancel_order),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
