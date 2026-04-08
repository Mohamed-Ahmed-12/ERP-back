from django.db import models
from core.models import BaseModel

class Site(BaseModel):
    name = models.CharField(max_length=255)
    site_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Partner(BaseModel):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class SitePartner(BaseModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_partners')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='partner_sites')

    class Meta:
        unique_together = ('site', 'partner')

    def __str__(self):
        return f"{self.partner.fname} {self.partner.lname} at {self.site.name}"