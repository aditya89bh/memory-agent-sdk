from dataclasses import dataclass, field
@dataclass
class MemoryPolicy:
    allow_sensitive: bool=False
    remember_preferences: bool=True
    remember_tasks: bool=True
    ignore_small_talk: bool=True
    sensitive_terms: set[str]=field(default_factory=lambda:{"password","api key","secret","token","ssn"})
    small_talk: set[str]=field(default_factory=lambda:{"hi","hello","hey","thanks","thank you","ok","okay"})
    def should_ignore(self,text:str,tags:list[str]|None=None)->bool:
        low=text.strip().lower(); ts=set(tags or [])
        return (self.ignore_small_talk and low in self.small_talk) or (not self.allow_sensitive and any(t in low for t in self.sensitive_terms)) or ("preference" in ts and not self.remember_preferences) or ("task" in ts and not self.remember_tasks)
    def should_remember(self,text:str,tags:list[str]|None=None)->bool: return bool(text.strip()) and not self.should_ignore(text,tags)
