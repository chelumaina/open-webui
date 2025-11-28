// API functions for payment operations
import { WEBUI_API_BASE_URL } from '$lib/constants';

export interface EmailVerifyResponse {
	success: boolean;
	message: string;
	data?: any;
}

 
/**
 * Verify a payment
 */
export const verifyEmail = async (
	email_verification_token: string
): Promise<EmailVerifyResponse> => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/auths/verify-email/${email_verification_token}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			// authorization: `Bearer ${token}`
		}
	}).then(async (res) => {
		console.log("Response from verify-email:");
			if (!res.ok) throw await res.json();
			return await res.json();
	})
	.catch((err) => {
		error = err.detail;
		console.error("Error verifying email:", error);
		return null;
	});

	if (error) {
		console.error("Throwing error:", error);
		throw error;
	}

	return res;
};