#!/usr/bin/env python
#
# File: http://github.com/opentraveldata/opentraveldata/blob/master/tools/
#
import duckdb
import polars as pl
import sqlalchemy
import csv

conn = duckdb.connect()
conn = duckdb.connect(database='db.duckdb', read_only=False)

geoname_base_dir: str = "../data/geonames/data/por"
geoname_csv_dir: str = f"{geoname_base_dir}/data"
geoname_pqt_dir: str = f"{geoname_base_dir}/parquet"

# allCountries
geoname_allctry_fn: str = "allCountries"
geoname_allctry_csv: str = f"{geoname_csv_dir}/{geoname_allctry_fn}.txt"
geoname_allctry_pqt: str = f"{geoname_pqt_dir}/{geoname_allctry_fn}.parquet"

geoname_allctry_cln = {
        "geonameid": "bigint",
        "name": "varchar",
        "asciiname": "varchar",
        "alternatenames": "varchar",
        "latitude": "double",
        "longitude": "double",
        "fclass": "char(1)",
        "fcode": "varchar(10)",
        "country": "varchar(2)",
        "cc2": "varchar",
        "admin1": "varchar",
        "admin2": "varchar",
        "admin3": "varchar",
        "admin4": "varchar",
        "population": "smallint",
        "elevation": "integer",
        "dem": "integer",
        "timezone": "varchar",
        "moddate": "date"
        }

geoname_allctry_query: str = f"""
COPY (
  SELECT *
  FROM read_csv_auto("{geoname_allctry_csv}",
                     header=True,
                     dateformat="%Y-%m-%d",
                     columns={geoname_allctry_cln},
                     quote=csv.QUOTE_NONE,
                     filename=True,
                     AUTO_DETECT=TRUE)
  )
  TO '{geoname_allctry_pqt}' (FORMAT 'parquet')
"""


# Alternate names
geoname_altname_fn: str = "alternateNames"
geoname_altname_csv: str = f"{geoname_csv_dir}/{geoname_altname_fn}.txt"
geoname_altname_pqt: str = f"{geoname_pqt_dir}/{geoname_altname_fn}.parquet"

geoname_altname_cln = {
        "alternatenameId": "bigint",
        "geonameid": "bigint",
        "isoLanguage": "varchar",
        "alternateName": "varchar",
        "isPreferredName": "smallint",
        "isShortName": "smallint",
        "isColloquial": "smallint",
        "isHistoric": "smallint"
        }

geoname_altname_query: str = f"""
COPY (
  SELECT *
  FROM read_csv_auto("{geoname_altname_csv}",
                     header=True,
                     dateformat="%Y-%m-%d",
                     columns={geoname_altname_cln},
                     quote=csv.QUOTE_NONE,
                     filename=True,
                     AUTO_DETECT=TRUE)
  )
  TO '{geoname_altname_pqt}' (FORMAT 'parquet')
"""

# CSV to Parquet for allCountries
conn.execute(geoname_allctry_query)

# CSV to Parquet for alternateNames
conn.execute(geoname_altname_query)

