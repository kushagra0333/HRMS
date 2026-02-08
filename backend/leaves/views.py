from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Leave
from .serializers import LeaveSerializer
from employees.models import Employee

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: # Admin sees all
            return Leave.objects.all().order_by('-applied_on')
        try:
            return Leave.objects.filter(employee=user.employee).order_by('-applied_on')
        except Employee.DoesNotExist:
            return Leave.objects.none()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
        # Djongo ObjectId handling hack
        if 'pk' in filter_kwargs and isinstance(filter_kwargs['pk'], str):
            from bson import ObjectId
            try:
                filter_kwargs['pk'] = ObjectId(filter_kwargs['pk'])
            except:
                pass # Let it fail normally if not a valid ObjectId

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        try:
            serializer.save(employee=self.request.user.employee)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("User is not linked to an Employee profile.")

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        print(f"DEBUG: Approve action called. PK: {pk}, User: {request.user}, Is Staff: {request.user.is_staff}")
        try:
            leave = self.get_object()
            print(f"DEBUG: Leave object found: {leave}")
            leave.status = 'Approved'
            leave.save()
            return Response({'status': 'leave approved'})
        except Exception as e:
            print(f"DEBUG: Error in approve: {e}")
            raise e

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
