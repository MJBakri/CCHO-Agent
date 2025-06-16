


from typing import List, Optional
from uuid import uuid4

from fastapi import WebSocket
from models.llm.attachments import MessageAttachment
from logger.logger import logger
from core.classes.conversation_manager import ConversationManager
from core.classes.message import ChatMessage
from core.classes.abstract_classes.llm import LLM
from services.llm.clients.groq import groq_client

class LLMGroq(LLM):
    """
    Groq LLM implementation.
    This class extends the base LLM class and provides specific functionality for Groq.
    """
    ROLE_TRANSLATOR = {
        "user": "user",
        "ai": "assistant",}
    def __init__(
        self,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
        model_name: Optional[str] = None,
        **kwargs
        ):
        super().__init__(temperature=temperature, top_p=top_p, max_tokens=max_tokens, model_name=model_name, **kwargs)
        self.client = groq_client.get_client()
            
    def _handle_message(self, message:str, attachments: Optional[List[MessageAttachment]]):
        
        content = []
        if attachments:
            with_attachment = {"role": "user", "content": []}
            if message:
                with_attachment["content"].append({
                    "type" : "text",
                    "text" : message,
                })
            #save image as base64 text to local
            
            logger.debug("With Attachments!")
            for attachment in attachments:

                if attachment.get("type") == "image":
                    with_attachment["content"].append({
                        "type" : "image_url",
                        "image_url": {
                            "url" : f'data:image/jpeg;base64,{attachment.get("data")}'
                        }
                    })
            content.append(with_attachment)
        else:
            content.append({"role": "user", "content": message})
        return content
        
    async def send_to_llm(self, message:str=None, ws_client:Optional[WebSocket]=None, conversation_manager:Optional[ConversationManager]=None, attachments:Optional[List[MessageAttachment]]=None, stream:bool=False):
        """
        Send a message to the Groq LLM and return the response.
        
        Args:
            message (str): The message to send to the LLM.
            ws_client: Optional WebSocket client for real-time communication.
            message_history (Optional[List[str]]): History of messages for context.
        
        Returns:
            str: The response from the LLM.
        """
        messages = []
        
        if self.prompt:
            messages.append({"role": "system", "content": self.prompt.get_formatted_prompt()})
        
        messages.extend(await conversation_manager.get_messages_to_llm(self._handle_message, message=message, attachments=attachments) if conversation_manager else 
            self._handle_message(message=message, attachments=attachments)
        )
        # logger.debug(f"Payload sent to Groq {messages}")
        if stream:
            stream = await self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                stream=True
            )
            ai_id = uuid4()
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    if conversation_manager:
                        await conversation_manager.handle_ai_message(chunk=chunk.choices[0].delta.content, id=ai_id)  
                    await ws_client.send_json({"reply":chunk.choices[0].delta.content})
        else:
            response = await self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                stream=False
            )
            if conversation_manager:
                await conversation_manager.handle_ai_message(chunk=response.choices[0].message.content)
            logger.debug(f"Groq LLM Raw Response: {response}")
            return response.choices[0].message.content
        
    def resources_recorder(self):
        """
        Record resources used by the LLM.
        This method can be implemented to log or track resource usage.
        """
        logger.info("Resources recording for Groq is to be implemented.")