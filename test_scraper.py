#!/usr/bin/env python3
"""
Test script for NFL Mock Draft Scraper
"""

try:
    from nfl_mock_draft_scraper import NFLMockDraftScraper
    
    print("Starting NFL Mock Draft Scraper test...")
    
    url = "https://www.nfl.com/news/bucky-brooks-2025-nfl-mock-draft-3-0-browns-take-shedeur-sanders-two-running-backs-in-top-10-picks"
    
    scraper = NFLMockDraftScraper()
    mock_drafts = scraper.run(url)
    
    print(f"\nTest completed successfully!")
    print(f"Total mock drafts processed: {len(mock_drafts)}")
    for draft in mock_drafts:
        print(f"- {draft['author']}: {len(draft['picks'])} picks")
        
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc() 