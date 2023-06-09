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

Getting More Accurate
---------------------

For some users the canonical recording isn't going to be good enough, so another step can be added to make it more precise.
Once a recording_mbid has been found, another lookup at the MusicBrainz API could be done. Assume that recording
d789aeeb-2b98-4430-8aa4-356c954b794f was returned as the canonical recording. Then you can make the following query to:

```
https://musicbrainz.org/ws/2/recording/d789aeeb-2b98-4430-8aa4-356c954b794f?fmt=json&inc=releases
```

Which will return the releases that this track appears on and you can choose the correct release. There are many
other steps that can be taken to further refine which recordign to tag your track as -- you can use the data returned
from this call to query other bits of data to find the correct recording.


Starting Typesense
------------------

To run this example as is, you will need to install Typesense ( https://typesense.org/ ). If you have docker
installed, you could create a typesense container (without persistence!) with this command:

```
docker run -p 8108:8108 -d --name=typesense typesense/typesense:0.19.0 --data-dir /var/local --api-key=1234567890
```
