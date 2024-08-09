# snATAC-seq
## Pipeline for snATAC-seq data processing to generate fragment files
### Requirements

This pipeline requires the following software:

- **BWA**: >=0.7.17
- **samtools**: >=1.12
- **snaptools**: >=1.4.8

### Additional Files

To run this pipeline, you also need to download the following files provided in this GitHub repository:

- **BarcodeCorrect.py**: Script for correcting barcodes.
- **FragmentCorrect.py**: Script for correcting fragments.
- **scATAC_v2_barcode_list.txt.gz**: Barcode whitelist file.

Make sure to download these files and place them in the appropriate directory before running the pipeline.

### Usage

```bash
threads=10 # Specify the number of threads to use
sample="sample1" # the prefix for the FASTQ files
BWA_index="PATH_TO_YOUR/mm10.fa" # the path of bwa index for reference genome
gsize="PATH_TO_YOUR/mm10.chrom.sizes" # the path of genome size file
tmpfold="PATH_TO_YOUR/temp" # temporary directory
logfile="PATH_TO_YOUR/snaptools.log"
outbam="PATH_TO_YOUR/${sample}.bam"
outsnap="PATH_TO_YOUR/${sample}.snap"
output="PATH_TO_YOUR/${sample}.temp.tsv.gz"
corrected_output="PATH_TO_YOUR/${sample}.tsv.gz"
fastq1="PATH_TO_YOUR/${sample}_R1.fastq.gz"
fastq2="PATH_TO_YOUR/${sample}_R2.fastq.gz"

# Step 1: Align paired-end reads
snaptools align-paired-end --input-reference=${BWA_index} --input-fastq1=${fastq1} --input-fastq2=${fastq2} --output-bam=${outbam} --aligner=bwa --read-fastq-command=zcat --min-cov=0 --num-threads=${threads} --if-sort=True --tmp-folder=${tmpfold} --overwrite=TRUE

# Step 2: Preprocess BAM file to generate SNAP file
snaptools snap-pre --input-file=${outbam} --output-snap=${outsnap} --genome-name=mm10 --genome-size=${gsize} --min-mapq=10 --min-flen=0 --keep-chrm=TRUE --keep-single=False --keep-secondary=False --overwrite=True --max-num=10000000 --verbose=False

# Step 3: Generate fragment file from SNAP file
snaptools dump-fragment --snap-file=${outsnap} --output-file=${output} --buffer-size=10000 --tmp-folder=${tmpfold} &> ${logfile}

# Step 4: Correct barcodes in the FASTQ files
python BarcodeCorrect.py  --fq ${fastq1}  -b scATAC_v2_barcode_list.txt.gz -O barcode_correct.txt

# Step 5: Correct fragment file using the corrected barcodes
python FragmentCorrect.py -F ${output} -C barcode_correct.txt -O ${corrected_output}

# Step 6: Sort, compress, and index the corrected fragment file
cat ${corrected_output} | sort -V -k1,1 -k2,2n  |  pbgzip -c > ${corrected_output}.gz

tabix -p bed ${corrected_output}.gz

# Optional: Clean up intermediate files
#rm -f ${output} barcode_correct.txt ${corrected_output}
'''
### Output

The final fragment file `${corrected_output}.gz` generated by this pipeline can be used as an input file for **ArchR** ([https://github.com/GreenleafLab/ArchR](https://github.com/GreenleafLab/ArchR)) to perform downstream analyses.
