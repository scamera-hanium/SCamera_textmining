# -*- coding: utf-8 -*

import sys
sys.path.insert(0, '/Users/davichiar/Documents/ADDAVICHI/Python/Sentimental-Analysis-master/Bidirectional_LSTM')

import os
import tensorflow as tf
import Bi_LSTM
import Word2Vec
import gensim
import numpy as np

W2V = Word2Vec.Word2Vec()

Batch_size = 1
Vector_size = 300
Maxseq_length = 2600
learning_rate = 0.001
lstm_units = 128
num_class = 2
keep_prob = 1.0

X = tf.placeholder(tf.float32, shape = [None, Maxseq_length, Vector_size], name = 'X')
Y = tf.placeholder(tf.float32, shape = [None, num_class], name = 'Y')
seq_len = tf.placeholder(tf.int32, shape = [None])

BiLSTM = Bi_LSTM.Bi_LSTM(lstm_units, num_class, keep_prob)

with tf.variable_scope("loss", reuse = tf.AUTO_REUSE):
    logits = BiLSTM.logits(X, BiLSTM.W, BiLSTM.b, seq_len)
    loss, optimizer = BiLSTM.model_build(logits, Y, learning_rate)

prediction = tf.nn.softmax(logits)

os.chdir("/Users/davichiar/Documents/ADDAVICHI/Python/Sentimental-Analysis-master/Bidirectional_LSTM")

def Convert2Vec(model_name, sentence):
    word_vec = []
    sub = []
    model = gensim.models.word2vec.Word2Vec.load(model_name)
    for word in sentence:
        if(word in model.wv.vocab):
            sub.append(model.wv[word])
        else:
            sub.append(np.random.uniform(-0.25,0.25,300)) ## used for OOV words
    word_vec.append(sub)
    return word_vec

saver = tf.train.Saver()
init = tf.global_variables_initializer()
modelName = "./BiLSTM_model.ckpt"

sess = tf.Session()
sess.run(init)
saver.restore(sess, modelName)

os.chdir("..")

def Grade(sentence):
    tokens = W2V.tokenize(sentence)
    
    embedding = Convert2Vec('./Word2Vec/Word2vec.model', tokens)
    zero_pad = W2V.Zero_padding(embedding, Batch_size, Maxseq_length, Vector_size)
    global sess
    result =  sess.run(tf.argmax(prediction,1), feed_dict = {X: zero_pad , seq_len: [len(tokens)] } ) 
    if(result == 1):
        return '긍정'
    else:
        return '부정'
            

    
