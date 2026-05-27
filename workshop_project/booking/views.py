from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Workshop, Booking
from .serializers import UserSerializer, WorkshopSerializer, BookingSerializer
from .permissions import IsAdminOrReadOnly, IsOwner

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            "workshop"
        )
