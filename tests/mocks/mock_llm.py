class MockLLMProvider:

    def generate(self, messages):
        # Always return valid explanation JSON
        return """
        {
            "title": "Mock Title",
            "explanation": "Mock Explanation",
            "key_points": ["Point 1", "Point 2"]
        }
        """