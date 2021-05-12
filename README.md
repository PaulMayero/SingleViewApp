# SingleViewApp
ETL tryouts with Django  
This application tries to demonstrate ingestion into Postgres database using Django Command.  


## How to run the app  
1. Git clone this repository by asting the follwing in your terminal : `https://github.com/PaulMayero/SingleViewApp.git`  
2. Move into the required created directory `cd SingleViewApp/`  
3. Note the Directory structure used  within the `SingleViewApp` directory  
<pre>
├── csvFileFolder #Stores the file containing the data to be reconciled and ingested into Postgres
| └── works_metadata.csv #file to be ingested
├── musicalsingleview #Django project directory
│   ├── musicalsingleview
│   │   └── __pycache__
│   └── musicalsingleviewapi #Django app directory
│       ├── management
│       │   └── commands 
│       │       └── __pycache__
│       ├── migrations
│       │   └── __pycache__
│       └── __pycache__
└── reconciledFileFolder #Stores the product of reconciliation, i.e file produced after reconciliation and is ingested into Postgres
│   └── 2021:05:11-22:00:33.462970-wimpy-chestnut-cuttlefish.csv file that is being produced
└── requirements.txt #text file that holds all python packages used in the project
</pre>
  
4. On your computer, ensure that Python and virtualenv are installed. If on linux, create your virtualenvironment as follows: `virtualenv venv/`. 
Note: Use Python3 within the virtualenvironment  
5. Activate your virtualenvironment by running `source venv/bin/activate`  on your terminal prompt  
6. Pip install all the project packages by running `pip install -r requirements.txt`
7. Install Postgres on your device as per your OS of use.  
8. Move into `musicalsingleview` Directory by `cd musicalsingleview/`  
9.Run ` python manage.py migrate` then `python manage.py makemigrations` then finally ` python manage.py migrate` to create the tables used by the app.    
10. Run `python manage.py runserver` to start the django server    

## How to ingest data
Data in the folder csvFileFolder is meant to be ingested into the Postgres Database.  
This is to be enabled by the Django command which is located at `musicalsingleviewapi` folder  
<pre>
 musicalsingleviewapi
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── management
    │   └── commands
    │       ├── ingest_csv_file.py #script that ingests the csv file after reconciliation
   

</pre>
To see usage of the command, at the current file level. (You should see manage.py).  
Run the command  
`
python manage.py ingest_csv_file --help
`
This will show the usage of the command file as depicted below. 

`
Ingests the csv file provided
positional arguments:
  path_to_csv_file      Provides path to file where csv file is
  path_to_reconciled_csv Provides path to where reconciled csv will be put
`
The main arguements needed are the `path_to_csv_file` and the `path_to_reconciled_file`. 

These two parameters **MUST** not be empty.  

For the `path_to_csv_file` just put the file path to the csv file you want ingested into the database.  

For the `path_to_reconciled_csv` add the location where you want the cleaned files that are to be ingested into the database to be stored.

When running the script you will have terminal communication to inform you of the progress.

## Reconciliation method used  

The data reconciliation was done using the python pandas package.  

The data was grouped by according to title and iswc columns.  

```
multiple_musical_works_df = csv_df[csv_df.groupby(['iswc','title'])
            ['iswc','title','contributors'].transform('count') > 1]
single_musical_works_df = csv_df[csv_df.groupby(['iswc','title'])
            ['iswc','title','contributors'].transform('count') == 1]
```
Refer to `ingest_csv_file.py` script.

All the empty rows are dropped in this dataframe and they are merged then ingested using postgres copy function.  

## how to automate the process
This process can be automated by creating a script that would check for new csv files using inotify then pass the path to the ingest_csv_file.py script.  


## To access the API 
head over to http://http://127.0.0.1:8000/musicalworks/ and see the distinct ingested Musical Works

## To query for a particular work
run curl command as below  
`
curl http://127.0.0.1:8000/musicalworks/?search=T0101974597 | jq
`
Only one item will be displayed

## If the Single view app had 20 million records, will the response time be the same?
No it will not be the same.

## How would it be improved
Response time can be improved by either indexing the database table or by using specialised search tools like ElasticSearch and lucene.


