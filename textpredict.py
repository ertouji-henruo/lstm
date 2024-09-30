import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras import optimizers
import sys
filename = "shakespeare.txt"
f = open(filename, "r", encoding="utf-8").read()
f = f.lower()
chars = sorted(list(set(f)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
n_chars = len(f)
n_vocab = len(chars)
sequence_length = 200
datX = []
daty = []
for i in range(0, n_chars - sequence_length, 1):
    seq_in = f[i:i + sequence_length]
    seq_out = f[i + sequence_length]
    datX.append([char_to_int[char] for char in seq_in])
    daty.append(char_to_int[seq_out])
n_patterns = len(datX)
X = np.reshape(datX, (n_patterns, sequence_length, 1))
y = np_utils.to_categorical(daty)
X = X / float(n_vocab)
print(np.shape(X))
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy")
filepath="weights-biggerimprovement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
#model.fit(X, y, epochs=500, batch_size=64, callbacks=callbacks_list)
filename = "weights-shakespeare-improvement-59-1.4429.hdf5"
model.load_weights(filename)
#model.fit(X, y, epochs=200, batch_size=64, callbacks=callbacks_list)
start = np.random.randint(0, len(datX) - 1)
pattern = datX[start]
print("Seed:")
print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
#generate characters
for i in range(1000):
    x = np.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = np.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
print("\nDone.")