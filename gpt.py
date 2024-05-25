import itertools
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

with open("file.txt", 'r', encoding='utf-8') as file:
  text = file.read()
#SETUP THE DEVICE
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

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
binaryDict = list(itertools.product([0, 1], repeat=12))
itob = {}
for chs in combChars:
  i = stoi[chs]
  itob[i] = binaryDict[i]
btoi = {b:i for i,b in itob.items()}
encode = lambda tks: [itob[stoi[tk]] for tk in tks]
decode = lambda binN: [itos[btoi[bn]] for bn in binN]
data = torch.tensor(encode(tks), dtype=torch.long)

