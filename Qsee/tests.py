from django.contrib.auth.models import User
from django.forms import ValidationError
from django.test import TestCase
from Qsee.models import Assay, Control, Analyser, Test
import random

# Create your tests here.
class AssayTestCase(TestCase):

    def setUp(self):
        """Testing suite creates a completely new test database.
        Setup created records in each of the tables in the database so that tests
        can be run on them."""

        # Create assay records
        Assay.objects.create(assay_name="test_assay")

        # Create control records
        Control.objects.create(
            assay_id=Assay.objects.get(assay_name="test_assay"),
            control_name="test_control",
            date_added="2022-02-14",
            lot_number="test1234",
            active=True
        )
        # Create analyser records
        Analyser.objects.create(analyser_name="test_analyser")

        # Create test records for test_control for test_assay used on test_analyser
        for i in range(20):
            Test.objects.create(
                result=random.randint(0,45),
                test_date=f"{i+1}/01/2022",
                control_id=Control.objects.get(control_name="test_control"),
                analyser_id=Analyser.objects.get(analyser_name="test_analyser"),
                operator="test_operator",
                note=f"test_{i+1}")
        

    def test_database_add(self):
        """Test to check items added to the database"""
        test_assay = Assay.objects.get(assay_name="test_assay")
        test_control = Control.objects.get(control_name="test_control")
        test_analyser = Analyser.objects.get(analyser_name="test_analyser")
        test_tests = Test.objects.all()

        self.assertEqual(test_assay.assay_name,"test_assay","Check item added to assay table correctly")
        self.assertEqual(test_control.control_name,"test_control","Check item added to control table correctly")
        self.assertEqual(test_analyser.analyser_name, "test_analyser","Check item added to analyser table correctly")
        self.assertEqual(len(test_tests), 20, "Check minium number of records have been entered for tests table")


    def test_result_range(self):
        """Check to see if there are results that are out of range, i.e. < 0 and > 45"""
        # Add test that has value that is out of range (i.e. < 0 and > 45)
        tests = Test.objects.all()
        for test in tests:
            self.assertTrue(test.result >= 0 and test.result <= 45)

    def test_check_date_format(self):
        """Check to see if the date has been entered in the corret format."""
        tests = Test.objects.all()
        self.assertEqual(tests[1].test_date, "2/01/2022", "Corect date format")
        self.assertNotEqual(tests[1].test_date, "02/01/2022", "Incorrect date format")

    def test_incorrect_date(self):
        """Try to create a record with incorrect date format"""
        try:
            Control.objects.create(
                assay_id=Assay.objects.get(assay_name="test_assay"),
                control_name="test_control_date",
                date_added="not a date", # invalid date
                lot_number="test1234",
                active=True
            )
        except ValidationError as e:
            # Check to see if the validation error was caused by the date field.
            self.assertTrue(e, ['“not a date” value has an invalid date format. It must be in YYYY-MM-DD format.'])


        

