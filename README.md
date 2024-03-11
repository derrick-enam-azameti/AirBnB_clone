# AirBnB Clone - The Console

## Project Overview
AirBnB Clone (the console) is a console application that is used to manage the various instances of class used in the AirBnB web application.

![Project Overview](/docs/AirBnB_Console_Project_Overview.jpg)

## Usage

### Starting the interpreter
The console interpreter can be used in both interactive and non-interactive modes

#### Interactive Mode
```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb) 
(hbnb) quit
$
```

#### Non-Interactive Mode
```bash
$ echo "help" | ./console.py
(hbnb) 
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb)
$
```

### Executing commands
To execute a command you specify it's name and optionally its arguments. Some commands have no arguments while others have multiple. The help command shows the details of all the commands.

#### Examples on Interactive Mode

```bash
$ ./console.py
(hbnb) create BaseModel
dc7f8788-7329-49df-a65b-323d96bd908c
(hbnb) all
["[BaseModel] (dc7f8788-7329-49df-a65b-323d96bd908c) {'id': 'dc7f8788-7329-49df-a65b-323d96bd908c', 'created_at': datetime.datetime(2024, 3, 10, 20, 19, 26, 112686), 'updated_at': datetime.datetime(2024, 3, 10, 20, 19, 26, 112708)}"]
(hbnb) show BaseModel dc7f8788-7329-49df-a65b-323d96bd908c
[BaseModel] (dc7f8788-7329-49df-a65b-323d96bd908c) {'id': 'dc7f8788-7329-49df-a65b-323d96bd908c', 'created_at': datetime.datetime(2024, 3, 10, 20, 19, 26, 112686), 'updated_at': datetime.datetime(2024, 3, 10, 20, 19, 26, 112708)}
(hbnb) quit
$
```

#### Examples on Non-Interactive Mode

```bash
❯ echo "create BaseModel" | ./console.py
(hbnb) a60f978b-e1e8-4fa4-b62e-00dc072988cc
(hbnb)
$
$ echo "destroy BaseModel 64b15c6c-6693-45fa-87c7-3ad1ae413b13" | ./console.py
(hbnb)
$
```

## Authors
1. Derrick Enam Azameti
2. Kelvin Abambora
