#!/usr/bin/env python
#
#rpoDdNscreen.py ("read pair overlap screen for DiscovarDeNovo) does what?
#  xyz
#
import sys
from Bio import SeqIO
from itertools import izip_longest
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

inpath = sys.argv[1]
goodreads1 = open("goodreads_1.fq", "a")
goodreads2 = open("goodreads_2.fq", "a")
discard1   = open("discard_1.fq", "a")
discard2   = open("discard_2.fq", "a")

verbose = 0
threshold = 40
i = 0

readiter = SeqIO.parse(open(inpath), "fastq")
for rec1, rec2 in izip_longest(readiter, readiter):

    i += 1
    if i%50000 == 0 :
       print "... now working on read pair %10d" % i

    rec2rc = rec2.reverse_complement(id="rec2rev")
    overlap     = pairwise2.align.globalms(rec1.seq, rec2rc.seq, 2, -1, -100, -1, penalize_end_gaps=0, score_only=1) / 2
    leftunique  = len(rec1.seq)-overlap
    rightunique = len(rec2.seq)-overlap

    if  overlap < threshold  or  leftunique < threshold  or  rightunique < threshold :
       SeqIO.write(rec1, discard1, "fastq")
       SeqIO.write(rec2, discard2, "fastq")
       if verbose :
          alignments = pairwise2.align.globalms(rec1.seq, rec2rc.seq, 2, -1, -100, -1, penalize_end_gaps=0)
          print(format_alignment(*alignments[0]))
#         print len(rec1.seq)-overlap, overlap, len(rec2.seq)-overlap
          print leftunique, overlap, rightunique
          print "\n\n"
    else :
       SeqIO.write(rec1, goodreads1, "fastq")
       SeqIO.write(rec2, goodreads2, "fastq")
