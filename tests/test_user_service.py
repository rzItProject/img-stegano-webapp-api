import pytest
from app.service.user import UserService, UserAlreadyExistsError
from app.schema.user import UserRegistrationInput
from app.repository.user import UserRepository

# Mocking get_user_by_email
@pytest.fixture
def mock_get_user_by_email(mocker):
    return mocker.patch.object(UserRepository, "get_user_by_email", return_value=None)

# Mocking create_user
@pytest.fixture
def mock_create_user(mocker):
    return mocker.patch.object(UserRepository, "create_user", return_value=None)

@pytest.mark.asyncio
async def test_register_user_successful(mock_get_user_by_email, mock_create_user):
    user_data = UserRegistrationInput(username="testuser", email="test@test.com", password="testpassword")
    user = await UserService.register_user(user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@test.com"

@pytest.mark.asyncio
async def test_register_user_email_exists(mocker, mock_get_user_by_email, mock_create_user):
    # Simulate a user existing in the database with the email
    mock_get_user_by_email.return_value = {"username": "existinguser", "email": "test@test.com", "password": "testpassword"}

    user_data = UserRegistrationInput(username="testuser", email="test@test.com", password="testpassword")

    with pytest.raises(UserAlreadyExistsError):
        await UserService.register_user(user_data)
