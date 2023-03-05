from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([lkp_overridecategory, lkp_region,
                     lkp_subregion, lkp_country, lkp_table7, table1, Lkptable2name, table2, table3, table4,
                     table5, table6])
