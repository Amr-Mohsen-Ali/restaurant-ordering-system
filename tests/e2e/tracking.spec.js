const { test, expect } = require('@playwright/test');

test('Track order status', async ({ page }) => {
  await page.goto('http://localhost:5000/tracking');
});