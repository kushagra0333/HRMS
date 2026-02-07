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

    def perform_create(self, serializer):
        try:
            serializer.save(employee=self.request.user.employee)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("User is not linked to an Employee profile.")

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'Approved'
        leave.save()
        return Response({'status': 'leave approved'})

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'Rejected'
        leave.save()
        return Response({'status': 'leave rejected'})
