"""product_framework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from product_app.views import (
    ChatsViewSets,
    EmployeesViewSets,
    EventTypesViewSets,
    EventsViewSets,
    NamespacesViewSets,
    PlansViewSets,
    ProductsViewSets,
)

router = routers.SimpleRouter(trailing_slash=False)
router.register("event-types", EventTypesViewSets, basename="event-types")  # Типы событий
router.register("events", EventsViewSets, basename="events")  # События
router.register("products", ProductsViewSets, basename="products")  # Продукты
router.register("namespaces", NamespacesViewSets, basename="namespaces")  # Пространства в Jira
router.register("chats", ChatsViewSets, basename="chats")  # Чат
router.register("plans", PlansViewSets, basename="plans")  # Планы
router.register("employees", EmployeesViewSets, basename="employees")  # Сотрудники


urlpatterns = [path("admin/", admin.site.urls), path("__debug__/", include("debug_toolbar.urls"))]


urlpatterns += [
    path("api/", include(router.urls)),
]
