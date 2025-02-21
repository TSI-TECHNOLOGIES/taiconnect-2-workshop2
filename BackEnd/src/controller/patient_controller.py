import pandas as pd
from src.utils.llm_call import LLMTrigger
from src.tools.tool_constructor import LLMToolConstructor

class PatientFlow:
    def __init__(self, userType, provider, userQuery, conversationHistory):
        self.patientDF = pd.read_csv("data/patientData.csv")
        self.userType = userType
        self.provider = provider
        self.userQuery = userQuery
        self.conversationHistory = conversationHistory

    def tool_constructor(self):
        tools = LLMToolConstructor(self.provider, self.userType).main()
        return tools

    def main(self):
        tools = self.tool_constructor()
        llmResponse =  LLMTrigger(self.provider, tools, self.userQuery, self.userType, self.conversationHistory).main()
        return {"response": llmResponse}