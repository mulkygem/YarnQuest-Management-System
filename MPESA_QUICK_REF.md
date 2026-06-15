# M-Pesa Integration - Quick Reference

## 🚀 Quick Setup (5 minutes)

```bash
# 1. Install dependencies
pip install requests

# 2. Run database migration
python migrate_payments.py

# 3. Edit mpesa_config.py with your credentials
CONSUMER_KEY = "your_key_from_daraja"
CONSUMER_SECRET = "your_secret_from_daraja"
PASSKEY = "your_passkey_from_daraja"
```

## 📍 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/payment/initiate` | POST | Start payment process |
| `/payment/check-status` | POST | Check payment status |
| `/payment/callback` | POST | M-Pesa webhook callback |
| `/payment/success` | GET | Success page |
| `/payment/failed` | GET | Failure page |

## 📦 Request/Response Examples

### Initiate Payment
```bash
curl -X POST /payment/initiate \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "254708374149",
    "amount": 1000
  }'
```

**Response (Success):**
```json
{
  "success": true,
  "checkout_request_id": "abc123xyz",
  "customer_message": "Enter your M-Pesa PIN to complete this transaction"
}
```

### Check Status
```bash
curl -X POST /payment/check-status \
  -H "Content-Type: application/json" \
  -d '{"checkout_request_id": "abc123xyz"}'
```

## 🧪 Testing

### Sandbox Credentials
| Field | Value |
|-------|-------|
| Test Phone | 254708374149 |
| Test PIN | 12345 |
| Business Code | 174379 |
| URL | https://sandbox.safaricom.co.ke |

### Test Payment Flow
```
1. Add items to cart
2. Click "Pay with M-Pesa"
3. Enter: 708374149
4. Enter: 1000 (or any amount)
5. Submit
6. Receive STK prompt on test phone
7. Enter PIN: 12345
8. Payment completes!
```

## 🔐 Security Tips

```python
# Use environment variables in production
import os
CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
PASSKEY = os.getenv('MPESA_PASSKEY')

# Never commit credentials
# Add to .gitignore:
mpesa_config.py
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "Invalid Consumer Key" | Check Daraja credentials, remove spaces |
| "STK not showing" | Verify phone format (254XXXXXXXXX) |
| "Callback not received" | Use ngrok locally, verify callback URL |
| "Status not updating" | Check database connection |

## 📊 Database Tables

```sql
-- Orders table
CREATE TABLE orders (
  id INT PRIMARY KEY,
  user_id INT,
  total_amount DECIMAL(10,2),
  mpesa_receipt VARCHAR(20),
  status VARCHAR(20),
  created_at TIMESTAMP
);

-- Order items
CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT,
  item_id INT,
  created_at TIMESTAMP
);

-- Payment logs
CREATE TABLE payment_logs (
  id INT PRIMARY KEY,
  checkout_request_id VARCHAR(100),
  status VARCHAR(50),
  created_at TIMESTAMP
);
```

## 🔄 Payment Status Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Timeout/Rejected |
| 2 | Cancelled |
| 500 | Server Error |

## 📱 Phone Number Formats

```python
# Accepted formats (all converted to 254XXXXXXXXX):
"254708374149"    ✓
"0708374149"      ✓ (auto-converts to 254)
"+254708374149"   ✓ (+ removed)
"708374149"       ✓ (prepends 254)
```

## 🚢 Production Checklist

- [ ] Get production credentials from Daraja
- [ ] Update BASE_URL to `https://api.safaricom.co.ke`
- [ ] Update BUSINESS_SHORT_CODE to your code
- [ ] Configure SSL/HTTPS
- [ ] Update callback URLs
- [ ] Set environment variables
- [ ] Test with real payment
- [ ] Monitor payment logs
- [ ] Set up error alerts

## 📝 Key Files

| File | Purpose |
|------|---------|
| `mpesa_config.py` | Configuration (UPDATE THIS) |
| `mpesa_api.py` | API wrapper class |
| `app.py` | Flask routes |
| `cart.html` | Payment UI |
| `MPESA_SETUP.md` | Full documentation |

## 🔗 Useful Links

- [Daraja Portal](https://developer.safaricom.co.ke)
- [API Documentation](https://developer.safaricom.co.ke/apis)
- [Test Credentials](https://developer.safaricom.co.ke/sample-credentials-and-shortcodes)
- [Support](https://developer.safaricom.co.ke/contact-us)

## 💡 Tips

1. **Test First**: Always test in sandbox before production
2. **Format Properly**: Ensure phone numbers are 254XXXXXXXXX
3. **Amount Validation**: Check amount > 0
4. **Logging**: Log all payment attempts for debugging
5. **Callbacks**: Verify callback signatures from M-Pesa
6. **Retry Logic**: Implement retry for failed requests
7. **Timeouts**: Handle payment timeouts gracefully

## 🎯 Next Steps

1. ✅ Get Daraja credentials
2. ✅ Update `mpesa_config.py`
3. ✅ Run `python migrate_payments.py`
4. ✅ Test in sandbox
5. ✅ Deploy to production
6. ✅ Monitor transactions

## 🆘 Quick Help

```python
# Check access token
mpesa = MpesaAPI()
token = mpesa.get_access_token()
print(token)

# Test STK push
result = mpesa.initiate_stk_push(
    phone_number="254708374149",
    amount=1000,
    order_id="ORDER-123",
    description="Test"
)
print(result)

# Check payment status
status = mpesa.query_stk_status("checkout_request_id")
print(status)
```

---
**Last Updated**: June 2024
**Version**: 1.0
**Status**: ✅ Production Ready
