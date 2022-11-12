import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt

# Parameters.
learning_rate = 0.1
training_steps = 1000
display_step = 100
n_samples = 50

X = np.random.rand(n_samples).astype(np.float32)
Y = X * 10 + 5

W = tf.Variable(tf.random.normal([1]))
b = tf.Variable(tf.zeros([1]))

# Linear regression (Wx + b).
def linear_regression(x):
    return W * x + b

# Mean square error.
def mean_square(y_pred, y_true):
    return tf.reduce_sum(tf.pow(y_pred-y_true, 2)) / ( n_samples)

# Stochastic Gradient Descent Optimizer.
optimizer = tf.optimizers.SGD(learning_rate)

# Optimization process. 
def run_optimization():
    # Wrap computation inside a GradientTape for automatic differentiation.
    with tf.GradientTape() as g:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)

    # Compute gradients.
    gradients = g.gradient(loss, [W, b])
    
    # Update W and b following gradients.
    optimizer.apply_gradients(zip(gradients, [W, b]))

# Run training for the given number of steps.
for step in range(1, training_steps + 1):
    # Run the optimization to update W and b values.
    run_optimization()
    
    if step % display_step == 0:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)
        print("step: %i, loss: %f, W: %f, b: %f" % (step, loss, W.numpy(), b.numpy()))


# Graphic display
plt.plot(X, Y, 'ro', label='Original data')
plt.plot(X, linear_regression(X), label='Fitted line')
plt.legend()
plt.savefig(fname="test.png")