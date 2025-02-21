import ast
import json
import inspect
import src.functions.custom_functions as functions

class LLMToolConstructor:
    def __init__(self, provider, userType):
        self.provider = provider
        self.userType = userType
    
    def getFunctionList(self):
        functionList = []
        for name, obj in inspect.getmembers(functions, inspect.isfunction):
            source = inspect.getsource(obj)
            if f"scope_{self.userType}" in source:
                functionList.append(obj)
        print("Function Objects ! : ", functionList)
        return functionList
    
    def extract_function_metadata(self, func):
        source_code = inspect.getsource(func)
        tree = ast.parse(source_code)
        
        function_description = None
        param_descriptions = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign): 
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        if var_name == "function_description":
                            function_description = ast.literal_eval(node.value)
                        elif var_name.endswith("_description"):
                            param_name = var_name.replace("_description", "")
                            param_descriptions[param_name] = ast.literal_eval(node.value)

        params = inspect.signature(func).parameters
        param_properties = {
            param: {
                "type": "string",
                "description": param_descriptions.get(param, f"{param} parameter of {func.__name__}")
            }
            for param in params
        }

        function_metadata = {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": function_description or "No description available",
                "parameters": {
                    "type": "object",
                    "properties": param_properties,
                    "required": list(params.keys())
                }
            }
        }
        if self.provider == "openai":
            function_metadata['function']['parameters']["additionalProperties"] = False
            function_metadata['function']['strict'] = True

        return function_metadata
    
    def toolConstructor(self):
        functionList = self.getFunctionList()
        functions_metadata = [self.extract_function_metadata(func) for func in functionList]
        return functions_metadata
    
    def main(self):
        if self.userType == "patient":
            return self.toolConstructor()
        else:
            return {"message": "LLM tool is not available"}
