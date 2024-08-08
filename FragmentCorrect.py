
import gzip
import argparse
import pysam
import time, os
from collections import defaultdict

def CommandLineParser():
    parser=argparse.ArgumentParser(description = "This is a description of input args")
    parser.add_argument("-F","--fragment", dest = "fragment",default = "")
    parser.add_argument("-C","--barcodecorrect",dest = "barcode_correct",default = "")
    parser.add_argument("-O", "--outfile", dest = "outfile",default = "")

    return parser.parse_args()

parser = CommandLineParser()
fragment = parser.fragment
barcode_correct = parser.barcode_correct
frag_correct = parser.outfile

start_time = time.time()
print("Start to read barcode correct file",time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
barcode_lib_dict = defaultdict(set)
with open(barcode_correct, "r") as barcode_correct_in:
    for line in barcode_correct_in:
        line_list = line.strip().split("\t")
        barcode_lib_dict[line_list[0]].add(line_list[2])
end_time = time.time()
print("End", time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

start_time = time.time()
print("Start to correct barcode",time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
frag_correct_out = open(frag_correct, "w")
total = 0 
keeped = 0
with gzip.open(fragment, "rt") as fragment_in:
    for line in fragment_in:
        total+=1
        line_list = line.strip().split("\t")
        barcode_obs = line_list[3]
        if barcode_obs in barcode_lib_dict:
            keeped+=1
            for bc in list(barcode_lib_dict[barcode_obs]):
                line_list[3] = bc
                outstr = "\t".join(line_list) + "\n"
                frag_correct_out.write(outstr)
        else:
            pass
end_time = time.time()
print("End", time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
print("%d processed \n  %d keeped \n" % (total,keeped))

