
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class SeoOptimizerAgent(BaseAgent):
    def run(self, input_data):
        title = input_data.get("title", "Sankalpa")
        desc = input_data.get("description", "The AI-powered app builder.")
        tags = input_data.get("keywords", ["AI", "automation", "builder"])

        content = f"""
<!-- SEO Meta Tags -->
<meta name=\"title\" content=\"{title}\" />
<meta name=\"description\" content=\"{desc}\" />
<meta name=\"keywords\" content=\"{', '.join(tags)}\" />
<meta name=\"author\" content=\"Sankalpa AI\" />
<meta property=\"og:title\" content=\"{title}\" />
<meta property=\"og:description\" content=\"{desc}\" />
<meta property=\"og:type\" content=\"website\" />
"""
        return {
            "message": "SEO meta tags generated.",
            "files": {
                "frontend/pages/_seo.tsx": content
            }
        }