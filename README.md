MusicBrainz Canonical Data Examples
===================================

This simple example shows how to lookup music metadata using the MusicBrainz canonical dataset. For more details,
please see our blog post [How to build your own tagger, with MusicBrainz Canonical Metadata](https://blog.metabrainz.org/?p=10350).

You'll need to download the https://metabrainz.org/datasets/derived-dumps#canonical dataset and extract the
file canonical_musicbrainz_data.csv and store it in top level directory of this repo.

You will also need to install the Typesense server -- see below.

Then, build the index with:

```
./build_index.py
```

This will take some time -- at the time of this writing this dataset contains near 23M rows!

Once the index is complete you can perform metadata lookups with:

```
./lookup.py "Portishead" "Glory Box"
```

And if everything is working, it should print the stats for the canonical track on stdout.


Starting Typesense
------------------

To run this example as is, you will need to install Typesense ( https://typesense.org/ ). If you have docker
installed, you could create a typesense container (without persistence!) with this command:

```
docker run -p 8108:8108 -d --name=typesense typesense/typesense:0.19.0 --data-dir /var/local --api-key=1234567890
```
