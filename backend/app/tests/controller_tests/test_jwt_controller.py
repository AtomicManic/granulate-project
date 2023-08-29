from unittest.mock import patch, Mock
import pytest
from app.errors.errors import MissingAttribute, UnAuthenticated
from app.controller.jwt_controller import JWTController
from app.models.user_model import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.config import settings
from app.errors.errors import EntityNotFound, JWTDecodeError, UnableToGet, CookieNotFound
from jose import jwt
from uuid import uuid4
from pymongo.errors import OperationFailure


@pytest.fixture(scope="function", autouse=True)
async def init_beanie_db():
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    database = client.database_name
    await init_beanie(database, document_models=[User])

# ************************* #
#   Test Login Controller   #
# ************************* #

email = "user222@example.com"
password = "password123"
user_id = "some_user_id"
access_token = "some_access_token"
refresh_token = "some_refresh_token"


@pytest.mark.asyncio
async def test_login_success(init_beanie_db):
    await init_beanie_db
    mock_user = type("User", (object,), {"user_id": user_id})
    with patch("app.services.user_service.UserService.authenticate", return_value=mock_user), \
            patch("app.controller.jwt_controller.create_access_token", return_value=access_token), \
            patch("app.controller.jwt_controller.create_refresh_token", return_value=refresh_token):

        result = await JWTController.login(email, password)
        assert result["access_token"] == access_token
        assert result["refresh_token"] == refresh_token


@pytest.mark.asyncio
async def test_login_missing_email(init_beanie_db):
    await init_beanie_db
    with pytest.raises(MissingAttribute) as exc_info:
        await JWTController.login(None, password)
    assert str(exc_info.value) == "Email"


@pytest.mark.asyncio
async def test_login_missing_password(init_beanie_db):
    await init_beanie_db
    with pytest.raises(MissingAttribute) as exc_info:
        await JWTController.login(email, None)
    assert str(exc_info.value) == "Password"


@pytest.mark.asyncio
async def test_login_unauthenticated(init_beanie_db):
    await init_beanie_db
    with patch("app.services.user_service.UserService.authenticate", return_value=None):
        with pytest.raises(UnAuthenticated):
            await JWTController.login(email, password)

# *************************** #
#   Test Refresh Controller   #
# *************************** #


@pytest.mark.asyncio
async def test_refresh_token_success(init_beanie_db):
    await init_beanie_db
    mock_user = type("User", (object,), {"user_id": "some_user_id"})
    token_data = {"sub": uuid4(), "exp": 1628888888}

    with patch("app.services.user_service.UserService.get_user_by_id", return_value=mock_user), \
            patch("app.controller.jwt_controller.create_access_token", return_value="new_access_token"), \
            patch("app.controller.jwt_controller.create_refresh_token", return_value="new_refresh_token"), \
            patch("app.controller.jwt_controller.jwt.decode", return_value=token_data)as mock_decode:

        result = await JWTController.refresh_token("valid_refresh_token")
        mock_decode.assert_called_once()

    assert result["access_token"] == "new_access_token"
    assert result["refresh_token"] == "new_refresh_token"


@pytest.mark.asyncio
async def test_refresh_token_operation_failure(init_beanie_db):
    await init_beanie_db
    with patch('jose.jwt.decode', return_value={'sub': uuid4()}):
        with patch("app.services.user_service.UserService.get_user_by_id", side_effect=OperationFailure("error message")):
            with pytest.raises(UnableToGet):
                await JWTController.refresh_token("valid_refresh_token")


@pytest.mark.asyncio
async def test_refresh_token_user_not_found(init_beanie_db):
    await init_beanie_db
    token_data = {"sub": uuid4(), "exp": 1628888888}

    with patch("app.services.user_service.UserService.get_user_by_id", return_value=None), \
            patch("jose.jwt.decode", return_value=token_data):
        with pytest.raises(EntityNotFound):
            await JWTController.refresh_token("valid_refresh_token")


@pytest.mark.asyncio
async def test_refresh_token_invalid_token(init_beanie_db):
    await init_beanie_db

    with patch("app.controller.jwt_controller.jwt.decode", side_effect=jwt.JWTError):
        with pytest.raises(JWTDecodeError):
            await JWTController.refresh_token("invalid_refresh_token")


# ****************************** #
#   Test Get Cookie Controller   #
# ****************************** #
@pytest.fixture
def mock_response():
    return Mock()


@pytest.mark.asyncio
async def test_get_cookie_no_cookie(mock_response):
    with patch('jose.jwt.encode', return_value='new_cookie_value'):
        result = await JWTController.get_cookie(None, mock_response)

    mock_response.set_cookie.assert_called_once()
    assert result == {"message": "cookie is set"}


@pytest.mark.asyncio
async def test_get_cookie_with_cookie(mock_response):
    result = await JWTController.get_cookie('existing_cookie', mock_response)

    mock_response.set_cookie.assert_not_called()
    assert result == {"message": "cookie exist"}


@pytest.mark.asyncio
async def test_get_cookie_exception(mock_response):
    with patch('jose.jwt.encode', side_effect=Exception()):
        with pytest.raises(CookieNotFound):
            await JWTController.get_cookie(None, mock_response)
