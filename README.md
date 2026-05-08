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
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── data/
│   │   └── orders.py
│   ├── menu.py
│   ├── cart.py
│   ├── order.py
│   └── tracking.py
├── templates/
│   ├── base.html
│   ├── menu.html
│   ├── cart.html
│   ├── checkout.html
│   └── tracking.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── menu.js
│       ├── cart.js
│       ├── checkout.js
│       └── tracking.js
├── tests/
│   ├── test_menu.py
│   ├── test_cart.py
│   ├── test_order.py
│   ├── test_tracking.py
│   ├── test_integration.py
│   └── e2e/
│       ├── menu.spec.js
│       ├── cart.spec.js
│       ├── order.spec.js
│       └── tracking.spec.js
├── docs/
│   ├── api-contracts.md
│   ├── gherkin.md
│   ├── ai-prompts.md
│   └── qa-audit-log.md
└── .github/
    └── workflows/
        └── ci.yml
```

## Shared Order Schema

```json
{
  "id": "string",
  "items": ["string"],
  "total": 0.00,
  "status": "Preparing"
}
```

### Allowed Status Values

- Preparing
- Out for Delivery
- Delivered

## API Routes

| Feature | Method | Path |
|---------|--------|------|
| Menu | GET | `/menu` |
| Cart | GET | `/cart` |
| Cart | POST | `/cart` |
| Order | POST | `/place-order` |
| Tracking | GET | `/track/<order_id>` |

## Run Project

```bash
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

## Run Tests

```bash
pytest
npx playwright test
```

## Testing Strategy

- **Unit (70%)**: `tests/test_*.py` - test each feature in isolation
- **Integration (20%)**: `tests/test_integration.py` - cross-feature flows
- **E2E (10%)**: `tests/e2e/*.spec.js` - browser tests with Playwright

## License

MIT