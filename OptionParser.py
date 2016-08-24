from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="file name of the pickled results", default="FirstOrderEnglishHyps.pkl")
parser.add_option("-d", "--datasize", dest="datasize", type="int", help="number of data points", default=100)
parser.add_option("-t", "--top", dest="top", type="int", help="top N count of hypotheses from each chain", default=100)
parser.add_option("-s", "--steps", dest="steps", type="int", help="steps for the chainz", default=10000)
parser.add_option("-c", "--chainz", dest="chains", type="int", help="number of chainz :P", default=15)

(options, args) = parser.parse_args()