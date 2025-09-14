import os
import sys
import json
from typing import List, Optional
from datetime import datetime

# Add the parent directory to the Python path so we can import filters
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from filters.idea_filter import IdeaFilter, IdeaProcessor, IdeaEvent



class TranscriptIdeaProcessor:
    """Processes meeting transcripts to extract ideas using the shared IdeaFilter."""
   
    def __init__(self):
        self.idea_filter = IdeaFilter()
        self.processor = IdeaProcessor(self.idea_filter)
   
    async def process_transcript(self, transcript_text: str, meeting_name: str = "Unknown Meeting", 
                                speaker_name: str = "Unknown Speaker") -> List[IdeaEvent]:
        """
        Process a transcript and return all ideas found.
        
        Args:
            transcript_text: The full transcript text
            meeting_name: Name of the meeting for context
            speaker_name: Name of the speaker (if single speaker)
        
        Returns:
            List of IdeaEvent objects containing found ideas
        """
        ideas = []
        
        try:
            # Split transcript into sentences or paragraphs for better analysis
            # You can adjust this splitting logic based on your needs
            segments = self._split_transcript(transcript_text)
            
            for i, segment in enumerate(segments):
                if not segment.strip():
                    continue
                    
                # Process each segment
                idea = await self.processor.process_text(
                    text=segment,
                    source="meeting_transcript",
                    context=meeting_name,
                    user_name=speaker_name
                )
                
                if idea:
                    ideas.append(idea)
            
            return ideas
           
        except Exception as e:
            print(f"Error processing transcript: {e}")
            return []
    
    def _split_transcript(self, text: str) -> List[str]:
        """
        Split transcript into segments for analysis.
        This is a simple implementation - you can enhance this based on your needs.
        """
        # Split by sentences (period followed by space and capital letter)
        import re
        sentences = re.split(r'\.\s+(?=[A-Z])', text)
        
        # Filter out very short segments
        segments = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        return segments
    
    async def process_transcript_file(self, file_path: str, meeting_name: str = "Unknown Meeting", 
                                    speaker_name: str = "Unknown Speaker") -> List[IdeaEvent]:
        """
        Process a transcript from a file.
        
        Args:
            file_path: Path to the transcript file
            meeting_name: Name of the meeting for context
            speaker_name: Name of the speaker
        
        Returns:
            List of IdeaEvent objects containing found ideas
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()
            
            return await self.process_transcript(transcript_text, meeting_name, speaker_name)
            
        except Exception as e:
            print(f"Error reading transcript file: {e}")
            return []


# Convenience functions for easy usage
async def process_transcript_text(transcript_text: str, meeting_name: str = "Unknown Meeting", 
                                speaker_name: str = "Unknown Speaker") -> List[IdeaEvent]:
    """
    Process transcript text and return ideas.
    """
    processor = TranscriptIdeaProcessor()
    return await processor.process_transcript(transcript_text, meeting_name, speaker_name)


async def process_transcript_file(file_path: str, meeting_name: str = "Unknown Meeting", 
                                speaker_name: str = "Unknown Speaker") -> List[IdeaEvent]:
    """
    Process transcript file and return ideas.
    """
    processor = TranscriptIdeaProcessor()
    return await processor.process_transcript_file(file_path, meeting_name, speaker_name)


# Example usage:
"""
# Process transcript text directly
ideas = await process_transcript_text(
    transcript_text="We should implement a new feature for user authentication...",
    meeting_name="Product Planning Meeting",
    speaker_name="John Doe"
)

# Process transcript from file
ideas = await process_transcript_file(
    file_path="meeting_transcript.txt",
    meeting_name="Weekly Standup",
    speaker_name="Team Lead"
)

# Print results
for idea in ideas:
    print(f"Idea: {idea.message_text}")
    print(f"Category: {idea.idea_category}")
    print(f"Confidence: {idea.confidence_score}")
    print("---")
"""
