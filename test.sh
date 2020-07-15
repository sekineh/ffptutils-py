error_exit() {
    echo "ERROR $*"
    exit 1
}

OUTFILE=tmpfilename

python ffpt2csv.py test/1.ffpt $OUTFILE || error_exit
diff -u test/1.csv $OUTFILE || error_exit
rm $OUTFILE

python csv2ffpt.py test/1.csv $OUTFILE || error_exit
diff -u test/1.ffpt $OUTFILE || error_exit
rm $OUTFILE

python ffpt2csv.py test/2.ffpt $OUTFILE || error_exit
diff -u test/2.csv $OUTFILE || error_exit
rm $OUTFILE

python csv2ffpt.py test/2.csv $OUTFILE || error_exit
diff -u test/2.ffpt $OUTFILE || error_exit
rm $OUTFILE


