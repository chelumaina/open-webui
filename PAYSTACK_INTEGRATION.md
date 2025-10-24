# Paystack Integration Documentation

This document explains how to set up and use the Paystack payment integration for Open WebUI subscriptions.

## Features

- ✅ Paystack inline payment (popup)
- ✅ Paystack redirect payment (hosted page)
- ✅ Payment verification
- ✅ Subscription management
- ✅ Transaction history
- ✅ Webhook support
- ✅ TypeScript support
- ✅ Error handling
- ✅ Loading states

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in your backend directory and add your Paystack credentials:

```bash
# Paystack Configuration
PAYSTACK_SECRET_KEY=sk_test_your_secret_key_here
PAYSTACK_PUBLIC_KEY=pk_test_your_public_key_here
```

For production, replace with your live keys:
```bash
PAYSTACK_SECRET_KEY=sk_live_your_live_secret_key_here
PAYSTACK_PUBLIC_KEY=pk_live_your_live_public_key_here
```

### 2. Frontend Configuration

Update the Paystack public key in the subscription page:

```typescript
// In src/routes/subscription/+page.svelte
const PAYSTACK_PUBLIC_KEY = 'pk_test_your_paystack_public_key_here';
```

### 3. Database Setup

The payment integration includes database models for:
- `payment_transactions` - Store payment transaction records
- `user_subscriptions` - Store user subscription data

Run the backend to automatically create these tables.

### 4. Webhook Configuration

To receive real-time payment notifications:

1. In your Paystack dashboard, go to Settings > Webhooks
2. Add your webhook URL: `https://your-domain.com/api/v1/payments/webhook`
3. Select events: `charge.success`, `charge.failed`, etc.
4. Note the webhook secret for signature verification

## Usage

### Basic Payment Flow

1. User selects a subscription plan
2. Frontend calls `/api/v1/payments/initialize` with payment details
3. Backend creates a Paystack transaction and returns authorization URL
4. User is redirected to Paystack checkout page
5. After payment, user is redirected to verification page
6. Verification page calls `/api/v1/payments/verify/{reference}` to confirm payment
7. Backend updates subscription status and user permissions

### API Endpoints

#### Initialize Payment
```http
POST /api/v1/payments/initialize
Authorization: Bearer {token}
Content-Type: application/json

{
  "amount": 10.00,
  "currency": "USD",
  "plan_id": "basic",
  "plan_name": "Basic Plan",
  "callback_url": "https://your-domain.com/subscription/verify"
}
```

#### Verify Payment
```http
GET /api/v1/payments/verify/{reference}
Authorization: Bearer {token}
```

#### Get User Subscription
```http
GET /api/v1/payments/subscription
Authorization: Bearer {token}
```

#### Get User Transactions
```http
GET /api/v1/payments/transactions?limit=10&offset=0
Authorization: Bearer {token}
```

#### Webhook Endpoint
```http
POST /api/v1/payments/webhook
X-Paystack-Signature: {signature}
Content-Type: application/json

{
  "event": "charge.success",
  "data": {
    "reference": "ref_123456",
    "status": "success",
    ...
  }
}
```

## Component Usage

### PaystackCheckout Component

```svelte
<script>
  import PaystackCheckout from '$lib/components/payment/PaystackCheckout.svelte';
  
  function handlePaymentSuccess(event) {
    const { transaction, plan, planData } = event.detail;
    console.log('Payment successful:', transaction);
    // Handle successful payment
  }
  
  function handlePaymentCancel(event) {
    const { plan } = event.detail;
    console.log('Payment cancelled for:', plan);
    // Handle payment cancellation
  }
</script>

<PaystackCheckout
  planId="basic"
  paystackPublicKey="pk_test_your_public_key_here"
  disabled={false}
  on:paymentSuccess={handlePaymentSuccess}
  on:paymentCancel={handlePaymentCancel}
/>
```

### Subscription Plans Configuration

Plans are defined in `src/lib/utils/paystack.ts`:

```typescript
export const SUBSCRIPTION_PLANS = {
  basic: {
    name: 'Basic Plan',
    amount: 10, // $10
    currency: 'USD',
    plan_code: 'basic_plan',
    interval: 'monthly',
    features: [
      'Feature 1',
      'Feature 2',
      // ...
    ]
  },
  enterprise: {
    name: 'Enterprise Plan',
    amount: 20, // $20
    currency: 'USD',
    plan_code: 'enterprise_plan',
    interval: 'monthly',
    features: [
      'Everything in Basic',
      'Feature 3',
      'Feature 4',
      // ...
    ]
  }
};
```

## Currency Support

The integration supports multiple currencies. Currently configured for:
- USD (US Dollar)
- NGN (Nigerian Naira) - Paystack's native currency

To add more currencies, update the plans and ensure Paystack supports them in your account.

## Security Considerations

1. **Environment Variables**: Never expose secret keys in frontend code
2. **Webhook Verification**: Always verify webhook signatures
3. **Token Validation**: Validate user tokens on all API endpoints
4. **Amount Validation**: Validate payment amounts server-side
5. **Reference Uniqueness**: Ensure payment references are unique

## Testing

### Test Credentials

Use Paystack test credentials for development:
- Test Secret Key: `sk_test_...`
- Test Public Key: `pk_test_...`

### Test Cards

Paystack provides test cards for various scenarios:
- Success: `4084084084084081`
- Insufficient Funds: `4000000000000002`
- Declined: `4000000000000069`

## Error Handling

The integration includes comprehensive error handling:

- Network errors
- Invalid payment data
- Authentication failures
- Paystack API errors
- Database errors

All errors are logged and user-friendly messages are displayed.

## Customization

### Styling

The PaystackCheckout component uses Tailwind CSS classes that match Open WebUI's design system. Customize by modifying the component's style section.

### Payment Methods

Supported payment methods can be configured in the payment initialization:

```typescript
channels: ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']
```

### Success/Failure Pages

Create custom success and failure pages by implementing:
- `/subscription/success` - Payment success page
- `/subscription/failed` - Payment failure page

## Production Deployment

1. Replace test keys with live keys
2. Update webhook URLs to production domains
3. Enable SSL/HTTPS for all endpoints
4. Set up monitoring for payment failures
5. Configure backup webhook endpoints
6. Test with small amounts first

## Troubleshooting

### Common Issues

1. **Payment initialization fails**
   - Check Paystack credentials
   - Verify user authentication
   - Check network connectivity

2. **Webhook not received**
   - Verify webhook URL accessibility
   - Check signature verification
   - Review Paystack dashboard logs

3. **Payment verification fails**
   - Ensure reference parameter exists
   - Check payment status on Paystack dashboard
   - Verify database connection

### Debug Mode

Enable debug logging by setting log level to DEBUG in your environment.

## Support

For issues specific to this integration:
1. Check the browser console for frontend errors
2. Check backend logs for API errors
3. Review Paystack dashboard for payment status
4. Verify webhook delivery in Paystack dashboard

For Paystack-specific issues, consult:
- [Paystack Documentation](https://paystack.com/docs)
- [Paystack Support](https://paystack.com/support)

## Contributing

To contribute to this payment integration:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure TypeScript types are properly defined
5. Update this documentation
6. Submit a pull request

## License

This integration follows the same license as Open WebUI.