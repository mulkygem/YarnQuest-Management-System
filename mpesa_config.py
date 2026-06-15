"""
M-Pesa Daraja API Configuration
Safaricom M-Pesa Integration for Lipa Na M-Pesa Online
"""

# M-Pesa Configuration - Get these from Safaricom Daraja Portal
MPESA_CONFIG = {
    # Daraja API Credentials (from your sandbox/live app on developer.safaricom.co.ke)
    'CONSUMER_KEY': 'YOUR_CONSUMER_KEY',  # Replace with your actual key
    'CONSUMER_SECRET': 'YOUR_CONSUMER_SECRET',  # Replace with your actual secret
    
    # Business Information
    'BUSINESS_SHORT_CODE': '174379',  # Your Safaricom business code (test: 174379)
    'PASSKEY': 'YOUR_PASSKEY',  # Your Lipa Na M-Pesa Online Passkey
    
    # API Endpoints
    'BASE_URL': 'https://sandbox.safaricom.co.ke',  # Use https://api.safaricom.co.ke for production
    'AUTH_URL': '/oauth/v1/generate?grant_type=client_credentials',
    'STK_PUSH_URL': '/mpesa/stkpush/v1/processrequest',
    'QUERY_URL': '/mpesa/stkpushquery/v1/query',
    'TRANSACTION_STATUS_URL': '/mpesa/transactionstatus/v1/query',
    
    # Callback URLs
    'CALLBACK_URL': 'https://yourserver.com/api/mpesa/callback',  # Update with your domain
    'TIMEOUT_URL': 'https://yourserver.com/api/mpesa/timeout',  # Update with your domain
    
    # For testing - use 254708374149 (test number)
    'TEST_PHONE': '254708374149',
}

# Instructions for setup:
"""
1. Go to https://developer.safaricom.co.ke
2. Sign up and create an account
3. Create a Sandbox App to get Consumer Key and Secret
4. Create another app for STK Push to get Passkey
5. Update CONSUMER_KEY, CONSUMER_SECRET, and PASSKEY above
6. For production, update BASE_URL to https://api.safaricom.co.ke
7. Update CALLBACK_URL and TIMEOUT_URL with your actual domain
8. Keep BUSINESS_SHORT_CODE as 174379 for testing, replace for production
"""
