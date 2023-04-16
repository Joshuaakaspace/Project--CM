from .serializer import *
from .models import *
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.permissions import IsAuthenticated
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.

class LoginApi(APIView):

    @staticmethod
    def post(request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        try:
            if User.objects.filter(username=username).first():
                user = User.objects.filter(username=username).first()
                if password != "":
                    if check_password(password, user.password):
                        token, created = Token.objects.get_or_create(user=user)
                        params = {
                            'user_id': user.pk,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'token': str(token.key),
                        }
                        return Response({'success': True, 'message': 'Logged in Successfully', 'data': params},
                                        status=status.HTTP_200_OK)
                    else:
                        return Response({'success': False,
                                         'message': "Incorrect password. Try different or forgot password.",
                                         'data': None},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'success': False, 'message': "Both fields are required", 'data': None},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'message': "Email/User not found. Try Signup", 'data': None},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': 'Something went wrong', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)


class GetData(APIView):
    def get(self, request):
        search = request.query_params.get('search', None)
        print("search", search)
        record_id = request.query_params.get('record_id', None)

        if search:
            try:
                search = int(search)
                qs = table1.objects.filter(permid__icontains=search)
                serializer = DataSerializers(qs, many=True)
                return Response({'success': True, 'message': '', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            except:
                qs = table1.objects.filter(name__icontains=search)
                serializer = DataSerializers(qs, many=True)
                return Response({'success': True, 'message': '', 'data': serializer.data},
                                status=status.HTTP_200_OK)
        elif record_id:
            qs = table1.objects.filter(id=int(record_id))
            if qs:
                serializer = DataSerializers(qs)
                return Response({'success': True, 'message': '', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': True, 'message': '', 'data': []},
                                status=status.HTTP_200_OK)
        else:
            qs = table1.objects.all().order_by('-lastmodifieddate')[0:10]
            serializer = DataSerializers(qs, many=True)
            return Response({'success': True, 'message': '', 'data': serializer.data},
                            status=status.HTTP_200_OK)

@login_required
def test(request):
    return render(request, "home.html")

def index(request):
    messages = ''
    if request.method == "POST":
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        print("email", email)
        print("password", password)
        user=authenticate(username= email, password= password)
        if user is not None:
            print("in if user")
            login(request, user)
            return redirect("home/")
        else:
            messages = "Invalid credentials! Please try again"
            print("in else user")
    return render(request, 'Login.html', {"messages": messages})

@login_required
def signout(request):
    logout(request)
    return render(request, 'Login.html', {"messages": ''})


@login_required(login_url="/")
def singleview(request, id):
    print("id", id)
    qs = table1.objects.filter(id=int(id)).first()
    if qs:
        serializer = DataSerializers(qs)
    return render(request, 'single.html', {"data":serializer.data})

@login_required(login_url="/")
def editview(request, id):
    if request.method == "POST":
        id = request.POST.get('id_record', '')
        permid = request.POST.get('permid', '')
        ultimateparentname = request.POST.get('ultimateparentname', '')
        state = request.POST.get('state', '')
        streetaddress = request.POST.get('streetaddress', '')
        organizationtype = request.POST.get('organizationtype', '')
        city = request.POST.get('city', '')
        heirarchie_name = request.POST.get('heirarchie_name', '')
        entityurl = request.POST.get('entityurl', '')
        country = request.POST.get('country', '')
        segment_source = request.POST.get('segment_source', '')
        region = request.POST.get('region', '')
        subregion = request.POST.get('subregion', '')
        customertype = request.POST.get('customertype', '')
        name = request.POST.get('name', '')
        oaaddresstype = request.POST.get('oaaddresstype', '')
        postcode = request.POST.get('postcode', '')
        reason = request.POST.get('reason', '')
        segment_name = request.POST.get('segment_name', '')
        segment_type = request.POST.get('segment_type', '')
        override = request.POST.get('override', '')
        manualapproval = request.POST.get('manualapproval', '')
        legalentity = request.POST.get('legalentity', '')
        if override:
            override = True
        if not override:
            override = False
        if legalentity:
            legalentity = True
        if not legalentity:
            legalentity = False
        print("override", override)
        print("legal entity", legalentity)

        if id:
            table1data = table1.objects.filter(id=int(id)).first()
            lasteditted = str(request.user.username)
            if table1data:
                if permid:
                    table1data.permid = permid
                if name:
                    table1data.name = name
                if streetaddress:
                    table1data.streetaddress = streetaddress
                if city:
                    table1data.city = city
                if state:
                    table1data.state = state
                if postcode:
                    table1data.postcode = postcode
                if oaaddresstype:
                    table1data.oaaddresstype = oaaddresstype
                if manualapproval:
                    table1data.manualapproval = True
                if not manualapproval:
                    table1data.manualapproval = False

                table1data.lastmodifieddate = datetime.now()
                table1data.lastmodifiedbyid = lasteditted
                table1data.save()
                if ultimateparentname:
                    try:
                        table4query = table4.objects.filter(table1id=int(id)).first()
                        table3query = table3.objects.filter(id=table4query.ultimateparentid.id).first()
                        table_id = table3query.table1id.id
                        get_name = table1.objects.filter(id=table_id).first()
                        get_name.name = ultimateparentname
                        get_name.save()
                    except:
                        pass
                if organizationtype:
                    sfdc = table2.objects.filter(table1id=int(id)).first()
                    if sfdc:
                        sfdc.value = organizationtype
                        sfdc.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table2.objects.filter(id=code1).exists():
                                break
                        table2record = table2(id=code1, table1id=table1data, value=organizationtype)
                        table2record.save()
                if entityurl:
                    sfdc = table2.objects.filter(table1id=int(id)).first()
                    if sfdc:
                        sfdc.cf_segmentation_website = entityurl
                        sfdc.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table2.objects.filter(id=code1).exists():
                                break
                        table2record = table2(id=code1, table1id=table1data, cf_segmentation_website=entityurl)
                        table2record.save()

                if segment_source:
                    sfdc = table2.objects.filter(table1id=int(id)).first()
                    if sfdc:
                        sfdc.cf_segmentattion_entityurl = segment_source
                        sfdc.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table2.objects.filter(id=code1).exists():
                                break
                        table2record = table2(id=code1, table1id=table1data, cf_segmentation_website=segment_source)
                        table2record.save()
                if country:
                    if table1data.lkp_countryid:
                        country1 = lkp_country.objects.filter(id=table1data.lkp_countryid.id).first()
                        country1.name = country
                        country1.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not lkp_country.objects.filter(id=code1).exists():
                                break
                        lkpcountry = lkp_country(id=code1,name=country, isactive=True, createddate=datetime.now(),
                                                 lastmodifieddate=datetime.now(), createdbyid=lasteditted, lastmodifiedbyid=lasteditted)
                        lkpcountry.save()
                        lkpcountryid = lkp_country.objects.filter(id=code1).first()
                        table1data.lkp_countryid = lkpcountryid
                        table1data.save()
                if customertype:
                    source_id = table3.objects.filter(table1id=str(id)).first()
                    if source_id:
                        source_id.customertype = customertype
                        source_id.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table3.objects.filter(id=code1).exists():
                                break
                        table3data = table3(id=code1, table1id=table1data, customertype=customertype, isactive=True, createddate=datetime.now(),
                                                 lastmodifieddate=datetime.now(), createdbyid=lasteditted, lastmodifiedbyid=lasteditted)
                        table3data.save()
                if region:
                    if table1data.lkp_countryid:
                        if table1data.lkp_countryid.lkp_regionid:
                            region1 = lkp_region.objects.filter(id=table1data.lkp_countryid.lkp_regionid.id).first()
                            region1.name = region
                            region1.save()
                        else:
                            while (1):
                                code1 = str(random.randint(0, 99999))
                                if not lkp_region.objects.filter(id=code1).exists():
                                    break
                            lkpregion = lkp_region(id=code1, name=region, createddate=datetime.now(),
                                                   createdbyid=lasteditted, isactive=True, lastmodifiedbyid=lasteditted,
                                                   lastmodifieddate=datetime.now())
                            lkpregion.save()
                            lkpcountryregion = lkp_country.objects.filter(id=table1data.lkp_countryid.id).first()
                            lkpcountryregion.lkp_regionid = lkpregion
                            lkpcountryregion.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not lkp_region.objects.filter(id=code1).exists():
                                break
                        while (1):
                            code2 = str(random.randint(0, 99999))
                            if not lkp_country.objects.filter(id=code2).exists():
                                break
                        lkpregion = lkp_region(id=code1, name=region, createddate=datetime.now(),
                                               createdbyid=lasteditted, isactive=True, lastmodifiedbyid=lasteditted,
                                               lastmodifieddate=datetime.now())
                        lkpregion.save()
                        lkpcountrysave = lkp_country(id=code2, lkp_regionid=lkpregion, isactive=True, createddate=datetime.now(),
                                                 lastmodifieddate=datetime.now(), createdbyid=lasteditted, lastmodifiedbyid=lasteditted)
                        lkpcountrysave.save()
                        table1data.lkp_countryid = lkpcountrysave
                        table1data.save()
                if subregion:
                    if table1data.lkp_countryid:
                        if table1data.lkp_countryid.lkp_subregionid:
                            region2 = lkp_subregion.objects.filter(id=table1data.lkp_countryid.lkp_subregionid.id).first()
                            region2.name = subregion
                            region2.save()
                        else:
                            while (1):
                                code1 = str(random.randint(0, 99999))
                                if not lkp_subregion.objects.filter(id=code1).exists():
                                    break
                            lkpsubregion = lkp_subregion(id=code1, name=subregion, createddate=datetime.now(),
                                                   createdbyid=lasteditted, isactive=True, lastmodifiedbyid=lasteditted,
                                                   lastmodifieddate=datetime.now())
                            lkpsubregion.save()
                            lkpcountryregion1 = lkp_country.objects.filter(id=table1data.lkp_countryid.id).first()
                            lkpcountryregion1.lkp_subregionid = lkpsubregion
                            lkpcountryregion1.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not lkp_region.objects.filter(id=code1).exists():
                                break
                        while (1):
                            code2 = str(random.randint(0, 99999))
                            if not lkp_country.objects.filter(id=code2).exists():
                                break
                        lkpsubregion = lkp_subregion(id=code1, name=region, createddate=datetime.now(),
                                               createdbyid=lasteditted, isactive=True, lastmodifiedbyid=lasteditted,
                                               lastmodifieddate=datetime.now())
                        lkpsubregion.save()
                        lkpcountrysave = lkp_country(id=code2, lkp_subregionid=lkpsubregion, isactive=True, createddate=datetime.now(),
                                                 lastmodifieddate=datetime.now(), createdbyid=lasteditted, lastmodifiedbyid=lasteditted)
                        lkpcountrysave.save()
                        table1data.lkp_countryid = lkpcountrysave
                        table1data.save()
                if heirarchie_name:
                    table4query = table4.objects.filter(table1id=int(id)).first()
                    if table4query:
                        table7query = lkp_table7.objects.filter(id=table4query.lkp_table7id.id).first()
                        if table7query:
                            table7query.name = heirarchie_name
                            table7query.save()
                            table4query.lastmodifieddate=datetime.now()
                            table4query.lastmodifiedbyid=lasteditted
                            table4query.save()
                        else:
                            while (1):
                                code1 = str(random.randint(0, 99999))
                                if not lkp_table7.objects.filter(id=code1).exists():
                                    break
                            lkp7 = lkp_table7(id=code1, name=heirarchie_name, createddate=datetime.now(),
                                                         createdbyid=lasteditted, isactive=True,
                                                         lastmodifiedbyid=lasteditted,
                                                         lastmodifieddate=datetime.now())
                            lkp7.save()
                            table4set = table4.objects.filter(table1id=int(id)).first()
                            table4set.lkp_table7id = lkp7
                            table4set.lastmodifieddate=datetime.now()
                            table4set.lastmodifiedbyid=lasteditted
                            table4set.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not lkp_table7.objects.filter(id=code1).exists():
                                break
                        while (1):
                            code2 = str(random.randint(0, 99999))
                            if not table4.objects.filter(id=code2).exists():
                                break
                        lkp7 = lkp_table7(id=code1, name=heirarchie_name, createddate=datetime.now(),
                                          createdbyid=lasteditted, isactive=True,
                                          lastmodifiedbyid=lasteditted,
                                          lastmodifieddate=datetime.now())
                        lkp7.save()
                        lkp4save = table4(id=code2, table1id=table1data, lkp_table7id=lkp7,
                                          lastverifiedbyid=lasteditted,
                                          lastverifieddate=datetime.now(), isactive=True,
                                                     createddate=datetime.now(),
                                                     lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                                     lastmodifiedbyid=lasteditted)
                        lkp4save.save()
                if reason:
                    table4query = table4.objects.filter(table1id=int(id)).first()
                    if table4query:
                        table5query = table5.objects.filter(table4id=table4query.id).first()
                        if table5query:
                            table5query.reason = reason
                            table5query.save()
                        else:
                            while (1):
                                code1 = str(random.randint(0, 99999))
                                if not table5.objects.filter(id=code1).exists():
                                    break
                            table5set = table5(id=code1, table4id=table4query, reason=reason, createddate=datetime.now(),
                                                     lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                                     lastmodifiedbyid=lasteditted, isactive=True)
                            table5set.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table4.objects.filter(id=code1).exists():
                                break
                        while (1):
                            code2 = str(random.randint(0, 99999))
                            if not table5.objects.filter(id=code2).exists():
                                break
                        lkp4save = table4(id=code1, table1id=table1data,
                                          lastverifiedbyid=lasteditted,
                                          lastverifieddate=datetime.now(), isactive=True,
                                          createddate=datetime.now(),
                                          lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                          lastmodifiedbyid=lasteditted)
                        lkp4save.save()
                        table5set = table5(id=code2, table4id=lkp4save, reason=reason, createddate=datetime.now(),
                                           lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                           lastmodifiedbyid=lasteditted, isactive=True)
                        table5set.save()
                if segment_name:
                    sfdc = table2.objects.filter(table1id=int(id)).first()
                    if sfdc:
                        if sfdc.lkp_table2nameid:
                            updatethis = Lkptable2name.objects.filter(id=sfdc.lkp_table2nameid.id).first()
                            updatethis.name = segment_name
                            updatethis.save()
                        else:
                            while (1):
                                code1 = str(random.randint(0, 99999))
                                if not Lkptable2name.objects.filter(id=code1).exists():
                                    break
                            createtable2 = Lkptable2name(id=code1, name=segment_name, createddate=datetime.now(),
                                           lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                           lastmodifiedbyid=lasteditted, isactive=True)
                            createtable2.save()
                            sfdc.lkp_table2nameid=createtable2
                            sfdc.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table2.objects.filter(id=code1).exists():
                                break
                        while (1):
                            code2 = str(random.randint(0, 99999))
                            if not Lkptable2name.objects.filter(id=code2).exists():
                                break
                        createtable2 = Lkptable2name(id=code1, name=segment_name, createddate=datetime.now(),
                                                     lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                                     lastmodifiedbyid=lasteditted, isactive=True)
                        createtable2.save()
                        createtable2data = table2(id=code1, table1id=table1data, lkp_table2nameid=createtable2, lastverifiedbyid=lasteditted,
                                          lastverifieddate=datetime.now(), isactive=True,
                                          createddate=datetime.now(),
                                          lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                          lastmodifiedbyid=lasteditted)
                        createtable2data.save()
                if segment_type:
                    sfdc = table2.objects.filter(table1id=int(id)).first()
                    if sfdc:
                        if sfdc.lkp_table2nameid:
                            updatethis = Lkptable2name.objects.filter(id=sfdc.lkp_table2nameid.id).first()
                            updatethis.type = segment_type
                            updatethis.save()
                        else:
                            while (1):
                                code1 = str(random.randint(0, 99999))
                                if not Lkptable2name.objects.filter(id=code1).exists():
                                    break
                            createtable2 = Lkptable2name(id=code1, type=segment_type, createddate=datetime.now(),
                                                         lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                                         lastmodifiedbyid=lasteditted, isactive=True)
                            createtable2.save()
                            sfdc.lkp_table2nameid = createtable2
                            sfdc.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table2.objects.filter(id=code1).exists():
                                break
                        while (1):
                            code2 = str(random.randint(0, 99999))
                            if not Lkptable2name.objects.filter(id=code2).exists():
                                break
                        createtable2 = Lkptable2name(id=code1, type=segment_type, createddate=datetime.now(),
                                                     lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                                     lastmodifiedbyid=lasteditted, isactive=True)
                        createtable2.save()
                        createtable2data = table2(id=code1, table1id=table1data, lkp_table2nameid=createtable2,
                                                  lastverifiedbyid=lasteditted,
                                                  lastverifieddate=datetime.now(), isactive=True,
                                                  createddate=datetime.now(),
                                                  lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                                  lastmodifiedbyid=lasteditted)
                        createtable2data.save()
                if override == True or override == False:
                    print("in if")
                    table4query = table4.objects.filter(table1id=int(id)).first()
                    if table4query:
                        print("in if if")
                        table4query.override = override
                        print("table check", table4query.override)
                        table4query.save()
                        print("table check", table4query.override)
                    else:
                        print("in if else")
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table4.objects.filter(id=code1).exists():
                                break
                        lkp4save = table4(id=code1, table1id=table1data,
                                          override=override,
                                          lastverifiedbyid=lasteditted,
                                          lastverifieddate=datetime.now(), isactive=True,
                                          createddate=datetime.now(),
                                          lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                          lastmodifiedbyid=lasteditted)
                        lkp4save.save()
                if legalentity == True or legalentity == False:
                    table4query = table4.objects.filter(table1id=int(id)).first()
                    if table4query:
                        table4query.legalentity = legalentity
                        table4query.save()
                    else:
                        while (1):
                            code1 = str(random.randint(0, 99999))
                            if not table4.objects.filter(id=code1).exists():
                                break
                        lkp4save = table4(id=code1, table1id=table1data,
                                          legalentity=legalentity,
                                          lastverifiedbyid=lasteditted,
                                          lastverifieddate=datetime.now(), isactive=True,
                                          createddate=datetime.now(),
                                          lastmodifieddate=datetime.now(), createdbyid=lasteditted,
                                          lastmodifiedbyid=lasteditted)
                        lkp4save.save()
                sfdc = table2.objects.filter(table1id=int(id)).first()
                sfdc.lastmodifieddate = datetime.now()
                sfdc.lastmodifiedbyid = lasteditted
                sfdc.save()





                # if streetaddress:
                #     table1data.streetaddress = streetaddress


    qs = table1.objects.filter(id=int(id)).first()
    if qs:
        serializer = DataSerializers(qs)
        print("data", serializer.data)
    return render(request, 'editview.html', {"data":serializer.data})
