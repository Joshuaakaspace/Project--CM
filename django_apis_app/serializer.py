from .models import *
from rest_framework import serializers

class DataSerializers(serializers.ModelSerializer):
    sourcereferenceid = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    subregion = serializers.SerializerMethodField()
    sfdc_segmentation = serializers.SerializerMethodField()
    segment_source = serializers.SerializerMethodField()

    entity_url = serializers.SerializerMethodField()
    heirarchie_name = serializers.SerializerMethodField()
    segment_type = serializers.SerializerMethodField()
    segment_name = serializers.SerializerMethodField()
    non_survivor = serializers.SerializerMethodField()
    survivor = serializers.SerializerMethodField()
    override_last_modified_id = serializers.SerializerMethodField()
    override_last_modified_date = serializers.SerializerMethodField()
    reason = serializers.SerializerMethodField()
    hi_last_modified_id = serializers.SerializerMethodField()
    hi_last_modified_date = serializers.SerializerMethodField()
    override = serializers.SerializerMethodField()
    legalentity = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()
    ultimate_parent_id = serializers.SerializerMethodField()
    customer_type = serializers.SerializerMethodField()
    # source_reference_id = serializers.SerializerMethodField()
    ot_lastmodified_by = serializers.SerializerMethodField()
    ot_lastmodified_date = serializers.SerializerMethodField()
    org_type = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    class Meta:
        model = table1
        fields = ["id", "permid", "name", "lastmodifieddate", "lastmodifiedbyid", "streetaddress",
                  "lkp_countryid", "city", "state", "postcode", "oaaddresstype", "createddate",
                  "createdbyid", "manualapprovaldate", "manualapproval", "region", "subregion", "sourcereferenceid", "sfdc_segmentation", "segment_source",
                  "entity_url", "org_type", "ot_lastmodified_date", "ot_lastmodified_by",
                  "customer_type", "ultimate_parent_id", "parent_id", "legalentity", "override", "hi_last_modified_date",
                  "hi_last_modified_id", "reason", "override_last_modified_date", "override_last_modified_id", "survivor",
                  "non_survivor", "segment_name", "segment_type", "heirarchie_name", "country"]
        # fields = ["a_number", "account_name", "account_status", "address", "country", "last_updated", "segment_source", "entity_url",
        #           "unavailable", "segmentation_details", "sfdc_segmentation", "modified"]



    def to_representation(self, instance):
        rep = super(DataSerializers, self).to_representation(instance)
        try:
            a = str(instance.lastmodifieddate)
            print("a", a)
            b = a.split(" ")
            date = b[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]
            time = b[1][0:5]
            print("datentime", date, time)
            date_time = time + "   " + date
        except:
            date_time = ""
        rep["lastmodifieddate"] = date_time
        try:
            a = str(instance.createddate)
            print("a", a)
            b = a.split(" ")
            date = b[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]
            time = b[1][0:5]
            print("datentime", date, time)
            date_time = time + "   " + date
        except:
            date_time = ""
        rep["createddate"] = date_time
        try:
            a = str(instance.manualapprovaldate)
            print("a", a)
            b = a.split(" ")
            date = b[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]
            time = b[1][0:5]
            print("datentime", date, time)
            date_time = time + "   " + date
        except:
            date_time = ""
        rep["manualapprovaldate"] = date_time
        # print("datentime", datentime)
        return rep

    def get_sourcereferenceid(self, obj):
        try:
            anumber = table3.objects.filter(table1id=obj.id).first()
            return str(anumber.sourcereferenceid)
        except:
            return ""

    def get_region(self, obj):
        try:
            region = lkp_region.objects.filter(id=obj.lkp_countryid.lkp_regionid.id).first()
            return str(region.name)
        except:
            return ""
    def get_country(self, obj):
        try:
            region = lkp_country.objects.filter(id=obj.lkp_countryid.id).first()
            return str(region.name)
        except:
            return ""

    def get_subregion(self, obj):
        try:
            subregion = lkp_subregion.objects.filter(id=obj.lkp_countryid.lkp_subregionid.id).first()
            return str(subregion.name)
        except:
            return ""

    def get_sfdc_segmentation(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.value)
        except:
            return ""

    def get_segment_source(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.cf_segmentation_website)
        except:
            return ""

    def get_entity_url(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.cf_segmentattion_entityurl)
        except:
            return ""

    def get_org_type(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.value)
        except:
            return ""

    def get_ot_lastmodified_date(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            a = str(sfdc.lastmodifieddate)
            print("a", a)
            b = a.split(" ")
            date = b[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]
            time = b[1][0:5]
            print("datentime", date, time)
            date_time = time + "   " + date
            return date_time
        except:
            return ""

    def get_ot_lastmodified_by(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.lastmodifiedbyid)
        except:
            return ""

    def get_customer_type(self, obj):
        try:
            source_id = table3.objects.filter(table1id=obj.id).first()
            return str(source_id.customertype)
        except:
            return ""

    def get_ultimate_parent_id(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            return str(table4query.ultimateparentid.sourcereferenceid)
        except:
            return ""

    def get_parent_id(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            return str(table4query.parentid.sourcereferenceid)
        except:
            return ""

    def get_legalentity(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            return str(table4query.legalentity)
        except:
            return ""

    def get_override(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            return str(table4query.override)
        except:
            return ""

    def get_hi_last_modified_date(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            a = str(table4query.lastmodifieddate)
            print("a", a)
            b = a.split(" ")
            date = b[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]
            time = b[1][0:5]
            print("datentime", date, time)
            date_time = time + "   " + date
            return str(date_time)
        except:
            return ""

    def get_hi_last_modified_id(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            return str(table4query.lastmodifiedbyid)
        except:
            return ""

    def get_reason(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            table5query = table5.objects.filter(table4id=table4query.id).first()
            return str(table5query.reason)
        except:
            return ""

    def get_override_last_modified_date(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            table5query = table5.objects.filter(table4id=table4query.id).first()
            a = str(table5query.lastmodifieddate)
            print("a", a)
            b = a.split(" ")
            date = b[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]
            time = b[1][0:5]
            print("datentime", date, time)
            date_time = time + "   " + date
            return date_time
        except:
            return ""

    def get_override_last_modified_id(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            table5query = table5.objects.filter(table4id=table4query.id).first()
            return str(table5query.lastmodifiedbyid)
        except:
            return ""

    def get_survivor(self, obj):
        try:
            table6query = table6.objects.filter(survivour_table1id=obj.id).first()
            if table6query:
                table3query = table3.objects.filter(table1id=table6query.survivour_table1id.id).first()
                survivor = table3query.sourcereferenceid
            return survivor
        except:
            return ""

    def get_non_survivor(self, obj):
        try:
            table6query = table6.objects.filter(nonsurvivour_table1id=obj.id).first()
            if table6query:
                table3query = table3.objects.filter(table1id=table6query.survivour_table1id.id).first()
                survivor = table3query.sourcereferenceid
            return survivor
        except:
            return ""

    def get_segment_name(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.lkp_table2nameid.name)
        except:
            return ""

    def get_segment_type(self, obj):
        try:
            sfdc = table2.objects.filter(table1id=obj.id).first()
            return str(sfdc.lkp_table2nameid.type)
        except:
            return ""

    def get_heirarchie_name(self, obj):
        try:
            table4query = table4.objects.filter(table1id=obj.id).first()
            return str(table4query.lkp_table7id.name)
        except:
            return ""

    # def get_name(self, obj):
    #     try:
    #         return obj.customermasterid.name
    #     except:
    #         return ""
    # def get_city(self, obj):
    #     try:
    #         return obj.customermasterid.city
    #     except:
    #         return ""
    # def get_Streetaddress_1(self, obj):
    #     try:
    #         return obj.customermasterid.streetaddress
    #     except:
    #         return ""
    # def get_sourcereferenceid(self, obj):
    #     try:
    #         a_number = Sourcesystem.objects.filter(customermasterid=obj.customermasterid).first()
    #         return a_number.sourcereferenceid
    #     except:
    #         return ""
