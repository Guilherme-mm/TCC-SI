import functions
import random
import functools

userMap = dict()
removedReviews = dict()
removedUser = dict()

dataFile = open('user_ratedmovies.dat', 'r')
# Total de Linhas que precisam ser Removidas
testReviewsCount = 171118 #Aprox. 20%
processedTestReviews = 0
testsVariation = list()


#### Preparando os Dados
# Para Cada Linha
for line in dataFile:  
    lineArray = line.split()
    
    # Pulando a linha de cabecalho
    if line[0].startswith('u') :
        continue

    #Aleatoriamente ignorando linhas do arquivo para serem usadas como teste:
    if bool(random.getrandbits(1)) and processedTestReviews <= testReviewsCount:
        removedReviews[lineArray[0]] = {"film":lineArray[1], "score":lineArray[2]}
        processedTestReviews = processedTestReviews + 1
        continue

    # Remove uma review de cada usuario    
    # if not lineArray[0] in removedUser:
    #     removedReviews[lineArray[0]] = {"film":lineArray[1], "score":lineArray[2]}
    #     removedUser[lineArray[0]] = True
    #     continue

    # Se o usuario nao estiver no mapa de usuarios, adiciona
    if not lineArray[0] in userMap:
        userMap[lineArray[0]] = {}
    
    # Adiciona a nota no objeto de notas
    userMap[lineArray[0]][lineArray[1]] = lineArray[2]
    
# Para cada linha de testes compara o score suposto com o real
for userID, reviewData in removedReviews.items():
    trueScore = float(reviewData["score"])
    supposedScore = 0
    recomendations = functions.getRecommendations(userMap, userID)

    for recomendation in recomendations:
        if reviewData["film"] == recomendation[1]:
            supposedScore = float(recomendation[0])
            break

    variation = abs((supposedScore - trueScore)/trueScore * 100)
    testsVariation.append(variation)

print(functools.reduce(lambda x, y: x + y, testsVariation) / len(testsVariation))
