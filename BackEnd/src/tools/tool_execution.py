class ExecuteTool:
    def __init__(self, functionName, functionArgs, availableFunctions):
        self.functionName = functionName
        self.functionArgs = functionArgs
        self.availableFunctions = availableFunctions

    def main(self):
        function_to_call = self.availableFunctions.get(self.functionName)
        if not function_to_call:
            raise ValueError(f"Function '{self.functionName}' not found in available functions.")
        return function_to_call(**self.functionArgs)
