import pytest
from urllib.parse import urlparse
from src.app.api import api
from playwright.sync_api import Page, expect

test_api = api.test_client()

@pytest.fixture(autouse=True)
def mock_request(page):
    def intercept_request(route):
        path = urlparse(route.request.url).path
        method = route.request.method.upper()

        client_method = getattr(test_api, method.lower())

        kwargs = {"headers": dict(route.request.headers)}
        if method in ["POST", "PUT", "PATCH"]:
            kwargs["data"] = route.request.post_data

        response = client_method(path, **kwargs)
        
        route.fulfill(
            body=response.data,
            headers=dict(response.headers),
            status=response.status_code
        )
    page.route("http://localhost:5000/**", intercept_request)
    yield

def test_health(page: Page):
    response = page.goto("http://localhost:5000/")
    assert response is not None
    assert response.ok
