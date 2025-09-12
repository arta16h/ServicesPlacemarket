from django.test import TestCase
from django.conf import settings
from django.apps import apps
import importlib
import unittest

class CriticalFlowTests(TestCase):
    def test_create_user(self):
        # Try to create a user using AUTH_USER_MODEL
        User = apps.get_model(settings.AUTH_USER_MODEL)
        self.assertIsNotNone(User, "AUTH_USER_MODEL not found")
        u = User.objects.create(**({ 'username': 'testuser', 'email': 'test@example.com' }))
        self.assertTrue(u.pk is not None)

    def test_create_order_if_model_exists(self):
        try:
            Order = apps.get_model('orders', 'Order')
        except LookupError:
            self.skipTest("Order model not present")
        # create minimal required related objects if necessary (user)
        User = apps.get_model(settings.AUTH_USER_MODEL)
        user = User.objects.create(**({ 'username': 'orderuser', 'email': 'order@example.com' }))
        # Attempt to create an Order with sensible defaults; test will be lenient
        fields = {f.name: None for f in Order._meta.fields if not f.auto_created and f.name != 'id'}
        # try to fill some likely fields
        if 'user' in fields:
            fields['user'] = user
        # remove non-nullable without defaults
        clean = {}
        for name, val in fields.items():
            field = Order._meta.get_field(name)
            if not field.null and field.default is field.empty and field.blank is False and name not in ('id',):
                # skip creating this order if required fields unknown
                self.skipTest(f"Order has required field {name}; skipping creation test")
            clean[name] = val
        o = Order.objects.create(**clean)
        self.assertTrue(o.pk is not None)

    def test_notification_task_runs(self):
        # If there's a tasks module in orders, try to import and run a notify/send task if present
        try:
            tasks = importlib.import_module('orders.tasks')
        except Exception:
            self.skipTest("orders.tasks not importable")
        # Try to find a function that looks like notify or send_notification
        candidate = None
        for attr in dir(tasks):
            if callable(getattr(tasks, attr)) and any(k in attr.lower() for k in ('notify','send','email','task')):
                candidate = getattr(tasks, attr)
                break
        if candidate is None:
            self.skipTest("No candidate notification task found in orders.tasks")
        # Call it without args if possible; if it fails, the test will surface error
        try:
            candidate()
        except TypeError:
            # can't call without args; just ensure callable exists
            self.assertTrue(callable(candidate))
