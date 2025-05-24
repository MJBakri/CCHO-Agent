

class Prompt:
    
    placeholders: dict = {}
    
    def __init__(self, prompt: str, placeholders:dict={}, **kwargs):
        """
        Initializes the Prompt class with a given prompt string.
        
        :param prompt: The prompt string to be used.
        """
        self.prompt = prompt
        self.placeholders = placeholders
        
    
    def __str__(self):
        """
        Returns the string representation of the prompt.
        
        :return: The prompt string.
        """
        return self.get_formatted_prompt()
    
    def get_formatted_prompt(self):
        """
        Formats the prompt with the provided keyword arguments.
        
        :return: The formatted prompt string.
        """
        return self.prompt.format(**self.placeholders)
    
    def set_placeholders(self, **kwargs:dict):
        """
        Sets a placeholder in the prompt.
        
        :param key: The placeholder key.
        :param value: The value to set for the placeholder.
        """
        self.placeholders.update(kwargs)

