import pytest
from datetime import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.request_model import TempRequest, InsightRequest
from app.services.config import settings
from app.controller.request_controller import RequestController
from unittest.mock import patch, Mock
from app.errors.errors import EntityNotFound, MissingAttribute, CookieNotFound, UnableToCreate, JWTDecodeError, UnableToGet, DuplicateEntity
from jose import JWTError
from pymongo.errors import DuplicateKeyError, WriteError


@pytest.fixture(scope="function", autouse=True)
async def init_beanie_db():
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    database = client.database_name
    await init_beanie(database, document_models=[TempRequest, InsightRequest])


mock_jwt_data = {
    "user_id": "123"
}

mock_insights = {
    "some": "insight"
}

test_data = {
    "valid_data": {
        "data": {
            "id": "1",
            "some_field": "value"
        }
    },
    "invalid_data": {
        "data": None
    }
}

# ********************************* #
#   Save Temp Request Controller    #
# ********************************* #


@pytest.mark.asyncio
async def test_save_temp_request_success(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {"anonymous_id": "fake_cookie"}
    mock_saved_data = TempRequest(
        user_id="some user id",
        file_id="some field id",
        data={"field": "value"},
        insights={"field": "value"},
        created_at=datetime.utcnow()
    )

    with patch("jose.jwt.decode", return_value=mock_jwt_data), \
            patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_temp_suggestion", return_value=mock_saved_data):
        result = await RequestController.save_temp_request(data, request, True)

    assert result == mock_saved_data


@pytest.mark.asyncio
async def test_save_temp_request_missing_file(init_beanie_db):
    await init_beanie_db
    data = test_data['invalid_data']
    request = Mock()
    request._cookies = {"anonymous_id": "fake_cookie"}

    with pytest.raises(MissingAttribute) as exc_info:
        await RequestController.save_temp_request(data, request, True)

    assert str(exc_info.value) == "file"


@pytest.mark.asyncio
async def test_save_temp_request_missing_cookie(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {}

    with pytest.raises(CookieNotFound):
        await RequestController.save_temp_request(data, request, True)


@pytest.mark.asyncio
async def test_save_temp_request_missing_user_id(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {"anonymous_id": "fake_cookie"}
    invalid_jwt_data = {"user_id": None}

    with patch("jose.jwt.decode", return_value=invalid_jwt_data), \
            pytest.raises(MissingAttribute) as exc_info:
        await RequestController.save_temp_request(data, request, True)

    assert str(exc_info.value) == "user id"


@pytest.mark.asyncio
async def test_save_temp_request_insights_not_generated(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {"anonymous_id": "fake_cookie"}
    mock_saved_data = TempRequest(
        user_id="some user id",
        file_id="some field id",
        data={"field": "value"},
        insights={"field": "value"},
        created_at=datetime.utcnow()
    )

    with patch("jose.jwt.decode", return_value=mock_jwt_data), \
            patch("app.controller.request_controller.RequestController.generate_insights", return_value=None), \
            patch("app.services.request_service.RequestService.save_temp_suggestion", return_value=mock_saved_data), \
            pytest.raises(UnableToCreate) as exc_info:
        await RequestController.save_temp_request(data, request, True)

    assert str(exc_info.value) == "insights"


@pytest.mark.asyncio
async def test_save_temp_request_jwt_fail(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {"anonymous_id": "fake_cookie"}

    with patch("jose.jwt.decode", side_effect=JWTError("Error decoding")), \
            pytest.raises(JWTDecodeError) as exc_info:
        await RequestController.save_temp_request(data, request, True)

    assert str(exc_info.value) == ""


@pytest.mark.asyncio
async def test_save_temp_request_duplicate_file(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {"anonymous_id": "fake_cookie"}

    with patch("jose.jwt.decode", return_value=mock_jwt_data), \
            patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_temp_suggestion", side_effect=DuplicateKeyError("Duplicate file")), \
            pytest.raises(DuplicateEntity) as exc_info:
        await RequestController.save_temp_request(data, request, True)

    assert str(exc_info.value) == "file"


@pytest.mark.asyncio
async def test_save_temp_request_post_fail(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    request = Mock()
    request.cookies = {"anonymous_id": "fake_cookie"}

    with patch("jose.jwt.decode", return_value=mock_jwt_data), \
            patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_temp_suggestion", return_value=None), \
            pytest.raises(UnableToCreate) as exc_info:
        await RequestController.save_temp_request(data, request, True)

    assert str(exc_info.value) == "request"


# ********************************* #
#   Save Auth Request Controller    #
# ********************************* #


@pytest.mark.asyncio
async def test_save_auth_request_success(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    id = "some_user_id"
    mock_saved_data = InsightRequest(
        user_id="some user id",
        file_id="some field id",
        data={"field": "value"},
        insights={"field": "value"},
        created_at=datetime.utcnow()
    )

    with patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_suggestion", return_value=mock_saved_data):

        result = await RequestController.save_auth_request(data, id, True)

    assert result == mock_saved_data


@pytest.mark.asyncio
async def test_save_auth_request_missing_data(init_beanie_db):
    await init_beanie_db
    data = test_data['invalid_data']
    id = "some_user_id"

    with pytest.raises(MissingAttribute) as exc_info:
        await RequestController.save_auth_request(data, id, True)

    assert str(exc_info.value) == "File data"


@pytest.mark.asyncio
async def test_save_auth_request_missing_id(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    id = None

    with pytest.raises(MissingAttribute) as exc_info:
        await RequestController.save_auth_request(data, id, True)

    assert str(exc_info.value) == "User id"


@pytest.mark.asyncio
async def test_save_auth_request_no_data_from_save(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    id = "some_user_id"

    with patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_suggestion", return_value=None):

        with pytest.raises(UnableToCreate) as exc_info:
            await RequestController.save_auth_request(data, id, True)

    assert str(exc_info.value) == "request"


@pytest.mark.asyncio
async def test_save_auth_request_insights_not_generated(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    id = "some_user_id"

    with patch("app.controller.request_controller.RequestController.generate_insights", return_value=None):
        with pytest.raises(UnableToCreate) as exc_info:
            await RequestController.save_auth_request(data, id, True)

    assert str(exc_info.value) == "insights"


@pytest.mark.asyncio
async def test_save_auth_request_duplicate_file(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    id = "some_user_id"

    with patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_suggestion", side_effect=DuplicateKeyError("duplicate")):

        with pytest.raises(DuplicateEntity) as exc_info:
            await RequestController.save_auth_request(data, id, True)

    assert str(exc_info.value) == "file"


@pytest.mark.asyncio
async def test_save_auth_request_write_error(init_beanie_db):
    await init_beanie_db
    data = test_data['valid_data']
    id = "some_user_id"

    with patch("app.controller.request_controller.RequestController.generate_insights", return_value=mock_insights), \
            patch("app.services.request_service.RequestService.save_suggestion", side_effect=WriteError("write error")):

        with pytest.raises(UnableToCreate) as exc_info:
            await RequestController.save_auth_request(data, id, True)

    assert str(exc_info.value) == "request"


# ********************** #
#   Generate Insights    #
# ********************** #
mock_data = {'key': 'value'}
mock_file_id = 'some_file_id'
mock_insight_id = 'some_insight_id'
mock_insights = {'insight_key': 'insight_value'}
mock_analyzed_insights = {'analyzed_key': 'analyzed_value'}


@pytest.mark.asyncio
async def test_generate_insights_success():
    with patch('app.services.intel_mock_service.IntelMockService.get_insight_id', return_value=mock_insight_id), \
            patch('app.services.intel_mock_service.IntelMockService.get_insights', return_value=mock_insights), \
            patch('app.util.insights_analysis.InsightAnalysis.analyze_insights', return_value=mock_analyzed_insights):

        result = await RequestController.generate_insights(mock_data, mock_file_id, True)
        assert result == mock_analyzed_insights


@pytest.mark.asyncio
async def test_generate_insights_no_insight_id():
    with patch('app.services.intel_mock_service.IntelMockService.get_insight_id', return_value=None):

        with pytest.raises(UnableToGet) as exc_info:
            await RequestController.generate_insights(mock_data, mock_file_id, True)

        assert str(exc_info.value) == "insights"


@pytest.mark.asyncio
async def test_generate_insights_no_insights():
    with patch('app.services.intel_mock_service.IntelMockService.get_insight_id', return_value=mock_insight_id), \
            patch('app.services.intel_mock_service.IntelMockService.get_insights', return_value=None):

        with pytest.raises(UnableToGet) as exc_info:
            await RequestController.generate_insights(mock_data, mock_file_id, True)

        assert str(exc_info.value) == "insights"


@pytest.mark.asyncio
async def test_generate_insights_no_analyzed_insights():
    with patch('app.services.intel_mock_service.IntelMockService.get_insight_id', return_value=mock_insight_id), \
            patch('app.services.intel_mock_service.IntelMockService.get_insights', return_value=mock_insights), \
            patch('app.util.insights_analysis.InsightAnalysis.analyze_insights', return_value=None):

        with pytest.raises(UnableToCreate) as exc_info:
            await RequestController.generate_insights(mock_data, mock_file_id, True)

        assert str(exc_info.value) == "insights"


@pytest.mark.asyncio
async def test_generate_insights_write_error():
    with patch('app.services.intel_mock_service.IntelMockService.get_insight_id', side_effect=WriteError("write error")):

        with pytest.raises(UnableToCreate) as exc_info:
            await RequestController.generate_insights(mock_data, mock_file_id, True)

        assert str(exc_info.value) == "insights"


# ********************** #
#   Generate Insights    #
# ********************** #
user_id = "some_user_id"
mock_response = [{"insight": "value"}]


@pytest.mark.asyncio
async def test_get_insights_by_user_id_success(init_beanie_db):
    await init_beanie_db
    with patch("app.services.request_service.RequestService.get_insights_by_user_id", return_value=mock_response):
        result = await RequestController.get_insights_by_user_id(user_id)
        assert result == mock_response


@pytest.mark.asyncio
async def test_get_insights_by_user_id_not_found(init_beanie_db):
    await init_beanie_db
    with patch("app.services.request_service.RequestService.get_insights_by_user_id", return_value=None):
        with pytest.raises(EntityNotFound) as exc_info:
            await RequestController.get_insights_by_user_id(user_id)
        assert str(exc_info.value) == "Insights list"


@pytest.mark.asyncio
async def test_get_insights_by_user_id_exception(init_beanie_db):
    await init_beanie_db
    with patch("app.services.request_service.RequestService.get_insights_by_user_id", side_effect=Exception("Some exception")):
        with pytest.raises(EntityNotFound) as exc_info:
            await RequestController.get_insights_by_user_id(user_id)
        assert str(exc_info.value) == "Insights list"
