import re
from app import app
from playwright.sync_api import sync_playwright, Page, expect

client = app.test_client()

def test_duties_show_on_page():
    response = client.get('/')
    assert "Duty 1" in response.text

def test_200_status():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        response = page.request.get("http://127.0.0.1:5000")
        assert response.status == 200
        # This is also acceptable:
        # response = page.request.get("http://127.0.0.1:5000")
        # assert response.status == 200

def test_title_is_present_on_page(page: Page):
    page.goto("http://127.0.0.1:5000")
    expect(page).to_have_title(re.compile(r"Duties"))

def test_heading_is_present_on_page(page: Page):
    page.goto("http://127.0.0.1:5000")
    expect(page.get_by_role("heading", name="Duties")).to_be_visible()
