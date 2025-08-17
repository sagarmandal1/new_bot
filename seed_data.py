"""
ডাটাবেস সিড স্ক্রিপ্ট - Sample Data Seeder
Database Seed Script - Sample Data Seeder
"""

from config.database import db, Quote
from datetime import datetime

def seed_quotes():
    """Add sample motivational quotes to database"""
    
    quotes_data = [
        {
            'text_bn': 'সফলতা আসে ধৈর্য এবং কঠিন পরিশ্রমের মাধ্যমে।',
            'text_en': 'Success comes through patience and hard work.',
            'author_bn': 'জনপ্রিয় প্রবাদ',
            'author_en': 'Popular Proverb',
            'category': 'success'
        },
        {
            'text_bn': 'প্রতিটি নতুন দিন একটি নতুন সুযোগ।',
            'text_en': 'Every new day is a new opportunity.',
            'author_bn': 'অজানা',
            'author_en': 'Unknown',
            'category': 'motivation'
        },
        {
            'text_bn': 'স্বপ্ন দেখুন, পরিকল্পনা করুন, কাজ করুন।',
            'text_en': 'Dream, plan, work.',
            'author_bn': 'প্রেরণাদায়ক',
            'author_en': 'Inspirational',
            'category': 'planning'
        },
        {
            'text_bn': 'অসুবিধাই আপনাকে শক্তিশালী করে তোলে।',
            'text_en': 'Difficulties make you stronger.',
            'author_bn': 'জীবনের শিক্ষা',
            'author_en': 'Life Lesson',
            'category': 'strength'
        },
        {
            'text_bn': 'আজকের ছোট প্রচেষ্টা আগামীর বড় সাফল্য।',
            'text_en': "Today's small effort is tomorrow's big success.",
            'author_bn': 'সফলতার মন্ত্র',
            'author_en': 'Success Mantra',
            'category': 'effort'
        },
        {
            'text_bn': 'জ্ঞানই শক্তি, শিক্ষাই আলো।',
            'text_en': 'Knowledge is power, education is light.',
            'author_bn': 'শিক্ষামূলক',
            'author_en': 'Educational',
            'category': 'education'
        },
        {
            'text_bn': 'ভালো কাজে দেরি করবেন না।',
            'text_en': 'Do not delay in doing good work.',
            'author_bn': 'নৈতিক শিক্ষা',
            'author_en': 'Moral Teaching',
            'category': 'ethics'
        },
        {
            'text_bn': 'একতাই বল, সংঘবদ্ধতাই শক্তি।',
            'text_en': 'Unity is strength, togetherness is power.',
            'author_bn': 'সামাজিক শিক্ষা',
            'author_en': 'Social Teaching',
            'category': 'unity'
        },
        {
            'text_bn': 'সময়ই অর্থ, সময়ের সদ্ব্যবহার করুন।',
            'text_en': 'Time is money, use time wisely.',
            'author_bn': 'সময়ের মূল্য',
            'author_en': 'Value of Time',
            'category': 'time'
        },
        {
            'text_bn': 'নিজের উপর বিশ্বাস রাখুন।',
            'text_en': 'Believe in yourself.',
            'author_bn': 'আত্মবিশ্বাস',
            'author_en': 'Self Confidence',
            'category': 'confidence'
        }
    ]
    
    try:
        with db.get_session() as session:
            # Check if quotes already exist
            existing_quotes = session.query(Quote).count()
            
            if existing_quotes == 0:
                for quote_data in quotes_data:
                    quote = Quote(
                        text_bn=quote_data['text_bn'],
                        text_en=quote_data['text_en'],
                        author_bn=quote_data['author_bn'],
                        author_en=quote_data['author_en'],
                        category=quote_data['category'],
                        is_active=True,
                        usage_count=0,
                        created_at=datetime.utcnow()
                    )
                    session.add(quote)
                
                session.commit()
                print(f"✅ Added {len(quotes_data)} motivational quotes to database!")
            else:
                print(f"ℹ️ Database already contains {existing_quotes} quotes, skipping seed.")
                
    except Exception as e:
        print(f"❌ Error seeding quotes: {e}")

def main():
    """Main seeder function"""
    print("🌱 Seeding database with sample data...")
    
    # Create tables
    db.create_tables()
    
    # Seed quotes
    seed_quotes()
    
    print("✅ Database seeding completed!")

if __name__ == "__main__":
    main()