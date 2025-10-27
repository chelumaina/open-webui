// Paystack integration utilities
import { get } from 'svelte/store';
import { user } from '$lib/stores';

export interface PaystackConfig {
	publicKey: string;
	currency?: string;
	environment?: 'test' | 'live';
}

export interface PaymentData {
	amount: number; // in kobo (smallest currency unit)
	email: string;
	currency?: string;
	group_id?: string;
	reference?: string;
	callback_url?: string;
	plan?: string;
	channels?: string[];
	metadata?: Record<string, any>;
	subaccount?: string;
	transaction_charge?: number;
	bearer?: 'account' | 'subaccount';
}

export interface PaystackResponse {
	success: boolean;
	message: string;
	data?: {
		authorization_url: string;
		access_code: string;
		reference: string;
	};
}

export class PaystackPayment {
	private config: PaystackConfig;
	private scriptLoaded: boolean = false;

	constructor(config: PaystackConfig) {
		this.config = {
			currency: 'USD',
			environment: 'test',
			...config
		};
	}

	/**
	 * Load Paystack inline script
	 */
	private async loadPaystackScript(): Promise<void> {
		if (this.scriptLoaded || window.PaystackPop) {
			return;
		}

		return new Promise((resolve, reject) => {
			const script = document.createElement('script');
			script.src = 'https://js.paystack.co/v1/inline.js';
			script.onload = () => {
				this.scriptLoaded = true;
				resolve();
			};
			script.onerror = () => reject(new Error('Failed to load Paystack script'));
			document.head.appendChild(script);
		});
	}

	/**
	 * Generate a unique reference
	 */
	private generateReference(): string {
		const timestamp = Date.now();
		const randomStr = Math.random().toString(36).substring(2, 8);
		return `ref_${timestamp}_${randomStr}`;
	}

	/**
	 * Convert amount to kobo (Paystack expects amount in smallest currency unit)
	 */
	private convertToKobo(amount: number): number {
		return Math.round(amount * 100);
	}

	/**
	 * Initialize payment with Paystack Popup
	 */
	async initializePayment(
		paymentData: Omit<PaymentData, 'reference'>,
		onSuccess?: (transaction: any) => void,
		onCancel?: () => void
	): Promise<void> {
		try {
			await this.loadPaystackScript();

			const reference = this.generateReference();
			
			const config = {
				key: this.config.publicKey,
				email: paymentData.email,
				amount: this.convertToKobo(paymentData.amount),
				currency: paymentData.currency || this.config.currency,
				ref: reference,
				metadata: {
					...paymentData.metadata,
					custom_fields: [
						{
							display_name: "Plan",
							variable_name: "plan",
							value: paymentData.plan || "subscription"
						}
					]
				},
				channels: paymentData.channels || ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer'],
				callback: (response: any) => {
					if (onSuccess) {
						onSuccess(response);
					}
				},
				onClose: () => {
					if (onCancel) {
						onCancel();
					}
				}
			};

			const handler = window.PaystackPop.setup(config);
			handler.openIframe();
		} catch (error) {
			console.error('Paystack payment initialization failed:', error);
			throw error;
		}
	}

	/**
	 * Verify payment transaction
	 */
	async verifyPayment(reference: string): Promise<any> {
		try {
			// This would typically be done on your backend
			// Here's a basic client-side verification approach
			const response = await fetch(`https://api.paystack.co/transaction/verify/${reference}`, {
				method: 'GET',
				headers: {
					'Authorization': `Bearer ${this.config.publicKey}`,
					'Content-Type': 'application/json',
				},
			});

			if (!response.ok) {
				throw new Error('Payment verification failed');
			}

			const data = await response.json();
			return data;
		} catch (error) {
			console.error('Payment verification error:', error);
			throw error;
		}
	}

	/**
	 * Redirect to Paystack checkout page
	 */
	async redirectToCheckout(paymentData: Omit<PaymentData, 'reference'>): Promise<void> {
		try {
			const reference = this.generateReference();
			
			const payload = {
				amount: paymentData.amount,
				currency: paymentData.currency || this.config.currency,
				group_id: paymentData.group_id,
				plan_id: paymentData.plan || 'unknown',
				plan_name: paymentData.metadata?.plan_name || 'Subscription',
				callback_url: paymentData.callback_url,
			};

			// Use our backend API to initialize the transaction
			const { initializePayment } = await import('$lib/apis/payments');
			
			if (!localStorage.token) {
				throw new Error('User not authenticated');
			}

			const response = await initializePayment(localStorage.token, payload);
			
			if (response.success && response.data?.authorization_url) {
				window.location.href = response.data.authorization_url;
			} else {
				throw new Error(response.message || 'Payment initialization failed');
			}
		} catch (error) {
			console.error('Redirect to checkout failed:', error);
			throw error;
		}
	}
}

/**
 * Create a Paystack payment instance
 */
export function createPaystackPayment(publicKey: string, options?: Partial<PaystackConfig>): PaystackPayment {
	return new PaystackPayment({
		publicKey,
		...options
	});
}

/**
 * Plan configurations for subscription plans
 */
export const SUBSCRIPTION_PLANS = {
	basic: {
		name: 'Basic Plan',
		amount: 5, // $10
		currency: 'USD',
		plan_code: 'basic_plan',
		group_id: '6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98',
		interval: 'monthly',
		features: [
			'Coverage: Basic statutes + case law',
			'Jurisdiction-ready citations with paragraph anchors',
			'Expanded messaging and uploads',
			'Expanded and faster image creation',
			'Longer memory and context',
			'Limited deep research',
			'10K API Calls / month',
			'Up to 8K context tokens / request',
			'20 requests / minute rate limit',
			'Up to 2GB knowledge index (RAG) storage',
			'Upload: 10MB per file, 2GB total',
			'Q&A with inline citations',
			'Basic semantic search over laws & cases',
			'PDF/Word ingestion (OCR optional)',
		]
	},
	enterprise: {
		name: 'Enterprise Plan',
		amount: 10, // $20
		currency: 'USD',
		plan_code: 'enterprise_plan',
		interval: 'monthly',
		group_id: '8ca4c096-2b16-4e19-9586-4a162448fd63',
		features: [
			"Everything in Basic",
			'Coverage: Comprehensive acts, laws, court decisions, gazette notices, and cases',
			'Daily content updates & versioned knowledge base',
			'Citations with source-location deep links',
			'Unlimited API Calls (fair use; custom SLAs)',
			'Up to 200K context tokens / request (long-context endpoints)',
			'Custom per-minute/second rate limits',
			'Scalable knowledge index (100GB+; dedicated vector store)',
			'Expanded messaging and uploads',
			'Expanded and faster image creation',
			'Expanded memory and context',
		]
	},
	enterprise_plus: {
		name: 'Enterprise Plus Plan',
		amount: 20, // $20
		currency: 'USD',
		plan_code: 'enterprise_plus_plan',
		interval: 'monthly',
		group_id: '8ca4c096-2b16-4e19-9586-4a162448fd63',
		features: [
			"Everything in Basic",
			'Coverage: Comprehensive acts, laws, court decisions, gazette notices, and cases',
			'Daily content updates & versioned knowledge base',
			'Citations with source-location deep links',
			'Unlimited API Calls (fair use; custom SLAs)',
			'Up to 200K context tokens / request (long-context endpoints)',
			'Custom per-minute/second rate limits',
			'Scalable knowledge index (100GB+; dedicated vector store)',
			'Expanded messaging and uploads',
			'Expanded and faster image creation',
			'Expanded memory and context',
		]
	},
	enterprise3: {
		name: 'Enterprise Plan',
		amount: 20, // $20
		currency: 'USD',
		plan_code: 'enterprise_plan',
		interval: 'monthly',
		group_id: '8ca4c096-2b16-4e19-9586-4a162448fd63',
		features: [
			"Everything in Basic",
			'Coverage: Comprehensive acts, laws, court decisions, gazette notices, and cases',
			'Daily content updates & versioned knowledge base',
			'Citations with source-location deep links',
			'Unlimited API Calls (fair use; custom SLAs)',
			'Up to 200K context tokens / request (long-context endpoints)',
			'Custom per-minute/second rate limits',
			'Scalable knowledge index (100GB+; dedicated vector store)',
			'Expanded messaging and uploads',
			'Expanded and faster image creation',
			'Expanded memory and context',
		]
	}
};

/**
 * Get user email from store or fallback
 */
export function getUserEmail(): string {
	const currentUser = get(user);
	return currentUser?.email || '';
}

/**
 * Format price for display
 */
export function formatPrice(amount: number, currency: string = 'USD'): string {
	return new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: currency,
	}).format(amount);
}

// Global type declaration for Paystack
declare global {
	interface Window {
		PaystackPop: {
			setup: (config: any) => {
				openIframe: () => void;
			};
		};
	}
}