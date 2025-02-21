import os
import json
import inspect
from groq import Groq
from openai import OpenAI
from src import configData
from src.tools.tool_execution import ExecuteTool
import src.functions.custom_functions as functions
from src.utils.prompt_constructor import PromptConstructor

class LLMTrigger:
    def __init__(self, provider, tools, userQuery, userType, conversationHistory):
        self.provider = provider
        self.tools = tools
        self.tool_call_identified = True
        self.userQuery = userQuery
        self.userType = userType
        self.messages =  None
        self.conversationHistory = conversationHistory
        self.groqClient =  Groq(api_key=os.getenv("groq_api_key"))
        self.openaiClient = OpenAI(api_key=os.getenv("openai_api_key"))
        self.configData = configData
    
    def functionCollector(self, module):
        func_dict = {}
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            source = inspect.getsource(obj)
            if f"scope_{self.userType}" in source:
                func_dict[name] = obj
        return func_dict
    
    def messageConstructor(self, prompt):
        self.messages = [
                    {"role": "system", "content": "You are useful hospistall assistat bot, who helps user by answer their queries about hospital and policies only from the provided documents also helps user to book appointment with the doctor."},
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
        return self.messages
    
    def openaicall(self):
        final_resonse =  None
        prompt =  PromptConstructor(self.userQuery, self.conversationHistory).prompt_maker()
        messages = self.messageConstructor(prompt)
        while self.tool_call_identified:
            response = self.openaiClient.chat.completions.create(
                            model=self.configData['openai_model_name'], 
                            messages=messages, 
                            tools=self.tools, 
                            tool_choice=self.configData['tool_choice'], 
                            max_tokens=self.configData['max_tokens']
                        )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            if tool_calls:
                available_functions = self.functionCollector(functions)
                messages.append(
                    {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments,
                                },
                                "type": tool_call.type,
                            }
                            for tool_call in tool_calls
                        ],
                    }
                )
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = ExecuteTool(function_name, function_args, available_functions).main()
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
            else:
                self.tool_call_identified = False
                final_response = response.choices[0].message.content
        return final_response    
    
    def groqCall(self):
        final_resonse =  None
        prompt =  PromptConstructor(self.userQuery, self.conversationHistory).prompt_maker()
        messages = self.messageConstructor(prompt)
        while self.tool_call_identified:
            response = self.groqClient.chat.completions.create(
            model=self.configData['model_name'], messages=messages, tools=self.tools, tool_choice=self.configData['tool_choice'], max_tokens=self.configData['max_tokens'], temperature=self.configData['temperature']
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            if tool_calls:
                available_functions = self.functionCollector(functions)
                messages.append(
                    {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments,
                                },
                                "type": tool_call.type,
                            }
                            for tool_call in tool_calls
                        ],
                    }
                )

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = ExecuteTool(function_name, function_args, available_functions).main()
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
            else:
                if '</function>' in response.choices[0].message.content:
                    pass
                else:
                    self.tool_call_identified = False
                    final_resonse = response.choices[0].message.content
        return final_resonse
     
    def main(self):
        if self.provider == "groq":
            return self.groqCall()
        elif self.provider == "openai":
            return self.openaicall()