## Search the column number according to column name
awk 'BEGIN {FS="\t"} NR==1 { for(i=1; i<=NF; i++) { if($i=="AutoInterpStatus") { print i } } }' file_path
