from dataclasses import dataclass


@dataclass
class Message:
    role: str  # "system", "user", или "assistant"
    content: str
    
    def to_dict(self) -> dict:
        """Конвертация в формат OpenAI API"""
        return {"role": self.role, "content": self.content}

