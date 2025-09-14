from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackToGraph import SlackIdeaProcessor
import requests

# Load environment variables
load_dotenv()

# Initialize Slack client
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    raise ValueError("SLACK_BOT_TOKEN environment variable is required")

slack_client = WebClient(token=slack_token)

# Create router for Slack endpoints
router = APIRouter(prefix="/slack", tags=["slack"])
processor = SlackIdeaProcessor()

class SlackEvent(BaseModel):
    token: str
    challenge: str
    type: str

def get_user_name(user_id: str) -> str:
    """Resolve a Slack user ID to the user's display name."""
    try:
        response = slack_client.users_info(user=user_id)
        user = response["user"]
        # Try to get display name first, then real name, then fall back to username
        return user.get("profile", {}).get("display_name") or \
               user.get("profile", {}).get("real_name") or \
               user.get("name", user_id)
    except SlackApiError as e:
        print(f"Error fetching user info for {user_id}: {e}")
        return user_id

def get_channel_name(channel_id: str) -> str:
    """Resolve a Slack channel ID to the channel's name."""
    try:
        response = slack_client.conversations_info(channel=channel_id)
        channel = response["channel"]
        # For public channels, get the name
        if channel.get("is_channel") or channel.get("is_group"):
            return f"#{channel.get('name', channel_id)}"
        # For DMs, try to get the user's name
        elif channel.get("is_im"):
            user_id = channel.get("user")
            if user_id:
                user_name = get_user_name(user_id)
                return f"DM with {user_name}"
        # For private groups
        elif channel.get("is_private"):
            return f"Private group: {channel.get('name', channel_id)}"
        else:
            return channel.get("name", channel_id)
    except SlackApiError as e:
        print(f"Error fetching channel info for {channel_id}: {e}")
        return channel_id

@router.post("/events")
async def slack_events(request: Request):
    """
    Handle Slack events including URL verification.
    According to Slack docs: https://docs.slack.dev/reference/events/url_verification/
    """
    # TODO: use team_id for multi-tenant support
    try:
        # Parse the JSON payload
        body = await request.json()
        
        # Check if this is a URL verification challenge
        match body.get("type"):
            case "url_verification":
                # Return the challenge value to verify the endpoint
                challenge = body.get("challenge")
                if challenge:
                    return {"challenge": challenge}
                else:
                    raise HTTPException(status_code=400, detail="Missing challenge value")
            case "event_callback":
                event = body.get("event")
                if not event:
                    return {}
                event_time = body.get("event_time") # unix timestamp (seconds)
                text = event.get("text") # message text
                user_id = event.get("user") # user ID
                channel_id = event.get("channel") # channel ID
                
                # Resolve IDs to names
                user_name = get_user_name(user_id) if user_id else "Unknown User"
                channel_name = get_channel_name(channel_id) if channel_id else "Unknown Channel"
                
                idea = await processor.process_slack_event({
                    "event": {
                        "text": text,
                        "user": user_name,
                        "channel": channel_name,
                    }
                })

                requests.get(f"{os.getenv("BACKEND_URL")}/transcript", params={
                    "text": idea.message_text,
                    "meeting_name": "",
                    "speaker_name": "",
                })
            case _:
                raise HTTPException(status_code=400, detail="Invalid event type")
        
        # Handle other event types here
        # For now, just acknowledge receipt
        return {"status": "ok"}
        
    except Exception as e:
        print(f"Error processing Slack event: {e}")
        raise HTTPException(status_code=400, detail="Invalid request")
