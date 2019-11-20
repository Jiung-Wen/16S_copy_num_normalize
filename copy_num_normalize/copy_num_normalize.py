#!/usr/bin/env python

import argparse
import os
import re
import pandas as pd
import numpy as np
from qiime2 import Artifact

DATABASES = ['silva','greengenes']

parser = argparse.ArgumentParser()

parser.add_argument("--table", type=str, required=True,
					 help='Path of QIIME2 Artifact FeatureTable Frequency')

parser.add_argument("--taxonomy", type=str, required=True,
					 help='Path of QIIME2 Artifact FeatureData Taxonomy')

parser.add_argument('-d', '--database', default='silva', choices=DATABASES,
					 help='16S rRNA sequence database for taxonomy annotation')

parser.add_argument("-o", "--output", type=str, required=True,
					 help='Output path')


dir_path = os.path.dirname(os.path.abspath(__file__))

df_rrndb = pd.read_csv(dir_path+'/rrnDB-5.6_pantaxa_stats_NCBI.tsv', sep='\t')

taxon2copynum = dict(zip(df_rrndb['name'],df_rrndb['mean']))


def main():

	args = parser.parse_args()

	if args.database=='silva':
		ranks = ['D_6__', 'D_5__', 'D_4__', 'D_3__', 'D_2__', 'D_1__', 'D_0__']
	if args.database=='greengenes':
		ranks = ['; s__', '; g__', '; f__', '; o__', '; c__', '; p__', 'k__']

	table = Artifact.load(args.table)
	df_table_asv = table.view(pd.DataFrame)

	taxonomy = Artifact.load(args.taxonomy)
	df_taxonomy = taxonomy.view(pd.DataFrame)

	d = {'taxon': df_taxonomy['Taxon'], 'copy_number': [1]*len(df_taxonomy['Taxon'])}
	df_copy_num = pd.DataFrame(d)


	for index, taxon in enumerate(df_copy_num['taxon']): # loop all the taxa
		if 'Unassigned' in taxon:
			continue

		for rank in ranks: # loop all the taxonomic ranks, from species to kingdom
			try: # check if the rank in the taxon
				taxa_rank = re.search(rank + '(.*?);', taxon)[1]
				try: # check if the rank match rrnDB database
					copy_num = taxon2copynum[taxa_rank]
					df_copy_num.iloc[index,1]=copy_num
					break # go check next taxon
				except: # if not, move higher rank
					continue
			except: # if not, move to higher rank
				continue

		for rank in ranks:
			try: # check if the lowest rank is in the taxon
				taxa_rank = re.search(rank + '(.*)', taxon)[1]
				try: # check if the rank match rrnDB database
					copy_num = taxon2copynum[taxa_rank]
					df_copy_num.iloc[index,1]=copy_num
					break # go check next taxon
				except: # if not, move higher rank
					continue
			except: # if not, move to higher rank
				continue

	if args.database=='greengenes':
		for index, taxon in enumerate(df_copy_num['taxon']): # loop all the taxa
			if '; s__' in taxon:
				genus_species = re.search('; g__' + '(.*)', taxon)[1]
				genus_species = re.sub('; s__',' ', genus_species)

				try: # check if the rank match rrnDB database
					copy_num = taxon2copynum[genus_species]
					df_copy_num.iloc[index,1]=copy_num
					continue # go check next taxon
				except: # if not, move higher rank
					pass



	df_copy_num.to_csv(args.output+'_16S_rRNA_copy_number.txt', sep='\t')
	asv2copynum = dict(zip(df_copy_num.index,df_copy_num['copy_number']))
	df_copy_num_normalized = (df_table_asv/[asv2copynum[i] for i in df_table_asv.columns])
	table_normalized = Artifact.import_data('FeatureTable[Frequency]', df_copy_num_normalized)
	table_normalized.save(args.output+'_copy_number_normalized')


if __name__ == '__main__':
	main()
