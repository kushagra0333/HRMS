from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
# from bson import ObjectId # Imported inside method to avoid global dependency issues if not installed
from .models import Leave
from .serializers import LeaveSerializer
from employees.models import Employee

class LeaveViewSet(viewsets.ModelViewSet):
    # Access all leave objects.
    queryset = Leave.objects.all()
    # Use the serializer we defined.
    serializer_class = LeaveSerializer
    # Ensure only logged-in users can access this API.
    permission_classes = [permissions.IsAuthenticated]

    # Custom logic to determine which leave requests the current user sees.
    def get_queryset(self):
        user = self.request.user
        # If the user is an Admin (is_staff=True), they see ALL leave requests (ordered by newest).
        if user.is_staff: 
            return Leave.objects.all().order_by('-applied_on')
        # If regular employee, they only see THEIR OWN leave requests.
        try:
            return Leave.objects.filter(employee=user.employee).order_by('-applied_on')
        except Employee.DoesNotExist:
            # If the user has no linked Employee profile, return nothing.
            return Leave.objects.none()

    # Custom logic to retrieve a single object.
    # This is overridden mainly to handle MongoDB ObjectIds which are strings in the URL 
    # but need to be converted to ObjectId objects for the query (sometimes).
    def get_object(self):
        # basic get_queryset + filter logic
        queryset = self.filter_queryset(self.get_queryset())
        
        # Determine the lookup field (usually 'pk' or 'id')
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        # Verify the URL argument exists
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
        # Djongo/MongoDB Hack:
        # If we are searching by 'pk' (primary key) and it's a string,
        # we try to convert it to a BSON ObjectId.
        if 'pk' in filter_kwargs and isinstance(filter_kwargs['pk'], str):
            from bson import ObjectId
            try:
                filter_kwargs['pk'] = ObjectId(filter_kwargs['pk'])
            except:
                pass # If it's not a valid ObjectId format, let Django handle the 404 naturally.

        # Retrieve the object or return 404 if not found.
        obj = get_object_or_404(queryset, **filter_kwargs)
        # Check if the user has permission to view this specific object.
        self.check_object_permissions(self.request, obj)
        return obj

    # Custom logic for creating a new Leave request.
    def perform_create(self, serializer):
        # Automatically associate the new leave request with the currently logged-in employee.
        try:
            serializer.save(employee=self.request.user.employee)
        except Employee.DoesNotExist:
            # Error if the user trying to apply doesn't have an employee profile.
            raise serializers.ValidationError("User is not linked to an Employee profile.")

    # Custom Action: Approve Leave.
    # Only Admins can access this (IsAdminUser).
    # detailed=True means this action is on a single object (e.g. /leaves/{id}/approve/).
    # methods=['patch'] means it expects a PATCH request.
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        print(f"DEBUG: Approve action called. PK: {pk}, User: {request.user}, Is Staff: {request.user.is_staff}")
        try:
            leave = self.get_object() # Fetch the leave request
            print(f"DEBUG: Leave object found: {leave}")
            leave.status = 'Approved' # Update status
            leave.save() # Save to DB
            return Response({'status': 'leave approved'})
        except Exception as e:
            print(f"DEBUG: Error in approve: {e}")
            raise e

    # Custom Action: Reject Leave.
    # Similar to approve, but sets status to 'Rejected'.
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        print(f"DEBUG: Reject action called. PK: {pk}, User: {request.user}, Is Staff: {request.user.is_staff}")
        try:
            leave = self.get_object()
            print(f"DEBUG: Leave object found: {leave}")
            leave.status = 'Rejected'
            leave.save()
            return Response({'status': 'leave rejected'})
        except Exception as e:
            print(f"DEBUG: Error in reject: {e}")
            raise e
