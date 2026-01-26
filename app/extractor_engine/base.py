from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, text_or_image, schema: dict) -> dict:
        """
        Extract data from text or image based on the provided schema.
        
        Args:
            text_or_image: The OCR text output or image object.
            schema: The schema dictionary to map extracted data to.
            
        Returns:
            dict: The extracted data matching the schema.
        """
        pass
