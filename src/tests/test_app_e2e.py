import re, pytest
from urllib.parse import urlparse
from app import app
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

def test_adding_a_new_duty_shows_it_on_the_page(page: Page):
    page.goto("http://127.0.0.1:5000")

    page.fill('input[name="identifier"]', "Duty 5")
    page.fill('input[name="description"]', "Build and operate")
    page.get_by_role("button", name="Add Duty").click()

    print(page.content())

    expect(page.get_by_role("heading", name="Duty 5")).to_be_visible()
    expect(page.get_by_text("Build and operate")).to_be_visible()
    expect(page.get_by_text("Duty 5 created!")).to_be_visible()