from django.db import models


class lkp_overridecategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)  # show on frontend as override category
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)

class lkp_region(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)  # show on frontend as region
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)

class lkp_subregion(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)  # show on frontend as Sub region
    lkp_regionid = models.ForeignKey(lkp_region, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)

class lkp_country(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)  # show on frontend Country
    lkp_subregionid = models.ForeignKey(lkp_subregion, on_delete=models.CASCADE, blank=True, null=True)
    lkp_regionid = models.ForeignKey(lkp_region, on_delete=models.CASCADE, blank=True, null=True)
    name_sales = models.CharField(max_length=200, blank=True, null=True)  # show on frontend
    name_sie = models.CharField(max_length=200, blank=True, null=True)  # show on frontend
    name_sap = models.CharField(max_length=200, blank=True, null=True)  # show on frontend
    name_ora = models.CharField(max_length=200, blank=True, null=True)  # show on frontend
    io2 = models.CharField(max_length=2, blank=True, null=True)
    io3 = models.CharField(max_length=3, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)


class lkp_table7(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)  # show on frontend Hiearchie name
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)




class table1(models.Model):  # table1 = table 1
    id = models.CharField(max_length=100, primary_key=True)  # show on frontend
    permid = models.BigIntegerField(blank=True, null=True)  # show on frontend
    name = models.CharField(max_length=500, blank=True, null=True)  # show on frontend
    streetaddress = models.CharField(max_length=500, blank=True, null=True)  ##show on frontend
    city = models.CharField(max_length=500, blank=True, null=True)  # show on frontend
    postcode = models.CharField(max_length=100, blank=True, null=True)  # show on frontend
    state = models.CharField(max_length=100, blank=True, null=True)  # show on frontend
    lkp_countryid = models.ForeignKey(lkp_country, on_delete=models.CASCADE, blank=True, null=True)
    oaaddresstype = models.CharField(max_length=50, blank=True, null=True)  # show on frontend
    manualapproval = models.BooleanField(blank=True, null=True)  # show on frontend checkbox
    manualapprovaldate = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True, default="")
    createddate = models.DateTimeField(blank=True, null=True)
    createdbyid = models.CharField(max_length=500, blank=True, null=True)
    lastmodifieddate = models.DateTimeField(blank=True, null=True)
    lastmodifiedbyid = models.CharField(max_length=500, blank=True, null=True)
    isactive = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Lkptable2name(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)  # show on frontend as Segment Name
    type = models.CharField(max_length=100, blank=True, null=True)  # show on frontend as Segment Type
    ismanaged = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    createdbyid = models.CharField(max_length=500, blank=True, null=True)
    lastmodifieddate = models.DateTimeField(blank=True, null=True)
    lastmodifiedbyid = models.CharField(max_length=500, blank=True, null=True)  # show on frontend as LM Segment ID
    isactive = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class table2(models.Model):
    id = models.CharField(max_length=38, primary_key=True)
    table1id = models.ForeignKey(table1, on_delete=models.CASCADE, blank=True, null=True)
    lkp_table2nameid = models.ForeignKey(Lkptable2name, on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField(max_length=500, blank=True, null=True)  # show on frontend as org type
    cf_segmentattion_entityurl = models.TextField(blank=True, null=True)  # show on frontend as entity website
    cf_segmentation_website = models.TextField(blank=True, null=True)  # show on frontend as URL
    description = models.TextField(blank=True, null=True)
    lastverifieddate = models.DateTimeField(blank=True, null=True)
    lastverifiedbyid = models.CharField(max_length=500, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    createdbyid = models.CharField(max_length=500, blank=True, null=True)
    lastmodifieddate = models.DateTimeField(blank=True, null=True)  # show on frontend as LM Segment Date
    lastmodifiedbyid = models.CharField(max_length=500, blank=True, null=True)  # show on frontend as LM Segment ID
    isactive = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class table3(models.Model):
    id = models.CharField(max_length=38, primary_key=True)
    table1id = models.ForeignKey(table1, on_delete=models.CASCADE, blank=True, null=True)
    lkp_table3nameid = models.ForeignKey(Lkptable2name, on_delete=models.CASCADE, blank=True, null=True)
    sourcereferenceid = models.CharField(max_length=100)  # show on frontend
    customertype = models.CharField(max_length=50)
    match_percentage = models.BigIntegerField(blank=True, null=True)
    address_validation_score = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)











class table4(models.Model):
    id = models.BigIntegerField(primary_key=True)
    table1id = models.ForeignKey(table1, on_delete=models.CASCADE, blank=True,
                                 null=True)  # show on frontend table3id of the table1id
    ultimateparentid = models.ForeignKey(table3, related_name='ultimate_parent', on_delete=models.CASCADE, blank=True,
                                         null=True)  # show on frontend table3id of the ultimateparentid
    parentid = models.ForeignKey(table3, related_name='parent_id', on_delete=models.CASCADE, blank=True,
                                 null=True)  # show on frontend table3id of the parentid
    lkp_table7id = models.ForeignKey(lkp_table7, on_delete=models.CASCADE, blank=True, null=True)
    legalentity = models.BooleanField()  # show on frontend as checkbox
    override = models.BooleanField()  # show on frontend as checkbox
    description = models.TextField(blank=True, null=True)
    lastverifieddate = models.DateTimeField(blank=True, null=True)  # show on frontend  HI verified Modified date
    lastverifiedbyid = models.CharField(max_length=500, blank=True,
                                        null=True)  # show on frontend  HI verified Modified ID
    createddate = models.DateTimeField(blank=True, null=True)
    createdbyid = models.CharField(max_length=500, blank=True, null=True)
    lastmodifieddate = models.DateTimeField(blank=True, null=True)  # show on frontend  HI last Modified date
    lastmodifiedbyid = models.CharField(max_length=500, blank=True, null=True)  # show on frontend HI last Modified id
    isactive = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.id)



class table5(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lkp_overridecategoryid = models.ForeignKey(lkp_overridecategory, on_delete=models.CASCADE, blank=True, null=True)
    table4id = models.ForeignKey(table4, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)  # show on frontend as override reason
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)







class table6(models.Model):
    id = models.BigIntegerField(primary_key=True)
    survivour_table1id = models.ForeignKey(table1, related_name='survivor', on_delete=models.CASCADE, blank=True, null=True)
    nonsurvivour_table1id = models.ForeignKey(table1, related_name='non_survivor', on_delete=models.CASCADE, blank=True, null=True)
    mergedate = models.DateTimeField()
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)


class lkp_table3name(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField()
    createdbyid = models.CharField(max_length=500)
    lastmodifieddate = models.DateTimeField()
    lastmodifiedbyid = models.CharField(max_length=500)
    isactive = models.BooleanField()

    def __str__(self):
        return str(self.id)