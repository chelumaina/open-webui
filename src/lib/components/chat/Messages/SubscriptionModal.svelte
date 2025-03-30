<script lang="ts">
	import { getContext, onMount, tick } from 'svelte';
	import Modal from '$lib/components/common/Modal.svelte';
    import { loadScript } from "@paypal/paypal-js";

    let paypal;
    let orderID;
	const i18n = getContext('i18n');
	export let show = false;
	export let citation;
	export let showPercentage = false;
	export let showRelevance = true;

	let mergedDocuments = [];

	onMount(async () => {
        paypal = await loadScript({ "client-id": "AV7CoRHni5FA0I-RQkQRcjGbmR6fiE2sxbOV9iivnm7Sn03UG5gufJceXBGj08qI4-N3cDE17i6bSR48" });

        if (!paypal) {
            console.error("PayPal SDK failed to load.");
            return;
        }

        paypal.Buttons({
            createOrder: async function () {
                const response = await fetch("http://localhost:8080/api/v1/subscriptions/create-payment", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ amount: 20.00 }),
                });
                const data = await response.json();
                orderID = data.order_id;
                return data.order_id;
            },
            onApprove: async function (data) {
                const response = await fetch(`http://localhost:8080/api/v1/subscriptions/capture-payment/${orderID}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                });
                const result = await response.json();
                alert("Payment Successful: " + JSON.stringify(result));
            }
        }).render("#paypal-button-container");
    });

 
</script>

<Modal size="full" bind:show>
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-2">
			<div class=" text-lg font-medium self-center capitalize">
				{$i18n.t('Subscription')}
			</div>
			<button class="self-center" on:click={() => { show = false;}}>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>

		<div class="flex flex-col md:flex-row w-full px-6 pb-5 md:space-x-4">
			<div class="flex flex-col w-full dark:text-gray-200 overflow-y-scroll">

				<section class="bg-white dark:bg-gray-900">
					<div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
						<div class="mx-auto max-w-screen-md text-center mb-8 lg:mb-12">
							<p class="mb-5 font-light text-gray-500 sm:text-xl dark:text-gray-400">Here at Flowbite we focus on markets where technology, innovation, and capital can unlock long-term value and drive economic growth.</p>
						</div>
						<div class="space-y-8 lg:grid lg:grid-cols-2 sm:gap-2 xl:gap-2 lg:space-y-0">
							<!-- Pricing Card -->
							<div class="flex flex-col p-6 mx-auto max-w-lg text-center text-gray-900 bg-white rounded-lg border border-gray-100 shadow dark:border-gray-600 xl:p-8 dark:bg-gray-800 dark:text-white">
								<h3 class="mb-4 text-2xl font-semibold">Free Plan</h3>
								<p class="font-light text-gray-500 sm:text-lg dark:text-gray-400">Explore how AI can help you with basic daily tasks</p>
								<div class="flex justify-center items-baseline my-8">
									<span class="mr-2 text-5xl font-extrabold">$0.00</span>
									<span class="text-gray-500 dark:text-gray-400">/month</span>
								</div>
								<!-- List -->
								<!-- <button type="button" class="text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 me-2 mb-2">
									<svg class="w-4 h-4 me-2 -ms-1" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="paypal" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="currentColor" d="M111.4 295.9c-3.5 19.2-17.4 108.7-21.5 134-.3 1.8-1 2.5-3 2.5H12.3c-7.6 0-13.1-6.6-12.1-13.9L58.8 46.6c1.5-9.6 10.1-16.9 20-16.9 152.3 0 165.1-3.7 204 11.4 60.1 23.3 65.6 79.5 44 140.3-21.5 62.6-72.5 89.5-140.1 90.3-43.4 .7-69.5-7-75.3 24.2zM357.1 152c-1.8-1.3-2.5-1.8-3 1.3-2 11.4-5.1 22.5-8.8 33.6-39.9 113.8-150.5 103.9-204.5 103.9-6.1 0-10.1 3.3-10.9 9.4-22.6 140.4-27.1 169.7-27.1 169.7-1 7.1 3.5 12.9 10.6 12.9h63.5c8.6 0 15.7-6.3 17.4-14.9 .7-5.4-1.1 6.1 14.4-91.3 4.6-22 14.3-19.7 29.3-19.7 71 0 126.4-28.8 142.9-112.3 6.5-34.8 4.6-71.4-23.8-92.6z"></path></svg>
									Check out with PayPal
								</button> -->

								<ul role="list" class="mb-8 space-y-4 text-left"> 
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Access to GPT-4o mini and reasoning</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Standard voice mode</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Real-time data from the web with <span class="font-semibold">search</span></span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Limited access to  <span class="font-semibold">GPT-4o</span></span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Use custom GPTs<span class="font-semibold">1000 tokens</span></span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Limited access to file uploads, advanced data analysis, and image generation <span class="font-semibold">1000 tokens</span></span>
									</li>
								</ul>
							</div>



							<!-- Pricing Card -->
							<div class="flex flex-col p-6 mx-auto max-w-lg text-center text-gray-900 bg-white rounded-lg border border-gray-100 shadow dark:border-gray-600 xl:p-8 dark:bg-gray-800 dark:text-white">
								<h3 class="mb-4 text-2xl font-semibold">Plus Plan</h3>
								<p class="font-light text-gray-500 sm:text-lg dark:text-gray-400">Level up productivity and creativity .</p>
								<div class="flex justify-center items-baseline my-8">
									<span class="mr-2 text-5xl font-extrabold">$15.00</span>
									<span class="text-gray-500 dark:text-gray-400">/month</span>
								</div>
								<!-- List -->
								<button type="button" class="text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 me-2 mb-2">
									<svg class="w-4 h-4 me-2 -ms-1" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="paypal" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="currentColor" d="M111.4 295.9c-3.5 19.2-17.4 108.7-21.5 134-.3 1.8-1 2.5-3 2.5H12.3c-7.6 0-13.1-6.6-12.1-13.9L58.8 46.6c1.5-9.6 10.1-16.9 20-16.9 152.3 0 165.1-3.7 204 11.4 60.1 23.3 65.6 79.5 44 140.3-21.5 62.6-72.5 89.5-140.1 90.3-43.4 .7-69.5-7-75.3 24.2zM357.1 152c-1.8-1.3-2.5-1.8-3 1.3-2 11.4-5.1 22.5-8.8 33.6-39.9 113.8-150.5 103.9-204.5 103.9-6.1 0-10.1 3.3-10.9 9.4-22.6 140.4-27.1 169.7-27.1 169.7-1 7.1 3.5 12.9 10.6 12.9h63.5c8.6 0 15.7-6.3 17.4-14.9 .7-5.4-1.1 6.1 14.4-91.3 4.6-22 14.3-19.7 29.3-19.7 71 0 126.4-28.8 142.9-112.3 6.5-34.8 4.6-71.4-23.8-92.6z"></path></svg>
									Check out with PayPal
								</button>

								<ul role="list" class="mb-8 space-y-4 text-left">
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Everything in Free</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Extended limits on messaging, file uploads, advanced data analysis, and image generation</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Standard and advanced voice mode</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Access to deep research, multiple reasoning models (o3-mini, o3-mini-high, and o1), and a research preview of GPT-4.5</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>More space for memories</span>
									</li>
									<li class="flex items-center space-x-3">
										<!-- Icon -->
										<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
										<span>Create and use tasks, projects, and custom GPTs</span>
									</li> 
											
								</ul>
							</div>
						</div>
					</div>
				</section>







				  <section class="bg-white dark:bg-gray-900">
					<div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
					
					  <div class="space-y-8 lg:grid lg:grid-cols-2 sm:gap-2 xl:gap-2 lg:space-y-0">
						<div class="min-w-0 flex-1 space-y-8">
						  
							<div class="space-y-4">
								<h3 class="text-xl font-semibold text-gray-900 dark:text-white">Payment</h3>
								<div id="paypal-button-container"></div>
								<!-- <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
									<div class="rounded-lg border border-gray-200 bg-gray-50 p-4 ps-4 dark:border-gray-700 dark:bg-gray-800">
										
										<div class="flex items-start">
											<div class="flex h-5 items-center">
											<input id="credit-card" aria-describedby="credit-card-text" type="radio" name="payment-method" value="" class="h-4 w-4 border-gray-300 bg-white text-primary-600 focus:ring-2 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-primary-600" checked />
											</div>
							
											<div class="ms-4 text-sm">
											<label for="credit-card" class="font-medium leading-none text-gray-900 dark:text-white"> Credit Card </label>
											<p id="credit-card-text" class="mt-1 text-xs font-normal text-gray-500 dark:text-gray-400">Pay with your credit card</p>
											</div>
										</div>			
						
										<div class="mt-4 flex items-center gap-2">
											<button type="button" class="text-sm font-medium text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Delete</button>
							
											<div class="h-3 w-px shrink-0 bg-gray-200 dark:bg-gray-700"></div>
							
											<button type="button" class="text-sm font-medium text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Edit</button>
										</div>
									</div>
						
								 
						
									<div class="rounded-lg border border-gray-200 bg-gray-50 p-4 ps-4 dark:border-gray-700 dark:bg-gray-800">
										<div class="flex items-start">
											<div class="flex h-5 items-center">
												<input id="paypal-2" aria-describedby="paypal-text" type="radio" name="payment-method" value="" class="h-4 w-4 border-gray-300 bg-white text-primary-600 focus:ring-2 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-primary-600" />
											</div>
							
											<div class="ms-4 text-sm">
												<label for="paypal-2" class="font-medium leading-none text-gray-900 dark:text-white"> Paypal account </label>
												<p id="paypal-text" class="mt-1 text-xs font-normal text-gray-500 dark:text-gray-400">Connect to your account</p>
											</div>
										</div>
						
										<div class="mt-4 flex items-center gap-2">
											<button type="button" class="text-sm font-medium text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Delete</button>
							
											<div class="h-3 w-px shrink-0 bg-gray-200 dark:bg-gray-700"></div>
							
											<button type="button" class="text-sm font-medium text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Edit</button>
										</div>
									</div>
								</div> -->
							</div>





							
						<div class="space-y-4">
							<h2 class="text-xl font-semibold text-gray-900 dark:text-white">Delivery Details</h2>
				  
							<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
							  <div>
								<label for="your_name" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white"> Your name </label>
								<input type="text" id="your_name" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder:text-gray-400 dark:focus:border-primary-500 dark:focus:ring-primary-500" placeholder="Bonnie Green" required />
							  </div>
				  
							  <div>
								<label for="your_email" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white"> Your email* </label>
								<input type="email" id="your_email" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder:text-gray-400 dark:focus:border-primary-500 dark:focus:ring-primary-500" placeholder="name@flowbite.com" required />
							  </div>
				
							 
				   
							</div>
						</div>
				
						
				   
						  
						</div>
				  
						<div class="mt-6 w-full space-y-6 sm:mt-8 lg:mt-0 lg:max-w-xs xl:max-w-md">
						  <div class="flow-root">
							<div class="-my-3 divide-y divide-gray-200 dark:divide-gray-800">
							  <dl class="flex items-center justify-between gap-4 py-3">
								<dt class="text-base font-normal text-gray-500 dark:text-gray-400">Subtotal</dt>
								<dd class="text-base font-medium text-gray-900 dark:text-white">$15</dd>
							  </dl>
				    
							  <dl class="flex items-center justify-between gap-4 py-3">
								<dt class="text-base font-normal text-gray-500 dark:text-gray-400">Tax</dt>
								<dd class="text-base font-medium text-gray-900 dark:text-white">$0</dd>
							  </dl>
				  
							  <dl class="flex items-center justify-between gap-4 py-3">
								<dt class="text-base font-bold text-gray-900 dark:text-white">Total</dt>
								<dd class="text-base font-bold text-gray-900 dark:text-white">$15</dd>
							  </dl>
							</div>
						  </div>
				  
						  <div class="space-y-3">
							<button type="submit" class="flex w-full items-center justify-center rounded-lg bg-primary-700 px-5 py-2.5 text-sm font-medium text-white hover:bg-primary-800 focus:outline-none focus:ring-4  focus:ring-primary-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Proceed to Payment</button>
				  
						  </div>
						</div>
					  </div>
					</div>
				  </section>

		
			</div>
		</div>
	</div>
</Modal>
