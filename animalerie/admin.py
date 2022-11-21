from django.contrib import admin

# Register your models here.
##Ajouter, modifier et supprimir "Equipemenet"
from .models import Equipement
admin.site.register(Equipement)

##Ajouter, modifier et supprimir "Animal"
from .models import Animal
admin.site.register(Animal)
