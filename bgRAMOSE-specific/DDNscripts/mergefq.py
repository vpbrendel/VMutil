#!/usr/bin/env python
#
#mergefq.py takes a pair of matched fastq files (reads1 and reads2, respectively)
#  and merges them so that each read1 is followed by its read2 partner.  The output
#  is printed to files of chunksize read pairs each, named outflable-mergedreads-number.
#
from Bio import SeqIO
import itertools
import sys
import os

def merge_fastq(fastq_path1, fastq_path2, outflabel, chunksize):
    chunksize = int(chunksize)
    i = -1
    fnlabel = 0
    fastq_iter1 = SeqIO.parse(open(fastq_path1),"fastq")
    fastq_iter2 = SeqIO.parse(open(fastq_path2),"fastq")
    for rec1, rec2 in itertools.izip(fastq_iter1, fastq_iter2):
        i += 1
        if i%chunksize == 0 :
           if i > 0 :
              outfile.close()
           fnlabel += 1
           outfname = "%s-mergedreads-%d" % (outflabel, fnlabel)
           outfile = open(outfname,"w")

        SeqIO.write([rec1,rec2], outfile, "fastq")
    outfile.close()

if __name__ == '__main__':
    merge_fastq(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
