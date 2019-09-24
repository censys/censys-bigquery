# Censys BigQuery Command Line Tool

This script allows users to query the data in Censys Data BigQuery Project from the command line. The results from the query can be exported as JSON, CSV, or viewed from the terminal screen.

Note: the Censys Data BigQuery Project is available to enterprise customers and approved academic researchers. For more information on product tiers, contact sales@censys.io.

##### Setting Up a Service Account in BigQuery:

Prior to using the BiqQuery Command Line Tool, you'll need to set up a service account that is associated with your Google Cloud Platform.

Google provides documentation on how to create a service account, either via the GCP Console or the Command Line.  Visit https://cloud.google.com/docs/authentication/getting-started for full documentation.

Be sure to set the GOOGLE_APPLICATION_CREDENTIALS environmental variable.
```$ export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"```


##### Installation:
```
pip install censys_bigquery_cli
```

OR

```
pip install git+https://github.com/censys/censys-bigquery
```


##### Usage:
The script allows you to input SQL queries as arguments in the script, returning the results as screen output (default), JSON, or CSV.

Here are some example queries:
```
$ censys_bq 'SELECT ip, ports, protocols, tags FROM `censys-io.ipv4_public.current` WHERE location.city = "Ann Arbor" and REGEXP_CONTAINS(TO_JSON_STRING(tags), r"rsa-export") LIMIT 25'
```
```
$ censys_bq 'with user_ports as (                            
SELECT [443, 3306, 6379] as selected_ports
)

SELECT DISTINCT ip, TO_JSON_STRING(user_ports.selected_ports)
  FROM `censys-io.ipv4_banners_public.current`, user_ports, UNNEST(services) as s
  WHERE (SELECT LOGICAL_AND(a_i IN (SELECT port_number FROM UNNEST(services))) FROM UNNEST(user_ports.selected_ports) a_i) LIMIT 15' --output csv
```

```
$ censys_bq 'SELECT COUNT(ip), p80.http.get.body_sha256
FROM `censys-io.ipv4_public.current`
WHERE REGEXP_CONTAINS(p80.http.get.body, r"(?i)coinhive.min.js>")
GROUP BY p80.http.get.body_sha256
ORDER BY 1 DESC' --output json
```

```
$ censys_bq 'with Data as (SELECT
  distinct fingerprint_sha256
FROM
  `censys-io.certificates_public.certificates`, UNNEST(parsed.subject.organization) as po, UNNEST(parsed.names) as parsed_names
WHERE
   REGEXP_CONTAINS(TO_JSON_STRING(parsed.names), r"[.]example[.]")
)

SELECT
  distinct ip
FROM
  `censys-io.ipv4_banners_public.current` as c, UNNEST(services)
      JOIN Data as d on d.fingerprint_sha256 = certificate.fingerprints.sha256
LIMIT 20' --output json
```
