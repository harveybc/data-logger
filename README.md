# DataLogger

Flexible RESTful API framework with configurable data structure, storage and autogenerated GUI for secure, generic data logging and visualization. 

[![Build Status](https://www.travis-ci.com/harveybc/data-logger.svg?branch=master)](https://www.travis-ci.com/harveybc/data-logger)
[![Documentation Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://harveybc-data_logger.readthedocs.io/en/latest/)
[![BCH compliance](https://bettercodehub.com/edge/badge/harveybc/data_logger?branch=master)](https://bettercodehub.com/)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/harveybc/data_logger/blob/master/LICENSE)

## Description

REST API framework that provides Authentication, Authorization and Accounting (AAA). The base data-logger API is expandable by using a plugin architecture and uses a json-configurable database engine and data structure that allows to auto-generate a Web GUI from the data structure. The GUI allows visualization of timeseries or statistical data and have dialogs for creating new data or editing current data (i.e. Configuration of control parameters of an IoT device). 

The data structures used can be divided in two groups: 
1.	Fixed data structures: they are the following tables: users, authorization, processes and log. Which provide AAA to the API and they are defined in the core plugin.
2.	Configurable data structures: they are defined in the store plugin configuration file (config_store.json), which contains a variable number of data-generating processes (groups of tables) and a variable number of tables per process, the created tables can be accessed via the "/process" route endpoints of the API, this is used to generate the GUI for visualizing the data but also can be used for any general-purpose Web application via a new gui plugin. 

The system has a plugin architecture that allows loading of plugins of three types configured from json files in the root directory:  
- Store plugin (config_store.json): Configures the initial data structure and a custom database engine to save all the data from all processes (default: sqlite_store).
- Core plugin (config_core.json): Configures the API endpoints and provides AAA , default: basic_auth_core, used [APIC:](https://github.com/bjdash/apic) design, documentation and testing tool for Swagger 2.0 API specification.
- GUI plugin (config_gui.json): Configures a graphical user interface, can be disabled if not required, default: visualizer_gui that auto generate plots and uses [AdminLTE:](https://github.com/ColorlibHQ/AdminLTE) Web dashboard based on Bootstrap 4.

This system can be useful for:
- IoT (Internet of Things): because it requires zero coding in exchange for the configuration of the data to be logged to auto-generate tables with timestamping and a Web GUI for visualizing or editing the data.
- Event Logging: can be used for logging software systems events, parameters and responses/payloads such as in distributed machine learning model parameter optimization experiments.
- As a framework for general-purpose Web application development because:
    - It features a plugin architecture and can be used as starting point for an expanded or modified application. 
    - A Model View Controller (MVC) design pattern of the core (back-end) and GUI (front-end) plugins allows data-logger to be easily modified or expanded to a general-purpose application (in a separate plugin).
    - The use of [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/) Object Relational Mapping (ORM) allows for object-oriented database-independent queries without SQL (configured from the store plugin).
    - The use of [Connexion](https://github.com/zalando/connexion) allows for API deployment from an OpenAPI/Swagger specification in the core plugin.

## Installation (Work In Progress, use github installation)

To install the package via PIP, use the following command:

> pip install -i https://test.pypi.org/simple/ data_logger

Also, the installation can be made by clonning the github repo and manually installing it as in the following instructions.

### Github Installation Steps
On Linux use the .sh scripts, on windows use the .bat scripts.

1. Clone the GithHub repo:   
> git clone https://github.com/harveybc/data-logger
2. Change to the repo folder:
> cd data_logger
3. Install requirements.
> pip install -r requirements.txt
4. Install python package (also installs the console command data-trimmer)
> python setup.py install
5. Create a test database (use .\scrips\migrate.bat on windows)
> ./scripts/migrate.sh
6. (Optional) Perform tests
> python setup.py test
7. (Optional) Generate Sphinx Documentation
> python setup.py docs


### Command-Line Execution

For ease of use, a script for setting the environment variables and executing the app is included, it must be executed in the root data-logger directory, where the scripts are located:

* For Linux and Mac:

> data_logger.sh

* For Windows:

> data_logger.bat

## Online documentation 

The Swagger UI Web interface provides API documentation and is installed by default at:

[http://localhost:5000/ui](http://localhost:5000/ui)

It documents the parameters for each API endpoint configured in the core plugin and alows to test them with your own parameters.

## Usage

The Web interface configured in the gui plugin can be accessed by default at:

[http://localhost:5000](http://localhost:5000)

The default port can be modified by setting the FLASK_RUN_PORT environment variable or bly using the --port argument to the flask run command.

A default user is created with the username: "test", and password: "pass", please delete this user once you have created another one.

### Plugins Configuration Files (WORK IN PROGRESS)

The plugin system searches for all installed plugins, which can be on separate repositories, and from the discovered plugins, it loads the ones indicated by the 3 configuration files: config_core.json, config_gui.json and config_store.json that configure the respective plugins.

The following is the default JSON configuration file config_store.json, where a the sqlite store is configured and a process with a single table with a column is defined, the default type of columns is float:

```
{
    "store_plugin": "sqlite_store",
    "store_plugin_config": {
        "filename": "db.sqlite3",
        "processes" : [
            {
                "name": "test",
                "tables": [ 	
                    {
                        "name": "test_table",
                        "columns": [
                            {"name" : "test_column"}
                        ]
                    }
                ]
            }
        ]
    }
}
```

The following is the default JSON configuration file config_core.json, where a the core api is configured via a swagger api specification file in json or yaml format (relative to the core plugin path):

```
{
    "core_plugin": "basic_auth_core", 
    "core_plugin_config": {
        "filename": "DataLogger-OAS.apic.json"
    }
}
```  
.

## Plugin creation (Work in Progress)
 




