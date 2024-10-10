#!/bin/bash

# FORMATTING CSV TO PROCESS
echo "PTCodes Super Script !!!"
echo "Copy codigos_postais.csv -> work.csv"
mkdir temp5
cp codigos_postais.csv temp5/work.csv
cd temp5
chmod 777 work.csv
echo "Formatting work.csv to initializate code."
echo "#########################################"
tail -n +2 work.csv >> work2.csv
chmod 777 work2.csv
cat work2.csv | cut -c 1-8 >> work3.csv
chmod 777 work3.csv
rm work.csv
rm work2.csv
echo ""
# DOWNLOADING DATABASE

echo "DOWNLOADING DATABASE"
#sleep 10
cd ..
cp sc4t.gp temp5/sc4t.gp
cd temp5
wget "http://download.geonames.org/export/zip/PT.zip"
unzip PT.zip
rm readme.txt
rm PT.zip
chmod 777 PT.txt
echo ""

# INICIALIZANDO O SCRIPT
echo "INICIALIZANDO O SCRIPT"
#sleep 10
gp -q sc4t.gp

awk -F'\t' '{print $2 "," $3 "," $4}' results.txt >> results_pac.csv

echo "VALID COUNTING RESULTS:"
wc -l results.txt | cut -c 1-4
echo ""

# CONVERTENDO PARA SQLITE3
echo "CONVERT TO DATABASE"
#sleep 10
sqlite3 PTCodes.db "CREATE TABLE Results (codigo_postal TEXT, concelho TEXT, distrito TEXT);"
sqlite3 PTCodes.db <<EOF
.mode csv
.import results_pac.csv Results
EOF
sqlite3 PTCodes.db "SELECT * FROM Results;"
echo ""

# TESTES
echo "CHECKING FILES"
echo ""
echo "DATABASE"
if [ -e "PT.txt" ]; then
    echo "PT.txt Checked!! File exist."
    wc -l PT.txt
else
    echo "PT.txt File does not exist."
fi
echo "DATABASE STATS"
sqlite3 PTCodes.db "PRAGMA Results; PRAGMA page_count; PRAGMA page_size; SELECT sqlite_version();"
echo ""
echo "Results:"
if [ -e "results.txt" ]; then
    echo "results.txt Checked!! File exist."
    wc -l results.txt
else
    echo "results.txt File does not exist."
fi
echo ""
echo "Results_pac:"
if [ -e "results_pac.csv" ]; then
    echo "results_pac.csv Checked!! File exist."
    wc -l results_pac.csv
else
    echo "results_pac.csv File does not exist."
fi
echo ""
echo "#LISTA DE TESTES DESENHADOS:"
echo "# 1) CHECKS IF DATABASE EXIST."
echo "# 2) CHECKS DATABASE STATS."
echo "# 3) CHECKS IF RESULTS.TXT EXIST."
echo "# 4) CHECKS IF RESULTS_PAC.CSV EXIST."
