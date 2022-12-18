from django.contrib import admin
from .models.ProductsModel import ProductsModel
from .models.ChatsModel import ChatsModel
from .models.PlansModel import PlansModel
from .models.EventsModel import EventsModel
from .models.EventTypesModel import EventTypesModel
from .models.NamespacesModel import NamespacesModel
from .models.EmployeesModel import EmployeesModel


# Register your samples here.

admin.site.register(ProductsModel)
admin.site.register(ChatsModel)
admin.site.register(PlansModel)
admin.site.register(EventsModel)
admin.site.register(EventTypesModel)
admin.site.register(NamespacesModel)
admin.site.register(EmployeesModel)
