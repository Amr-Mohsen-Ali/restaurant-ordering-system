const { test, expect } = require('@playwright/test');

test('Menu displays items', async ({ page }) => {
  await page.goto('http://localhost:5000/menu');
});