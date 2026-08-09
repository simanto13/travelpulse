class MCPTools:
    def __init__(self, transport):
        self.transport=transport
        self._tools={}
    async def discover(self):
        self._tools={"forecast":"Forecast Tool","alerts":"Alerts Tool","air_quality":"Air Quality Tool","marine":"Marine Tool","historical":"Historical Tool"}
        return self._tools
    def exists(self,name):
        return name in self._tools
