#!/usr/bin/python3
"""
Command line interpreter/console for hbnb
"""


import cmd
from shlex import split
import re

import models
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State


# A global constant for representing all classes
classes = [
    "BaseModel",
    "User",
    "City",
    "Place",
    "State",
    "Amenity",
    "Review"
]


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


def check_args(args):
    """
    Checks whether the arguments passed to the prompt are valid.
    """
    arg_list = parse(args)
    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in classes:
        print("** class doesn't exist **")
    else:
        return arg_list


class HBNBCommand(cmd.Cmd):
    """ The class that implements the customized cmdline interface."""
    prompt = "(hbnb) "
    storage = models.storage

    def emptyline(self):
        """
        Prints an empty prompts when the enter key is pressed without
        argument pass
        """
        return False

    def default(self, arg):
        """ Describes the behavior of the cmd under different functions."""
        action_map = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "create": self.do_create
        }

        match = re.search(r"\.", arg)
        if match:
            arg1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg1[1])
            if match:
                command = [arg1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in action_map:
                    call = "{} {}".format(arg1[0], command[1])
                    return action_map[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))

    def do_EOF(self, argv):
        """
        EOF signal to imply end of program.
        """
        print("")
        return True

    def do_quit(self, argv):
        """Command which allows the user to exit the console."""
        return True

    def do_create(self, argv):
        """
        Creates a new instance of BaseModel, saves it to the JSON file
        and prints the instance id.
        """
        args = check_args(argv)
        if args:
            instance = eval(args[0])()
            print(instance.id)
            instance.save()
            return True

    def do_show(self, argv):
        """
        Prints the string representation of an instance based on class name
        and its instance id.
        """
        args = check_args(argv)
        if args:
            if len(args) != 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in self.storage.all():
                    print("** no instance found **")
                else:
                    print(str(self.storage.all()[key]))

    def do_all(self, argv):
        """
        Prints all instances currently in storage.
        """
        arg_list = split(argv)
        objects = self.storage.all().values()
        if not arg_list:
            print([str(obj) for obj in objects])
        else:
            if arg_list[0] not in classes:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in objects if arg_list[0] in str(obj)])

    def do_destroy(self, argv):
        """Deletes instances based on id."""
        arg_list = check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(*arg_list)
                if key in self.storage.all():
                    del self.storage.all()[key]
                    self.storage.save()
                else:
                    print("** no instance found **")

    def do_update(self, argv):
        """Updates the attributes of an instance."""
        arg_list = check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                instance_id = "{}.{}".format(arg_list[0], arg_list[1])
                if instance_id in self.storage.all():
                    if len(arg_list) == 2:
                        print("** attribute name missing **")
                    elif len(arg_list) == 3:
                        print("** value is missing **")
                    else:
                        obj = self.storage.all()[instance_id]
                        if arg_list[2] in obj.__class__.__dict__:
                            v_type = type(obj.__class__.__dict__[arg_list[2]])
                            setattr(obj, arg_list[2], v_type(arg_list[3]))
                        else:
                            setattr(obj, arg_list[2], arg_list[3])
                else:
                    print("** no instance found **")

            self.storage.save()

    def do_count(self, arg):
        """ counts the number of class instances."""
        arg1 = parse(arg)
        count = 0
        for obj in models.storage.all().values():
            if arg1[0] == type(obj).__name__:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
