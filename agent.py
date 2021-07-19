import numpy as np
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import Dense,Conv2D,Dropout,Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from collections import deque
import random
import os

class DQNAgent:

    def __init__(self,state_size,action_size,action_space):

        self.model_name = "mazemodel.h5"
        self.model_name2 = "targetmazemodel.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.action_space = action_space
        self.start = 1000
        self.steps = 1
        self.dir = ["left",'right','down','up']
        self.learning_rate = 0.001
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.998
        self.batch_size = 64
        # self.brain = tf.keras.models.load_model("./model/" + self.model_name)
        # self.target_brain = tf.keras.models.load_model("./model/" + self.model_name2)
        self.brain = self.build_model()
        self.target_brain = self.build_model()
        self.update_target_brain()


        self.memory = deque()
        self.memory_size = 100000

    def build_model(self):
        self.model = Sequential()

        self.model.add(Conv2D(32, (3, 3), input_shape= self.state_size,activation='relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Conv2D(32, (3, 3),activation='relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Flatten())
        self.model.add(Dense(256, activation='relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(self.action_size))
        self.model.summary()
        self.model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))

        return self.model

    def update_target_brain(self):
        self.target_brain.set_weights(self.brain.get_weights())

    def get_act(self,state):

        if np.random.rand() <= self.epsilon:
            rand_axis = random.randrange(self.action_size)
            print("agent.py>>DQNAgent>>get_act>> " + self.dir[rand_axis])
            return rand_axis

        print("agent.py>>DQNAgent>>get_act>> using greed now")
        state = np.resize(state,(1,81,81,1))
        action_predict = self.brain.predict(np.asarray(state))
        model_action = np.argmax(action_predict[0])

        print("agent.py>>DQNAgent>>get_act>> " + self.dir[model_action])
        return model_action

    def add_memory(self,state, action, reward, next_state, done):

        self.memory.append((state, action, reward, next_state, done))
        if (len(self.memory) > self.memory_size):
            print("agent.py>>DQNAgent>>add_memory>> memory full now, pop left")
            self.memory.popleft()

    def train(self):
        if(len(self.memory) > self.start and self.steps % 2 == 0):

            print("agent.py>>DQNAgent>>replay>> model fit setup")

            sample = random.sample(self.memory,self.batch_size)
            states = np.asarray([idx[0] for idx in sample])
            next_states = np.asarray([idx[3] for idx in sample])
            next_q_values = self.target_brain.predict_on_batch(next_states)
            current_q_values = self.brain.predict_on_batch(states)

            for i in range(self.batch_size):
                _, action, reward, _, done = sample[i]


                if not done:
                    next_q_value = reward + self.gamma * np.amax(next_q_values[i])
                else:
                    next_q_value = reward

                current_q_values[i,action] = next_q_value

            print("agent.py>>DQNAgent>>replay>> model fit start")
            self.brain.fit(states, current_q_values,batch_size=self.batch_size ,epochs=1, verbose=0,shuffle=False)
            print("agent.py>>DQNAgent>>replay>> model fit fin")





    def epsilon_update(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            print("agent.py>>DQNAgent>>replay>> epsilon update (to "+str(self.epsilon)+")")


    def save_model(self):
        if not os.path.exists("./model"):
            os.mkdir("./model")
        self.brain.save( "./model/"+self.model_name)
        self.target_brain.save( "./model/target"+self.model_name)



class DQNPlayAgent:

    def __init__(self,state_size,action_size,action_space):

        self.model_name = "mazemodel.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.action_space = action_space
        self.steps = 1
        self.dir = ["left", 'right', 'down', 'up']
        self.brain = self.load_model()


    def get_act(self,state):

        print("agent.py>>DQNAgent>>get_act>> using greed now")
        state = np.resize(state, (1, 81, 81, 1))
        action_predict = self.brain.predict(np.asarray(state))
        model_action = np.argmax(action_predict[0])

        print("agent.py>>DQNAgent>>get_act>> " + self.dir[model_action])
        return model_action


    def load_model(self):
        if not os.path.exists("./model"):
            os.mkdir("./model")
        brain = tf.keras.models.load_model( "./model/"+self.model_name)

        return brain








