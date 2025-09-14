import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from filters.idea_filter import IdeaFilter, IdeaProcessor, IdeaEvent


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


# Usage example for integration with your Slack bot
async def process_slack_message(event_data: Dict) -> Optional[IdeaEvent]:
    """
    Main function to process Slack messages and extract ideas.
    Call this from your Slack bot's event handler.
    """
    processor = SlackIdeaProcessor()
    return await processor.process_slack_event(event_data)


# Example usage in your app.py:
"""
from slackToGragh import process_slack_message


@app.post("/slack/events")
async def slack_events(request: Request):
    try:
        body = await request.json()
       
        if body.get("type") == "event_callback":
            event = body.get("event")
            if event and event.get("type") == "message":
                # Process for ideas
                idea = await process_slack_message(body)
                if idea:
                    print(f"Found idea: {idea.message_text}")
       
        return {"status": "ok"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid request")
"""