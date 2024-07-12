## Search the column number according to column name
awk 'BEGIN {FS="\t"} NR==1 { for(i=1; i<=NF; i++) { if($i=="AutoInterpStatus") { print i } } }' file_path

### replace the script and output for different sample analysis
vcf_file=$1
name=${vcf_file%%.*}

cp raw.sh ./${name}.sh
sed -i "s|\${cpu}|10|g" ./${name}.sh
sed -i "s|\${chip_type}|we7v|g" ./${name}.sh
sed -i "s|\${oud}|/mnt/GenePlus002/genecloud/Org_terminal/org_52/terminal/wangym_16601250368/vcf_generate/raw_result|g" ./${name}.sh
sed -i "s|\${module_bin}|/mnt/DB-linjian/DB/privateDB/cnc-confighub/cnc-release/20240104/81ad467c521b43b51d0960859ab9d23b2f623474/workflow/WESPair/modules/SomVAS/bin|g" ./${name}.sh
sed -i "s|\${sample}|${name}|g" ./${name}.sh
sed -i "s|sample=24A900036BD_24A900036FD|sample=${name}|g" ./${name}.sh
sed -i "s|\${input_vcf}|/mnt/GenePlus002/genecloud/Org_terminal/org_52/terminal/wangym_16601250368/vcf_generate/cooked_vcf/${name}.vcf.gz|g" ./${name}.sh
### end
