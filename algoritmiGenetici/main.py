import copy, random, math


#ret 1 random bit
def randomB():
    x = random.random()
    if x < 0.5:
        return 1
    return 0

#genereaza cromozom de lungime length
def genCrom(l):
    return [randomB() for y in range(l)]

#gen prima populatie
def genPop():
    pop = [genCrom(lCrom) for x in range(dimPop)]
    return pop

# functia fitnes e functia data
def fit(x):
    return x*x*x + 3*(x*x) - 4*x + 7

def convertBinToDec(cromozom):
    x = 0
    for b in cromozom:      #convert crom din binar in decimal
        x = (x << 1) | b
    return (domDef[1] - domDef[0]) / (pow(2, lCrom)) * x + domDef[0] #calc val crom pt domeniul dat

def getConvertedPopulation(populatie):
    return [fit(convertBinToDec(crom)) for crom in populatie]       #fitnes pt toti crom din pop=>lista pop

def printCromBinar(l):
    return "".join(map(str, l))


def printPop(populatie):
    if iteration == 1:
        for i in range(1, len(populatie)+1):
            x = convertBinToDec(populatie[i - 1])
            fout.write(str(i) + " : ")
            fout.write(printCromBinar(populatie[i - 1]) + ", x=")
            fout.write('{:f}, '.format(x))
            fout.write(str(fit(x)))
            fout.write('\n')
        fout.write('\n')
    return


def getProbabilitatiSelectie(populatie):
    l = []
    valPop = getConvertedPopulation(populatie)
    f = sum(valPop)
    for fX in valPop:
        l.append(fX / f)   #=p   unde fX=caz favorabil
    if iteration == 1:
        fout.write("Probabilitati selectie:\n")
        for i in range(1, dimPop + 1):
            fout.write("cromozom " + format(i, '2') + '-> probabilitate: ' + str(l[i - 1]) + '\n')
        fout.write("\n")
    return l


def getIntervaleSelectie(probSelectie):
    s = 0
    l = []
    for p in probSelectie:
        l.append(s)
        s += p                      #prob de selectie devin intervale de selectie
    l.append(1.0)

    if iteration == 1:
        fout.write("Intervale probabilitati selectie:\n")
        for j in l:
            fout.write(str(j) + ' ')
        fout.write("\n")
    return l


def selectie():
    suma_probabilitatilor = sum(crom[1] for crom in populatie)
    probabilitati_cumulate = 0
    for cromozom in populatie:          #calc prob de selectie fiecarui cromozom
        probabilitate = cromozom[1] / suma_probabilitatilor
        probabilitati_cumulate += probabilitate
        ips.append(probabilitati_cumulate)

    for _ in range(dimPop):
        u = random.random()  # Generăm un număr aleator uniform pe [0,1)
        interval_selectat = cautareBinara(ips, u)
        if iteration == 1:
            fout.write("u=" + str(u) + " selectam cromozomul " + str(interval_selectat) + "\n")
        populatie.append(populatie[interval_selectat])

    return populatie


def cautareBinara(l, x):
    st = 0
    dr = len(l) - 1
    while st <= dr:
        m = (st + dr) // 2
        if l[m] < x:
            st = m + 1
        elif l[m] > x:
            dr = m - 1
        else:
            return m
    return st


def getCrossoverPopulation(populatie, pRecombinare):
    l = []
    for i in range(1, dimPop + 1):    #pt fiecare crom avem sansa in [0,1] de recomb iar dc < p_recombinare il recombinam
        s = random.random()
        t = ""
        t += (str(i) + ": ")
        t += (printCromBinar(populatie[i - 1]) + ", u=")
        t += (str(s))
        if s < pRecombinare:
            l.append(i - 1)
            t += " < " + str(pRecombinare) + " =>participa"
        if iteration == 1:
            fout.write(t + '\n')
    return l


def crossover(population):

    while len(population) >= 2:
        parts = random.sample(population, 2) #2 crom folositi in trecut
        population.remove(parts[0])
        population.remove(parts[1])

        pRupere = random.randrange(0, lCrom)     #punct rupere aleator
        if iteration == 1:
            fout.write("\n")
            fout.write("Recombinare dintre cromozomul {0} cu cromozomul {1}:\n".format(parts[0] + 1, parts[1] + 1))
            fout.write("{0} {1} punct {2}\n".format(printCromBinar(new_pop[parts[0]]), printCromBinar(new_pop[parts[1]]),pRupere))

        comb1 = new_pop[parts[0]][:pRupere] + new_pop[parts[1]][pRupere:]           #obtin cele 2 combinatii dupa crossover
        comb2 = new_pop[parts[1]][:pRupere] + new_pop[parts[0]][pRupere:]

        if iteration == 1:
            fout.write("Rezultat: {0} {1}\n".format(printCromBinar(comb1), printCromBinar(comb2)))
        new_pop[parts[0]] = comb1
        new_pop[parts[1]] = comb2
    return


def mutatie():

    if iteration == 1:
        fout.write("Probabilitatea de mutatie pentru fiecare gena {0}. Au fost modificati cromozomii:\n".format(probMutatie))

    for i in range(dimPop - 1):
        u = random.random()
        if u < probMutatie:             #dc prob crom selectat e mai mic
            if iteration == 1:
                fout.write(str(i + 1) + '\n')
            poz = random.randrange(0, lCrom - 1)
            new_pop[i][poz] = abs(new_pop[poz][i] - 1)  #interschimbare val pt un bit random
    return


def getFittestCrom(populatie):             #crom cel mai fit
    iX = 0
    valMax = fit(convertBinToDec(populatie[0]))
    for i in range(len(populatie)):
        fX = fit(convertBinToDec(populatie[i]))
        if fX > valMax:
            iX = i
            valMax = fX
    return iX


def getNotFittestCrom(populatie):           #crom cel mai not fit
    iX = 0
    valMin = fit(convertBinToDec(populatie[0]))
    for i in range(len(populatie)):
        f_x = fit(convertBinToDec(populatie[i]))
        if valMin > f_x:
            iX = i
            valMin = f_x
    return iX


def critElitist():
    iFittestCrom = getFittestCrom(populatie)
    iNotFittestCrom = getNotFittestCrom(new_pop)

    new_pop[iNotFittestCrom] = copy.copy(populatie[iFittestCrom])       #inlocuim vechiul FittestCrom cu noul NotFittestCrom
    return

#MAIN

fout = open("output", "w")
with open("input") as fin:
    linii = fin.read().splitlines()

dimPop = int(linii[0])
domDef = [int(x) for x in linii[1].split()]
coefFunctie = [int(x) for x in linii[2].split()]
precizie = int(linii[3])
probRecombinare = float(linii[4])
probMutatie = float(linii[5])
nrEtape = int(linii[6])
iteration = 1

#lungimea cromozomului pt a retine (dr-st)*10^precizie subintervale
lCrom = math.floor(math.log((domDef[1] - domDef[0]) * (math.pow(10, precizie)), 2))

populatie = genPop()        #generam populatia de cromozomi

if iteration == 1:
    fout.write("Populatia initiala:\n")
    printPop(populatie)

while iteration <= nrEtape:

    ps = getProbabilitatiSelectie(populatie)        #prob de selectie pt fiecare cromozom
    ips = getIntervaleSelectie(ps)                  #intervale prob selectie
    new_pop = selectie()                            #generare pop nou

    if iteration == 1:
        fout.write("\nDupa selectie:\n")
        printPop(new_pop)

    crossoverList = getCrossoverPopulation(new_pop, probRecombinare)
    crossover(crossoverList)              #incrucisare/crossover pe lista cromozomilor selectati

    if iteration == 1:
        fout.write("\nDupa recombinare:\n")
        printPop(new_pop)                        #dupa recombinare

    mutatie()
    if iteration == 1:
        fout.write("Dupa mutatie: \n")
        printPop(new_pop)                    #mutatie

    critElitist()                    #crit elitist:inlocuiesc cel mai bun cromozom din pop initiala cu cel mai prost din populatia noua

    if iteration == 1:
        fout.write("Dupa aplicarea criteriului elitist: \n")
        printPop(new_pop)

    #valoarea maxima
    #functia pt ind max pe pop noua, transf in baza 10 + fitness
    if iteration == 1:
        fout.write("Evolutia maximului: \n")
    fout.write(str(convertBinToDec(new_pop[getFittestCrom(new_pop)])) + ' ' + str(fit(convertBinToDec(new_pop[getFittestCrom(new_pop)]))))

    iteration += 1          #next iteration
    populatie = copy.deepcopy(new_pop)

