# Reference MorvanPython

# Classify 2 types of wave

from __future__ import print_function
import tensorflow as tf
import random
import numpy as np
from scipy.fftpack import fft

time = np.linspace(0, 20, 80000)

noise1 = np.random.normal(0, 1, time.shape)
pure_wave1 = np.cos(4.25*np.pi*time) + np.cos(7.75*np.pi*time)
wave1 = pure_wave1 + noise1
label1 = np.asarray([1, 0]);

noise2 = np.random.normal(0, 1, time.shape)
pure_wave2 = np.cos(4*np.pi*time) + np.cos(8*np.pi*time)
wave2 = pure_wave2 + noise2
label2 = np.asarray([0, 1]);

train_noise1 = np.random.normal(0, 1, time.shape)
train_wave1 = pure_wave1 + train_noise1
train_noise2 = np.random.normal(0, 1, time.shape)
train_wave2 = pure_wave2 + train_noise2

INPUT_SIZE = 4000

def add_layer(inputs, in_size, out_size, activation_function=None,):
    # add one more layer and return the output of this layer
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1,)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b,)
    return outputs

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result

def fft_x(wave):
    return np.abs(fft(wave))

def next_batch(wave, label, width=INPUT_SIZE, batch_size=200):
    global index
    if index >= 80000-width-batch_size:
        index = 0
    old_index = index
    index += batch_size
    return np.asarray([fft_x(wave[i:i+width]) for i in range(old_index,index)])/2000, np.asarray(np.tile(label,(batch_size,1)))

def get_train_batch(wave, label, width=INPUT_SIZE, batch_size=200):
    return np.asarray([fft_x(wave[i:i+width]) for i in range(0, batch_size*100, 100)])/2000, np.asarray(np.tile(label,(batch_size,1)))


# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, INPUT_SIZE]) # 28x28
ys = tf.placeholder(tf.float32, [None, 2])

# add output layer
prediction = add_layer(xs, INPUT_SIZE, 2, activation_function=tf.nn.softmax)

# the error between prediction and real data
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                              reduction_indices=[1]))       # loss
train_step = tf.train.GradientDescentOptimizer(0.9).minimize(cross_entropy)

sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init)

index = 0
for i in range(3000):
    batch_xs, batch_ys = next_batch(wave1, label1)
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
    batch_xs, batch_ys = next_batch(wave2, label2)
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
    if i % 1 == 0:
        x1, y1 = get_train_batch(train_wave1, label1)
        x2, y2 = get_train_batch(train_wave2, label2)
        v_xs = np.concatenate((x1, x2))
        v_ys = np.concatenate((y1, y2))
        print(compute_accuracy(v_xs, v_ys))
