from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository

if __name__ == "__main__":
    cognito_repo = CognitoRepository(
        user_pool_id="us-east-1_A0J5cfw5x",
        client_id="mm4ken4292p7vui2onh38h1ok",
    )

    # response = cognito_repo.register_user(
    #     username="moribeiro",
    #     password="Mor!2024",
    #     email="moribeiro@gmail.com",
    # )
    #
    # print("User registered:", response)

    response = cognito_repo.authenticate(
        username="moribeiro@gmail.com",
        password="Mor!2024",
    )

    print("Authentication response:", response)