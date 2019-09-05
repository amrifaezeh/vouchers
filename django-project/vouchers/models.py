from django.db import models

# Create your models here.
class Voucher(models.Model):
    voucher_code=models.CharField(max_length=50)
    discount_value= models.IntegerField()
    discount_type= models.CharField(max_length=3)
    pub_date= models.DateTimeField('date published')
    usage_number= models.IntegerField()
    max_usage= models.IntegerField(default=3)

    def __str__(self):
        return f"{self.voucher_code} used {self.usage_number}/{self.max_usage}"

    def still_can_use(self):
        return self.usage_number< self.max_usage