from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from philbizz_api.serializers import TokenizeInformationSerializer, ValidateTokenizeSerializer


class ValidateTokenizeView(GenericAPIView):
    serializer_class = ValidateTokenizeSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = serializer.validate_token(serializer.validated_data)

        if result.tokenize_information:
            tokenize_information_serializer = TokenizeInformationSerializer(result.tokenize_information)
            return Response({"tokenize_information": tokenize_information_serializer.data}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid token or information."}, status=status.HTTP_400_BAD_REQUEST)