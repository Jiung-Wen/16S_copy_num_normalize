## 16S_copy_num_normalize

This script is executable in QIIME2 environment.  
Usage:
Normalize sequences by 16S rRNA gene copy number based on *rrn*DB database (version 5.6).

```
copy_num_normalize.py --table table.qza --taxonomy taxonomy.qza -d silva -o output_file_name
```

* ```--table``` PATH - Path of QIIME2 artifact ```FeatureTable[Frequency]```
* ```--taxonomy``` PATH - path of QIIME2 artifact ```FeatureData[Taxonomy]``` 
* ```-d``` STRING - database used for sequence annotation {silva, greengenes}
* ```-o``` PATH - path of output file


Currently in Beta version.
