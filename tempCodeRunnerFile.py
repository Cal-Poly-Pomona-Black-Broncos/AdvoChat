"""Handle user input and generate a response."""
        if not user_message:
            self.display_message("bot", "I didn't catch that. Please try again.")
            return

        try:
            response = self.chat_with_gpt(user_message)
            self.display_message("bot", response)
        except Exception as e:
            self.display_message("bot", f"An error occurred: {e}")