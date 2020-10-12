from django.shortcuts import render
# API
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserApiSerializer
import requests
import json



# Create your views here.
class fallBackAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    print("Authenticated api!!!!!!")
    # def get(self, request):
    #     users = UserApi.objects.all()
    #     # many = True, many objects at the same time
    #     serializer = UserApiSerializer(users, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        """
        Envia un método post con el mensaje fall_back al bot de rasa y su respuesta
        es enviada a Lili nuevamente.

        Parametros
        fall_back: mensaje de Lili
        param_top: retornar el top n
        """
        post_data = request.data
        params = ['fall_back', 'param_top']
        # verificar si los parametros se enviaron
        if params[0] in post_data and params[1] in post_data:
            data_rasa = json.dumps({"sender": "Lili", "message": post_data['fall_back']})
            headers = {'Content-type': 'application/json'}
            # res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data_rasa, headers=headers)
            res = requests.post('http://localhost:5002/webhooks/rest/webhook', data=data_rasa, headers=headers)
            res = res.json()
            dict_response = res[0]
            # retorna diccionario con la respuesta de rasa bot
            return Response(data=dict_response)
        return Response(data="Parametros no reconocidos")
