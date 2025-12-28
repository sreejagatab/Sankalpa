# Custom agents package
# This package contains dynamically generated agents

# Import agents that should be directly accessible
try:
    from agents.custom.hello_world import HelloWorldAgent
except ImportError:
    pass

try:
    from agents.custom.custom_calculator import CustomCalculatorAgent
except ImportError:
    pass

try:
    from agents.custom.code_summarizer import CodeSummarizerAgent
except ImportError:
    pass

try:
    from agents.custom.date_formatter import DateFormatterAgent
except ImportError:
    pass

# Dict of available agents for easier loading
CUSTOM_AGENTS = {
    "hello_world": "HelloWorldAgent",
    "custom_calculator": "CustomCalculatorAgent",
    "code_summarizer": "CodeSummarizerAgent",
    "date_formatter": "DateFormatterAgent",
}