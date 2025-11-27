import re

def extract_movie_code(text: str) -> str:
    """Extract movie code from text using regex pattern"""
    if not text:
        return None
        
    patterns = [
        r'kod[: ]*(\d+)',
        r'#(\d+)',
        r'kino[: ]*(\d+)',
        r'film[: ]*(\d+)',
        r'(\d{3,6})'  # 3-6 xonali raqamlar
    ]
    
    text_lower = text.lower()
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            code = match.group(1)
            print(f"🔍 Extracted code: {code} from pattern: {pattern}")
            return code
    
    # Agar hech qanday pattern ishlamasa, faqat raqamlarni qidirish
    numbers = re.findall(r'\d{3,}', text)
    if numbers:
        print(f"🔍 Found numbers: {numbers}, using first: {numbers[0]}")
        return numbers[0]
    
    print(f"❌ No code found in text: {text[:100]}...")
    return None