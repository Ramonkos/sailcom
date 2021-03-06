from django.http import HttpResponse
from rest_framework.generics import GenericAPIView

from .serializers import CreateRegistrationSerializer, ValidateRegistrationSerializer


class CreateRegistrationView(GenericAPIView):
    """ create inactive user """
    serializer_class = CreateRegistrationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer.validated_data)

        res = {
            "Ein Token wurde an die Email geschickt"
        }
        return HttpResponse(res, status=200)


class ValidateRegistrationView(GenericAPIView):
    """ update user info and activate account """
    permission_classes = []
    serializer_class = ValidateRegistrationSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer.validated_data)

        res = {
            "Vielen Dank für Ihre Registrierung! Sie können sich jetzt anmelden"
        }
        return HttpResponse(res, status=200)
