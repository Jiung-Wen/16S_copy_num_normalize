## 16S_copy_num_normalize

This script is executable in QIIME2 environment.  
### Description:
Normalize sequences by 16S rRNA gene copy number (GCN) based on *rrn*DB database (version 5.6). The script matches the taxa of sequences with the ```rrnDB-5.6_pantaxa_stats_NCBI.tsv``` file, starting from the lowest rank. If a match is found, the mean of GCN for the taxon is assigned; if not, the script will try to match a higher rank until the highest rank is met. All the unassigned sequences are assumed to have one GCN.

Note that the **mean** column in the ```rrnDB-5.6_pantaxa_stats_NCBI.tsv``` is, according to the [*rrn*DB manual](https://rrndb.umms.med.umich.edu/help/), calculated from the means of the pan-taxa of immediate lower rank. Therefore, the mean of GCN might be different from the *rrn*db online search result. For example, the "mean" of GCN for bacteria is 2.02 in the downloading tsv file, whereas the mean of GCN for all the bacterial taxa is 5.0 if you search *rrn*DB.

### Usage:

```
copy_num_normalize.py --table table.qza --taxonomy taxonomy.qza -d silva -o output_file_name
```

* ```--table``` PATH - path of QIIME2 artifact ```FeatureTable[Frequency]```
* ```--taxonomy``` PATH - path of QIIME2 artifact ```FeatureData[Taxonomy]``` 
* ```-d``` STRING - database used for sequence annotation {silva, greengenes}
* ```-o``` PATH - path of output file


Currently in Beta version.
