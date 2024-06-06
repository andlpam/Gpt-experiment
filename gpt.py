import sqlite3
import itertools
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

#CONSTANTES
DATA_BASE = 'gpt.db'
CPU = 'cpu'
CUDA = 'cuda:0'
ONLY_VID_TEXT = "SELECT vidText FROM Videos"
BINARY_FIT_SIZE = 13

#CREATE THE DATABASE AND READ DATA FROM THEM
connection = sqlite3.connect(DATA_BASE)
cursor = connection.cursor()
cursor.execute(ONLY_VID_TEXT)
text = ''
for vidtext in cursor:
  text += vidtext[0]


#SETUP THE DEVICE
device = torch.device(CUDA if torch.cuda.is_available() else CPU)

#GET TOUPLES INDEX
chars = sorted(list(set(text)))
textL = list(text)
combChars,tks = [], []
for ch1 in zip(chars):
  for ch2 in zip(chars):
        combChars.append(ch1+ch2)
for l1, l2 in zip(textL, textL[1:]):
  tks.append((l1,l2))

#BINARY ENCODING n=12  #transform tks in indexes and after we transform in binary(could be more efficient) #s-i-b
stoi = {s:i for i,s in enumerate(combChars)}
itos = {i:s for i,s in enumerate(combChars)}
binaryDict = list(itertools.product([0, 1], repeat= BINARY_FIT_SIZE)) 
itob = {}

for chs in combChars:
  i = stoi[chs]
  itob[i] = binaryDict[i]
btoi = {b:i for i,b in itob.items()}
encode = lambda tks: [itob[stoi[tk]] for tk in tks]
decode = lambda binN: [itos[btoi[bn]] for bn in binN]
data = torch.tensor(encode(tks), dtype=torch.long)

print(data[0][:10])



