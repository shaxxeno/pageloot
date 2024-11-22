from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Expense, User


class ExpenseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.expense = Expense.objects.create(
            user=self.user,
            title="Lunch",
            amount=15.00,
            date="2024-11-22",
            category="Food",
        )

    def test_create_expense(self):
        url = reverse("expense-list")
        data = {
            "user": self.user.id,
            "title": "Dinner",
            "amount": 20.00,
            "date": "2024-11-23",
            "category": "Food",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(
            Expense.objects.get(id=response.data["id"]).title,
            "Dinner",
        )

    def test_retrieve_expense(self):
        url = reverse("expense-detail", args=[self.expense.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Lunch")

    def test_list_expenses_by_date_range(self):
        url = reverse("expense-by-date-range")
        response = self.client.get(
            url,
            {
                "user_id": self.user.id,
                "start_date": "2024-11-01",
                "end_date": "2024-11-30",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Lunch")

    def test_category_summary(self):
        url = reverse("expense-category-summary")
        response = self.client.get(
            url,
            {"user_id": self.user.id, "month": "2024-11"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["category"], "Food")
        self.assertEqual(response.data[0]["total_amount"], 15.00)
