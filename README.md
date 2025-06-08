# NFL Mock Draft Scraper

This program scrapes NFL mock draft data from NFL.com, processes it according to specified authors, and generates a Word document with the extracted data.

## Features

- Scrapes mock draft data from NFL.com
- Filters data by specific authors from your spreadsheets
- Extracts draft picks with team, player, position, and school information
- Saves output to a "processed" folder

## Target Authors

The program looks for mock drafts from these authors (based on your spreadsheets):
            'Bucky Brooks': 'https://www.nfl.com/news/bucky-brooks-2025-nfl-mock-draft-4-0-steelers-land-shedeur-sanders-cowboys-broncos-select-rbs',
            'Daniel Jeremiah': 'https://www.nfl.com/news/daniel-jeremiah-2025-nfl-mock-draft-4-0',
            'Lance Zierlein': 'https://www.nfl.com/news/lance-zierlein-2025-nfl-mock-draft-4-0-colts-trade-up-for-colston-loveland-saints-go-get-jaxson-dart',
            'Charles Davis': 'https://www.nfl.com/news/charles-davis-2025-nfl-mock-draft-3-0-cam-ward-only-qb-in-round-1-eagles-pick-te-mason-taylor',
            'Eric Edholm': 'https://www.nfl.com/news/eric-edholm-2025-nfl-mock-draft-3-0-four-first-round-quarterbacks-jaguars-take-rb-ashton-jeanty',
            'Dan Parr': 'https://www.nfl.com/news/dan-parr-2025-nfl-mock-draft-2-0-offensive-linemen-dominate-top-10-bears-grab-tight-end-tyler-warren',
            'Chad Reuter': 'https://www.nfl.com/news/seven-round-2025-nfl-mock-draft-round-one',
            'Gennaro Filice': 'https://www.nfl.com/news/gennaro-filice-2025-nfl-mock-draft-2-0-rb-ashton-jeanty-goes-top-5-cowboys-jump-for-jalon-walker',
            'Marc Ross': 'https://www.nfl.com/news/marc-ross-2025-nfl-mock-draft-1-0-three-qbs-selected-in-top-10-jets-snag-rb-ashton-jeanty'

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