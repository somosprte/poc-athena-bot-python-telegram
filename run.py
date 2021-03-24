import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer

intensao = []
frases = []
f = open("intensoes.txt", "r") 

for x in f:
	classe, texto = x.split(">>") 
	intensao.append(classe)
	frases.append(texto.rstrip()) #rstrip remove o \n

#Converte as sentenças em BOW
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,strip_accents='unicode')
intensaoBow = vectorizer.fit_transform(frases)

intensaoNumpy = np.array(intensao)
leaveOneOut = LeaveOneOut()
leaveOneOut.get_n_splits(intensaoBow)

result = []

for train_index, test_index in leaveOneOut.split(intensaoBow):
  X_train, X_test = intensaoBow[train_index], intensaoBow[test_index]
  y_train, y_test = intensaoNumpy[train_index], intensaoNumpy[test_index]
  
  #KNN
  model = KNeighborsClassifier(n_neighbors=1)
  model.fit(X_train,y_train)
  
  resultado = model.predict(X_test)[0]
  result.append(resultado) 

import telepot
apikey = "1765992736:AAFJGuA668ycHfIwC_LSQfEUjqIopggp7iY"
tele = telepot.Bot(apikey)

def responder(userId, username, intensao):

  if intensao == 'saudacao':
    tele.sendMessage(userId, "Olá, "+username+"!")

  elif intensao == 'despedida':
    tele.sendMessage(userId, "Até mais, "+username)

  elif intensao == 'ajuda':
    tele.sendMessage(userId, "No que eu posso te ajudar?")

  elif intensao == 'agradecimento':
    tele.sendMessage(userId, "De nada! Se precisar estamos aí o/")

  elif intensao == 'agendaDoDia':
    tele.sendMessage(userId, "Essa é sua agenda do dia")

  elif intensao == 'agendaSemanal':
    tele.sendMessage(userId, "Essa é sua agenda da semana")

  elif intensao == 'agendaMensal':
    tele.sendMessage(userId, "Essa é sua agenda do mês")

  elif intensao == 'happyHour':
    tele.sendMessage(userId, "Será sexta-feira, 26/03, às 16:30hs. #Sextou")

  else:
    tele.sendMessage(userId, "Sinto mt,"+username+". Não entendi o que vc disse. Me explica de outra forma")

def receberMensagem(msg):
  inst = vectorizer.transform([msg['text']])
  intensao = model.predict(inst)
  responder(msg['from']['id'], msg['from']['first_name'], intensao[0])

tele.message_loop(receberMensagem)

while True:
  pass
