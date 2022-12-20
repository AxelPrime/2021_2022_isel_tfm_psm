## Software Platform for Mental Patients Management in Social Institutions at HFF

Hospital Fernando Fonseca is an organization that manages patients with mental diseases sent to Care Houses that are able to take care of them for 24 hours a day. These patients can be sent to the Care Houses by the hospital itself or by other institutions. Once a patient has entered a Care House, the HFF is responsible for the payment of the daily cares of the patient. In case the patient comes from another institution, then it is the institution’s responsibility to make these payments.

Once in the Care House, a patient might need to go to other institutions, such as hospitals, for other health related reasons. During these days, the care of the patients should not be billed since they are not in the Care House. This however, poses a problem be- cause the HFF cannot track these visits since they are only managed by the Care House, which can lead to the days being billed without the knowledge of the HFF.

The current process of referring a patient to a Care House and managing their internment is made manually, and the communication between the HFF and the Care Houses is made via e-mail. This makes the process slow and prone to failure.

This project is a partnership between ISEL and HFF to develop a web application that can be accessed by the members of the HFF involved in the referral process and financial management, as well as the members of the Care Houses who manage the interned patients, which allows the different departments that take part in this process to communicate better with each other in order to simplify the process and guarantee the correct billing for the care of the patients.

<img src="isel-meic-HFF-PSM-thesis_presentation.gif" width="600">

## Getting Started

In order to run an instance of the PSM application, a series of steps must be followed in order to ensure that the application is correctly configured. 
This guide will allow any user to configure the execution environment in order to test the application and all its functionalities.

### Requirements
- Python (>= 3.8)
- PostgreSQL (version 12)

### Step 1 - Configuring the Database.

The PSM application relies on a PostgreSQL database to store data regarding users, internments, referrals and other useful information. As such, the first step is to create a database using the command below:
```sql
CREATE DATABASE psm_database;
```

In order to use the database, a user must be created with the necessary permissions to make queries over the data. The user can be created by executing the commands below:
```sql
CREATE USER myprojectuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE psm_database TO myprojectuser;
```

### Step 2 - Setting up the Python Environment

After the database has been created with success, the next step is to create the environment to execute the application. As such, the command below will create the Python virtual environment where the Python package requirements will be installed:
```sh
cd psm/
python3 -venv env
source env/bin/activate
```

After the creation of the environment, it is necessary to install the Python package requirements. The command below will complete the installation:

```sh
pip install -r requirements.txt
```

Finally, in order to create the connection between the application and the database, it is necessary to create a ```.env``` file with the following variables:

```
# Django Secret Key
SECRET_KEY=key

# Prod DB Data
PROD_DB_USER=myprojectuser
PROD_DB_NAME=psm_database
PROD_DB_PASSWORD=password

# Dev DB Data
DEV_DB_USER=myprojectuser
DEV_DB_NAME=psm_database
DEV_DB_PASSWORD=password
```

### Step 3 - Inserting the test data

The application can only be executed using the development settings, since the access to the Hosix WebService is only allowed in the HFF's servers. As such, the next commands will be executed using the ```--settings=psm_django.settings.dev``` flag.

The first step in the data insertion is to create the tables in the database, which are defined in the models of each application. The tables will be created using the migrations previously created using the following command:

```sh
python manage.py migrate --settings=psm_django.settings.dev
```

After applying the migrations, the test data is now ready to be inserted. A script will be run that will create a set of institutions, care houses, patients, users, referrals, and other records that can be used to fully test the application. The insertion of the data can be done by running the command listed below:

```sh
python manage.py runscript create_test_data --settings=psm_django.settings.dev
```

In order to simulate requests to the Hosix WebService, it is necessary to create an SQLite database. The database can be created using the following command:

```sh
python manage.py runscript create_local_patient_db --settings=psm_django.settings.dev
```

### Step 4 - Running the application

After completing the previous steps successfully, the application is ready to be executed. To do this, execute the command listed below. The command will run the application on host ```0.0.0.0``` and port ```8000```:

```sh
python manage.py runscript runserver 0.0.0.0:8000 --settings=psm_django.settings.dev
```
