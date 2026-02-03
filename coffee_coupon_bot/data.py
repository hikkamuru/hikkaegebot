"""Data models and storage for coffee subscription cards."""
from dataclasses import dataclass
from typing import Optional
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta

STORAGE_FILE = Path(__file__).parent / "data" / "storage.json"

# Subscription duration in days
SUBSCRIPTION_DURATION_DAYS = 30

# Image URLs (Unsplash, free to use)
IMAGES = {
    "welcome": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800",
    "coffee_base": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800",
    "coffee_milk": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800",
    "coffee_all": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "success": "https://images.unsplash.com/photo-1511920170033-83939e383859?w=800",
    "my_cards": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800",
}


@dataclass
class SubscriptionCard:
    """Coffee subscription card (абонемент)."""
    id: str
    name: str
    description: str
    details: str  # What's included
    price: int  # in rubles
    image_url: str


@dataclass
class PurchasedCard:
    """User's purchased subscription card."""
    id: str
    card_id: str
    user_id: int
    code: str
    name: str
    used: bool = False
    purchase_date: str = ""  # Format: DD.MM.YYYY
    expiration_date: str = ""  # Format: DD.MM.YYYY


@dataclass
class PendingRequest:
    """Pending purchase request (awaiting admin confirmation)."""
    id: str
    user_id: int
    username: str
    full_name: str
    phone: str
    card_id: str
    card_name: str
    price: int


# Subscription cards catalog
SUBSCRIPTION_CARDS: list[SubscriptionCard] = [
    SubscriptionCard(
        id="baza",
        name="☕️ БАЗОВЫЙ",
        description="Эспрессо и американо",
        details="Эспрессо • Американо",
        price=1680,
        image_url="https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800",
    ),
    SubscriptionCard(
        id="milk",
        name="🥛 МОЛОЧНЫЙ",
        description="Эспрессо, американо, капучино, латте",
        details="Эспрессо • Американо • Капучино • Латте",
        price=2850,
        image_url="https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800",
    ),
    SubscriptionCard(
        id="all",
        name="🌟 ВСЕ ВКЛЮЧЕНО",
        description="Весь ассортимент кофейни",
        details="Полный ассортимент напитков",
        price=3580,
        image_url="https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    ),
]


def get_card_by_id(card_id: str) -> Optional[SubscriptionCard]:
    """Get card by ID."""
    for c in SUBSCRIPTION_CARDS:
        if c.id == card_id:
            return c
    return None


def _load_storage() -> dict:
    """Load storage from file."""
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STORAGE_FILE.exists():
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"purchases": [], "pending": []}


def _save_storage(data: dict) -> None:
    """Save storage to file."""
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_pending_request(user_id: int, username: str, full_name: str, phone: str, card: SubscriptionCard) -> PendingRequest:
    """Create pending request, return it."""
    data = _load_storage()
    if "pending" not in data:
        data["pending"] = []
    req_id = uuid.uuid4().hex[:12]
    req = {
        "id": req_id,
        "user_id": user_id,
        "username": username or "",
        "full_name": full_name or "Без имени",
        "phone": phone or "",
        "card_id": card.id,
        "card_name": card.name,
        "price": card.price,
    }
    data["pending"].append(req)
    _save_storage(data)
    return PendingRequest(**req)


def get_pending_request(req_id: str) -> Optional[PendingRequest]:
    """Get pending request by ID."""
    data = _load_storage()
    for r in data.get("pending", []):
        if r["id"] == req_id:
            return PendingRequest(**r)
    return None


def confirm_pending_request(req_id: str) -> Optional[PurchasedCard]:
    """Confirm payment, create purchase, remove from pending. Returns PurchasedCard or None."""
    data = _load_storage()
    pending = data.get("pending", [])
    for i, r in enumerate(pending):
        if r["id"] == req_id:
            card = get_card_by_id(r["card_id"])
            if not card:
                return None
            purchased = add_purchase(r["user_id"], card)
            data["pending"] = pending[:i] + pending[i + 1:]
            _save_storage(data)
            return purchased
    return None


def decline_pending_request(req_id: str) -> bool:
    """Decline pending request. Returns True if found."""
    data = _load_storage()
    pending = data.get("pending", [])
    for i, r in enumerate(pending):
        if r["id"] == req_id:
            data["pending"] = pending[:i] + pending[i + 1:]
            _save_storage(data)
            return True
    return False


def add_purchase(user_id: int, card: SubscriptionCard) -> PurchasedCard:
    """Add a purchase and return the purchased card."""
    data = _load_storage()
    code = f"CARD-{uuid.uuid4().hex[:8].upper()}"
    
    # Calculate dates
    now = datetime.now()
    purchase_date = now.strftime("%d.%m.%Y")
    expiration_date = (now + timedelta(days=SUBSCRIPTION_DURATION_DAYS)).strftime("%d.%m.%Y")
    
    purchase = {
        "id": str(uuid.uuid4()),
        "card_id": card.id,
        "user_id": user_id,
        "code": code,
        "name": card.name,
        "used": False,
        "purchase_date": purchase_date,
        "expiration_date": expiration_date,
    }
    data["purchases"].append(purchase)
    _save_storage(data)
    return PurchasedCard(**purchase)


def get_user_purchases(user_id: int) -> list[PurchasedCard]:
    """Get all purchases for a user."""
    data = _load_storage()
    result = []
    for p in data["purchases"]:
        if p["user_id"] != user_id:
            continue
        # Migrate old format (coupon_id -> card_id)
        p = dict(p)
        if "card_id" not in p and "coupon_id" in p:
            p["card_id"] = p.pop("coupon_id", "")
        # Add default dates if not present
        if "purchase_date" not in p:
            p["purchase_date"] = ""
        if "expiration_date" not in p:
            p["expiration_date"] = ""
        result.append(PurchasedCard(**{k: v for k, v in p.items() if k in ("id", "card_id", "user_id", "code", "name", "used", "purchase_date", "expiration_date")}))
    return result


def get_days_remaining(expiration_date: str) -> int:
    """Calculate days remaining until expiration."""
    if not expiration_date:
        return 0
    try:
        exp = datetime.strptime(expiration_date, "%d.%m.%Y")
        now = datetime.now()
        remaining = (exp - now).days
        return max(0, remaining)
    except:
        return 0
