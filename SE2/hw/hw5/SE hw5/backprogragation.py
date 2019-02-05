# -*- coding: utf-8 -*-
import math
import random

random.seed(0)

def sigmoid(x):
    """
    sigmoid :1/(1+e^-x)
    """
    return 1.0 / (1.0 + math.exp(-x))

def dsigmoid(y):
    """
    derivative of sigmoid 
    """
    return y * (1 - y)

def rand(x, y):
    return (y - x) * random.random() + x

def generateMatrix(I, J):
    a = []
    for j in range(I):
        a.append([0.0] * J)
    return a

def randomizeMatrix(matrix, x, y):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = random.uniform(x, y)

class neural_network:
    def __init__(self, ni, nh, no):
        """
        :param ni:number of input nodes
        :param nh:number of hidden nodes
        :param no:number of output nodes
        """
        self.ni = ni + 1  # +1 for offset node
        self.nh = nh       
        self.no = no
        
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no

        self.wi = generateMatrix(self.ni, self.nh)  # input layers to hidden layers weights
        self.wo = generateMatrix(self.nh, self.no)  # hidden layers to output layers weights
    
        randomizeMatrix(self.wi, -1, 1)
        randomizeMatrix(self.wo, -1, 1)
        
        print' '
        print'Initial weights:'
        print'(input layers to hidden layers weights:)'
        for i in range(self.ni):
            if i==self.nh:
                print self.wi[i],'(Offset node)'
            else:                    
                print self.wi[i]
        print'(hidden layers to output layers weights:)'
        for j in range(self.nh):                 
            print self.wo[j]
        print ' '  
    
        self.ci = generateMatrix(self.ni, self.nh)
        self.co = generateMatrix(self.nh, self.no)

  
    def run(self, inputs):
        if len(inputs) != self.ni - 1:
            print 'incorrect number of inputs'

        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]

        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum += ( self.ai[i] * self.wi[i][j] )
            self.ah[j] = sigmoid(sum)

        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum += ( self.ah[j] * self.wo[j][k] )
            self.ao[k] = sigmoid(sum)

        return self.ao
    
    def backPropagate(self, targets, N, M):
        # calculate deltas in output layers
        # dE/dw[j][k] = (t[k] - ao[k]) * s'( SUM( w[j][k]*ah[j] ) ) * ah[j]
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = error * dsigmoid(self.ao[k])

        # update weights in output layers
        for j in range(self.nh):
            for k in range(self.no):
                # output_deltas[k] * self.ah[j] is dError/dweight[j][k]
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += N * change + M * self.co[j][k]
                self.co[j][k] = change

        # calculate deltas in hidden layers
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = error * dsigmoid(self.ah[j])

        # update weights in input layers
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                # print 'activation',self.ai[i],'synapse',i,j,'change',change
                self.wi[i][j] += N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        # Calculate the sum of squares of error.
        error = 0.0
        for k in range(len(targets)):
            error = 0.5 * (targets[k] - self.ao[k]) ** 2
        return error
    def final_weights(self):
        print' '
        print 'Final weights:'
        print '(input layers to hidden layers weights:)'
        for i in range(self.ni):
            if i==self.nh:
                print self.wi[i],'(Offset node)'
            else:                    
                print self.wi[i]
        print '(hidden layers to output layers weights:)'
        for j in range(self.nh):                 
            print self.wo[j]
        print ''
            
    def train(self, training_set,N,target_error,max_iterations=1000,M=0.5):
        """
        :param training_set:tranining set
        :param max_iterations:max number of iterations
        :param N:learning rate
        :param M:learning for last time (algorithm optimization)
        :param target_error
        """
        M=N / 2
        for i in range(max_iterations):
            for p in training_set:
                inputs = p[0]
                targets = p[1]
                self.run(inputs)
                error = self.backPropagate(targets, N, M)
            if i==0:
                print 'The first-batch error      --> ', error
            if i==max_iterations-1:
                    print 'Can not achieve the target error:',target_error,', please change the learning rate.'
                    return 0;
            if error<target_error:
                print 'The final error            --> ', error,'<',target_error
                print' '
                print 'Total number of batches run through in training is:',i+1,'times.'
                break


def main():
    training_set = [[[0, 0], [0]], [[0, 1], [1]],[[1, 0], [1]],[[1, 1], [0]]]
    target_error = float(raw_input('Please input a float target_error:'))   
    learning_rate = float(raw_input('Please input a float learning_rate:'))
    nn = neural_network(2, 2, 1)
    if nn.train(training_set,learning_rate,target_error)!=0:
       nn.final_weights()

if __name__ == "__main__":
    main()