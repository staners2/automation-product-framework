from django.contrib import admin
from .models import ProductsModel, ChatsModel, PlansModel, EventsModel, EventTypesModel, NamespacesModel, EmployeesModel

# Register your samples here.

admin.site.register(ProductsModel)
admin.site.register(ChatsModel)
admin.site.register(PlansModel)
admin.site.register(EventsModel)
admin.site.register(EventTypesModel)
admin.site.register(NamespacesModel)
admin.site.register(EmployeesModel)
