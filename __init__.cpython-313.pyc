# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customers(models.Model):
    cus_id = models.CharField(db_column='Cus_ID', primary_key=True, max_length=5, db_collation='Thai_CI_AS')  # Field name made lowercase.
    cus_name = models.CharField(db_column='Cus_name', max_length=20, db_collation='Thai_CI_AS')  # Field name made lowercase.
    room_id = models.CharField(db_column='Room_ID', max_length=5, db_collation='Thai_CI_AS')  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=20, db_collation='Thai_CI_AS')  # Field name made lowercase.
    member_type = models.CharField(db_column='Member_Type', max_length=10, db_collation='Thai_CI_AS', blank=True, null=True)  # Field name made lowercase.
    regist_date = models.DateField(db_column='Regist_Date')  # Field name made lowercase.
    total_points = models.IntegerField(db_column='Total_Points')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customers'


class Employees(models.Model):
    emp_id = models.CharField(db_column='Emp_ID', primary_key=True, max_length=5, db_collation='Thai_CI_AS')  # Field name made lowercase.
    emp_name = models.CharField(db_column='Emp_name', max_length=50, db_collation='Thai_CI_AS')  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=50, db_collation='Thai_CI_AS')  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=20, db_collation='Thai_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employees'


class OrderDetails(models.Model):
    order_detail_id = models.AutoField(db_column='Order_Detail_ID', primary_key=True)  # Field name made lowercase.
    order = models.ForeignKey('Orders', models.DO_NOTHING, db_column='Order_ID')  # Field name made lowercase.
    service = models.ForeignKey('Services', models.DO_NOTHING, db_column='Service_ID')  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=10, decimal_places=2)  # Field name made lowercase.
    unit_price = models.DecimalField(db_column='Unit_Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    sub_total = models.DecimalField(db_column='Sub_Total', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Order_Details'


class Orders(models.Model):
    order_id = models.CharField(db_column='Order_ID', primary_key=True, max_length=5, db_collation='Thai_CI_AS')  # Field name made lowercase.
    cus = models.ForeignKey(Customers, models.DO_NOTHING, db_column='Cus_ID')  # Field name made lowercase.
    order_date = models.DateTimeField(db_column='Order_date')  # Field name made lowercase.
    pickup_date = models.DateTimeField(blank=True, null=True)
    is_express = models.CharField(db_column='Is_Express', max_length=10, db_collation='Thai_CI_AS')  # Field name made lowercase.
    total_amount = models.DecimalField(db_column='Total_Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    discount_amount = models.DecimalField(db_column='Discount_Amount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reward = models.ForeignKey('RewardRules', models.DO_NOTHING, db_column='Reward_ID', blank=True, null=True)  # Field name made lowercase.
    order_status = models.CharField(db_column='Order_Status', max_length=20, db_collation='Thai_CI_AS')  # Field name made lowercase.
    emp = models.ForeignKey(Employees, models.DO_NOTHING, db_column='Emp_ID')  # Field name made lowercase.
    actual_pickup_date = models.DateTimeField(db_column='Actual_Pickup_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Orders'


class Payments(models.Model):
    pay_id = models.AutoField(db_column='Pay_ID', primary_key=True)  # Field name made lowercase.
    order = models.ForeignKey(Orders, models.DO_NOTHING, db_column='Order_ID')  # Field name made lowercase.
    pay_date = models.DateTimeField(db_column='Pay_Date')  # Field name made lowercase.
    pay_method = models.CharField(db_column='Pay_Method', max_length=20, db_collation='Thai_CI_AS')  # Field name made lowercase.
    pay_amount = models.DecimalField(db_column='Pay_Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Payments'


class RewardRules(models.Model):
    reward_id = models.IntegerField(db_column='Reward_ID', primary_key=True)  # Field name made lowercase.
    reward_name = models.CharField(db_column='Reward_Name', max_length=50, db_collation='Thai_CI_AS')  # Field name made lowercase.
    points_required = models.IntegerField(db_column='Points_Required')  # Field name made lowercase.
    discount_value = models.DecimalField(db_column='Discount_Value', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reward_Rules'


class Services(models.Model):
    service_id = models.CharField(db_column='Service_ID', primary_key=True, max_length=5, db_collation='Thai_CI_AS')  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, db_collation='Thai_CI_AS')  # Field name made lowercase.
    item_name = models.CharField(db_column='Item_Name', max_length=50, db_collation='Thai_CI_AS')  # Field name made lowercase.
    unit_type = models.CharField(db_column='Unit_type', max_length=20, db_collation='Thai_CI_AS')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    express_price = models.DecimalField(db_column='Express_Price', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Services'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='Thai_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
