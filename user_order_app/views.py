from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views, permissions
from .models import Order
from .serializers import OrderSerializer
from django.http import Http404, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



@api_view(['POST'])
def login_view(request):
    password = request.data.get('password')
    username = request.data.get('username')
    user = authenticate(username=username, password=password)
    
    if user is not None and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"detail":"Invalid credentials"})



@api_view(['GET'])
def get_emails(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = list(User.objects.all().values_list('email',flat=True))
        return Response(users,status=status.HTTP_200_OK)
    return Response("Non Auth User",status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_emails(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = list(User.objects.all().values_list('email',flat=True))
        return Response(users,status=status.HTTP_200_OK)
    return Response("Non Auth User",status=status.HTTP_401_UNAUTHORIZED)
        


@api_view(['GET'])
def order_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        emails = request.query_params.getlist('email')
        orders = Order.objects.filter(customer__email__in=emails)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response("Non Auth User",status=status.HTTP_401_UNAUTHORIZED)




class OrderListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(customer=self.request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderRetrieveUpdateDestroyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk, customer=self.request.user)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
