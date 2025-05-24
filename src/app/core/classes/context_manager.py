from typing import List, Union
from models.llm.context import LLMContext
from uuid import uuid4


class ContextManager:
    
    contexts: list[LLMContext] = []
    def add_context(self, context: Union[LLMContext, List[LLMContext]]):
        if isinstance(context, list):
            self.contexts.extend(context)
        elif isinstance(context, dict):
            if 'id' not in context or context['id'] is None:
                context['id']= str(uuid4())
            self.contexts.append(context)
        else:
            raise TypeError("Context must be a LLMContext or a list of LLMContexts")
        
    def get_constructed_contexts(self, display_label: bool=True) -> str:
        """Constructs a string representation of all contexts."""
        if len(self.contexts) < 1:
            return ""
        
        # Filter for contexts with type='file'
        file_contexts = [context for context in self.contexts if context.get('type', '') == 'file']
        
        if len(file_contexts) < 1:
            return ""
            
        return "\n\n".join([f"{context['label']}:\n{context['context']}" for context in file_contexts]) if display_label else "\n".join([context['context'] for context in file_contexts])