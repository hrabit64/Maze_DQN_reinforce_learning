import environment
import agent


class train_sys:
    def __init__(self):
        self.episodes = 30000
        self.env = environment.Env(render_speed=0.05)
        self.env.reset(0)
        self.state = self.env.get_state()
        self.state_size = self.state.shape
        self.action_size = self.env.action_size
        self.action_space = self.env.action_space
        self.Agent = agent.DQNAgent(state_size=self.state_size,action_size=self.action_size,action_space=self.action_space)
        self.reward = 0
        self.end_count = 0
    def run(self):
        for epi in range(self.episodes):
            done = False
            self.reward = 0
            self.Agent.steps = 1
            while not done:

                action = self.Agent.get_act(self.state)

                print("log>> agent "+str(action)+" "+str(self.env.reward)+" "+str(self.Agent.steps))
                next_state,self.reward,done= self.env.step(action)
                self.Agent.add_memory(self.state, action, self.reward, next_state, done)
                self.Agent.train()
                self.state = next_state
                self.Agent.steps = self.env.steps
                if(self.Agent.steps > 500):
                    print("log>> over 500 step, break now!")
                    break

            print("Episode >> " +str(epi)+" reward("+str(self.env.reward)+")")

            self.Agent.update_target_brain()
            self.Agent.epsilon_update()

            if(self.Agent.steps <= 15 and self.Agent.epsilon == self.Agent.epsilon_min):
                self.end_count += 1
                print("Agent get count"+str(self.end_count))
            if(self.end_count > 6):
                self.Agent.save_model()
                print("Agent find nice way now, stop")
                break

            self.env.reset(epi+1)
            if (epi % 5 == 0):
                #모델 저장
                self.Agent.save_model()


class test_sys:
    def __init__(self):
        self.env = environment.Env(render_speed=0.5)
        self.env.reset(0)
        self.state = self.env.get_state()
        self.state_size = self.state.shape
        self.action_size = self.env.action_size
        self.action_space = self.env.action_space
        self.Agent = agent.DQNPlayAgent(state_size=self.state_size,action_size=self.action_size,action_space=self.action_space)
        self.reward = 0

    def run(self):
        done = False
        self.reward = 0
        self.Agent.steps = 1
        while not done:

            action = self.Agent.get_act(self.state)

            print("log>> agent "+str(action)+" "+str(self.env.reward)+" "+str(self.Agent.steps))
            next_state,self.reward,done= self.env.step(action)
            self.state = next_state
            self.Agent.steps = self.env.steps

            print("Episode >> reward("+str(self.env.reward)+")")



if(__name__ == "__main__"):
    # train = train_sys()
    # _ = input("press any key to start")
    # train.run()
    test = test_sys()
    test.run()


