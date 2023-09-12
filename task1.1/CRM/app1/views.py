


from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import User, Customer, Service, Active
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from django.http import HttpResponse
import json
import bcrypt 
from django.db.models import Q


# -------------------------------------
class registerVueView(APIView):
    def post(self, request):
        errors = User.objects.basic_validator(request.data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return JsonResponse(errors, safe=False)
        else:
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            email = request.data.get('email')
            pwd_hash = bcrypt.hashpw(request.data.get('pwd').encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(fname=fname, lname=lname, email=email, pwd_hash=pwd_hash)
            request.session['id'] = user.id
            request.session['fname'] = fname
        return JsonResponse({"response": True}, safe=False)



class allCust(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializers = CustomerSerializer(customers, many=True)

        return JsonResponse(serializers.data, safe=False)


class allServ(APIView):
    def get(self, request):
        Services = Service.objects.all()
        serializers = ServiceSerializer(Services, many=True)
        print(request.session.get('id'))
        print("/-"*50)
        return JsonResponse(serializers.data, safe=False)


class AddCustomerPage(APIView):
    def post(self, request):
        errors = Customer.objects.basic_validator(request.data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return JsonResponse(errors, safe=False)
        else:
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            email = request.data.get('email')
            phone = request.data.get('phone')
            address = request.data.get('address')

            customer = Customer.objects.create(fname=fname, lname=lname, email=email, phone=phone, address=address,user=User.objects.get(id=1))

        return JsonResponse({"response": True}, safe=False)





class CustInfo(APIView):
    def get(self, request, id):
        customer = Customer.objects.get(id = id)
        serializers = CustomerSerializer(customer, many=False)

        return JsonResponse(serializers.data, safe=False)

class updateCustomerPage(APIView):
    def post(self, request):
        errors = Customer.objects.basic_validator(request.data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return JsonResponse(errors, safe=False)
        else:
            
            id = request.data.get('id')
            customer = Customer.objects.get(id=int(id))
            customer.id = int(id)
            customer.fname = request.data.get('fname')
            customer.lname = request.data.get('lname')
            customer.email = request.data.get('email')
            customer.phone = request.data.get('phone')
            customer.address = request.data.get('address')
            customer.save()

        return JsonResponse({"response": "updated"}, safe=False)

# loginVue

# class loginVue(View):
#     def post(self, request):
#         errors = User.objects.login_validator(request.POST)
#         if len(errors) > 0:
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return JsonResponse(errors, safe=False)
#         else:
#             email = request.POST['email']
#             user = User.objects.filter(email=email)
#             request.session['id'] = user[0].id
#             return JsonResponse({"response": True}, safe=False)


# AllServInCust

class AllServInCust(APIView):
    def get(self, request, id):
        customer = Customer.objects.get(id = id)
        actives = Active.objects.filter(customer = customer)
        allServinCust = []
        for i in actives:
            allServinCust.append(i.service)
        serializers = ServiceSerializer(allServinCust, many=True)
        return JsonResponse(serializers.data, safe=False)
    



class AllServNotInCust(APIView):
    def get(self, request, id):
        customer = Customer.objects.get(id=id)
        services = Service.objects.all()
        activeCust = Active.objects.filter(customer=customer)
        active_services = list(activeCust.values_list('service_id', flat=True))
        services = services.exclude(id__in=active_services)
        serializers = ServiceSerializer(services, many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)


class addServ(APIView):
    def get(self, request, custId, servId):
        customer = Customer.objects.get(id=custId)
        service = Service.objects.get(id = servId)
        active = Active.objects.create(isActive=True,service=service,customer=customer)

        actives = Active.objects.filter(customer = customer)
        allServinCust = []
        for i in actives:
            allServinCust.append(i.service)
        serializer1 = ServiceSerializer(allServinCust, many=True)


        services = Service.objects.all()
        activeCust = Active.objects.filter(customer=customer)
        active_services = list(activeCust.values_list('service_id', flat=True))
        services = services.exclude(id__in=active_services)

        serializer2 = ServiceSerializer(services, many=True)
        # -------------------------
        AllActivesForCustMainAA1 = AllActivesForCustMainAA()
        AllActivesForCustMainAA1A = AllActivesForCustMainAA1.get(request=request,custId = custId)
        print(AllActivesForCustMainAA1A)
        
        print('/4'*70)
        # -----------------------
        # return JsonResponse(serializers.data, safe=False)
        Serializer_list = [serializer1.data, serializer2.data]

        content = {
            'status': 1, 
            'responseCode' : status.HTTP_200_OK, 
            'data': Serializer_list,
        }
        return Response(content)

class log(View):
    def get(seld, request,email, pwd):
        postData= {
            'email': email,
            'pwd': pwd,
        }
        errors = User.objects.login_validator(postData)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return JsonResponse(errors, safe=False)
        else:
            
            user = User.objects.filter(email=email)
            request.session['id'] = user[0].id
            return JsonResponse({"response": True}, safe=False)


# activation

class activation(APIView):
    def get(self, request, custId, activeId):
        AllActivesForCustMainAA1 = AllActivesForCustMainAA()
        AllActivesForCustMainAA1A = AllActivesForCustMainAA1.get(request=request,custId = custId)
        customer = Customer.objects.get(id=custId)
        active =Active.objects.get(id = activeId)
        if active.isActive:
            active.isActive = False
        else:
            active.isActive = True
        active.save()
        print("l/m"*70)
        actives = Active.objects.filter(customer = customer)
        allServinCust = []
        for i in actives:
            allServinCust.append(i.service)
        serializer1 = ServiceSerializer(allServinCust, many=True)


        services = Service.objects.all()
        activeCust = Active.objects.filter(customer=customer)

        active_services = list(activeCust.values_list('service_id', flat=True))

        services = services.exclude(id__in=active_services)

        serializer2 = ServiceSerializer(services, many=True)

        Serializer_list = [serializer1.data, serializer2.data,AllActivesForCustMainAA1A]

        content = {
            'status': 1, 
            'responseCode' : status.HTTP_200_OK, 
            'data': Serializer_list,
        }
        return Response(content)

class AllActivesForCustMain(APIView):
    def get(self, request, custId):
        customer = Customer.objects.get(id = custId)
        actives = Active.objects.filter(customer = customer)
        
        data = [
            {
                'id': active.id,
                'isActive': active.isActive,
                'service': {
                    'id':active.service.id,
                    'name':active.service.name,
                    'desc':active.service.desc,
                    'price':active.service.price,
                    'isActive':active.service.isActive,
                },
                'customer':{
                    'id':active.customer.id,
                    'fname':active.customer.fname,
                    'lname':active.customer.lname,
                    'email':active.customer.email,
                    'phone':active.customer.phone,
                    'address':active.customer.address,
                    
                } 
            }
            for active in actives
        ]
        return JsonResponse(data, safe=False)



class AllActivesForCustMainAA(APIView):
    def get(self, request, custId):
        customer = Customer.objects.get(id = custId)
        actives = Active.objects.filter(customer = customer)
        
        data = [
            {
                'id': active.id,
                'isActive': active.isActive,
                'service': {
                    'id':active.service.id,
                    'name':active.service.name,
                    'desc':active.service.desc,
                    'price':active.service.price,
                    'isActive':active.service.isActive,
                },
                'customer':{
                    'id':active.customer.id,
                    'fname':active.customer.fname,
                    'lname':active.customer.lname,
                    'email':active.customer.email,
                    'phone':active.customer.phone,
                    'address':active.customer.address,
                    
                } 
            }
            for active in actives
        ]
        return data


class SearchView(APIView):
    def get(self, request,searchSrt):
        search_query = searchSrt
        customers = Customer.objects.filter(Q(fname__icontains=search_query) | Q(lname__icontains=search_query))
        if customers:
                
            serializer = CustomerSerializer(customers, many=True)

            return Response(serializer.data)
        else:
            return Response({'customers':[]})



# class activationServ(APIView):
#     def get(self, request, servId):        
#         service = Service.objects.get(id = servId)
#         if (service.isActive == True):
#             service.isActive = False
#         else:
#             service.isActive = True
#         service.save()
#         services = Service.objects.all()
#         serializer = ServiceSerializer(services, many=True)
#         return JsonResponse(serializer, safe=False)


class activationServ(APIView):
    def get(self, request, servId):
        try:
            service = Service.objects.get(id=servId)
            service.isActive = not service.isActive
            service.save()
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Service.DoesNotExist:
            return JsonResponse({"message": "Service not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        





class deleteCust(APIView):
    def get(self, request, custId):
        try:
            customer = Customer.objects.get(id=custId)
            customer.delete()
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Service.DoesNotExist:
            return JsonResponse({"message": "customer not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
