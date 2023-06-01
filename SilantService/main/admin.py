from django.contrib import admin

from .models import ReferenceTable, Machine, Reclamation, Maintenance

admin.site.register(ReferenceTable)
admin.site.register(Machine)
admin.site.register(Reclamation)
admin.site.register(Maintenance)
