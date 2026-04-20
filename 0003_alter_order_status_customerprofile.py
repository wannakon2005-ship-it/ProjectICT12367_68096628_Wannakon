from django.contrib import admin
from .models import Customers, Employees, Orders # ใส่ชื่อ Class ที่อยู่ใน models.py

admin.site.register(Customers)
admin.site.register(Employees)
admin.site.register(Orders)