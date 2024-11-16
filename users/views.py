# users/views.py
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.db.models import Q

class LoadUserDataView(APIView):
    def get(self, request):
        # Retrieve all users from the database
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        print(request.FILES)
        # Check if a file was uploaded
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Read and parse the JSON file
        try:
            data = json.load(uploaded_file)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON file"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the data is a list of user dictionaries
        if not isinstance(data, list):
            return Response({"error": "Expected a list of user data objects in the file"}, status=status.HTTP_400_BAD_REQUEST)

        # Iterate through each user in the list and validate/save
        for user_data in data:
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()  # Save each valid user to the database
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User data loaded successfully"}, status=status.HTTP_201_CREATED)

class SearchUserView(APIView):
    def get(self, request):
        search_query = request.query_params.get('query', None)
        if not search_query:
            return Response({"error": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter users based on the search query in multiple fields
        users = User.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(contact_number__icontains=search_query)
        )

        if users.exists():
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No users found matching the search query"}, status=status.HTTP_404_NOT_FOUND)
