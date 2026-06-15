# M-Pesa Payment Integration Setup Guide

## Overview
This guide helps you set up M-Pesa payment integration for YarnQuest using the Safaricom Daraja API (Lipa Na M-Pesa Online).

## Prerequisites
- Safaricom M-Pesa account
- Access to Daraja Developer Portal
- HTTPS domain for production (required by M-Pesa)
- Python 3.7+ with Flask

## Step 1: Create Daraja Account
1. Go to https://developer.safaricom.co.ke
2. Click **Sign Up** and create an account
3. Verify your email address
4. Log in to your Daraja account

## Step 2: Create Sandbox Application
1. In Daraja dashboard, click **Create App**
2. Fill in app details:
   - **App Name**: YarnQuest Payments
   - **App Description**: M-Pesa payment processing for online yarn shop
3. Click **Create**
4. You'll get:
   - **Consumer Key**
   - **Consumer Secret**
   
   Save these credentials!

## Step 3: Enable Lipa Na M-Pesa Online
1. In your app, go to **API Keys** section
2. Look for "Lipa Na M-Pesa Online"
3. Click **Enable**
4. You'll get a **Passkey** - save this!

## Step 4: Update Configuration
Edit `mpesa_config.py` and update:

```python
MPESA_CONFIG = {
    'CONSUMER_KEY': 'YOUR_CONSUMER_KEY',      # From Daraja
    'CONSUMER_SECRET': 'YOUR_CONSUMER_SECRET', # From Daraja
    'BUSINESS_SHORT_CODE': '174379',           # Keep for testing
    'PASSKEY': 'YOUR_PASSKEY',                 # From Daraja
    'BASE_URL': 'https://sandbox.safaricom.co.ke',  # For testing
    ...
}
```

## Step 5: Set Up Callback URLs
1. In Daraja app settings, configure:
   - **Callback URL**: `https://yourdomain.com/payment/callback`
   - **Timeout URL**: `https://yourdomain.com/payment/timeout`

For testing locally:
- Use ngrok to expose your local server: `ngrok http 5000`
- Update callback URLs with ngrok URL

## Step 6: Install Dependencies
```bash
pip install requests
```

This is already in your Flask dependencies.

## Step 7: Create Database Tables
Run the migration script:

```bash
python migrate_payments.py
```

This creates:
- `orders` table - stores order information
- `order_items` table - stores items in each order
- `payment_logs` table - tracks payment attempts (for debugging)

## Step 8: Test Integration

### In Sandbox Mode:
Use test credentials:
- **Phone**: 254708374149 (Safaricom test number)
- **Amount**: Any amount (won't be charged)
- **PIN**: 12345 (test PIN)

### Test Flow:
1. Add items to cart
2. Click "Pay with M-Pesa"
3. Enter test phone number: 708374149
4. Enter amount
5. You should receive STK push prompt
6. Enter PIN: 12345
7. Payment should complete

## Step 9: Prepare for Production

### Get Live Credentials:
1. In Daraja, upgrade to production app
2. Update `mpesa_config.py`:

```python
'BASE_URL': 'https://api.safaricom.co.ke',  # Change from sandbox
'CONSUMER_KEY': 'YOUR_PROD_KEY',
'CONSUMER_SECRET': 'YOUR_PROD_SECRET',
'PASSKEY': 'YOUR_PROD_PASSKEY',
```

### Update Business Code:
- Request your actual business code from Safaricom
- Replace `174379` with your code

### HTTPS Setup:
- Install SSL certificate on your domain
- Update callback URLs to use HTTPS
- Ensure server is publicly accessible

## API Endpoints Created

### `/payment/initiate` (POST)
Initiates M-Pesa STK push
- **Body**: `{ phone: "254XXXXXXXXX", amount: 1000 }`
- **Response**: `{ success: true, checkout_request_id: "..." }`

### `/payment/check-status` (POST)
Checks payment status
- **Body**: `{ checkout_request_id: "..." }`
- **Response**: M-Pesa API response with status

### `/payment/callback` (POST)
Webhook for M-Pesa payment confirmation
- Automatically processes successful payments
- Creates order records in database
- Clears cart after successful payment

### `/payment/success`
Success page shown after payment

### `/payment/failed`
Failure page if payment is cancelled

## File Structure
```
yarnquest/
├── mpesa_config.py          # M-Pesa configuration
├── mpesa_api.py             # M-Pesa API wrapper class
├── migrate_payments.py       # Database migration script
├── app.py                   # Main app with new payment routes
├── templates/
│   ├── cart.html            # Updated with payment modal
│   ├── payment_success.html  # Success page
│   └── payment_failed.html   # Failed page
└── requirements.txt
```

## Troubleshooting

### "Invalid Consumer Key/Secret"
- Verify credentials are copied correctly from Daraja
- Check for extra spaces in credentials
- Make sure you're using sandbox keys for testing

### "Callback not received"
- Ensure callback URL is publicly accessible
- Check firewall/router settings
- Verify HTTPS is working (use ngrok for testing)
- Check M-Pesa logs in Daraja dashboard

### "STK not showing"
- Verify phone number format (254XXXXXXXXX)
- Check M-Pesa account balance on test phone
- Ensure amount is valid (not 0 or negative)

### "Payment status not updating"
- Check database connection
- Verify callback URL is correct
- Check server logs for errors

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** in production:
   ```python
   MPESA_CONFIG = {
       'CONSUMER_KEY': os.environ.get('MPESA_CONSUMER_KEY'),
       'CONSUMER_SECRET': os.environ.get('MPESA_CONSUMER_SECRET'),
       ...
   }
   ```

3. **Validate all inputs** server-side
4. **Use HTTPS** always in production
5. **Log all transactions** for audit trail
6. **Implement rate limiting** on payment endpoints
7. **Verify callback signatures** from M-Pesa

## Testing Checklist
- [ ] Consumer Key and Secret added to config
- [ ] Passkey added to config
- [ ] Database migration run successfully
- [ ] Test payment initiated with 254708374149
- [ ] STK push received on test phone
- [ ] Payment completed successfully
- [ ] Order created in database
- [ ] Cart cleared after payment
- [ ] Success page displayed
- [ ] Email receipt sent (if configured)

## Support
- Daraja Documentation: https://developer.safaricom.co.ke/docs
- M-Pesa API: https://developer.safaricom.co.ke/apis
- Contact Safaricom Support: support@daraja.safaricom.co.ke

## Next Steps
1. Complete all steps above
2. Test thoroughly in sandbox mode
3. Request production credentials from Safaricom
4. Deploy to production with HTTPS
5. Update callback URLs to production domain
6. Monitor transactions for any issues
