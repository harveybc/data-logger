# DataLogger: data_logger Component

Configurable structure, configurable storage, generic data-logger API.

[![Build Status](https://travis-ci.org/harveybc/data_logger.svg?branch=master)](https://travis-ci.org/harveybc/data_logger)
[![Documentation Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://harveybc-data_logger.readthedocs.io/en/latest/)
[![BCH compliance](https://bettercodehub.com/edge/badge/harveybc/data_logger?branch=master)](https://bettercodehub.com/)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/harveybc/data_logger/blob/master/LICENSE)

## Description

El propósito de este subsistema es proveer conectividad con diferentes motores de bases de datos configurables via plugins, implementa un sistema de Autenticación, Autorización y Accounting (AAA), que permite asegurar, controlar y registrar el acceso a los datos de los usuarios para proveer trazabilidad de todas las operaciones realizadas, con lo que se dispone de un historial de datos y operaciones. Usa un sistema configurable de estructura de datos basado en procesos que captan información para almacenarla en tablas configurables de la base de datos.
Los componentes de este subsistema son los siguientes:

The purpose of this system is to implement a reusable REST API that provides Authentication, Authorization and Accounting (AAA), the API is scalable by using a processes table that stores configurable data structures and tables for the data to be used by an application.

The system has a database plugin architecture that allows loading of plugins that configure a custom database engine to save all the data from all processes.

The data structures used can be divided in two groups: 
a)	The fixed data structures that are the users and the processes tables.
b)	The configurable data structures are a variable number of tables per process that are created on the database upon creation of a process, the created tables can be used by other processes and accessed via the process route endpoints.

## Installation

To install the package via PIP, use the following command:

> pip install -i https://test.pypi.org/simple/ data_logger

Also, the installation can be made by clonning the github repo and manually installing it as in the following instructions.

### Github Installation Steps
On Linux use the .sh scripts, on windows use the .bat scripts.

1. Clone the GithHub repo:   
> git clone https://github.com/harveybc/data_logger
2. Change to the repo folder:
> cd data_logger
3. Install requirements.
> pip install -r requirements.txt
4. Install python package (also installs the console command data-trimmer)
> python setup.py install
5. Add the repo folder to the environment variable PYTHONPATH
6. Create a test database (use migrate.bat on windows)
> scripts/migrate.sh
7. Populate the test database (use test_data_seed.bat on Windows)
> scripts/test_data_seed.sh
6. (Optional) Perform tests
> python setup.py test
7. (Optional) Generate Sphinx Documentation
> python setup.py docs


### Command-Line Execution

For ease of use, a script for setting the environment variables and executing the app is included, it must be executed in the root feature-extractor directory, where the scripts are located:

* For Linux and Mac:

> data_logger.sh

* For Windows:

> data_logger.bat

## Usage

The Web intreface can be accessed by default at:

[localhost:5000](localhost:5000)

The default port can be modified by setting the FLASK_RUN_PORT environment variable or bly using the --port argument to the flask run command.

A default user us created with the username: "test", and password: "pass", please delete this user once you have created another one.

### Configuration File

The data_logger uses a configuration file located in the data_logger/data_logger directory that sets the Web service parameters and the configuration of the input and output plugins.

The following is the default JSON configuration file:


```
{
    "input_plugin": "vis_input_sqlite",
    "input_plugin_config": {
        "filename": "test/db/plots.sqlite",
        "tables": [
            {
                "table_name": "training_progress",
                "fields": [
                    "mse",
                    "mae",
                    "r2"
                ]
            },
            {
                "table_name": "validation_stats",
                "fields": [
                    "mse",
                    "mae",
                    "r2"
                ]
            },
            {
                "table_name": "validation_plots",
                "fields": [
                    "original",
                    "predicted"
                ]
            }
        ]
    },
    "output_plugin": "vis_output",
    "output_plugin_config": {
        "dashboard": [
            {
                "table_name": "training_progress",
                "online": true,
                "delay": 3,
                "points": 800,
                "title": "Progress of Last Training Process",
                "fields": [
                    "mse"
                ]
            },
            {
                "table_name": "validation_plots",
                "title": "Validation Data Plot"
            },
            {
                "table_name": "validation_stats",
                "title": "List of Feature Extractor Stats on Validation Data"
            }
        ],
        "views": [
            {
                "table_name": "training_progress",
                "title": "Progress of Training Process",
                "online": true,
                "delay": 3,
                "points": 1600,
                "fields": [
                    "mse",
                    "mae",
                    "r2"
                ]
            },
            {
                "table_name": "validation_plots",
                "title": "Validation Data Plot",
                "online":  false,
                "fields": [
                    "original",
                    "predicted"
                ]
            },
            {
                "table_name": "validation_stats",
                "title": "Feature Extractor Stats on Validation Data",
                "online": false,
                "fields": [
                    "mse",
                    "mae",
                    "r2"
                ]
            }
        ]
    }
}
```




.






