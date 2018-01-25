# Reference MorvanPython

# Classify three types of num list

from __future__ import print_function
import tensorflow as tf
import random
import numpy as np

def generate_type1(num):
    return [random.uniform(0,1) if random.randint(0,1) == 0 and i % 2 == 0 else 0 for i in range(num)]

def generate_type2(num):
    return [random.uniform(0,1) if random.randint(0,1) == 0 and i % 3 == 0 else 0 for i in range(num)]

def generate_type3(num):
    return [random.uniform(0,1) if random.randint(0,1) == 0 and i % 4 == 0 else 0 for i in range(num)]

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

INPUT_SIZE = 200
OUTPUT_SIZE = 3

xs = tf.placeholder(tf.float32, [None, INPUT_SIZE])
ys = tf.placeholder(tf.float32, [None, OUTPUT_SIZE])

# add output layer
prediction = add_layer(xs, INPUT_SIZE, OUTPUT_SIZE,  activation_function=tf.nn.softmax)

# the error between prediction and real data
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                              reduction_indices=[1]))       # loss
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init)

TRAIN_SIZE = 200
train_x1 = np.asarray([generate_type1(INPUT_SIZE) for _ in range(TRAIN_SIZE)])
train_x2 = np.asarray([generate_type2(INPUT_SIZE) for _ in range(TRAIN_SIZE)])
train_x3 = np.asarray([generate_type3(INPUT_SIZE) for _ in range(TRAIN_SIZE)])
train_y1 = np.asarray([[1,0,0] for _ in range(TRAIN_SIZE)])
train_y2 = np.asarray([[0,1,0] for _ in range(TRAIN_SIZE)])
train_y3 = np.asarray([[0,0,1] for _ in range(TRAIN_SIZE)])


test_x1 = np.asarray([generate_type1(INPUT_SIZE) for _ in range(TRAIN_SIZE)])
test_x2 = np.asarray([generate_type2(INPUT_SIZE) for _ in range(TRAIN_SIZE)])
test_x3 = np.asarray([generate_type3(INPUT_SIZE) for _ in range(TRAIN_SIZE)])
test_y1 = np.asarray([[1,0,0] for _ in range(TRAIN_SIZE)])
test_y2 = np.asarray([[0,1,0] for _ in range(TRAIN_SIZE)])
test_y3 = np.asarray([[0,0,1] for _ in range(TRAIN_SIZE)])

print("type1:", generate_type1(40))
print("type2:", generate_type2(40))
print("type3:", generate_type3(40))

for i in range(20):
    sess.run(train_step, feed_dict={xs: train_x1, ys: train_y1})
    sess.run(train_step, feed_dict={xs: train_x2, ys: train_y2})
    sess.run(train_step, feed_dict={xs: train_x3, ys: train_y3})
    print("*****",i+1,"*****")
    print(compute_accuracy(test_x1, test_y1))
    print(compute_accuracy(test_x2, test_y2))
    print(compute_accuracy(test_x3, test_y3))


"""
for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
    if i % 50 == 0:
        print(compute_accuracy(
            mnist.test.images, mnist.test.labels))
"""
