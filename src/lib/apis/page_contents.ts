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

export interface PageResponse {
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
 * get Pages
 */
export const getPages = async (token: string): Promise<PageResponse> => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/features/pages`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	}).then(async (res) => {
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
 * get Pages
 */
export const getPage = async (token: string, slug: string): Promise<PageResponse> => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/features/page/`+slug, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	}).then(async (res) => {
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
