from dataclasses import dataclass, field


@dataclass
class Quote:
    text: str
    author: str
    author_url: str
    tags: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "author": self.author,
            "author_url": self.author_url,
            "tags": self.tags
        }


@dataclass
class Author:
    """Représentation d'un auteur."""
    name: str
    bio: str = ""
    born_date: str = ""
    born_location: str = ""
    url: str = ""
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "bio": self.bio,
            "born_date": self.born_date,
            "born_location": self.born_location,
            "url": self.url
        }