import yaml
import os
import json
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

# Reading the data

data = yaml.safe_load(open('nlu\\train.yml').read())

inputs, outputs = [], []

for command in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append('{}\\{}'.format(command['entity'], command ['action']))

# Create a dataset
# Choose a level of tokenization: byte-level



# Create input data

max_sent = max([len(x) for x in inputs])

# Create arrays one-hot encoding (number of examples, sequence length, vocab_size)
input_data = np.zeros((len(inputs), max_sent, 256), dtype='float32')

for i, inp in enumerate(inputs):
    for k, ch in enumerate(bytes(inp.encode('utf-8'))):
        input_data[i, k,int(ch)]  = 1.0

#output_data = to_categorical(output_data, len(output_data))

#print(input_data.shape)

print(input_data[0].shape)

#print(len(chars))
#print('Max input seq:', max_sent)

labels = set(outputs)

label2idx = {}
idx2label = {}

for k, label in enumerate(labels):
    label2idx[label] = k
    idx2label[k] = label

output_data = []

for output in outputs:
    output_data.append(label2idx[output])

print(output_data)
