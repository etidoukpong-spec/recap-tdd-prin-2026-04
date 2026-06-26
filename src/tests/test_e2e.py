import pytest
from urllib.parse import urlparse
from src.app.app import app
from playwright.sync_api import Page, expect

test_app = app.test_client()

@pytest.fixture(autouse=True)
def mock_request(page):
    def intercept_request(route):
        path = urlparse(route.request.url).path
        method = route.request.method

        if method == "POST":
            response = test_app.post(
                path, 
                data=route.request.post_data,
                headers=dict(route.request.headers)
                )

        else:
            response = test_app.get(path)
        route.fulfill(
            body=response.data,
            headers=dict(response.headers),
            status=response.status_code
        )
    page.route("http://localhost:5000/**", intercept_request)
    yield

def test_user_can_register_and_view_duties(page: Page):
    page.goto("http://localhost:5000/")
    
    expect(page.locator("h1")).to_have_text("Automate Coin Duties")
    
    page.select_option("select[name='duty_id']", value="Duty 5")
    page.fill("textarea[name='description']", "Build and operate automation pipelines")
    page.click("button[type='submit']")
    
    inventory_table = page.locator("#registered-inventory")
    
    expect(inventory_table).to_contain_text("Duty 5")
    expect(inventory_table).to_contain_text("Build and operate automation pipelines")
    expect(inventory_table).to_contain_text("Automate")