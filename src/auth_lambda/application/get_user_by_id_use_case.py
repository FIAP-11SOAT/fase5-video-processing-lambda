from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.repositories import IAuthRepository


class GetUserByIdUseCase:
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, user_id: str) -> User:
        if not user_id:
            raise ValueError("User ID is required")
        
        return self.auth_repository.get_user_by_id(user_id)
