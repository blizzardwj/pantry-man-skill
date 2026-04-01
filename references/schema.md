# Pantry Data Schema

Complete data structure definitions for pantry management.

## pantry.json

Food inventory organized by storage zone.

```json
{
  "meta": {
    "lastUpdated": "2026-04-01T17:45:00+08:00",
    "version": "1.0"
  },
  "zones": {
    "cold": {
      "name": "Refrigerator",
      "icon": "🧊",
      "items": []
    },
    "frozen": {
      "name": "Freezer",
      "icon": "❄️",
      "items": []
    },
    "ambient": {
      "name": "Ambient Storage",
      "icon": "📦",
      "items": []
    }
  }
}
```

### Item Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `item_a1b2c3` |
| `name` | string | Item name | `milk` |
| `quantity` | object | Amount with unit | `{"value": 1, "unit": "L"}` |
| `bought` | string | Purchase date | `2026-04-01` |
| `expires` | string | Expiry date | `2026-04-07` |
| `tags` | array | Categories for filtering | `["dairy", "breakfast"]` |
| `status` | string | fresh / expiring_soon / expired | `fresh` |

---

## shopping.json

Shopping list organized by category.

```json
{
  "meta": {
    "lastUpdated": "2026-04-01T17:45:00+08:00"
  },
  "categories": {
    "food": {
      "name": "Food",
      "icon": "🥬",
      "items": []
    },
    "daily": {
      "name": "Daily Items",
      "icon": "🧴",
      "items": []
    }
  }
}
```

### Item Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `shop_x9y8z7` |
| `name` | string | Item name | `tomato` |
| `quantity` | object | Amount with unit | `{"value": 3, "unit": "pcs"}` |
| `priority` | string | low / normal / high | `normal` |
| `added` | string | Date added to list | `2026-04-01` |
| `checked` | boolean | Marked as bought | `false` |
| `tags` | array | Categories for filtering | `["vegetable"]` |

---

## history/YYYY-MM.json

Purchase records organized by month.

```json
{
  "month": "2026-04",
  "records": [],
  "stats": {
    "totalSpent": 0.0,
    "recordCount": 0
  }
}
```

### Record Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `rec_m5n6p7` |
| `date` | string | Purchase date | `2026-04-01` |
| `items` | array | List of purchased items | See below |
| `total` | number | Total amount spent | `27.0` |
| `store` | string | Store name (optional) | `Hema` |
| `notes` | string | Additional notes (optional) | `weekend shopping` |

### Purchased Item Structure (within record.items)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Item name | `milk` |
| `quantity` | object | Amount with unit | `{"value": 1, "unit": "L"}` |
| `price` | number | Price of this item | `15.0` |

---

## Common Tags

### Food Categories
- `dairy` - Dairy products (milk, cheese, yogurt)
- `meat` - Meat (beef, pork, chicken)
- `seafood` - Fish and seafood
- `vegetable` - Vegetables
- `fruit` - Fruits
- `grain` - Grains, rice, pasta
- `condiment` - Sauces, spices, oil
- `snack` - Snacks
- `beverage` - Drinks
- `frozen` - Frozen foods

### Daily Items
- `cleaning` - Cleaning supplies
- `personal` - Personal care
- `kitchen` - Kitchen supplies
- `paper` - Paper products
