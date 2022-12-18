# module models
from .models import ChatsModel, EmployeesModel, EventTypesModel, EventsModel, NamespacesModel, PlansModel, ProductsModel

# module viewsets
from product_app.controllers.EventTypesViewSets import EventTypesViewSets
from product_app.controllers.ProductsViewSets import ProductsViewSets
from product_app.controllers.EventsViewSets import EventsViewSets
from product_app.controllers.NamespacesViewSets import NamespacesViewSets
from product_app.controllers.PlansViewSets import PlansViewSets
from product_app.controllers.EmployeesViewSets import EmployeesViewSets
from product_app.controllers.ChatsViewSets import ChatsViewSets
