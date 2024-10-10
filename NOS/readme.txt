REQUERIMENTS:
sudo apt-get install libreoffice
sudo apt pari-gp
sudo apt install texlive-latex-base

EXECUTE:
./PTCodes.sh | tee output.txt

SHOW:
sqlite3 PTCodes.db "SELECT * FROM Results;"
sort -u results_pac.csv >> results3.csv

