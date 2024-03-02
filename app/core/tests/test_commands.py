"""
Test custom django management commands
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if db is ready"""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(database=["default'"])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting an operational error"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # the first 2 times of running this mocked function Psycopg2Error will be raised
        # from times 3 to 5 django OperationalError will be raised in this mock
        # the 6th time it returns True 
        # backslash is the syntax to break it into 2 lines so it migth look like:
        #pathced_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(database=["default"])
