error_exit() {
    echo "ERROR $*"
    exit 1
}

OUTFILE=tmpfilename

python ffptutils/scripts/ffpt2csv.py tests/data/1.ffpt $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/1.csv $OUTFILE || error_exit
rm $OUTFILE

python ffptutils/scripts/csv2ffpt.py tests/data/1.csv $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/1.ffpt $OUTFILE || error_exit
rm $OUTFILE

python ffptutils/scripts/ffpt2csv.py tests/data/2.ffpt $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/2.csv $OUTFILE || error_exit
rm $OUTFILE

python ffptutils/scripts/csv2ffpt.py tests/data/2.csv $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/2.ffpt $OUTFILE || error_exit
rm $OUTFILE


