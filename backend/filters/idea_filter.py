import openai
import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from openai import OpenAI


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@dataclass
class IdeaEvent:
    """Represents a filtered event containing an idea."""
    source: str  # "slack", "meeting", "transcript", etc.
    user_name: str
    context: str  # channel_name, meeting_name, etc.
    message_text: str
    timestamp: int
    event_time: str
    confidence_score: float
    idea_category: str
    processed_at: str


class IdeaFilter:
    """Universal filter to identify ideas in any text using OpenAI API."""
   
    def __init__(self):
        self.model = "gpt-4o-mini"  # Using GPT-4o-mini for cost efficiency
        self.idea_keywords = [
            "idea", "suggestion", "proposal", "concept", "thought",
            "brainstorm", "innovation", "solution", "improvement",
            "feature", "enhancement", "recommendation", "insight"
        ]
       
    def is_potential_idea(self, text: str) -> bool:
        """Quick pre-filter to check if text might contain an idea."""
        if not text or len(text.strip()) < 10:
            return False  
        text_lower = text.lower()
        return True # any(keyword in text_lower for keyword in self.idea_keywords)
   
    async def analyze_with_openai(self, text: str, source: str, context: str) -> Tuple[bool, float, str]:
        """
        Use OpenAI to analyze if text contains a valuable idea.
        Returns: (is_idea, confidence_score, category)
        """
        prompt = f"""
        Analyze this {source} text to determine if it contains a valuable idea, suggestion, or insight.
       
        Text: "{text}"
        Source: {source}
        Context: {context}
       
        Consider this an idea if it contains:
        - New concepts or proposals
        - Suggestions for improvement
        - Creative solutions to problems
        - Innovative thinking
        - Actionable recommendations
        - Strategic insights
       
        Exclude:
        - Casual conversation
        - Questions without suggestions
        - Complaints without solutions
        - Random thoughts without substance
        - Noise or spam
       
        Respond in JSON format:
        {{
            "is_idea": true/false,
            "confidence": 0.0-1.0,
            "category": "innovation|improvement|solution|strategy|creative|other",
            "idea": "the idea"
        }}
        """
       
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant that identifies valuable ideas in text. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            print("HERE HERE HERE")
            print(text)
            print(result)
           
            return (
                result.get("is_idea", False),
                result.get("confidence", 0.0),
                result.get("category", "other")
            )
        except Exception as e:
            print(f"Error analyzing text with OpenAI: {e}")
            return False, 0.0, "error"
   
    async def filter_text(self, text: str, source: str, context: str, user_name: str = "unknown") -> Optional[IdeaEvent]:
        """
        Filter text to extract ideas.
        Returns IdeaEvent if it contains an idea, None otherwise.
        """
        try:
            # Quick pre-filter
            if not self.is_potential_idea(text):
                return None
        
            # Analyze with OpenAI
            is_idea, confidence, category = await self.analyze_with_openai(text, source, context)
           
            if is_idea and confidence > 0.5:  # Threshold for idea confidence
                current_time = datetime.now()
                return IdeaEvent(
                    source=source,
                    user_name=user_name,
                    context=context,
                    message_text=text,
                    timestamp=int(current_time.timestamp()),
                    event_time=current_time.isoformat(),
                    confidence_score=confidence,
                    idea_category=category,
                    processed_at=current_time.isoformat()
                )
           
            return None
           
        except Exception as e:
            print(f"Error filtering text: {e}")
            return None


class IdeaProcessor:
    """Processes and stores filtered ideas."""
   
    def __init__(self, idea_filter: IdeaFilter):
        self.idea_filter = idea_filter
        self.ideas: List[IdeaEvent] = []
   
    async def process_text(self, text: str, source: str, context: str, user_name: str = "unknown") -> Optional[IdeaEvent]:
        """Process text and return idea if found."""
        idea = await self.idea_filter.filter_text(text, source, context, user_name)
       
        if idea:
            self.ideas.append(idea)
            await self.save_idea(idea)
            print(f"💡 IDEA FOUND: {idea.user_name} in {idea.context}")
            print(f"   Source: {idea.source} | Category: {idea.idea_category} (Confidence: {idea.confidence_score:.2f})")
            print(f"   Text: {idea.message_text[:100]}...")
            print("-" * 50)
       
        return idea
   
    async def save_idea(self, idea: IdeaEvent):
        """Save idea to storage (implement your preferred storage method)."""
        # TODO: Implement storage (database, file, etc.)
        idea_data = {
            "source": idea.source,
            "user_name": idea.user_name,
            "context": idea.context,
            "message_text": idea.message_text,
            "timestamp": idea.timestamp,
            "event_time": idea.event_time,
            "confidence_score": idea.confidence_score,
            "idea_category": idea.idea_category,
            "processed_at": idea.processed_at
        }
       
        # For now, just log to console
        print(f"💾 SAVED IDEA: {json.dumps(idea_data, indent=2)}")
   
    def get_recent_ideas(self, limit: int = 10) -> List[IdeaEvent]:
        """Get recent ideas."""
        return sorted(self.ideas, key=lambda x: x.timestamp, reverse=True)[:limit]
   
    def get_ideas_by_category(self, category: str) -> List[IdeaEvent]:
        """Get ideas by category."""
        return [idea for idea in self.ideas if idea.idea_category == category]
    
    def get_ideas_by_source(self, source: str) -> List[IdeaEvent]:
        """Get ideas by source."""
        return [idea for idea in self.ideas if idea.source == source]
