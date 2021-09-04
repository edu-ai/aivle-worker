import gym

from aivle_grader.abc.agent import Agent


class CartPoleAgent(Agent):
    def step(self, state):
        return gym.spaces.Discrete(2).sample()

    def reset(self):
        pass
