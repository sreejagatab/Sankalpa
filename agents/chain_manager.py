class ChainManager:
    def __init__(self, agent_chain: list, memory):
        self.agent_chain = agent_chain
        self.memory = memory

    def run(self, input_data):
        result = input_data
        for agent in self.agent_chain:
            result = agent.run(result)
            self.memory.save(agent.name, result)
        return result
