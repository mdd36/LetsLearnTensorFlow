from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import image.recoginition.data_helpers as data_helpers

batch_size = 100
learning_rate = 0.005
max_steps = 1000

data_sets = data_helpers.load_data()

images_placeholder = tf.placeholder(tf.float32, shape=[None, 3072])
labels_placeholder = tf.placeholder(tf.int64, shape=[None])

weights = tf.Variable(tf.zeros([3072, 10]))
biases = tf.Variable(tf.zeros([10]))

logits = tf.matmul(images_placeholder, weights) + biases

loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels_placeholder))

train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

correct_prediction = tf.equal(tf.argmax(logits, 1), labels_placeholder)

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(max_steps):
        indices = np.random.choice(data_sets['images_train'].shape[0], batch_size)
        image_batch = data_sets['images_train'][indices]
        labels_batch = data_sets['labels_train'][indices]

        sess.run(train_step, feed_dict={
            images_placeholder: image_batch,
            labels_placeholder: labels_batch
        })

        if i % 100 == 0:
            train_accuracy = sess.run(accuracy,feed_dict={
                images_placeholder: image_batch,
                labels_placeholder: labels_batch
            })
            print("Training Step {:5d}: The model is now {:g}% accurate".format(i, train_accuracy * 100))

    test_accuracy = sess.run(accuracy, feed_dict={
        images_placeholder: data_sets['images_test'],
        labels_placeholder: data_sets['labels_test']
    })

    print("Final Test: The model is now {:g}% accurate".format(test_accuracy * 100))