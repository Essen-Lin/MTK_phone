import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt
import csv

class LinearRegression():

    def __init__(self, learning_rate = 0.1, epochs = 1000, display_step = 100, 
                 n_samples = 50, input_numbers = 2, X = 0, Y = 0):
        # Parameters.
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.display_step = display_step
        self.n_samples = n_samples
        # Number of Input X (PMU counts)
        self.input_numbers = input_numbers

        # self.X = np.random.rand(n_samples,input_numbers).astype(np.float32)
        # self.Y = tf.add(tf.matmul(self.X, np.array([[10],[5]])), 5)
        self.X = X
        self.Y = Y
        self.W = tf.Variable(tf.random.normal([input_numbers,1]))
        self.b = tf.Variable(tf.zeros([1]))

        # Stochastic Gradient Descent Optimizer.
        self.optimizer = tf.optimizers.SGD(self.learning_rate)

    # Linear regression (Wx + b).
    def linear_regression(self, x):
        return tf.add(tf.matmul(x, self.W), self.b)

    # Mean square error.
    def mean_square(self, y_pred, y_true):


        return tf.reduce_sum(tf.pow(y_pred-y_true, 2)) / ( self.n_samples)

    # Optimization process. 
    def run_optimization(self):
        # "Forward Propagation"
        # Wrap computation inside a GradientTape for automatic differentiation.
        with tf.GradientTape() as g:
            pred = self.linear_regression(self.X)
            # "Loss Estimation"
            loss = self.mean_square(pred, self.Y)
        
        # "Backward Propagation"
        # Compute gradients.
        gradients = g.gradient(loss, [self.W, self.b])
        # Update W and b following gradients.
        self.optimizer.apply_gradients(zip(gradients, [self.W, self.b]))

    def run(self):
        # Run training for the given number of steps.
        for step in range(1, self.epochs + 1):
            # Run the optimization to update W and b values.
            self.run_optimization()
            
            if step % self.display_step == 0:
                pred = self.linear_regression(self.X)
                loss = self.mean_square(pred, self.Y)

                print("step: %i, loss: %.10f," % (step, loss) ,"W:", self.W.numpy().ravel(), ", b:", self.b.numpy())

# with open('test2.csv', newline='') as csvfile:
#     rows = csv.DictReader(csvfile)
#     frequency = []
#     count = []
#     time = []

#     for row in rows:
#         if row['event'] == 'raw-br-immed-spec':
#             print(row)
#             frequency.append(float(row['frequency']))
#             count.append(float(row['count'].replace(',','')))
#             time.append(float(row['time']))

#     # Normalization
#     layer = tf.keras.layers.Normalization(axis=None)
#     layer.adapt(frequency)
#     frequency = layer(frequency)
#     layer.adapt(count)
#     count = layer(count)
#     X = tf.transpose([frequency, count])
#     #X = tf.transpose([frequency,count])

#     #layer.adapt(time)
#     #Y = tf.transpose([layer(time)])
#     Y = tf.transpose([time])
#     print(X)
#     print(Y)

#     LinearRegression(X=X, Y=Y, n_samples =6, input_numbers = 2, epochs = 1000).run()


with open('test2.csv', newline='') as csvfile:
    rows = csv.DictReader(csvfile)
    frequency = []
    count = []
    time = []

    for row in rows:
        if row['setup core'] == '0' and row['frequency'] == '300000':
            #print(row)
            count.append(float(row['count'].replace(',','')))
            time.append(float(row['time']))

    # Normalization
    layer = tf.keras.layers.Normalization(axis=None)
    layer.adapt(count)
    count = layer(count)
    X = tf.Variable([count])

    Y=tf.reduce_mean(time)
    print(X)
    print(Y)

    LinearRegression(X=X, Y=Y, n_samples =1, input_numbers = 150, epochs = 100, display_step = 10).run()