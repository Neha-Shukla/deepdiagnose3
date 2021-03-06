
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=250, unique=True)
    email_id = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=12)
    address_line1 = models.CharField(max_length=125)
    city = models.CharField(max_length=125)
    state = models.CharField(max_length=125)
    logo = models.ImageField(upload_to='logo')

    def __str__(self):
        return str(self.company_name)


class TestCategory(models.Model):
    category = models.CharField(max_length=125)

    def __str__(self):
        return str(self.category)


class Meta:
    verbose_name = 'TestCategory'
    verbose_name_plural = 'TestCategory'


class Tests(models.Model):
    test_name = models.CharField(max_length=125)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.test_name)

    class Meta:
        verbose_name = 'Tests'
        verbose_name_plural = 'Tests'


class CompanyTests(models.Model):
    company_name = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    tests = models.ForeignKey(Tests, on_delete=models.CASCADE)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return str(self.company_name)

    class Meta:
        verbose_name_plural = 'CompanyTests'


class OrderInfo(models.Model):
    order_no = models.AutoField(primary_key=True, default=0)
    company_name = models.CharField(max_length=125, default='NULL')
    test_name = models.CharField(max_length=125, default='NULL')
    user_name = models.CharField(max_length=125)
    email_id = models.EmailField()
    age = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=125)
    city = models.CharField(max_length=125)
    state = models.CharField(max_length=125)
    zip_code = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=12)
    suitable_date = models.CharField(max_length=12)
    suitable_time = models.CharField(max_length=12)


class Company(models.Model):
    company = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'