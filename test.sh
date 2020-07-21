error_exit() {
    echo "ERROR $*"
    exit 1
}

OUTFILE=tmpfilename

ffpt2csv tests/data/1.ffpt $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/1.csv $OUTFILE || error_exit
rm $OUTFILE

csv2ffpt tests/data/1.csv $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/1.ffpt $OUTFILE || error_exit
rm $OUTFILE

ffpt2csv tests/data/2.ffpt $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/2.csv $OUTFILE || error_exit
rm $OUTFILE

csv2ffpt tests/data/2.csv $OUTFILE || error_exit
diff -u --ignore-space-change tests/data/2.ffpt $OUTFILE || error_exit
rm $OUTFILE


