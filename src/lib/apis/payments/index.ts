
// API functions for payment operations
import { WEBUI_API_BASE_URL } from '$lib/constants';

export interface PaymentInitializeRequest {
	amount: number;
	currency?: string;
	group_id?: string;
	plan_id: string;
	plan_name: string;
	callback_url?: string;
}

export interface PaymentInitializeResponse {
	success: boolean;
	message: string;
	data?: {
		authorization_url: string;
		access_code: string;
		reference: string;
	};
}

export interface PaymentVerifyResponse {
	success: boolean;
	message: string;
	data?: any;
}

export interface UserSubscription {
	id: number;
	plan_id: string;
	plan_name: string;
	status: string;
	amount: number;
	currency: string;
	billing_cycle: string;
	started_at: string;
	expires_at?: string;
}

export interface PaymentTransaction {
	id: number;
	reference: string;
	amount: number;
	currency: string;
	plan_id: string;
	plan_name: string;
	status: string;
	paid_at?: string;
	created_at: string;
}

/**
 * Initialize a payment with the backend
 */
export const initializePayment = async (
	token: string,
	paymentData: PaymentInitializeRequest
): Promise<PaymentInitializeResponse> => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/payments/initialize`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify(paymentData)
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

/**
 * Verify a payment
 */
export const verifyPayment = async (
	token: string,
	reference: string
): Promise<PaymentVerifyResponse> => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/payments/verify/${reference}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

/**
 * Get user's current subscription
 */
export const getUserSubscription = async (token: string): Promise<{ subscription: UserSubscription | null }> => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/payments/subscription`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

/**
 * Get user's payment transactions
 */
export const getUserTransactions = async (
	token: string,
	limit: number = 10,
	offset: number = 0
): Promise<{ transactions: PaymentTransaction[] }> => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/payments/transactions?limit=${limit}&offset=${offset}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};