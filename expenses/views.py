from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Expense, User
from .serializers import ExpenseSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @action(detail=False, methods=["get"])
    def by_date_range(self, request):
        user_id = request.query_params.get("user_id")
        start_date = parse_date(request.query_params.get("start_date"))
        end_date = parse_date(request.query_params.get("end_date"))
        if not user_id or not start_date or not end_date:
            raise ValidationError(
                "Please provide user_id, start_date, and end_date in YYYY-MM-DD format."
            )
        expenses = self.queryset.filter(
            user_id=user_id,
            date__range=(start_date, end_date),
        )
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def category_summary(self, request):
        user_id = request.query_params.get("user_id")
        month = request.query_params.get("month")
        if not user_id or not month:
            raise ValidationError("Please provide user_id and month in YYYY-MM format.")
        try:
            year, month = map(int, month.split("-"))
        except ValueError:
            raise ValidationError("Invalid month format. Use YYYY-MM.")
        expenses = self.queryset.filter(
            user_id=user_id,
            date__year=year,
            date__month=month,
        )
        summary = expenses.values("category").annotate(total_amount=Sum("amount"))
        return Response(summary)
