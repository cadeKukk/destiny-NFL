#!/usr/bin/env python3
"""
NFL Screenshot Complete - All Authors, 20 Picks, Optimized Formatting
Takes screenshots of all NFL.com mock draft pages with improved spacing and coverage
"""

import os
import time
from datetime import datetime
from docx import Document
from docx.shared import Inches, RGBColor, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NFLScreenshotComplete:
    def __init__(self):
        self.setup_selenium()
        
        # UPDATED URLs as provided by user
        self.author_urls = {
            'Bucky Brooks': 'https://www.nfl.com/news/bucky-brooks-2025-nfl-mock-draft-4-0-steelers-land-shedeur-sanders-cowboys-broncos-select-rbs',
            'Daniel Jeremiah': 'https://www.nfl.com/news/daniel-jeremiah-2025-nfl-mock-draft-4-0',
            'Lance Zierlein': 'https://www.nfl.com/news/lance-zierlein-2025-nfl-mock-draft-4-0-colts-trade-up-for-colston-loveland-saints-go-get-jaxson-dart',
            'Charles Davis': 'https://www.nfl.com/news/charles-davis-2025-nfl-mock-draft-3-0-cam-ward-only-qb-in-round-1-eagles-pick-te-mason-taylor',
            'Eric Edholm': 'https://www.nfl.com/news/eric-edholm-2025-nfl-mock-draft-3-0-four-first-round-quarterbacks-jaguars-take-rb-ashton-jeanty',
            'Dan Parr': 'https://www.nfl.com/news/dan-parr-2025-nfl-mock-draft-2-0-offensive-linemen-dominate-top-10-bears-grab-tight-end-tyler-warren',
            'Chad Reuter': 'https://www.nfl.com/news/seven-round-2025-nfl-mock-draft-round-one',
            'Gennaro Filice': 'https://www.nfl.com/news/gennaro-filice-2025-nfl-mock-draft-2-0-rb-ashton-jeanty-goes-top-5-cowboys-jump-for-jalon-walker',
            'Marc Ross': 'https://www.nfl.com/news/marc-ross-2025-nfl-mock-draft-1-0-three-qbs-selected-in-top-10-jets-snag-rb-ashton-jeanty'
        }
        
        os.makedirs('processed/complete_screenshots', exist_ok=True)

    def setup_selenium(self):
        """Setup Selenium WebDriver for taking screenshots"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1800,1400')  # Large window
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--force-device-scale-factor=1')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ Selenium WebDriver setup complete")
        except Exception as e:
            print(f"⚠️ Selenium setup failed: {e}")
            self.driver = None

    def screenshot_webpage_content(self, url, author):
        """Take screenshots of NFL.com webpage content - ALWAYS returns something for every author"""
        if not self.driver:
            print(f"⚠️ No WebDriver available for {author}")
            return [f"No WebDriver available for {author}"]
            
        screenshots = []
        
        try:
            print(f"📸 Capturing screenshots for {author}...")
            
            # Navigate to the page
            self.driver.get(url)
            time.sleep(12)  # Extended wait for page to fully load
            
            # Remove overlays
            self.remove_overlays()
            time.sleep(3)
            
            # Get article header (always try to get something)
            header_screenshot = self.screenshot_article_header(author)
            if header_screenshot:
                screenshots.append(header_screenshot)
            
            # Get individual draft picks (UP TO 20 PICKS)
            pick_screenshots = self.screenshot_individual_picks(author)
            screenshots.extend(pick_screenshots)
            
            # If no picks found, ALWAYS get page sections so author appears in document
            if not pick_screenshots:
                print(f"   📄 No individual picks found for {author}, taking page sections...")
                section_screenshots = self.screenshot_page_sections(author)
                screenshots.extend(section_screenshots)
            
            # If still no screenshots at all, take a full page screenshot as last resort
            if not screenshots:
                print(f"   🚨 Last resort: taking full page screenshot for {author}")
                fallback_screenshot = self.screenshot_full_page_fallback(author)
                if fallback_screenshot:
                    screenshots.append(fallback_screenshot)
                
        except Exception as e:
            print(f"   ⚠️ Error processing {author}: {e}")
            # Even if there's an error, try to get a fallback screenshot
            try:
                fallback_screenshot = self.screenshot_full_page_fallback(author)
                if fallback_screenshot:
                    screenshots.append(fallback_screenshot)
            except:
                pass
        
        # Ensure every author has at least one entry
        if not screenshots:
            screenshots = [f"Could not capture content for {author}"]
            
        print(f"   ✓ Captured {len([s for s in screenshots if s.endswith('.png')])} screenshots for {author}")
        return screenshots

    def remove_overlays(self):
        """Remove cookie banners and overlays"""
        try:
            overlay_selectors = [
                '[data-module="CookieBanner"]',
                '.onetrust-banner-sdk',
                '.cookie-banner',
                '[class*="overlay"]',
                '[class*="modal"]',
                '.nfl-banner',
                '[id*="onetrust"]'
            ]
            
            for selector in overlay_selectors:
                try:
                    overlays = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for overlay in overlays:
                        if overlay.is_displayed():
                            self.driver.execute_script("arguments[0].style.display = 'none';", overlay)
                except:
                    continue
                    
            # Try to click close buttons
            close_selectors = ['[aria-label="Close"]', '.close-button', '[data-dismiss]']
            for selector in close_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed():
                            button.click()
                            time.sleep(1)
                except:
                    continue
                    
        except Exception as e:
            print(f"   ⚠️ Error removing overlays: {e}")

    def screenshot_article_header(self, author):
        """Screenshot the article header"""
        try:
            header_selectors = [
                '.nfl-c-article__header',
                'h1',
                '.article-header',
                '.article-title'
            ]
            
            for selector in header_selectors:
                try:
                    header_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if header_element.is_displayed():
                        # Scroll to element
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header_element)
                        time.sleep(3)
                        
                        # Take screenshot
                        screenshot_path = f"processed/complete_screenshots/{author}_header.png"
                        header_element.screenshot(screenshot_path)
                        
                        print(f"   ✓ Header screenshot: {author}_header.png")
                        return screenshot_path
                except:
                    continue
        except Exception as e:
            print(f"   ⚠️ Could not capture header for {author}: {e}")
            
        return None

    def screenshot_individual_picks(self, author):
        """Screenshot individual NFL draft picks - UP TO 20 PICKS"""
        screenshots = []
        
        try:
            # Wait for content to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            
            # Look for NFL.com draft pick elements
            pick_selectors = [
                '.nfl-o-ranked-item.nfl-o-ranked-item--side-by-side',
                '.nfl-o-ranked-item',
                '[class*="ranked-item"]',
                '.mock-draft-pick',
                '.draft-pick'
            ]
            
            pick_elements = []
            for selector in pick_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        pick_elements = elements[:20]  # UP TO 20 PICKS
                        print(f"   📋 Found {len(pick_elements)} draft picks for {author} using: {selector}")
                        break
                except:
                    continue
            
            if pick_elements:
                for i, pick_element in enumerate(pick_elements, 1):
                    try:
                        # Scroll to the pick
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pick_element)
                        time.sleep(2)
                        
                        # Take direct element screenshot
                        screenshot_path = f"processed/complete_screenshots/{author}_pick_{i:02d}.png"
                        pick_element.screenshot(screenshot_path)
                        
                        screenshots.append(screenshot_path)
                        print(f"   ✓ Pick {i} screenshot captured")
                        
                    except Exception as e:
                        print(f"   ⚠️ Error capturing pick {i}: {e}")
                        continue
            else:
                print(f"   ⚠️ No draft pick elements found for {author}")
                
        except Exception as e:
            print(f"   ⚠️ Error finding draft picks for {author}: {e}")
            
        return screenshots

    def screenshot_page_sections(self, author):
        """Take page section screenshots as backup"""
        screenshots = []
        
        try:
            # Scroll to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Get page dimensions
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Take screenshots in sections
            section_height = viewport_height
            sections = min(4, max(1, total_height // section_height))  # Max 4 sections
            
            for i in range(sections):
                scroll_position = i * section_height
                
                # Scroll to position
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(4)  # Wait for content to load
                
                # Take screenshot
                screenshot_path = f"processed/complete_screenshots/{author}_section_{i+1:02d}.png"
                self.driver.save_screenshot(screenshot_path)
                
                screenshots.append(screenshot_path)
                print(f"   ✓ Section {i+1} screenshot captured")
                
        except Exception as e:
            print(f"   ⚠️ Error taking page sections for {author}: {e}")
            
        return screenshots

    def screenshot_full_page_fallback(self, author):
        """Take a full page screenshot as absolute fallback"""
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            
            screenshot_path = f"processed/complete_screenshots/{author}_fullpage.png"
            self.driver.save_screenshot(screenshot_path)
            
            print(f"   ✓ Fallback full page screenshot: {author}_fullpage.png")
            return screenshot_path
        except Exception as e:
            print(f"   ⚠️ Could not take fallback screenshot for {author}: {e}")
            return None

    def create_screenshot_document(self, all_screenshots):
        """Create Word document with optimized spacing and formatting"""
        print("📄 Creating optimized Word document with all authors...")
        
        doc = Document()
        
        # Set tight margins for more content
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.4)
            section.bottom_margin = Inches(0.4)
            section.left_margin = Inches(0.4)
            section.right_margin = Inches(0.4)
        
        # Title with reduced spacing
        title = doc.add_heading('NFL 2025 Mock Draft Collection', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_run = title.runs[0]
        title_run.font.size = Pt(22)  # Slightly smaller
        title_run.font.color.rgb = RGBColor(0, 53, 148)
        title.space_after = Pt(6)  # Reduce space after title
        
        # Subtitle with minimal spacing
        subtitle = doc.add_paragraph(f'Complete NFL.com Mock Draft Screenshots - {datetime.now().strftime("%B %d, %Y")}')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle_run = subtitle.runs[0]
        subtitle_run.font.size = Pt(10)
        subtitle_run.font.color.rgb = RGBColor(107, 114, 128)
        subtitle.space_after = Pt(8)
        
        # Group screenshots by author
        authors_screenshots = {}
        for screenshot_data in all_screenshots:
            author = screenshot_data['author']
            if author not in authors_screenshots:
                authors_screenshots[author] = []
            authors_screenshots[author].extend(screenshot_data['screenshots'])
        
        # Add each author's screenshots with optimized spacing
        for i, (author, screenshots) in enumerate(authors_screenshots.items()):
            
            # Author section with minimal spacing
            if i > 0:  # Only add page break after first author
                doc.add_page_break()
            
            # Author header with reduced spacing
            author_para = doc.add_paragraph()
            author_run = author_para.add_run(f"🏈 {author}")
            author_run.font.size = Pt(18)  # Smaller header
            author_run.font.bold = True
            author_run.font.color.rgb = RGBColor(0, 53, 148)
            author_para.space_after = Pt(4)  # Minimal spacing
            
            # Count actual screenshots vs text entries
            actual_screenshots = [s for s in screenshots if isinstance(s, str) and s.endswith('.png')]
            
            # Add brief description with minimal spacing
            if actual_screenshots:
                desc_para = doc.add_paragraph(f"📸 {len(actual_screenshots)} screenshots captured from NFL.com")
            else:
                desc_para = doc.add_paragraph(f"⚠️ Unable to capture screenshots for this author")
            
            desc_run = desc_para.runs[0]
            desc_run.font.size = Pt(9)
            desc_run.font.color.rgb = RGBColor(107, 114, 128)
            desc_para.space_after = Pt(4)
            
            # Add each screenshot with minimal spacing
            for screenshot_path in screenshots:
                try:
                    if isinstance(screenshot_path, str) and screenshot_path.endswith('.png') and os.path.exists(screenshot_path):
                        # Add screenshot with reduced width for tighter layout
                        doc.add_picture(screenshot_path, width=Inches(7.0))  # Slightly smaller
                        
                        # Minimal spacing around images
                        last_paragraph = doc.paragraphs[-1]
                        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        last_paragraph.space_before = Pt(3)  # Minimal spacing
                        last_paragraph.space_after = Pt(3)   # Minimal spacing
                        
                    elif isinstance(screenshot_path, str) and not screenshot_path.endswith('.png'):
                        # Handle text entries (error messages)
                        error_para = doc.add_paragraph(f"⚠️ {screenshot_path}")
                        error_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        error_run = error_para.runs[0]
                        error_run.font.size = Pt(10)
                        error_run.font.color.rgb = RGBColor(200, 100, 100)
                        error_para.space_after = Pt(6)
                        
                except Exception as e:
                    print(f"⚠️ Could not add screenshot {screenshot_path}: {e}")
        
        # Save document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f'processed/NFL_COMPLETE_ALL_AUTHORS_{timestamp}.docx'
        doc.save(output_path)
        
        print(f"✓ Complete document saved: {output_path}")
        return output_path

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

def main():
    print("=== NFL Complete Screenshot Creator ===")
    print("📸 ALL 9 AUTHORS with up to 20 picks each")
    print("🎯 Optimized formatting with reduced spacing")
    print("✅ Every author guaranteed to appear in document")
    print("=" * 55)
    
    creator = NFLScreenshotComplete()
    
    if not creator.driver:
        print("❌ Cannot proceed without WebDriver")
        return
    
    try:
        all_screenshots = []
        
        # Process ALL authors
        for author, url in creator.author_urls.items():
            screenshots = creator.screenshot_webpage_content(url, author)
            
            all_screenshots.append({
                'author': author,
                'screenshots': screenshots
            })
        
        # Create Word document with all authors
        output_path = creator.create_screenshot_document(all_screenshots)
        
        print(f"\n🎉 SUCCESS! Complete NFL.com screenshots captured!")
        print("=" * 55)
        print(f"📁 Document: {output_path}")
        print(f"📸 Screenshots: processed/complete_screenshots/")
        
        total_screenshots = sum(len([s for s in author_data['screenshots'] if isinstance(s, str) and s.endswith('.png')]) for author_data in all_screenshots)
        print(f"\n📊 Summary:")
        print(f"   • {len(creator.author_urls)} authors processed (ALL)")
        print(f"   • {total_screenshots} total screenshots captured")
        print(f"   • Up to 20 picks per author")
        print(f"   • Optimized spacing and formatting")
        print(f"   • Every author appears in document")
        print(f"   • Ready for viewing in Word")
        
    finally:
        creator.cleanup()

if __name__ == "__main__":
    main() 