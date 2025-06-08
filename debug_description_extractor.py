#!/usr/bin/env python3
"""
Comprehensive debug script to understand exact pick-to-analysis mapping
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def setup_selenium():
    """Setup Selenium WebDriver"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1800,1400')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        driver = webdriver.Chrome(options=chrome_options)
        print("✓ Selenium WebDriver setup complete")
        return driver
    except Exception as e:
        print(f"⚠️ Selenium setup failed: {e}")
        return None

def comprehensive_mapping_analysis():
    """Create comprehensive pick-to-analysis mapping understanding"""
    driver = setup_selenium()
    if not driver:
        return
    
    # Test with Bucky Brooks URL
    test_url = 'https://www.nfl.com/news/bucky-brooks-2025-nfl-mock-draft-4-0-steelers-land-shedeur-sanders-cowboys-broncos-select-rbs'
    
    try:
        print(f"🔍 Loading: {test_url}")
        driver.get(test_url)
        time.sleep(8)
        
        # Remove overlays quickly
        overlay_selectors = [
            '[data-module="CookieBanner"]',
            '.onetrust-banner-sdk',
            '.cookie-banner'
        ]
        
        for selector in overlay_selectors:
            try:
                overlays = driver.find_elements(By.CSS_SELECTOR, selector)
                for overlay in overlays:
                    if overlay.is_displayed():
                        driver.execute_script("arguments[0].style.display = 'none';", overlay)
            except:
                continue
        
        # Fast scroll to load content
        for i in range(6):
            driver.execute_script(f"window.scrollTo(0, {2000 * (i+1)});")
            time.sleep(1)
        
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        print("\n🎯 COMPREHENSIVE PICK-TO-ANALYSIS MAPPING:")
        
        # Get ALL picks and their positions
        pick_elements = driver.find_elements(By.CSS_SELECTOR, '.nfl-o-ranked-item.nfl-o-ranked-item--side-by-side')
        print(f"📋 Found {len(pick_elements)} total pick elements")
        
        # Get ALL analysis paragraphs and their positions
        all_paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p')
        analysis_paragraphs = []
        
        for i, para in enumerate(all_paragraphs):
            try:
                text = para.get_attribute('textContent').strip()
                location = para.location['y']
                if (text and len(text) > 50 and len(text) < 1000 and
                    any(keyword in text.lower() for keyword in ['quarterback', 'player', 'draft', 'team', 'offense', 'defense', 'potential', 'needs', 'season', 'franchise']) and
                    not text.startswith('Pick') and
                    '©' not in text and
                    'nfl.com' not in text.lower() and
                    'cookie' not in text.lower() and
                    'privacy' not in text.lower()):
                    analysis_paragraphs.append((location, text, i))
            except:
                continue
        
        analysis_paragraphs.sort(key=lambda x: x[0])  # Sort by Y position
        print(f"📊 Found {len(analysis_paragraphs)} analysis paragraphs")
        
        # Create pick info list
        picks_info = []
        for i, pick_element in enumerate(pick_elements, 1):
            try:
                pick_text = pick_element.get_attribute('textContent')
                lines = [line.strip() for line in pick_text.split('\n') if line.strip()]
                
                team_name = None
                player_name = None
                
                for line in lines:
                    if any(team in line.lower() for team in ['titans', 'browns', 'giants', 'patriots', 'raiders', 'jaguars', 'jets', 'panthers', 'saints', 'lions', 'cowboys', 'dolphins', 'colts', 'falcons', 'cardinals', 'bengals', 'vikings', 'buccaneers', 'broncos', 'chargers', 'steelers', 'packers', 'texans', 'rams', 'eagles', 'bills', 'chiefs', 'seahawks', 'commanders']):
                        team_name = line
                    elif len(line.split()) == 2 and line[0].isupper() and 'pick' not in line.lower():
                        player_name = line
                        break
                
                pick_location = pick_element.location['y']
                picks_info.append((i, team_name, player_name, pick_location))
            except:
                picks_info.append((i, "Unknown", "Unknown", 0))
        
        print(f"\n📋 PICK INFORMATION:")
        for pick_num, team, player, location in picks_info:
            team_str = team if team else "Unknown"
            player_str = player if player else "Unknown"
            print(f"   Pick {pick_num:2d}: {team_str:20s} | {player_str:15s} | Y:{location:4d}")
        
        print(f"\n📝 ANALYSIS PARAGRAPHS (in order):")
        for i, (location, text, para_idx) in enumerate(analysis_paragraphs):
            print(f"   {i+1:2d}. (Y:{location:4d}, Para#{para_idx:3d}) {text[:60]}...")
        
        print(f"\n🎯 ATTEMPTING TO CREATE PROPER MAPPING:")
        
        # Strategy: Create mapping by finding which analysis paragraph comes after each pick
        # and is before the next pick
        pick_to_analysis_mapping = {}
        
        for i, (pick_num, team, player, pick_location) in enumerate(picks_info):
            # Find the next pick's location for boundary
            next_pick_location = picks_info[i+1][3] if i+1 < len(picks_info) else float('inf')
            
            # Find analysis paragraphs that fall between this pick and the next pick
            relevant_analysis = []
            for location, text, para_idx in analysis_paragraphs:
                if pick_location < location < next_pick_location:
                    relevant_analysis.append((location, text, para_idx))
            
            pick_to_analysis_mapping[pick_num] = relevant_analysis
            
            team_str = team if team else "Unknown"
            player_str = player if player else "Unknown"
            print(f"\nPick {pick_num} ({team_str} - {player_str}):")
            print(f"   Pick location: Y:{pick_location}")
            print(f"   Next pick location: Y:{next_pick_location}")
            print(f"   Analysis candidates between picks:")
            
            if relevant_analysis:
                for j, (loc, text, para_idx) in enumerate(relevant_analysis):
                    print(f"      {j+1}. (Y:{loc}, Para#{para_idx}) {text[:80]}...")
            else:
                print("      ❌ No analysis found between this pick and next pick")
            
            # Show what would be the best choice
            if relevant_analysis:
                best_text = relevant_analysis[0][1]  # First analysis after pick
                print(f"   ✅ BEST CHOICE: {best_text[:100]}...")
            else:
                print(f"   ⚠️ NO ANALYSIS FOUND")
        
        print(f"\n📊 MAPPING SUMMARY:")
        print(f"   Total picks: {len(picks_info)}")
        print(f"   Total analysis: {len(analysis_paragraphs)}")
        
        picks_with_analysis = sum(1 for analyses in pick_to_analysis_mapping.values() if analyses)
        picks_without_analysis = len(picks_info) - picks_with_analysis
        
        print(f"   Picks with analysis: {picks_with_analysis}")
        print(f"   Picks without analysis: {picks_without_analysis}")
        
        # Check for analysis paragraphs that aren't between any picks
        used_paragraphs = set()
        for analyses in pick_to_analysis_mapping.values():
            for _, _, para_idx in analyses:
                used_paragraphs.add(para_idx)
        
        unused_paragraphs = []
        for location, text, para_idx in analysis_paragraphs:
            if para_idx not in used_paragraphs:
                unused_paragraphs.append((location, text, para_idx))
        
        print(f"   Unused analysis paragraphs: {len(unused_paragraphs)}")
        if unused_paragraphs:
            print(f"   These are likely intro/outro text:")
            for location, text, para_idx in unused_paragraphs[:5]:
                print(f"      Para#{para_idx}: {text[:60]}...")
        
        # Alternative strategy: Sequential mapping
        print(f"\n🔄 ALTERNATIVE: SEQUENTIAL MAPPING STRATEGY:")
        print("   Filtering out intro/outro paragraphs and mapping sequentially...")
        
        # Filter analysis paragraphs to remove intro/outro
        filtered_analysis = []
        for location, text, para_idx in analysis_paragraphs:
            # Skip paragraphs that are likely intro/outro
            if (location > picks_info[0][3] and  # After first pick
                location < picks_info[-1][3] + 2000 and  # Before way after last pick
                'finally the week' not in text.lower() and
                'trades that are struck' not in text.lower() and
                'in his final mock' not in text.lower() and
                'with round 1' not in text.lower()):
                filtered_analysis.append((location, text, para_idx))
        
        print(f"   Filtered analysis paragraphs: {len(filtered_analysis)}")
        
        # Create sequential mapping
        for i, (pick_num, team, player, pick_location) in enumerate(picks_info):
            if i < len(filtered_analysis):
                analysis_text = filtered_analysis[i][1]
                print(f"   Pick {pick_num:2d} → Analysis {i+1:2d}: {analysis_text[:60]}...")
            else:
                print(f"   Pick {pick_num:2d} → ❌ No analysis available")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    comprehensive_mapping_analysis() 