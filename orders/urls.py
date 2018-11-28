from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name = "login"),
    path("register/", views.register, name = "register"),
    path("logout/", views.logout_view, name = "logout"),
    path("pizzas/", views.pizza_view, name = "pizzas"),
    path("subs/", views.sub_view, name = "subs"),
    path("platters/", views.platter_view, name = "dinner_platters"),
    path("salads/", views.salad_view, name = "salads"),
    path("pasta/", views.pasta_view, name = "pasta"),
    path("price/", views.price_view, name = "price"),
    path("cart/", views.cart_view, name = "cart"),
    path("orders-page/", views.order_view, name = "orders-page")
]
