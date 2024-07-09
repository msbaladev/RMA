from django.db import models



class rma_file(models.Model):
    item = models.CharField(max_length=100, null=True)
    quarter = models.CharField(max_length=100, null=True)
    pn = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    qty = models.CharField(max_length=100, null=True)
    usd = models.CharField(max_length=100, null=True)
    scrap = models.FloatField(null=True)
    unit_freight = models.FloatField(null=True)
    unit_price = models.FloatField(null=True)
    ext_price = models.FloatField(null=True)
    remark = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=150, null=True)
    approval_comments = models.CharField(max_length=150, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class bulk_attchements(models.Model):
    file = models.CharField(max_length=100, null=True)
    quarter = models.CharField(max_length=100, null=True)
    stored_name=models.CharField(max_length=100,null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.file
