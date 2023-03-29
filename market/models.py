from django.db import models
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    price = models.FloatField('Price', default=0)
    date_created = models.DateTimeField()
    post_id = models.AutoField(primary_key=True)
    influencer_id = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    platform_id = models.ForeignKey('Platform', on_delete=models.CASCADE)
    platform_type_id = models.ForeignKey(
        'PlatformType', on_delete=models.CASCADE)

    def __str__(self):
        return 'Post ' + str(self.date_created)

    # def get_absolute_url(self):
    #     """Returns the URL to access a detail record for this book."""
    #     return reverse('', args=[str(self.id)])


class Type(models.Model):
    type_id = models.AutoField(primary_key=True, unique=True)
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_name


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True, unique=True)
    platform_name = models.CharField(max_length=255)

    def __str__(self):
        return self.platform_name


class PlatformType(models.Model):

    platform_type_id = models.AutoField(primary_key=True, unique=True)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)
    platform_id = models.ForeignKey(Platform, on_delete=models.CASCADE,default=0)
    def __str__(self):
        return str(self.type_id.type_name)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, unique=True)
    customer_id = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE)    
    created_at = models.DateTimeField()
    def __str__(self):
        return str(self.order_id)
    