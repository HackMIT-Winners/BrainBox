import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from idea_filter import IdeaFilter, IdeaProcessor, IdeaEvent


class SlackIdeaProcessor:
    """Processes Slack messages to extract ideas using the shared IdeaFilter."""
   
    def __init__(self):
        self.idea_filter = IdeaFilter()
        self.processor = IdeaProcessor(self.idea_filter)
   
    async def process_slack_event(self, event_data: Dict) -> Optional[IdeaEvent]:
        """
        Process a Slack event and return idea if found.
        """
        try:
            # Extract event details
            event = event_data.get("event", {})
            text = event.get("text", "")
            user_id = event.get("user", "")
            channel_id = event.get("channel", "")
            event_time = event_data.get("event_time", 0)
           
            # Get user and channel names (you might want to pass these from the main app)
            user_name = f"user_{user_id}"  # You can enhance this with actual name resolution
            channel_name = f"channel_{channel_id}"  # You can enhance this with actual name resolution
           
            # Use the shared filter to process the text
            idea = await self.processor.process_text(
                text=text,
                source="slack",
                context=channel_name,
                user_name=user_name
            )
           
            return idea
           
        except Exception as e:
            print(f"Error processing Slack event: {e}")
            return None

event_data = {
    "event": {
        "text": "We should implement a new feature for user authentication on our new platform",
        "user": "U1234567890",
        "channel": "C1234567890"
    }
}

async def main():
    processor = SlackIdeaProcessor()
    idea = await processor.process_slack_event(event_data)
    print(idea)
    return idea


if __name__ == "__main__":
    asyncio.run(main())