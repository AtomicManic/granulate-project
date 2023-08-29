import pytest
from app.controller.user_controller import UserController
from app.models.user_model import User
from app.errors.errors import DuplicateEntity
from unittest.mock import patch
from pymongo.errors import DuplicateKeyError
from app.services.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="module", autouse=True)
async def init_beanie_db():
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    database = client.database_name
    await init_beanie(database, document_models=[User])


@pytest.mark.asyncio
async def test_register_success(init_beanie_db):
    await init_beanie_db
    mock_data = {"email": "user11@gmail.com",
                 "first_name": "string",
                 "last_name": "string",
                 "hashed_password": "hash_pass"}
    mock_user = User(**mock_data)

    with patch('app.services.user_service.UserService.create_user', return_value=mock_user) as mock_create_user:
        result = await UserController.register(mock_data)

        mock_create_user.assert_called_once_with(mock_data)
        assert result == mock_user


@pytest.mark.asyncio
async def test_register_duplicate_email():
    mock_data = {"email": "user11@gmail.com",
                 "first_name": "string",
                 "last_name": "string",
                 "hashed_password": "hash_pass"}

    with patch('app.services.user_service.UserService.create_user', side_effect=DuplicateKeyError("duplicate")):
        with pytest.raises(DuplicateEntity):
            await UserController.register(mock_data)


@pytest.mark.asyncio
async def test_register_db_failure():
    mock_data = {"email": "user11@gmail.com",
                 "first_name": "string",
                 "last_name": "string",
                 "hashed_password": "hash_pass"}
    with patch('app.services.user_service.UserService.create_user', return_value=None):
        result = await UserController.register(mock_data)
        assert result == None
