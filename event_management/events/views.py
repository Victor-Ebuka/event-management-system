from django.shortcuts import render, get_object_or_404
from .serializers import EventSerializer, RSVPSerializer
from .models import Event
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.response import Response

# Create your views here.

class EventListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        events = Event.objects.filter(created_by=request.user)
        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return get_object_or_404(Event, pk=pk, created_by=user)
    
    def get(self, request, pk):
        event = self.get_object(pk, request.user)
        serializer = EventSerializer(event)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        event = self.get_object(pk, request.user)
        serializer = EventSerializer(event, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request, pk):
        event = self.get_object(pk, request.user)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        event = self.get_object(pk, request.user)
        event.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RSVPView(APIView):
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            event = serializer.validated_data['event']
            if event.capacity <= event.rsvps.count():
                return Response({'detail': 'This event is fully booked.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)