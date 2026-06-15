# Payment Integration - Fix for "Failed to Access Token" Error

## ✅ What Was Fixed

You were getting **"Failed to access token"** because the M-Pesa credentials in `mpesa_config.py` were not set. They were still placeholder values:

```python
'CONSUMER_KEY': 'YOUR_CONSUMER_KEY',        # ❌ Not set
'CONSUMER_SECRET': 'YOUR_CONSUMER_SECRET',  # ❌ Not set
'PASSKEY': 'YOUR_PASSKEY',                  # ❌ Not set
```

## ✅ What I Added

1. **Better Error Handling** - The app now detects when credentials are missing and shows a clear error message
2. **Setup Instructions Page** - A dedicated page showing step-by-step setup instructions at `/mpesa/setup`
3. **Terminal Logging** - The Flask terminal now shows helpful error messages
4. **User-Friendly Error Messages** - The cart page shows exactly what's needed to get M-Pesa working

## 🚀 How to Fix It

### Step 1: Get Your Credentials from Daraja

1. Go to https://developer.safaricom.co.ke
2. Sign up or log in to your account
3. Click "Create App" and fill in:
   - **App Name:** YarnQuest Payments
   - **Description:** M-Pesa payment processing for online yarn shop
4. Copy your **Consumer Key** and **Consumer Secret**
5. Find "Lipa Na M-Pesa Online" and enable it
6. Copy the **Passkey** you receive

### Step 2: Update mpesa_config.py

Open `mpesa_config.py` and update these lines:

```python
MPESA_CONFIG = {
    'CONSUMER_KEY': 'YOUR_REAL_CONSUMER_KEY_HERE',          # ✅ Replace
    'CONSUMER_SECRET': 'YOUR_REAL_CONSUMER_SECRET_HERE',    # ✅ Replace
    'BUSINESS_SHORT_CODE': '174379',                        # Keep for testing
    'PASSKEY': 'YOUR_REAL_PASSKEY_HERE',                    # ✅ Replace
    # ... rest stays the same
}
```

**Example** (with fake keys):
```python
MPESA_CONFIG = {
    'CONSUMER_KEY': 'abc123xyz789DEF',
    'CONSUMER_SECRET': 'xyzDEF456ABC789',
    'BUSINESS_SHORT_CODE': '174379',
    'PASSKEY': 'abc123xyz789!@#$%^',
    # ...
}
```

### Step 3: Restart Your Flask App

1. Stop the current app (press CTRL+C in the terminal)
2. Run `python app.py` again
3. The app should start without errors

### Step 4: Test the Payment

1. Go to http://127.0.0.1:5000
2. Add items to cart
3. Go to cart page
4. Click "Pay with M-Pesa"
5. Enter phone: `708374149` (for test)
6. Click Pay

**In sandbox mode**, you'll get an STK push on your test phone (or see a success message).

## 🧪 Testing

### Test Credentials (Sandbox)
- **Phone:** 254708374149
- **PIN:** 12345
- **Amount:** Any amount (won't be charged)

### What to expect:
1. Click "Pay with M-Pesa"
2. Modal appears asking for phone number
3. Enter `708374149`
4. Click Pay
5. STK push sent message appears
6. Payment completes (or timeout)

## 📊 Error Messages - What They Mean

### "M-Pesa Setup Required"
→ Your credentials are still set to placeholder values
→ Follow the "Get Your Credentials" steps above

### "Failed to access token"
→ Either credentials are wrong, or network issue
→ Check that you copied credentials correctly
→ Make sure you're in the right app in Daraja portal

### "STK push sent but no response"
→ This is normal in sandbox - payment may timeout
→ In production, you'll get real M-Pesa prompts

## 🔗 Useful Links

- **Daraja Portal:** https://developer.safaricom.co.ke
- **API Documentation:** https://developer.safaricom.co.ke/docs
- **Sample Credentials:** https://developer.safaricom.co.ke/sample-credentials-and-shortcodes
- **Support:** support@daraja.safaricom.co.ke

## ✅ Verification Checklist

- [ ] Created app in Daraja Portal
- [ ] Got Consumer Key
- [ ] Got Consumer Secret
- [ ] Got Passkey from "Lipa Na M-Pesa Online"
- [ ] Updated all three values in `mpesa_config.py`
- [ ] Restarted Flask app
- [ ] Terminal shows "Running on http://127.0.0.1:5000"
- [ ] No errors in terminal
- [ ] Can access payment setup page at `/mpesa/setup`

## 📝 Files Updated

1. **app.py** - Added credential check in `/payment/initiate` route
2. **mpesa_api.py** - Better error logging for debugging
3. **cart.html** - Shows helpful error messages with setup link
4. **mpesa_setup.html** - New dedicated setup guide page

## 🆘 Still Getting Errors?

1. **Check the terminal output** - Flask terminal shows detailed error messages
2. **Verify credentials** - Make sure no extra spaces before/after keys
3. **Check app selection** - Make sure you're in the right app in Daraja
4. **Restart the app** - Always restart after updating config.py

## 📱 Production Deployment

When ready for production:

1. In Daraja, switch app to production
2. Get production Consumer Key/Secret
3. Update mpesa_config.py:
   ```python
   'BASE_URL': 'https://api.safaricom.co.ke',  # Change from sandbox
   'CONSUMER_KEY': 'YOUR_PROD_KEY',
   'CONSUMER_SECRET': 'YOUR_PROD_SECRET',
   'PASSKEY': 'YOUR_PROD_PASSKEY',
   ```
4. Update callback URLs to use your domain
5. Test with real M-Pesa account
6. Deploy

---

**Status:** ✅ Error handling and setup page added
**Next Step:** Follow the setup steps above to add your credentials
**Support:** Check the setup guide at `/mpesa/setup` in your app
