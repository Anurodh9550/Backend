from decimal import Decimal
import re

from django.core.management.base import BaseCommand

from catalog.models import Collection, GoogleReview, Product


DETAIL_PRODUCTS = [
    {
        "slug": "opulent-neo",
        "title": "Opulent Neo Massage Chair",
        "subtitle": "Premium 4D robotic relaxation for home and office wellness.",
        "price": "Rs. 339,999.00",
        "old_price": "Rs. 399,000.00",
        "image": "/items/p1.jpg",
        "features": ["4D Intelligent Rollers", "Zero Gravity Recline", "Heat Therapy"],
    },
    {
        "slug": "enigma-plus",
        "title": "Enigma Plus Chair",
        "subtitle": "Smart massage programs with deep tissue and calf support.",
        "price": "Rs. 289,999.00",
        "old_price": "Rs. 349,000.00",
        "image": "/items/p3.jpg",
        "features": ["AI Body Scan", "Foot & Calf Care", "Bluetooth Controls"],
    },
    {
        "slug": "magic-plus",
        "title": "Magic Plus Advanced Chair",
        "subtitle": "Compact premium comfort with heat and zero gravity modes.",
        "price": "Rs. 98,999.00",
        "old_price": "Rs. 245,000.00",
        "image": "/p5.png",
        "features": ["Space Saving Design", "Heat Therapy", "Family Friendly"],
    },
    {
        "slug": "majestic-neo",
        "title": "Majestic Neo Zero Gravity",
        "subtitle": "Balanced full-body therapy with luxury recline comfort.",
        "price": "Rs. 210,999.00",
        "old_price": "Rs. 295,000.00",
        "image": "/items/p2.jpg",
        "features": ["Zero Gravity", "Air Compression Massage", "Back Relief Mode"],
    },
    {
        "slug": "eye-massager",
        "title": "Eye Massager",
        "subtitle": "Gentle eye care for stress reduction and quick relaxation.",
        "price": "Rs. 8,999.00",
        "old_price": "Rs. 12,999.00",
        "image": "/items/p1.jpg",
        "features": ["Heat Compress", "Vibration Therapy", "Portable Use"],
    },
    {
        "slug": "hand-massager",
        "title": "Hand Massager",
        "subtitle": "Targeted palm and finger relief after long work sessions.",
        "price": "Rs. 7,499.00",
        "old_price": "Rs. 10,499.00",
        "image": "/items/p2.jpg",
        "features": ["Air Pressure Massage", "Portable Build", "Easy Controls"],
    },
    {
        "slug": "massage-cushion",
        "title": "Massage Cushion",
        "subtitle": "Portable back and waist support for chair, car, or office use.",
        "price": "Rs. 5,999.00",
        "old_price": "Rs. 8,499.00",
        "image": "/items/p3.jpg",
        "features": ["Dual Node Massage", "Heat Option", "Multi-Use Design"],
    },
    {
        "slug": "eden-foot",
        "title": "Eden Foot Massager",
        "subtitle": "Comfortable foot care with rolling and kneading therapy.",
        "price": "Rs. 20,999.00",
        "old_price": "Rs. 28,999.00",
        "image": "/items/p1.jpg",
        "features": ["Kneading Rollers", "Relax Mode", "Deep Tissue Relief"],
    },
    {
        "slug": "alis-foot",
        "title": "Alis Foot Massager",
        "subtitle": "Compact massager for daily leg and foot relaxation.",
        "price": "Rs. 18,499.00",
        "old_price": "Rs. 24,999.00",
        "image": "/items/p2.jpg",
        "features": ["Compact Body", "Easy Cleaning", "Gentle Compression"],
    },
    {
        "slug": "sage-leg",
        "title": "Sage Leg Massager",
        "subtitle": "Relieve leg fatigue with dynamic compression and heat support.",
        "price": "Rs. 15,999.00",
        "old_price": "Rs. 21,999.00",
        "image": "/items/p3.jpg",
        "features": ["Leg Compression", "Heat Relaxation", "Adjustable Modes"],
    },
    {
        "slug": "cosset-leg",
        "title": "Cosset Leg Massager",
        "subtitle": "Advanced leg therapy for recovery and daily comfort.",
        "price": "Rs. 17,999.00",
        "old_price": "Rs. 23,999.00",
        "image": "/items/p1.jpg",
        "features": ["Calf Coverage", "Pressure Control", "Recovery Programs"],
    },
    {
        "slug": "minilux-back",
        "title": "Minilux Back Massager",
        "subtitle": "Portable back relaxation with focused shiatsu points.",
        "price": "Rs. 6,999.00",
        "old_price": "Rs. 9,999.00",
        "image": "/items/p2.jpg",
        "features": ["Shiatsu Nodes", "Heat Assist", "Office Friendly"],
    },
    {
        "slug": "smart-pad",
        "title": "Smart Pad Massager",
        "subtitle": "Lightweight portable massage pad for neck and back support.",
        "price": "Rs. 4,999.00",
        "old_price": "Rs. 7,499.00",
        "image": "/items/p3.jpg",
        "features": ["Portable Pad", "Quick Sessions", "Rechargeable"],
    },
]

HOME_PRODUCTS = [
    ("kila-opulant-neo", "Opulant Neo Massage Chair", "Premium 4D", "Rs. 339,999.00", "Rs. 399,000.00", "/items/p1.jpg", True),
    ("kila-royal-recline", "Royal Recline Massage Chair", "Luxury Series", "Rs. 289,999.00", "Rs. 349,000.00", "/items/p3.jpg", True),
    ("kila-majestic-neo", "Majestic Neo Zero Gravity", "Zero Gravity", "Rs. 210,999.00", "Rs. 295,000.00", "/items/p2.jpg", True),
    ("kila-serene-office", "Serene Office Smart Chair", "Office Comfort", "Rs. 161,499.00", "Rs. 195,000.00", "/items/p1.jpg", True),
    ("kila-magic-plus", "Magic Plus Advanced Chair", "Family Choice", "Rs. 98,999.00", "Rs. 245,000.00", "/p5.png", True),
    ("kila-elegant-body", "Elegant Full Body Chair", "Full Body", "Rs. 144,999.00", "Rs. 189,000.00", "/items/p2.jpg", True),
    ("kila-zen-heat", "Zen Heat Therapy Chair", "Heat Therapy", "Rs. 124,999.00", "Rs. 169,000.00", "/items/p3.jpg", True),
    ("kila-compact-lite", "Compact Lite Massage Chair", "Compact Series", "Rs. 84,999.00", "Rs. 119,000.00", "/items/p1.jpg", True),
    ("kila-regal-ai", "Regal AI Voice Chair", "AI Smart", "Rs. 399,999.00", "Rs. 449,000.00", "/items/p2.jpg", True),
    ("kila-dual-relief", "Dual Relief Leg Massage Chair", "Leg Care", "Rs. 174,999.00", "Rs. 219,000.00", "/items/p3.jpg", False),
]

REVIEWS = [
    {
        "name": "Sonu Prasad",
        "reviewed_at": "2023-01-10",
        "source_label": "Google",
        "rating": 5,
        "review_text": "Writing this review after using the chair for 10 days. I sit all day in the office and used to have body pain and stiffness. Robocura's Serene has helped me relax and smoothen my muscles.",
    },
    {
        "name": "Kailash Babu",
        "reviewed_at": "2020-08-20",
        "source_label": "Google",
        "rating": 5,
        "review_text": "Nice products",
    },
    {
        "name": "Sadaf Chaudhry",
        "reviewed_at": "2020-05-12",
        "source_label": "Google",
        "rating": 5,
        "review_text": "Tried in GIP Mall Noida. Amazing experience and felt refreshed",
    },
]


def money_to_decimal(value: str) -> Decimal:
    numeric = value.replace("Rs.", "").replace(",", "").strip()
    return Decimal(numeric)


def slugify_text(value: str) -> str:
    v = re.sub(r"[^a-z0-9\s-]+", "", value.lower().strip())
    v = re.sub(r"\s+", "-", v)
    v = re.sub(r"-{2,}", "-", v)
    return v.strip("-")


class Command(BaseCommand):
    help = "Seed frontend static catalog/reviews into backend DB."

    def handle(self, *args, **options):
        collections_count = 0
        products_count = 0
        reviews_count = 0

        for item in DETAIL_PRODUCTS:
            collection, created = Collection.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["title"],
                    "description": item["subtitle"],
                },
            )
            collections_count += int(created)

            _, prod_created = Product.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "collection": collection,
                    "name": item["title"],
                    "short_description": item["subtitle"],
                    "image": item["image"],
                    "price": money_to_decimal(item["price"]),
                    "old_price": money_to_decimal(item["old_price"]),
                    "product_features": item.get("features", []),
                    "in_stock": True,
                },
            )
            products_count += int(prod_created)

        for order, (
            slug,
            name,
            category,
            price,
            old_price,
            image,
            in_stock,
        ) in enumerate(HOME_PRODUCTS):
            collection_slug = slugify_text(category)
            collection, created = Collection.objects.update_or_create(
                slug=collection_slug,
                defaults={
                    "name": category,
                    "description": f"{category} products imported from frontend home page.",
                },
            )
            collections_count += int(created)

            _, prod_created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "collection": collection,
                    "name": name,
                    "short_description": f"{category} category product.",
                    "image": image,
                    "price": money_to_decimal(price),
                    "old_price": money_to_decimal(old_price),
                    "in_stock": in_stock,
                    "show_on_home": True,
                    "home_order": order,
                    "product_features": [
                        f"{category} comfort design",
                        "Advanced massage programs",
                        "Daily wellness support",
                    ],
                },
            )
            products_count += int(prod_created)

        for idx, review in enumerate(REVIEWS):
            _, created = GoogleReview.objects.update_or_create(
                name=review["name"],
                review_text=review["review_text"],
                defaults={
                    "rating": review["rating"],
                    "source_label": review["source_label"],
                    "reviewed_at": review["reviewed_at"],
                    "is_featured": True,
                    "display_order": idx,
                },
            )
            reviews_count += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Frontend data sync complete. New collections={collections_count}, new products={products_count}, new reviews={reviews_count}."
            )
        )
