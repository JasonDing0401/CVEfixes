#!/usr/bin/env bash
#
# create a SQLite3 database file of the CVEfixes.

# ------------------------------------------------------------------------------
zcat CVEfixes_v1.0.7/Data/CVEfixes_v1.0.7.sql.gz | sqlite3 output/CVEfixes.db

#------------------------------------------------------------------------------