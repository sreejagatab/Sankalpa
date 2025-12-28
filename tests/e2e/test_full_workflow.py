"""
End-to-end tests for full application workflow
"""

import pytest
import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Skip these tests if Selenium is not installed
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_E2E_TESTS"),
    reason="E2E tests are only run when RUN_E2E_TESTS environment variable is set"
)

@pytest.fixture(scope="module")
def browser():
    """Set up the browser for testing"""
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Create the browser
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Clean up
    driver.quit()

@pytest.fixture(scope="module")
def app_server():
    """Start the application server for testing"""
    import subprocess
    import time
    
    # Start the backend server
    backend_process = subprocess.Popen(
        ["python", "run_sankalpa.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to start
    time.sleep(5)
    
    yield
    
    # Clean up
    backend_process.terminate()
    backend_process.wait()

def test_home_page(browser, app_server):
    """Test the home page loads correctly"""
    # Navigate to the home page
    browser.get("http://localhost:3000")
    
    # Check the title
    assert "Sankalpa" in browser.title
    
    # Check for main elements
    assert browser.find_element(By.TAG_NAME, "h1").text == "Sankalpa"
    
    # Check for navigation links
    nav_links = browser.find_elements(By.CSS_SELECTOR, "nav a")
    nav_text = [link.text for link in nav_links]
    assert "Home" in nav_text
    assert "Playground" in nav_text
    assert "Composer" in nav_text
    assert "Memory" in nav_text

def test_playground_workflow(browser, app_server):
    """Test the playground workflow"""
    # Navigate to the playground
    browser.get("http://localhost:3000/playground")
    
    # Wait for the page to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
    )
    
    # Check the title
    assert "Playground" in browser.find_element(By.TAG_NAME, "h1").text
    
    # Select an agent
    agent_select = browser.find_element(By.ID, "agent-select")
    agent_select.click()
    
    # Select the first agent option
    agent_options = browser.find_elements(By.CSS_SELECTOR, "#agent-select option")
    if len(agent_options) > 1:
        agent_options[1].click()
    
    # Enter input
    input_area = browser.find_element(By.ID, "input-area")
    input_area.clear()
    input_area.send_keys("Test input for playground")
    
    # Click the run button
    run_button = browser.find_element(By.ID, "run-button")
    run_button.click()
    
    # Wait for the result
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, "result-area"))
    )
    
    # Check that we got a result
    result_area = browser.find_element(By.ID, "result-area")
    assert result_area.text != ""

def test_chat_workflow(browser, app_server):
    """Test the chat workflow"""
    # Navigate to the chat page
    browser.get("http://localhost:3000/chat")
    
    # Wait for the page to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
    )
    
    # Check the title
    assert "Chat" in browser.find_element(By.TAG_NAME, "h1").text
    
    # Enter a message
    message_input = browser.find_element(By.ID, "message-input")
    message_input.clear()
    message_input.send_keys("Hello, agent!")
    
    # Send the message
    send_button = browser.find_element(By.ID, "send-button")
    send_button.click()
    
    # Wait for the response
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".message.agent"))
    )
    
    # Check that we got a response
    messages = browser.find_elements(By.CSS_SELECTOR, ".message")
    assert len(messages) >= 2  # At least our message and a response
    
    # Check our message is displayed
    user_messages = browser.find_elements(By.CSS_SELECTOR, ".message.user")
    assert any("Hello, agent!" in msg.text for msg in user_messages)

def test_memory_workflow(browser, app_server):
    """Test the memory workflow"""
    # Navigate to the memory page
    browser.get("http://localhost:3000/memory")
    
    # Wait for the page to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
    )
    
    # Check the title
    assert "Memory" in browser.find_element(By.TAG_NAME, "h1").text
    
    # Wait for memory keys to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".memory-key"))
    )
    
    # Click on a memory key
    memory_keys = browser.find_elements(By.CSS_SELECTOR, ".memory-key")
    if memory_keys:
        memory_keys[0].click()
        
        # Wait for the memory value to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".memory-value"))
        )
        
        # Check that we got a value
        memory_value = browser.find_element(By.CSS_SELECTOR, ".memory-value")
        assert memory_value.text != ""

def test_composer_workflow(browser, app_server):
    """Test the composer workflow"""
    # Navigate to the composer page
    browser.get("http://localhost:3000/composer")
    
    # Wait for the page to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
    )
    
    # Check the title
    assert "Composer" in browser.find_element(By.TAG_NAME, "h1").text
    
    # Wait for the agent list to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-item"))
    )
    
    # Drag an agent to the canvas
    agent_items = browser.find_elements(By.CSS_SELECTOR, ".agent-item")
    canvas = browser.find_element(By.ID, "composer-canvas")
    
    if agent_items:
        # Use ActionChains for drag and drop
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(browser)
        actions.drag_and_drop(agent_items[0], canvas).perform()
        
        # Check that the agent was added to the canvas
        canvas_agents = browser.find_elements(By.CSS_SELECTOR, ".canvas-agent")
        assert len(canvas_agents) >= 1
