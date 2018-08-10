from django.contrib import admin
from .models import *

from datetime import datetime

admin.site.register(Permit)
admin.site.register(Department)
admin.site.register(StockComment)
admin.site.register(Approval)
admin.site.register(UserDepartment)


# Register your models here.
