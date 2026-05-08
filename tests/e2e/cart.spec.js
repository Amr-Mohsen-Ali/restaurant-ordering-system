const { test, expect } = require('@playwright/test');

test('Cart shows items and total', async ({ page }) => {
  await page.goto('http://localhost:5000/cart');
});