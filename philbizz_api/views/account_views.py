from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from philbizz_api.serializers import AccountCreateSerializer, AccountLoginSerializer
import logging

logger = logging.getLogger(__name__)

class AccountCreationView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            if response == 200:
                return Response(
                    {"message": response},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": response.name}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountLoginView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            response_data = response.dict()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)