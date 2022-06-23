from analyze import * 

# results = \
#     [
#         [ { 'title': 'MUL-11',\
#             'files': ["data/bloat/11.csv", "data/bloat/11.neutral.csv"] },\
#             { 'title': 'PAR-12',\
#                 'files': ["data/bloat/parity.csv", "data/bloat/parity.neutral.csv"] } ],\
#         [{ 'title': 'MAJ-13',\
#             'files': [ "data/bloat/majority.csv", "data/bloat/majority.neutral.csv" ] },\
#             { 'title': 'CMP-5',\
#                 'files': [ "data/bloat/comparator.csv",  "data/bloat/comparator.neutral.csv"]\
#             } ]\
#     ]

results = \
    [
        # [ { 'title': None, 'files': ["data/20/mul.csv", "data/20/mul.mut.csv", "data/20/mul.a.csv", "data/20/mul.n.2.csv"] } ]
        # [ { 'title': 'KJ11', 'files': ["kj11.csv", "kj11.n.csv"] } ]
        # [ { 'title': 'NG12', 'files': ["ng12.csv", "ng12.n.csv"] } ]
        # [ { 'title': 'KJ4', 'files': ["kj4.csv", "kj4.n.csv"] } ]
        #[ { 'title': 'NG12', 'files': ["ng12.csv", "ng12.n.csv"] } ]
        # [ { 'title': 'PG1', 'files': ["pg1.csv", "pg1.n.csv"] } ]
        # [ { 'title': 'R1', 'files': ["r1.csv", "r1.n.csv"] } ],
        # [ { 'title': 'R2', 'files': ["r2.csv", "r2.n.csv"] } ],
        # [ { 'title': 'keijzer-3', 'files': ["data/2021-11-20/kj3.csv", "data/2021-11-20/kj3.n.csv"] } ],
        # [ { 'title': 'keijzer-11', 'files': ["bog-Kj11-RTsTx-7379006.csv", "bog-Kj11-RTsTmx-1-7379006.csv", "bog-Kj11-RTsTmx-10-7379006.csv", "bog-Kj11-RTsTxN-str4-7379006.csv"] } ],
        [ { 'title': 'keijzer-3', 'files': ["bog-Kj3-RTsTx-7379006.csv", "bog-Kj3-RTsTmx-1-7379006.csv", "bog-Kj3-RTsTmx-10-7379006.csv", "bog-Kj3-RTsTxN-str4-7379006.csv"] } ],
        # [ { 'title': 'KJ4', 'files': ["kj4.csv", "kj4.n.csv"] } ],
        # [ { 'title': 'KJ11', 'files': ["kj11.csv", "kj11.n.csv"] } ],
        # [ { 'title': 'NG9', 'files': ["ng9.csv", "ng9.n.csv"] } ],
        # [ { 'title': 'NG12', 'files': ["ng12.csv", "ng12.n.csv"] } ],
        # [ { 'title': 'PG1', 'files': ["pg1.csv", "pg1.n.csv"] } ],
        # [ { 'title': 'VL1', 'files': ["vl1.csv", "vl1.n.csv"] } ]

        # [ { 'title': None, 'files': ["mul.csv", "mul.a.csv", "mul.n.csv"] } ]
        # # [ { 'title': 'MUL-11', 'files': ["data/11/mul.csv", "mul.mut.csv", "data/11/mul.n.csv"] },
        # #     { 'title': 'PAR-11', 'files': ["data/11/par.csv", "par.mut.csv", "data/11/par.n.csv"] } ],
        # # [ { 'title': 'MAJ-11', 'files': ["data/11/maj.csv", "maj.mut.csv", "data/11/maj.n.csv"] },
        # #     { 'title': 'CMP-11', 'files': ["data/11/cmp.csv", "cmp.mut.csv", "data/11/cmp.n.csv"] } ]
        # # [ { 'title': None, 'files': ["data/11/par.csv", "data/11/par.a.csv", "data/11/par.n.csv"] } ]
        # # [ { 'title': None, 'files': ["data/11/maj.csv", "data/11/maj.a.csv", "data/11/maj.n.csv"] } ]
        # # [ { 'title': None, 'files': ["data/11/cmp.csv", "data/11/cmp.a.csv", "data/11/cmp.n.csv"] } ]
        #     # { 'title': 'PAR-11', 'files': ["par.csv", "par.a.csv", "par.n.csv"] } 
        # # ],
        # # [ { 'title': 'MAJ-11', 'files': ["maj.csv", "maj.a.csv", "maj.n.csv"] },
        # #     { 'title': 'CMP-12', 'files': ["cmp.csv", "cmp.a.csv", "cmp.n.csv"] } 
        # # ]
    ]

# colors = [ {'color': '#cc4bc1', 'title':'RTsTx', 'marker':'x'}, { 'color': '#8a85f5', 'title': 'RTsTmx', 'marker':'o' }, { 'color': '#45c46f', 'title': 'RTsNaTx', 'marker':'v' }, { 'color': '#fa8b5f', 'title': 'RTsNTx', 'marker':'s' } ]
#colors = [ {'color': '#cc4bc1', 'title':'RTsTx-6', 'marker':'x'}, { 'color': '#45c46f', 'title': 'RTsTx-10', 'marker':'v' }, { 'color': '#fa8b5f', 'title': 'RTsNTx-6', 'marker':'s' }, { 'color': '#8a85f5', 'title': 'RTsNTx-10', 'marker':'o' } ]
colors = [ {'color': '#cc4bc1', 'title':'Koza GP', 'marker':'x'}, { 'color': '#8a85f5', 'title': 'mut 1%', 'marker':'o' }, { 'color': '#45c46f', 'title': 'mut 10%', 'marker':'v' }, { 'color': '#fa8b5f', 'title': 'NRO, str4', 'marker':'s' } ]

for resLine in results:
    for res in resLine:
        res['data'] = [ read(expFile) for expFile in res['files'] ]
        res['bors'] = bor(res['data'])
        # print(f"test {res['bors'][0]} and {res['bors'][1]}")
        res['stats'] = allStats(res['bors'])
        res['fs'] = [ {'data': r, 'color': colors[i]['color'], 'title':colors[i]['title'], 'marker': colors[i]['marker']} for (i, r) in enumerate(res['data']) ]
        print(f"Stats for {res['title']}:\n{res['stats']}\n ")

#charts(results, "KJ4.png")

charts([results[0]], "keijzer-3.png")
# charts([results[1]], "R2.png")
# charts([results[2]], "KJ3.png")
# charts([results[3]], "KJ4.png")
# charts([results[4]], "KJ11.png")
# charts([results[5]], "NG9.png")
# charts([results[6]], "NG12.png")
# charts([results[7]], "PG1.png")
# charts([results[8]], "VL1.png")


#---- boxplots for last gen and bor 
expResultFolder = [ "data", "2022-04-15" ]
experiments = ["7379006"]
problems = [ "R1", "R2", "Kj3", "Kj4", "Kj11", "Ng9", "Ng12", "Pg1", "Vl1"]
settings = {"RTsTx": [""], "RTsTmx": ["1", "10"], "RTsTxN": ["str1", "str2", "str3", "str4"] }
                

os.path.join(expResultFolder + [])

# for d in os.listdir(expResultFolder, )
with open("", "r") as expStats: 
    for line in expStats.readlines(): 
        if "" != line:
            [runId, borSize, borDepth, meanSize, meanDepth, maxGen, found, ms, borFitness, borFitnessTestSet, fitnessStdev, aucRoc, nroRate, nroRevs] = line.split(" ")




# # bors = bor(exps)
# # print(bors)
# #print(allStats(bor1, bor2, althyp="two-sided"))
# print(allStats(bors))

# bor1 = [run[-1] for run in r1]
# bor2 = [run[-1] for run in r2]

# print(bor1)
# print(bor2)

# #print(allStats(bor1, bor2, althyp="two-sided"))
# print(allStats(bor1, bor2, althyp="less"))


# charts([
#     [ 
#         {'title': 'MUX-11', 'fs': [{'data':r1, 'color': '#6060ee', 'title': 'RTsTx', 'marker':'o'}, {'data':r2, 'color': '#dd6060', 'title':'RTsNTx', 'marker':'s'}] },
#         {'title': 'MUX-11', 'fs': [{'data':r1, 'color': '#6060ee', 'title': 'RTsTx', 'marker':'o'}, {'data':r2, 'color': '#dd6060', 'title':'RTsNTx', 'marker':'s'}] }
#     ],
#     [ 
#         {'title': 'MUX-11', 'fs': [{'data':r1, 'color': '#6060ee', 'title': 'RTsTx', 'marker':'o'}, {'data':r2, 'color': '#dd6060', 'title':'RTsNTx', 'marker':'s'}] },
#         {'title': 'MUX-11', 'fs': [{'data':r1, 'color': '#6060ee', 'title': 'RTsTx', 'marker':'o'}, {'data':r2, 'color': '#dd6060', 'title':'RTsNTx', 'marker':'s'}] }
#     ]
# ])

bor1 = [run[-1] for run in r1]
bor2 = [run[-1] for run in r2]

print(bor1)
print(bor2)

#print(allStats(bor1, bor2, althyp="two-sided"))
print(allStats(bor1, bor2, althyp="greater"))


bor1 = [run[-1] for run in r1]
bor2 = [run[-1] for run in r2]

print(bor1)
print(bor2)

#print(allStats(bor1, bor2, althyp="two-sided"))
print(allStats(bor1, bor2, althyp="less"))
# print(allStats(bor1, bor2, althyp="two-sided"))
