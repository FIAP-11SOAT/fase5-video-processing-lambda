from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: str
    username: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    enabled: bool = True
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'enabled': self.enabled
        }


@dataclass
class AuthToken:
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    
    def to_dict(self) -> dict:
        return {
            'access_token': self.access_token,
            'id_token': self.id_token,
            'refresh_token': self.refresh_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in
        }
