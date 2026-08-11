import pytest
from urllib.parse import urlparse
from src.app.api import api
from playwright.sync_api import Page, expect

test_api = api.test_client()

@pytest.fixture(autouse=True)
def mock_request(page):
    def intercept_request(route):
        path = urlparse(route.request.url).path
        method = route.request.method

        if method == "POST":
            response = test_api.post(
                path, 
                data=route.request.post_data,
                headers=dict(route.request.headers)
                )

        else:
            response = test_api.get(path)
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

def test_blank_name_shows_graceful_error(page: Page):
    page.goto("http://localhost:5000/")
    
    page.select_option("select[name='duty_id']", value="") 
    page.fill("textarea[name='description']", "Donec eget pulvinar")
    page.click("button[type='submit']")
    
    error_text = page.locator(".error-message")
    expect(error_text).to_be_visible()
    expect(error_text).to_contain_text("Name cannot be blank")

def test_blank_description_shows_graceful_error(page: Page):
    page.goto("http://localhost:5000/")
    
    page.select_option("select[name='duty_id']", value="Duty 5")
    page.fill("textarea[name='description']", "") 
    page.click("button[type='submit']")
    
    error_alert = page.locator("[role='alert']")
    expect(error_alert).to_be_visible()
    expect(error_alert).to_contain_text("Description cannot be blank")

def test_duplicate_duty_shows_graceful_error(page: Page):
    page.goto("http://localhost:5000/")
    
    page.select_option("select[name='duty_id']", value="Duty 7")
    page.fill("textarea[name='description']", "Lorem ipsum dolor")
    page.click("button[type='submit']")
    
    page.select_option("select[name='duty_id']", value="Duty 7")
    page.fill("textarea[name='description']", "Orci varius natoque")
    page.click("button[type='submit']")
    
    error_text = page.locator(".error-message")
    expect(error_text).to_be_visible()
    expect(error_text).to_contain_text("Duty with this name already exists")