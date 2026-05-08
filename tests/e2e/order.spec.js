const { test, expect } = require('@playwright/test');

test('Place order from checkout', async ({ page }) => {
  await page.goto('http://localhost:5000/checkout');
});