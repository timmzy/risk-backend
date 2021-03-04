Django app built for dynamic model creation
===========================================

Sample Project

Basic Commands
--------------

Setting Up Your Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Cloning the app from the repo.

* Preferably, create a virtual environment::

    $ python -m venv venv

* Install package and dependencies::

    $ python pip install requirements.txt

* Create a .env file in folder ``britecore/settings/``. You will need to create ``SECRET_KEY``, ``DEBUG``, ``ALLOWED_HOST``, ``DB_HOST``, ``DB_USER``, ``DB_PASS``, ``DB_NAME``, ``S3_BUCKET``, ``S3_URL``, ``API_CROSS_ORIGIN``. ``DB_*`` respresent your postgres database settings and database name created.

* To create a superuser::

    $ python manage.py createsuperuser


Run Test
^^^^^^^^^^^^^

To run tests::

    $ python manage.py test

This tests for the RestAPI for all risk and field type, single risk and test for posting data as admin. The ORM is also tested for different cases such as deleting/renaming a model, adding/altering/deleting a field.


Steps to deploy to AWS Lambda:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install Zappa::

    $ pip install zappa

* Setup Zappa and enter details and note the environment name::

    $ zappa init

* To deploy the app on AWS lambda::

    $ zappa deploy

* Make sure you update the allowed host to the url given by zappa. You can also use S3 for staticfiles

* Migrate using::

    $ zappa manage <the environment name> migrate

* To update the app on lambda when you make any changes::

    $ zappa update

* Goto the url provided and login to admin

* Enter risk types and the risk fields.

* You can view the risks types and risk fields on the vuejs app
