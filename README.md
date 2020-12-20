# FeatureExtractor: data_logger Component

Uses a Web UI to visualize plots and statistics with the data generated during feaure-extractor training or evaluation.

[![Build Status](https://travis-ci.org/harveybc/data_logger.svg?branch=master)](https://travis-ci.org/harveybc/data_logger)
[![Documentation Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://harveybc-data_logger.readthedocs.io/en/latest/)
[![BCH compliance](https://bettercodehub.com/edge/badge/harveybc/data_logger?branch=master)](https://bettercodehub.com/)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/harveybc/data_logger/blob/master/LICENSE)

## Description

Visualize via Web, data obtained from an input plugin, the data obtained via the input plugin may contain batch or real-time results of multiple feature-extractor trainers or evaluators (from now on called processes).  By default uses a Sqlite input plugin.  

It uses multiple output visualization plugins, each of which generate a new element in the feature-extractor dashboard views of the feature-extractor processes.  By default uses output plugins for: real-time MSE plot during training and batch calculated MSE plot from the evaluation of a pre-trained feature-extractor on a validation dataset. 

The data_logger uses a JSON configuration file for setting the Web service parameters and the configuration of the input and output plugins.

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






.