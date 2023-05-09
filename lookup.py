#!/usr/bin/env python3

import csv
import re

import typesense
import typesense.exceptions
from unidecode import unidecode

TYPESENSE_HOST = "localhost"
TYPESENSE_PORT = 8108
TYPESENSE_API_KEY = "1234567890"
TYPESENSE_COLLECTION = "musicbrainz_canonical_data"


def make_combined_lookup(artist_name, recording_name):
    """ Given the artist name and recording name, return a combined_lookup string """
    return unidecode(re.sub(r'[^\w]+', '', artist_name + recording_name).lower())


def build_index(csv_file):
    """ Import the MusicBrainz Canonical Data CSV file into typesense """

    max_score = 4 * 1024 * 1024 * 1024  # a sufficiently large number
    client = typesense.Client({
        'nodes': [{
            'host': "localhost",
            'port': 8108,
            'protocol': 'http',
        }],
        'api_key': TYPESENSE_API_KEY,
        'connection_timeout_seconds': 1000000
    })

    schema = {
        'name': TYPESENSE_COLLECTION,
        'fields': [
            {
                'name': 'combined',
                'type': 'string'
            },
            {
                'name': 'score',
                'type': 'int32'
            },
        ],
        'default_sorting_field': 'score'
    }
    client.collections.create(schema)

    try:
        documents = []
        with open(csv_file) as csv_file:
            for i, row in enumerate(csv.reader(csv_file, delimiter=',')):
                if i == 0:
                    continue
                document = {
                    'artist_credit_id': row[1],
                    'artist_mbids': "{" + row[2] + "}",
                    'artist_credit_name': row[3],
                    'release_mbid': row[4],
                    'release_name': row[5],
                    'recording_mbid': row[6],
                    'recording_name': row[7],
                    'score': max_score - int(row[9]),
                    'combined': make_combined_lookup(row[7], row[3])
                }
                documents.append(document)

                if len(documents) == 50000:
                    client.collections[TYPESENSE_COLLECTION].documents.import_(documents)
                    documents = []
                    print(f"imported {i:,} rows")

            if documents:
                client.collections[TYPESENSE_COLLECTION].documents.import_(documents)

    except typesense.exceptions.TypesenseClientError as err:
        print("typesense index: Cannot build index: ", str(err))


def lookup_track(artist_name, recording_name):
    """ Lookup a track given the artist_name and recording_name. Print results to stdout. """

    combined_lookup = make_combined_lookup(artist_name, recording_name)
    match = datastore_lookup(combined_lookup)
    if match is None:
        print("track was not found")
    else:
        print("track was matched:")
        print(f"  artist: {match['artist_credit_name']}")
        print(f"  release_mbid: {match['artist_mbids']}")
        print(f"  release: {match['release_name']}")
        print(f"  release_mbid: {match['release_mbid']}")
        print(f"  recording: {match['recording_name']}")
        print(f"  recording_mbid: {match['recording_mbid']}")


if __name__ == "__main__":
    print("meh")
    if len(sys.argv) != 2:
        print("Usage: lookup.py <artist_name> <recording_name>")
    else:
        lookup_track(sys.argv[1], sys.argv[2])
