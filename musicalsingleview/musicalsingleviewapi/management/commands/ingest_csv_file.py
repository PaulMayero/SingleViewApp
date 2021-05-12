import os
from copy import deepcopy
from json import dumps
from sys import exit

from django.core.management.base import BaseCommand
from pandas import concat, read_csv
from random_name import generate_name
from datetime import datetime
import psycopg2

class Command(BaseCommand):
    help = 'Ingests the csv file provided'

    def add_arguments(self, parser):
        parser.add_argument('path_to_csv_file', type=str, 
                            help='Provides path to file where csv file is')

        parser.add_argument('path_to_reconciled_csv', type=str,
                            help='Provides path to where reconciled csv will be put')




    def handle(self, *args, **kwargs):
        csv_file = kwargs['path_to_csv_file']

        reconciled_file_path = kwargs['path_to_reconciled_csv']
        
        #reconciliation and matching logic
        csv_df = read_csv(csv_file)

        multiple_musical_works_df = csv_df[csv_df.groupby(['iswc','title'])
            ['iswc','title','contributors'].transform('count') > 1]

        single_musical_works_df = csv_df[csv_df.groupby(['iswc','title'])
            ['iswc','title','contributors'].transform('count') == 1]

        multiple_musical_works_df = multiple_musical_works_df.dropna()
        single_musical_works_df = single_musical_works_df.dropna()

        frames = [multiple_musical_works_df, single_musical_works_df]

        result = concat(frames)

        result.drop_duplicates(subset=['iswc'],inplace=True,
                               ignore_index=True)

        result['contributors'] = result['contributors'].str.split('|')

        def make_columns_ingestible(column_content):
            return (str(column_content).replace("[","{").replace("]","}")) 

        result['contributors'] = result['contributors'].apply(lambda x : make_columns_ingestible(x))

        gypsy = deepcopy(result)

        result = result.to_dict(orient='records')

        if len(result) > 0:

            self.stdout.write('Data extracted \n')

            self.stdout.write(dumps(result, indent=4))

            self.stdout.write('\n')

            try:
                os.makedirs(reconciled_file_path)
            except FileExistsError:
                self.stdout.write('The folder already exists. it will put there \n')
            except Exception:
                self.stdout.write("something went wrong now \n")
                exit(0)
            else:
                self.stdout.write('we just made your reconciled file path at %s' %reconciled_file_path)
                self.stdout.write('\n')


            reconciled_csv_file_name = reconciled_file_path + datetime.now().strftime("%Y:%m:%d-%H:%M:%S.%f") + '-' + generate_name() + '.csv'

            gypsy = gypsy[['title','contributors','iswc']]
            

            gypsy.to_csv(reconciled_csv_file_name, encoding='utf-8', index=False, header=False, sep="\t")

            self.stdout.write('reconciled csv saved as %s' %reconciled_csv_file_name)

            self.stdout.write('\n')

            self.stdout.write('Starting ingestion in a bit \o/')

            conn = psycopg2.connect(host="localhost", port = 5432, database="musical_works", user="bmat", password="bmat")

            cur = conn.cursor()

            try:
                self.stdout.write('ingestion starting now')
                with open(reconciled_csv_file_name, 'r') as f:
                    cur.copy_from(f, "musicalsingleviewapi_musicalwork" , columns=('title','contributors','iswc'),  sep='\t')
                conn.commit()
                self.stdout.write('Ingestion finished')
                
            except (Exception, psycopg2.DatabaseError) as error:
                self.stdout.write(error)
                exit(0)

            finally:
                cur.close()
                conn.close()
                self.stdout.write('Database connection closed.')


        if len(result) == 0:
            self.stdout.write('Sorry we failed you :(')
            exit(0)

    









