#!/usr/bin/python3
"""Module console

This module contains the definition for HBNBCommand Class
"""

import cmd
import importlib
import json
import re
from models import storage

class HBNBCommand(cmd.Cmd):
    """HBNB command console class"""
    prompt = "(hbnb) "

    def emptyline(self):
        """
        Prevents the default behavior of cmd to 
        ignore running a command on an empty line.
        """
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Exit the console using Ctrl + D."""
        print()  # Print a newline before exiting for better readability
        return True

    def do_create(self, line):
        """Creates a new object and saves it."""
        obj_cls = self.get_class_from_input(line)
        if obj_cls:
            new_obj = obj_cls()
            try:
                new_obj.save()
                print(new_obj.id)
            except Exception as e:
                print(f"Error creating object: {str(e)}")

    def do_show(self, line):
        """Prints the string representation of an instance based on name and ID."""
        key = self.get_obj_key_from_input(line)
        if not key:
            return

        saved_obj = storage.all().get(key)
        if not saved_obj:
            print("** no instance found **")
        else:
            print(saved_obj)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and ID and saves the change into the JSON file."""
        key = self.get_obj_key_from_input(line)
        if not key:
            return

        saved_obj = storage.all().pop(key, None)
        if saved_obj:
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """Prints string representation of all instances based on the class name."""
        tokens = line.split()
        if not tokens:
            result = storage.all().values()
        else:
            obj_cls = self.get_class_from_input(line)
            if not obj_cls:
                return
            result = filter(lambda item: isinstance(item, obj_cls), storage.all().values())

        print([str(item) for item in result])

    def do_update(self, line):
        """Updates an instance based on the class name and ID by adding or updating attribute."""
        key = self.get_obj_key_from_input(line)
        if not key:
            return

        saved_obj = storage.all().get(key)
        if not saved_obj:
            print("** no instance found **")
            return

        attr_name, attr_val = self.get_attribute_name_value_pair(line)
        if attr_name is None or attr_val is None:
            return

        setattr(saved_obj, attr_name, attr_val)
        saved_obj.save()

    def do_count(self, line):
        """Prints the count of all instances based on the class name."""
        obj_cls = self.get_class_from_input(line)
        if not obj_cls:
            return

        result = filter(lambda item: isinstance(item, obj_cls), storage.all().values())
        print(len(result))


    def get_obj_key_from_input(self, line):
        """Parses and returns object key from input."""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is None:
            return None

        obj_id = self.get_id_from_input(line)
        if obj_id is None:
            return None

        return f"{obj_cls.__name__}.{obj_id}"

    def get_class_from_input(self, line):
        """Parses and returns class from input."""
        tokens = line.split()
        if not tokens:
            print("** class name missing **")
            return None

        class_name = tokens[0]
        return self.get_class(class_name)

    def get_id_from_input(self, line):
        """Parses and returns id from input."""
        tokens = line.split()
        if len(tokens) < 2:
            print("** instance id missing **")
            return None

        return tokens[1]


    def get_attribute_name_value_pair(self, line):
        """Parses and returns a tuple of attribute name and value."""
        cmds = line.split(maxsplit=3)

        if len(cmds) < 3:
            print("** attribute name missing **")
            return None, None

        attr_name = cmds[2].strip('"')

        if len(cmds) < 4:
            print("** value missing **")
            return attr_name, None

        attr_val = cmds[3].strip('"')

        return attr_name, attr_val

    def get_class(self, name):
        """Returns a class from models module using its name."""
        try:
            module_name = f"models.{name.lower()}"
            module = importlib.import_module(module_name)
            return getattr(module, name)
        except (AttributeError, ImportError):
            print("** class doesn't exist **")
            return None

    def default(self, line):
        if '.' not in line:
            return super().default(line)

        cls_name, func_name, obj_id, args = self.parse_input(line)

        if cls_name is None:
            print("** class name missing **")
            return

        if func_name is None:
            print("** incorrect function (all, count, show, destroy, update) **")
            return

        obj_id = obj_id if obj_id is not None else ""

        if func_name == "count":
            self.do_count(cls_name)
        elif func_name == "all":
            self.do_all(cls_name)
        elif func_name == "show":
            self.do_show(f"{cls_name} {obj_id}")
        elif func_name == "destroy":
            self.do_destroy(f"{cls_name} {obj_id}")
        elif func_name == "update":
            if isinstance(args, str):
                args = " ".join([obj_id, args])
                self.do_update(f"{cls_name} {args}")
            elif isinstance(args, dict):
                for k, v in args.items():
                    self.do_update(f"{cls_name} {obj_id} {k} {v}")


    def parse_input(self, input_str):
        args = input_str.split('.', 1)  # Split only once to handle arguments containing dots
        if len(args) != 2:
            return None, None, None, None

        cls_name, command_str = args
        valid_commands = ["all", "count", "show", "destroy", "update"]

        if '(' not in command_str or ')' not in command_str:
            return cls_name, None, None, None

        func_name, arg_str = command_str.split('(', 1)
        if func_name not in valid_commands:
            return cls_name, None, None, None

        id_match = re.match(r'^"([\w-]+)"', arg_str)
        if not id_match:
            return cls_name, func_name, None, None

        obj_id = id_match.group(1)
        arg_str = arg_str.replace(id_match.group(0), '').strip(')')

        if not arg_str:
            return cls_name, func_name, obj_id, ''

        try:
            arg_dict = json.loads(arg_str)
            return cls_name, func_name, obj_id, arg_dict
        except json.JSONDecodeError:
            return cls_name, func_name, obj_id, arg_str


if __name__ == '__main__':
    HBNBCommand().cmdloop()
