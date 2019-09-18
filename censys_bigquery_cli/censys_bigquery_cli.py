import csv
import json
import os
import pprint
import time

from google.cloud import bigquery


class CensysBigQuery:

    def _build_query(self, query, **kwargs):

        # Split the query at the FROM statement
        # Also split the query at the tilde ` character
        # Then split it one more time at the . periods to get the dates
        database_string = query.split('FROM')[1].split('`')[1].split('.')
        pprint.pprint(database_string)

    def format_json_result(self, result):
        record_dict = {x[0]: x[1] for x in result}
        return record_dict

    def _write_csv_file(self, results):

        output_filename = os.path.join(
            os.getcwd(),
            "{}.csv".format(self.output_file)
        )

        with open(output_filename, 'w') as csv_file:
            field_names_set = False
            writer = None

            for result in results:
                # During the first run, set the column headers
                formatted_result = self.format_json_result(result.items())
                row_names = [x for x in formatted_result]

                if not field_names_set:
                    writer = csv.DictWriter(csv_file, fieldnames=row_names)
                    writer.writeheader()
                    field_names_set = True

                writer.writerow(formatted_result)

        print('Wrote approximately {} bytes to file {}'.format(os.path.getsize(output_filename), output_filename))

    def _write_json_file(self, results):

        output_filename = os.path.join(
            os.getcwd(),
            "{}.json".format(self.output_file)
        )

        with open(output_filename, 'w') as json_file:
            for row in results:
                data = json.dumps(self.format_json_result(row.items()))
                json_file.write(data)

        print('Wrote approximately {} bytes to file {}'.format(os.path.getsize(output_filename), output_filename))

    def _write_results(self, results, output_type=None):

        if "screen" in output_type:
            for row in results:
                print(json.dumps(self.format_json_result(row.items())))

        if "json" in output_type:
            self._write_json_file(results)

        if "csv" in output_type:
            self._write_csv_file(results)

    def __init__(self, **kwargs):

        self.creds = kwargs.get('google_application_credentials', os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None))

        if self.creds:
            self.bq_client = bigquery.Client()
        else:
            raise Exception("Please set the system variable GOOGLE_APPLICATION_CREDENTIALS")

        if kwargs.get('user_filename', None) is None or kwargs.get('user_filename', None) == 'None':
            self.output_file = 'censys-bq-output-{}'.format(time.time())
        else:
            self.output_file = kwargs.get('user_filename')

    def query_censys(self, query, **kwargs):

        client = self.bq_client

        query_job = client.query("{}".format(query))
        results = query_job.result()  # Waits for job to complete.

        self._write_results(results=results, output_type=kwargs.get('output_type', 'screen'))

        return results
