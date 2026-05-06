import re, pytest
from urllib.parse import urlparse
from app import app
from playwright.sync_api import Page, expect

test_app = app.test_client()

@pytest.fixture(autouse=True)
def mock_request(page):
    def intercept_request(route):
        path = urlparse(route.request.url).path
        response = test_app.get(path)
        route.fulfill(
            body=response.data,
            headers=dict(response.headers),
            status=response.status_code
        )
    page.route("http://127.0.0.1:5000/**", intercept_request)
    yield

def test_200_status(page: Page):
    response = page.goto("http://127.0.0.1:5000")
    assert response.status == 200

def test_title_is_present_on_page(page: Page):
    page.goto("http://127.0.0.1:5000")
    expect(page).to_have_title(re.compile(r"Duties"))

def test_heading_is_present_on_page(page: Page):
    page.goto("http://127.0.0.1:5000")
    expect(page.get_by_role("heading", name="Duties")).to_be_visible()

def test_add_duty_button_is_present_on_page(page: Page):
    page.goto("http://127.0.0.1:5000")
    expect(page.get_by_role("button", name="Add Duty")).to_be_visible()