# Restaurant Ordering System

Flask-based restaurant ordering system with modular features.

## Features

| Feature | Developer | Branch |
|---------|-----------|--------|
| Menu Browsing | Abdallah | `feature/abdallah-menu` |
| Cart | Hala | `feature/hala-cart` |
| Order Placement | Gaber | `feature/gaber-order` |
| Order Tracking | Amr | `feature/amr-tracking` |

## Project Structure

```
restaurant-project/
├── app.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data/orders.py
│   ├── menu.py
│   ├── cart.py
│   ├── order.py
│   └── tracking.py
├── templates/
├── static/
├── tests/
├── docs/
└── .github/workflows/ci.yml
```

## Shared Order Schema

```json
{
  "id": "string",
  "items": ["string"],
  "total": 0.00,
  "status": "Preparing" | "Out for Delivery" | "Delivered"
}
```

## API Routes

| Feature | Method | Path |
|---------|--------|------|
| Menu | GET | `/menu` |
| Cart | GET/POST | `/cart` |
| Order | POST | `/place-order` |
| Tracking | GET | `/track/<id>` |

## Setup

```bash
pip install -r requirements.txt
pytest
```

## Testing

- Unit tests: `tests/test_*.py`
- Integration: `tests/test_integration.py`
- E2E: `tests/e2e/*.spec.js`

## License

MIT