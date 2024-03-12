#!/usr/bin/python3
"""Module test_amenity

This Module contains tests for Amenity Class
"""

import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand

class TestConsole(unittest.TestCase):
    """Tests the console app"""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the test console"""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Removes the file.json temporary file"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_create_command_missing_class_name_error(self):
        """Tests the 'create' command when class name is missing."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_create_command_class_not_found_error(self):
        """Tests the 'create' command when the specified class does not exist."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_create_creates_an_object(self):
        """Tests the 'create' command creates an instance"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip()
            self.assertNotEqual(id, "")  # Ensure an ID is generated

        # Check if the created object is shown using 'show' command
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'show BaseModel {id}')
            self.assertIn(id, output.getvalue())

    def test_show_errors_when_class_name_missing(self):
        """Tests the 'show' command error when class name is missing"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_show_errors_when_class_does_not_exist(self):
        """Tests the 'show' command error when class doesn't exist"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_show_displays_an_object(self):
        """Tests the 'show' command displays an instance"""
        # Create an object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip()
        
        # Show the created object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'show BaseModel {id}')
            self.assertIn("BaseModel", output.getvalue())

    def test_destroy_errors_when_class_name_missing(self):
        """Tests the 'destroy' command error when class name is missing"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_destroy_errors_when_class_does_not_exist(self):
        """Tests the 'destroy' command error when class doesn't exist"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_destroy_prints_instance_not_found(self):
        """Tests the 'destroy' command prints instance not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BaseModel adfadfadf')
            self.assertIn("** no instance found **", output.getvalue())

    def test_destroy_deletes_an_object(self):
        """Tests the 'destroy' command deletes an instance"""
        # Create an object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip()

        # Destroy the created object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'destroy BaseModel {id}')
            # After deletion, the object should not be found
            self.assertIn("** no instance found **", output.getvalue())

    def test_all_displays_instance_objects(self):
        """Tests the 'all' command displays all instance objects"""
        # Create two objects of BaseModel
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create BaseModel')

        # Show all objects
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('all')
            # Both objects should be displayed
            self.assertIn("BaseModel", output.getvalue())
            self.assertGreaterEqual(output.getvalue().count("BaseModel"), 2)

    def test_all_displays_class_instance_objects(self):
        """Tests the 'all' command displays class instance objects"""
        # Create objects of BaseModel and User
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create User')

        # Show all objects of User class
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'all User')
            # Only objects of User class should be displayed
            self.assertIn("User", output.getvalue())
            self.assertNotIn("BaseModel", output.getvalue())

    def test_update_attr_name_missing_error(self):
        """Tests 'update' command displays attribute name missing error"""
        # Create an object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip()

        # Attempt to update without providing attribute name
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'update BaseModel {id}')
            self.assertIn("** attribute name missing **", output.getvalue())

    def test_update_attr_value_missing_error(self):
        """Tests 'update' command displays attribute value missing error"""
        # Create an object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip()

        # Attempt to update without providing attribute value
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'update BaseModel {id} fname')
            self.assertIn("** value missing **", output.getvalue())

    def test_update_updates_instance(self):
        """Tests the 'update' command updates an instance"""
        # Create a State object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create State')
            id = output.getvalue().strip('\n')

        # Update the State object with a new name
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'update State {id} name example_state')
            # Check if the name attribute is updated
            self.assertIn('name', output.getvalue())
            self.assertIn('example_state', output.getvalue())

    def test_classname_all_displays_instance_objects(self):
        """Tests the class name followed by 'all()' displays instance objects"""
        # Create two BaseModel objects
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create BaseModel')

        # Retrieve all instances of BaseModel
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BaseModel.all()')
            # Check if both BaseModel instances are displayed
            self.assertIn("BaseModel", output.getvalue())
            self.assertGreaterEqual(output.getvalue().count("BaseModel"), 2)

    def test_classname_count_displays_instance_objects(self):
        """Tests the class name followed by 'count()' displays instance objects"""
        # Create five Place objects
        with patch('sys.stdout', new=StringIO()) as output:
            for _ in range(5):
                self.cmd.onecmd('create Place')

        # Get the count of instances of Place
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('Place.count()')
            # Check if the count is 5
            self.assertIn('5', output.getvalue())

    def test_classname_show_displays_an_object(self):
        """Tests if 'show' displays an instance by class name and id"""
        # Create a BaseModel object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')

        # Show the BaseModel instance by class name and id
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'BaseModel.show("{id}")')
            # Check if BaseModel is displayed
            self.assertIn("BaseModel", output.getvalue())

    def test_classname_destroy_deletes_an_object(self):
        """Tests if 'destroy' deletes an instance by class name and id"""
        # Create a BaseModel object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')

        # Destroy the BaseModel instance by class name and id
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'BaseModel.destroy("{id}")')
            # Attempt to show the BaseModel instance again
            self.cmd.onecmd(f'show BaseModel {id}')
            # Check if the instance is not found
            self.assertIn("** no instance found **", output.getvalue())

    def test_classname_update_updates_instance(self):
        """Tests if 'update' updates an instance by class name and id"""
        # Create a Review object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Review')
            id = output.getvalue().strip('\n')

        # Update the Review instance by class name, id, and attributes
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'Review.update("{id}", "rev_k", "rev_v")')
            # Show the updated Review instance
            self.cmd.onecmd(f'show Review {id}')
            # Check if the attributes are updated
            self.assertIn('rev_k', output.getvalue())
            self.assertIn('rev_v', output.getvalue())

    def test_classname_update_updates_instance_with_dict(self):
        """Tests if 'update' updates an instance with a dictionary of attributes"""
        # Create an Amenity object
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Amenity')
            id = output.getvalue().strip('\n')

        # Define a dictionary of attributes
        dict_att = "{ 'name' : 'amne', 'rev_k' : 'rev_v' }"

        # Update the Amenity instance with the dictionary of attributes
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'Amenity.update("{id}", {dict_att})')

        # Show the updated Amenity instance
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'show Amenity {id}')
            # Check if the attributes are updated
            self.assertIn('name', output.getvalue())
            self.assertIn('amne', output.getvalue())
            self.assertIn('rev_k', output.getvalue())
            self.assertIn('rev_v', output.getvalue())


