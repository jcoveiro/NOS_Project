a=readstr("work3.csv");
for(x=1,length(a),system("""cat PT.txt | grep "a[x]" >> 'results.txt'""");print("PROCESSANDO: "x"/"length(a)))


quit
