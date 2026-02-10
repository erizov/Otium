# Plan: Yandex Maps as Source for Maps and Images

## Goal

Use Yandex Maps as the primary source for:
1. **Maps** — already using static maps API (enhance if needed)
2. **Images** — search Yandex Maps by place name and extract high-quality photos

Driving force: **place name** (monastery/park/palace/metro station/museum/sculpture name).

## Current State

- **Maps**: Using `https://static-maps.yandex.ru/1.x/` with coordinates (lat/lon)
- **Images**: Manual Commons URLs in `data/*_image_urls.py` (one URL per image file)

## Approach

### Option A: Yandex Maps Web Scraping (Recommended)

Yandex Maps web pages contain photos for places. We can:
1. Search Yandex Maps by place name (e.g., "Красная площадь Москва")
2. Extract photo URLs from the place page HTML
3. Download and use those images

**Pros**: No API key needed, high-quality photos, many photos per place
**Cons**: HTML parsing, may need browser automation for JavaScript-rendered content

### Option B: Yandex Places API + Web Scraping

1. Use Yandex Geocoding API to find place by name → get coordinates/place ID
2. Construct Yandex Maps URL: `https://yandex.ru/maps/?text=PLACE_NAME&z=16`
3. Scrape photos from that page

**Pros**: More reliable place matching
**Cons**: Requires API key, still need scraping for photos

## Implementation Steps

### 1. Yandex Maps Search Script

**scripts/yandex_maps_images.py**:
- `search_place_by_name(name: str, city: str = "Москва") -> list[str]`:
  - Search Yandex Maps: `https://yandex.ru/maps/?text={name} {city}`
  - Extract photo URLs from page HTML (or use Playwright for JS-rendered content)
  - Return list of image URLs (prefer high-resolution)
- `get_place_images(name: str, city: str = "Москва", max_images: int = 4) -> list[str]`:
  - Call `search_place_by_name`, filter/rank images, return top N

**Requirements**:
- Use Playwright (already in requirements) for JavaScript-rendered pages
- Parse HTML for photo URLs (Yandex Maps photo structure)
- Handle rate limiting and errors gracefully

### 2. Integration into Workflow

**Option 1: Generate `*_image_urls.py` from Yandex Maps**
- Script: `scripts/generate_yandex_image_urls.py`
- For each guide, load items, call `get_place_images(name)` for each item
- Generate `data/<guide>_image_urls.py` with Yandex Maps URLs
- Run once to populate URLs, then commit

**Option 2: Dynamic fetching during download**
- Modify `scripts/download_images.py` or `scripts/build_pdf.py`
- If URL missing in `*_image_urls.py`, fetch from Yandex Maps on-the-fly
- Cache results

**Recommendation**: Option 1 (generate once, commit URLs) — more reliable, reproducible builds.

### 3. Update Image URL Structure

Keep current structure (`{slug}_1.jpg`, `{slug}_2.jpg`, etc.) but populate URLs from Yandex Maps instead of manual Commons URLs.

### 4. Fallback Strategy

- Primary: Yandex Maps images
- Fallback: Existing Commons URLs (if Yandex search fails or returns no images)
- Validation: Ensure at least 1 image per item (can mix sources)

## Technical Details

### Yandex Maps Photo URLs

Yandex Maps photos are typically:
- Thumbnails: `https://avatars.mds.yandex.net/get-images-cbir/...`
- Full size: Similar pattern, or direct URLs from photo viewer

**Strategy**: Use Playwright to:
1. Navigate to place page
2. Click "Photos" tab or scroll to photos section
3. Extract image URLs (prefer full-size)
4. Return list

### Example Flow

```python
from playwright.sync_api import sync_playwright

def get_yandex_place_images(name: str, city: str = "Москва") -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"https://yandex.ru/maps/?text={name} {city}"
        page.goto(url)
        # Wait for photos to load, extract URLs
        # Return list of image URLs
```

## Success Criteria

1. Script can search Yandex Maps by place name and extract 4+ photo URLs per place
2. Generated `*_image_urls.py` files contain Yandex Maps URLs
3. Images download successfully and display in PDFs
4. Fallback to Commons URLs if Yandex search fails
5. No breaking changes to existing workflow

## Future Enhancements

- Cache Yandex Maps results to avoid repeated searches
- Use Yandex Places API for better place matching (if API key available)
- Prefer photos that match place name semantically (future: CLIP/image recognition)
