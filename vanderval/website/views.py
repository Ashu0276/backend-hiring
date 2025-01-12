from .serializers import SiteSerializers, UserRecordsSerializers, JobSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Site,UserRecords, Job
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import AllowAny
from django.utils.timezone import now 
from .tasks import task_01,task_02,task_03,task_04,task_05



class SiteCreateAPIView(APIView):
    """
    API view for creating a new Site object.

    This API allows users to create a new site by providing the necessary information such as
    the name, domain, URL, record capacity, and description. The API validates the input data,
    creates a new Site instance, and returns the site details along with the generated Site ID.

    Permissions:
        - AllowAny: This API is accessible to any user.

    HTTP Method:
        - POST: Used to create a new site.

    Request Body (JSON):
        - name (string): The name of the site.
        - domain (string): The domain of the site.
        - url (string): The URL of the site.
        - record_capacity (integer): The capacity of records the site can hold.
        - description (string): A description of the site.

    Response (JSON):
        - success (boolean): Whether the operation was successful.
        - site_id (integer): The ID of the newly created site.
        - name (string): The name of the site.
        - domain (string): The domain of the site.
        - url (string): The URL of the site.
        - record_capacity (integer): The record capacity of the site.
        - description (string): The description of the site.
        - errors (object): If there were any validation errors, this field contains the errors.

    Error Responses:
        - HTTP 400: If the input data is invalid.
        - HTTP 500: If an internal server error occurs during the processing of the request.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        API to create a new site.

        **POST /site/**
        
        **Description**: This API endpoint allows the user to create a new site by submitting necessary information 
        such as name, domain, URL, record capacity, and an optional description. If the data is valid, a new site 
        is created, and the site details along with the Site ID are returned in the response.

        **Request Parameters**:
        - `name` (string): The name of the site. (Required)
        - `domain` (string): The domain of the site. (Required)
        - `url` (string): The URL of the site. (Required)
        - `record_capacity` (integer): The capacity of records the site can hold. (Required)
        - `description` (string): A description of the site. (Optional)

        **Response**:
        - `201 Created`: If the site is successfully created, the response will include the details of the new site.
        - `400 Bad Request`: If the validation of input fails, the errors will be returned.
        - `500 Internal Server Error`: If an unexpected error occurs while creating the site.
        """

        # Deserialize incoming data using the Site serializer
        serializer = SiteSerializers(data=request.data)

        try:
            # Check if the serializer is valid
            if serializer.is_valid():
                # Extract validated data from the serializer
                name = serializer.validated_data.get('name')
                domain = serializer.validated_data.get('domain')
                url = serializer.validated_data.get('url')
                record_capacity = serializer.validated_data.get('record_capacity')
                #record_capacity = serializer.validate_record_capacity(record_capacity)
                description = request.data.get('description')
                # Create a new Site object with the validated data
                site_object = Site.objects.create(
                    name=name,
                    domain=domain,
                    url=url,
                    record_capacity=record_capacity,
                    description=description
                )
                site_object.save()  # Save the new site to the database

                # Return a success response with the site details
                return Response({
                    "Success": True,
                    "Site_id": site_object.id,
                    "name": site_object.name,
                    "domain": site_object.domain,
                    "url": site_object.url,
                    "record_capacity": site_object.record_capacity,
                    "description": site_object.description
                }, status=status.HTTP_201_CREATED)

            # If the serializer is not valid, return a 400 Bad Request with validation errors
            return Response({"success": False, "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any unexpected errors and return a 500 Internal Server Error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRecordCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user record with the provided data.
        
        Request body:
        {
            "site": int,           # ID of the related Site object
            "name": string,        # Name of the user
            "email": string,       # Email address of the user
            "phone": string,       # Phone number of the user
            "address": string,     # Address of the user
            "country": string,     # Country of the user
            "state": string,       # State of the user
            "city": string,        # City of the user
            "pincode": string,     # Pincode of the user
            "dob": date,           # Date of birth of the user
            "is_active": boolean   # Boolean flag indicating whether the user is active
        }

        Response:
        - If successful, returns status 201 Created along with the user details (ID).
        - If validation fails, returns status 400 Bad Request with the errors.
        - If any exception occurs, returns status 500 Internal Server Error with error details.
        """
        # Initialize serializer to validate the incoming data
        serializer = UserRecordsSerializers(data=request.data)

        try:
            # Check if the provided data is valid according to the serializer
            if serializer.is_valid():
                # Extract validated data from the serializer
                site = serializer.validated_data.get('site')
                name = serializer.validated_data.get('name')
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('phone')
                address = serializer.validated_data.get('address')
                country = serializer.validated_data.get('country')
                state = serializer.validated_data.get('state')
                city = serializer.validated_data.get('city')
                pincode = serializer.validated_data.get('pincode')
                dob = serializer.validated_data.get('dob')

                # Create a new UserRecords object with the validated data
                userObj = UserRecords.objects.create(
                    site=site,  # Associate the User with a specific Site
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    country=country,
                    state=state,
                    city=city,
                    pincode=pincode,
                    dob=dob,
                    is_active=True
                )

                # Save the user object to the database
                userObj.save()

                # Return the response with the success status and the created user ID
                return Response({
                    "Success": True,
                    "cust_id": userObj.id,
                    "name": userObj.name,
                    "email": userObj.email,
                    "phone": userObj.phone,
                    "address": userObj.address,
                    "country": userObj.country,
                    "state": userObj.state,
                    "city": userObj.city,
                    "pincode": userObj.pincode,
                    "dob": userObj.dob,
                    "is_active": True,
                }, status=status.HTTP_201_CREATED)

            # If the serializer is not valid, return the validation errors
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # If any exception occurs, return a 500 Internal Server Error with the exception message
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


def does_customer_exist(cust_id):
    """
    Checks whether the customer with the given `cust_id` exists or not.

    Args:
        cust_id: The ID of the customer.

    Returns:
        bool: True if the customer exists, False otherwise.
    """
    try:
        # Try to get the user record by customer ID
        user_record = UserRecords.objects.get(id=cust_id)
        if user_record:
            return True
        return False
    except UserRecords.DoesNotExist:
        # If the user record does not exist, return False
        return False


class JobCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new job for a customer with the provided data.

        Request body:
        {
            "cust_id": int,        # The customer ID
            "job_type": int        # The type of job to be executed (1, 2, 3, etc.)
        }

        Response:
        - If the customer does not exist, returns 404 Not Found with an error message.
        - If the job is created successfully, returns 200 OK with job details.
        - If the job creation fails, returns 400 Bad Request with failure message.
        - If any exception occurs, returns 500 Internal Server Error with the error message.
        """
        # Initialize serializer to validate incoming data
        serializer = JobSerializers(data=request.data)

        try:
            # Check if the provided data is valid according to the serializer
            if serializer.is_valid():
                # Extract validated data from the serializer
                cust_id = serializer.validated_data['cust_id']
                job_type = serializer.validated_data['job_type']

                # Check if the customer exists using the helper function
                cust_id_exist = does_customer_exist(cust_id.id)
                if not cust_id_exist:
                    # If customer does not exist, return 404 Not Found
                    return Response({"detail": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)

                # Get the associated site from the specific `cust_id`
                site_obj = cust_id.site  # Access the site via the `cust_id` instance

                # Create a new Job object and set its status to 'in_progress'
                job_obj = Job.objects.create(
                    cust_id=cust_id,
                    job_type=job_type,
                )
                job_obj.status = 'in_progress'
                job_obj.save()

                # Initialize the result variable to track the success of the job
                result = False
                # Perform specific tasks based on the job type
                if job_type == 1:
                    result = task_01(site_obj.id)
                elif job_type == 2:
                    result = task_02(site_obj.id)
                elif job_type == 3:
                    result = task_03(site_obj.id)
                elif job_type == 4:
                    result = task_04(site_obj.id)
                elif job_type == 5:
                    result = task_05(site_obj.id)

                # If the task is successful, update job status to 'completed'
                if result:
                    job_obj.status = 'completed'
                    job_obj.job_end_time = now()  # Record the end time
                    job_obj.save()

                    # Return a detailed success response
                    return Response({
                        "detail": "Job completed successfully.",
                        "cust_id": job_obj.cust_id.id,
                        "cust_name": job_obj.cust_id.name,
                        "job_id": job_obj.id,
                        "job_status": job_obj.status,
                        "job_start_time": job_obj.job_start_time,
                        "job_end_time": job_obj.job_end_time,
                        "site_name": site_obj.name,
                    }, status=status.HTTP_200_OK)

                # If the task fails, return a failure response
                return Response({"detail": "Job failed."}, status=status.HTTP_400_BAD_REQUEST)

            # If the serializer data is invalid, return a 400 response with errors
            return Response({
                "detail": "Invalid data provided.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # If any exception occurs, return a 500 Internal Server Error
            return Response({
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
