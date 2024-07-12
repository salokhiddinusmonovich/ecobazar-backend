# from django.contrib.auth.models import User
# from django.db import models
# from django.contrib.auth import get_user_model
# from order.models import Order, OrderItem
#
#
# class Country(models.Model):
#     country = models.CharField(max_length=25)
#
# class States(models.Model):
#     state = models.CharField(max_length=25)
#
# class PaymentMethod(models.Model):
#     state = models.CharField(max_length=25)
#
#
# class BillingInformation(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
#     orderitem = models.ManyToManyField(OrderItem)
#     first_name = models.CharField(max_length=25)
#     street_address = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=25)
#     company_name = models.CharField(max_length=25, blank=True, null=True)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     state = models.ForeignKey(States, on_delete=models.CASCADE)
#     zip_code = models.CharField(max_length=5)
#     email = models.EmailField()
#     phone = models.IntegerField(max_length=15)
#     note = models.TextField()
#
#     def calc_total(self):
#         total = 0
#         for orderitem in self.orderitem.objects.all():
#             total += orderitem.total_price
#         return total