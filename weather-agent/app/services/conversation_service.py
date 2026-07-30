class ConversationService:
    def __init__(self):
        self._store={}
    async def load_history(self,cid):
        return self._store.get(cid,[])
    async def save_turn(self,conversation_id,user_message,assistant_message,metadata=None):
        self._store.setdefault(conversation_id,[]).extend([
            {"role":"user","content":user_message},
            {"role":"assistant","content":assistant_message}
        ])
    async def delete(self,cid):
        self._store.pop(cid,None)
