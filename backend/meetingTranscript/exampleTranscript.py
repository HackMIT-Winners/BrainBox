import asyncio
from TranscriptToGragh import TranscriptIdeaProcessor


async def main():
    processor = TranscriptIdeaProcessor()
    ideas = await processor.process_transcript_file("exampleTranscript.txt", "Example Meeting", "Unknown Speaker")
    
    print(f"Found {len(ideas)} ideas:")
    print("=" * 50)
    
    for i, idea in enumerate(ideas, 1):
        print(f"Idea #{i}:")
        print(f"  Text: {idea.message_text}")
        print(f"  Category: {idea.idea_category}")
        print(f"  Confidence: {idea.confidence_score:.2f}")
        print(f"  Speaker: {idea.user_name}")
        print(f"  Processed: {idea.processed_at}")
        print("-" * 30)


if __name__ == "__main__":
    asyncio.run(main())