from multiprocessing import Process

import gym
import numpy
from aivle_gym.agent_env import AgentEnv
from aivle_gym.env_serializer import EnvSerializer
from aivle_gym.judge_env import JudgeEnv

from aivle_grader.evaluator import StepCountEvaluator
from aivle_grader.test_case import ReinforcementLearningTestCase
from aivle_grader.test_suite import TestSuite
from agent import CartPoleAgent


class CartPoleEnvSerializer(EnvSerializer):
    def action_to_json(self, action):
        return action

    def json_to_action(self, action_json):
        return action_json

    def observation_to_json(self, obs):
        return obs.tolist()

    def json_to_observation(self, obs_json):
        return numpy.array(obs_json)

    def info_to_json(self, info):
        return info

    def json_to_info(self, info_json):
        return info_json


class CartPoleJudgeEnv(JudgeEnv):
    def __init__(self):
        self.env = gym.make("CartPole-v0")
        super().__init__(
            CartPoleEnvSerializer(),
            self.env.action_space,
            self.env.observation_space,
            self.env.reward_range,
        )

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode="human"):
        return self.env.render(mode=mode)

    def close(self):
        self.env.close()

    def seed(self, seed=None):
        self.env.seed(seed)


class CartPoleAgentEnv(AgentEnv):
    def __init__(self):
        base_env = gym.make("CartPole-v0")
        super().__init__(
            CartPoleEnvSerializer(),
            base_env.action_space,
            base_env.observation_space,
            base_env.reward_range,
            uid=0,
        )  # uid can be any int for single-agent agent env


def create_agent(**kwargs):
    return CartPoleAgent()


def main():
    judge_env = CartPoleJudgeEnv()
    judge_proc = Process(target=judge_env.start, args=())
    judge_proc.start()
    try:
        n_runs = 10
        env = CartPoleAgentEnv()
        evaluator = StepCountEvaluator()
        seeds = [2333 for _ in range(n_runs)]
        test_case = ReinforcementLearningTestCase(
            t_max=10000,
            env=env,
            evaluator=evaluator,
            agent_init={},
            seeds=seeds,
            case_id=0,
            time_limit=3600,
            n_runs=n_runs,
        )
        test_suite = TestSuite(suite_id="cart_pole_test", cases=[test_case])
        res = test_suite.run(create_agent)
        print(res)
    finally:
        judge_proc.terminate()


if __name__ == "__main__":
    main()
