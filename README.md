# PEDSnetCDMs

A python app for CDM model classes and DDL autogeneration.

The pedsnetcdms app creates python-importable sqlalchemy AND django style models for PEDSnet, Vocab, I2B2, and PCORnet CDMs. In addition, alembic AND django migrations can be created from those models. The alembic migrations can be used to auto-generate DDL files for all four CDMs.

The pedsnetcdms app is based on the declarative definition of models in JSON format (found in the `models.json` files) and the dynamic generation of python classes from those models (found in the `dj_makers.py` and `sa_makers.py` files). The generating functions are used in each CDM's `models.py` and `sa_models.py` files to put the model classes where the ORMs can find them. The `settings.py`, `alembic.ini`, and `alembic/env.py` files are simply ORM module configuration.

## Installation

A `pip install pedsnetcdms` should get you the package with the generated models and migrations ready for import into your python environment.

However, if you want to generate the DDLs yourself or use the migrations directly on your database, you will have to clone the repository and install some or all of the following python packages and their (in some cases non-Python) dependencies, depending on which DBMS you are using:

- cx-Oracle
- psycopg2
- pymssql
- MySQL-python

This is left as an exercise for the reader. (Although perhaps a Dockerfile is in order...PR anyone?)

## DDL Files

DDL files for all four CDMs in PostgreSQL, Oracle, SQL Server, and MySQL dialects are available in the `pedsnetcdms/ddloutput` directory. They are hypothetical, so please test them and post an issue if you find a problem.

## Model Usage

Django models are available at `pedsnetcdms.<CDM>.models` and sqlalchemy models are available at `pedsnetcdms.<CDM>.sa_models`, where `<CDM>` should be replaced with one of the following:

- pedsnetcdm
- itwobtwocdm
- vocabcdm
- pcornetcdm

You can also include any of these apps in your django `INSTALLED_APPS` setting.

## DDL Generation

In order to generate the DDL, install the required package(s) for your DBMS(s) from the list above, clone the repository and install the package.

Edit the `pedsnetcdms/<CDM>/alembic/env.py` file for your desired CDMs to restrict the DBMSs for which DDL will be output (hint: the iterated list of tuples inside the `run_migrations_offline` function).

From within the `pedsnetcdms` package directory (where the `alembic.ini` file is), run `alembic -n <CDM> upgrade head --sql` and watch your DDL files appear!

## Direct Migration Use

Install requirements, clone, and install the package as above.

Edit the `alembic.ini` or `settings.py` files to specify the database URI you wish to connect to (notice that the setting is repeated under each CDMs section in `alembic.ini`).

Run `alembic -n <CDM> upgrade head` or `python manage.py migrate <CDM>`.
