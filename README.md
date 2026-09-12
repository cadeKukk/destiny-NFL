# NFL Mock Draft Scraper

This program scrapes NFL mock draft data from NFL.com, processes it according to specified authors, and generates a Word document with the extracted data.

## Saved output

![First saved Bucky Brooks draft pick capture](processed/complete_screenshots/Bucky%20Brooks_pick_1.png)

This image is an existing capture under `processed/complete_screenshots/`. It shows the source material collected for the 2025 mock-draft documents, not current draft predictions. NFL.com owns the captured article content and imagery.

[Download a completed Word document](processed/NFL_COMPLETE_20250608_170704.docx) to inspect the June 8, 2025 output without rerunning the scraper. The [saved source page](ref/Bucky%20Brooks%202025%20NFL%20mock%20draft%204.0_%20Steelers%20land%20Shedeur%20Sanders%3B%20Cowboys%2C%20Broncos%20select%20RBs.html) is also included for comparison.

## Features

- Scrapes mock draft data from NFL.com
- Filters data by specific authors from your spreadsheets
- Extracts draft picks with team, player, position, and school information
- Saves output to a "processed" folder

## Target Authors

The program looks for mock drafts from these authors:
- Bucky Brooks
- Daniel Jeremiah
- Lance Zierlein
- Charles Davis
- Eric Edholm
- Dan Parr
- Chad Reuter
- Gennaro Filice
- Marc Ross

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the scraper:
```bash
python nfl_mock_draft_scraper.py
```

The program will:
1. Scrape the specified NFL.com URL
2. Look for related 2025 mock draft articles
3. Extract all mock draft data
4. Filter by target authors
5. Generate a Word document in the "processed" folder

### Output

The program creates:
- A "processed" folder (if it doesn't exist)
- A Word document named `NFL_Mock_Drafts_2025_YYYYMMDD_HHMMSS.docx`

The Word document includes:
- Title page with generation date and summary
- Table of contents listing all mock drafts
- Individual sections for each mock draft with:
  - Author and title information
  - Date and URL
  - Table of draft picks with pick number, team, player, position, and school

## Customization

You can modify the program by:
- Changing the target URL in the `main()` function
- Adding or removing authors in the `target_authors` list
- Adjusting the extraction patterns in `extract_draft_picks()` method

## Notes

- The program includes respectful delays between requests
- It handles various HTML structures and patterns
- Error handling is included for network issues
- The scraper is designed to be robust and adaptive to different page layouts
