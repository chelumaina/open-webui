<script lang="ts">
	import {
		chats,
		config,
		settings,
		token_cost,
		user as _user,
		mobile,
		currentChatPage,
		temporaryChatEnabled
	} from '$lib/stores';
	import { tick, getContext, onMount, createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	import { toast } from 'svelte-sonner';
	import { getChatList, updateChatById } from '$lib/apis/chats';
	import { copyToClipboard, extractCurlyBraceWords } from '$lib/utils';

	import Message from './Messages/Message.svelte';
	import Loader from '../common/Loader.svelte';
	import Spinner from '../common/Spinner.svelte';
	import SubscriptionModal from '$lib/components/chat/Messages/SubscriptionModal.svelte';
	import { getAndUpdateUserLocation, getUserSettings } from '$lib/apis/users';

	let showSubscriptionModal = false;
	let selectedSubscription: any = null;
	let showPercentage = false;
	let showRelevance = true;


 	
	import ChatPlaceholder from './ChatPlaceholder.svelte';
	import { t } from 'i18next';

	const i18n = getContext('i18n');

	export let className = 'h-full flex pt-8';

	export let chatId = '';
	export let user = $_user;

	export let prompt;
	export let history:any = [];
	export let selectedModels;
	export let atSelectedModel;

	let messages:any = [];

	export let sendPrompt: Function;
	export let continueResponse: Function;
	export let regenerateResponse: Function;
	export let mergeResponses: Function;

	export let chatActionHandler: Function;
	export let showMessage: Function = () => {};
	export let submitMessage: Function = () => {};
	export let addMessages: Function = () => {};

	export let readOnly = false;

	export let bottomPadding = false;
	export let autoScroll: any;
	export let userSettings={};

	let messagesCount = 20;
	let messagesLoading = false;

	// alert('This is a test alert!');
	// console.log("model_config33333", model_config)

	const loadMoreMessages = async () => {
		// scroll slightly down to disable continuous loading
		const element = document.getElementById('messages-container');
		element.scrollTop = element.scrollTop + 100;

		messagesLoading = true;
		messagesCount += 20;

		await tick();

		messagesLoading = false;
	};

	$: if (history.currentId) {
		let _messages = [];

		let message = history.messages[history.currentId];
		while (message && _messages.length <= messagesCount) {
			_messages.unshift({ ...message });
			message = message.parentId !== null ? history.messages[message.parentId] : null;
		}

		messages = _messages;
	} else {
		messages = [];
	}

	$: if (autoScroll && bottomPadding) {
		(async () => {
			await tick();
			scrollToBottom();
		})();
	}

	const scrollToBottom = () => {
		const element = document.getElementById('messages-container');
		element.scrollTop = element.scrollHeight;
	};

	const updateChat = async () => {
		if (!$temporaryChatEnabled) {
			history = history;
			await tick();
			await updateChatById(localStorage.token, chatId, {
				history: history,
				messages: messages
			});

			currentChatPage.set(1);
			await chats.set(await getChatList(localStorage.token, $currentChatPage));
		}
	};

	const gotoMessage = async (message:any, idx:any) => {
		// Determine the correct sibling list (either parent's children or root messages)
		let siblings;
		if (message.parentId !== null) {
			siblings = history.messages[message.parentId].childrenIds;
		} else {
			siblings = Object.values(history.messages)
				.filter((msg:any) => msg.parentId === null)
				.map((msg:any) => msg.id);
		}

		// Clamp index to a valid range
		idx = Math.max(0, Math.min(idx, siblings.length - 1));

		let messageId = siblings[idx];

		// If we're navigating to a different message
		if (message.id !== messageId) {
			// Drill down to the deepest child of that branch
			let messageChildrenIds = history.messages[messageId].childrenIds;
			while (messageChildrenIds.length !== 0) {
				messageId = messageChildrenIds.at(-1);
				messageChildrenIds = history.messages[messageId].childrenIds;
			}

			history.currentId = messageId;
		}

		await tick();

		// Optional auto-scroll
		if ($settings?.scrollOnBranchChange ?? true) {
			const element = document.getElementById('messages-container');
			autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	};

	const showPreviousMessage = async (message:any) => {
		if (message.parentId !== null) {
			let messageId =
				history.messages[message.parentId].childrenIds[
					Math.max(history.messages[message.parentId].childrenIds.indexOf(message.id) - 1, 0)
				];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		} else {
			let childrenIds = Object.values(history.messages)
				.filter((message:any) => message.parentId === null)
				.map((message:any) => message.id);
			let messageId = childrenIds[Math.max(childrenIds.indexOf(message.id) - 1, 0)];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		}

		await tick();

		if ($settings?.scrollOnBranchChange ?? true) {
			const element = document.getElementById('messages-container');
			autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	};

	const showNextMessage = async (message:any) => {
		if (message.parentId !== null) {
			let messageId =
				history.messages[message.parentId].childrenIds[
					Math.min(
						history.messages[message.parentId].childrenIds.indexOf(message.id) + 1,
						history.messages[message.parentId].childrenIds.length - 1
					)
				];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		} else {
			let childrenIds = Object.values(history.messages)
				.filter((message:any) => message.parentId === null)
				.map((message:any) => message.id);
			let messageId =
				childrenIds[Math.min(childrenIds.indexOf(message.id) + 1, childrenIds.length - 1)];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		}

		await tick();

		if ($settings?.scrollOnBranchChange ?? true) {
			const element = document.getElementById('messages-container');
			autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	};


	const rateMessage = async (messageId:any, rating:any) => {
		history.messages[messageId].annotation = {
			...history.messages[messageId].annotation,
			rating: rating
		};

		await updateChat();
	};

	const editMessage = async (messageId:any, content:any, submit = true) => {
		if (history.messages[messageId].role === 'user') {
			if (submit) {
				// New user message
				let userPrompt = content;
				let userMessageId = uuidv4();

				let userMessage = {
					id: userMessageId,
					parentId: history.messages[messageId].parentId,
					childrenIds: [],
					role: 'user',
					content: userPrompt,
					...(history.messages[messageId].files && { files: history.messages[messageId].files }),
					models: selectedModels,
					timestamp: Math.floor(Date.now() / 1000) // Unix epoch
				};

				let messageParentId = history.messages[messageId].parentId;

				if (messageParentId !== null) {
					history.messages[messageParentId].childrenIds = [
						...history.messages[messageParentId].childrenIds,
						userMessageId
					];
				}

				history.messages[userMessageId] = userMessage;
				history.currentId = userMessageId;

				await tick();
				await sendPrompt(history, userPrompt, userMessageId);
			} else {
				// Edit user message
				history.messages[messageId].content = content;
				await updateChat();
			}
		} else {
			if (submit) {
				// New response message
				const responseMessageId = uuidv4();
				const message = history.messages[messageId];
				const parentId = message.parentId;

				const responseMessage = {
					...message,
					id: responseMessageId,
					parentId: parentId,
					childrenIds: [],
					files: undefined,
					content: content,
					timestamp: Math.floor(Date.now() / 1000) // Unix epoch
				};

				history.messages[responseMessageId] = responseMessage;
				history.currentId = responseMessageId;

				// Append messageId to childrenIds of parent message
				if (parentId !== null) {
					history.messages[parentId].childrenIds = [
						...history.messages[parentId].childrenIds,
						responseMessageId
					];
				}

				await updateChat();
			} else {
				// Edit response message
				history.messages[messageId].originalContent = history.messages[messageId].content;
				history.messages[messageId].content = content;
				await updateChat();
			}
		}
	};

	const actionMessage = async (actionId:any, message:any, event = null) => {
		await chatActionHandler(chatId, actionId, message.model, message.id, event);
	};

	const saveMessage = async (messageId:any, message:any) => {
		history.messages[messageId] = message;
		await updateChat();
	};

	const deleteMessage = async (messageId:any) => {
		const messageToDelete = history.messages[messageId];
		const parentMessageId = messageToDelete.parentId;
		const childMessageIds = messageToDelete.childrenIds ?? [];

		// Collect all grandchildren
		const grandchildrenIds = childMessageIds.flatMap(
			(childId:any) => history.messages[childId]?.childrenIds ?? []
		);

		// Update parent's children
		if (parentMessageId && history.messages[parentMessageId]) {
			history.messages[parentMessageId].childrenIds = [
				...history.messages[parentMessageId].childrenIds.filter((id) => id !== messageId),
				...grandchildrenIds
			];
		}

		// Update grandchildren's parent
		grandchildrenIds.forEach((grandchildId:any) => {
			if (history.messages[grandchildId]) {
				history.messages[grandchildId].parentId = parentMessageId;
			}
		});

		// Delete the message and its children
		[messageId, ...childMessageIds].forEach((id) => {
			delete history.messages[id];
		});

		await tick();

		showMessage({ id: parentMessageId });

		// Update the chat
		await updateChat();
	};

	const triggerScroll = () => {
		if (autoScroll) {
			const element = document.getElementById('messages-container');
			autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;
			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	};
	 
</script>

<SubscriptionModal
	bind:show={showSubscriptionModal}
	citation={selectedSubscription}
	{showPercentage}
	{showRelevance}
	/>
<div class={className}>

	
	{#if Object.keys(history?.messages ?? {}).length == 0}
		
		<ChatPlaceholder
			modelIds={selectedModels}
			{atSelectedModel}
			submitPrompt={async (p) => {
				let text = p;

				if (p.includes('{{CLIPBOARD}}')) {
					const clipboardText = await navigator.clipboard.readText().catch((err) => {
						toast.error($i18n.t('Failed to read clipboard contents'));
						return '{{CLIPBOARD}}';
					});

					text = p.replaceAll('{{CLIPBOARD}}', clipboardText);
				}

				prompt = text;
				await tick();
			}}
		/>
	{:else}
	
		<div class="w-full pt-2">
			
			{#key chatId}
				<div class="w-full">
					{#if messages.at(0)?.parentId !== null}
						<Loader
							on:visible={(e) => {
								console.log('visible');
								if (!messagesLoading) {
									loadMoreMessages();
								}
							}}
						>
							<div class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2">
								<Spinner className=" size-4" />
								<div class=" ">Loading...</div>
							</div>
						</Loader>
					{/if}

					{#each messages as message, messageIdx (message.id)}
						<Message
							{chatId}
							bind:history
							messageId={message.id}
							idx={messageIdx}
							{user}
							{gotoMessage}
							{showPreviousMessage}
							{showNextMessage}
							{updateChat}
							{editMessage}
							{deleteMessage}
							{rateMessage}
							{actionMessage}
							{saveMessage}
							{submitMessage}
							{regenerateResponse}
							{continueResponse}
							{mergeResponses}
							{addMessages}
							{triggerScroll}
							{readOnly}
						/>
					{/each}
					{#if messagesLoading}
						<div class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2">
							<Spinner className=" size-4" />
							<div class=" ">Loading...</div>
						</div>
					{/if}

					{#if $token_cost.cost > 1 && $token_cost.is_user_subscription_valid==false} 
						<div class="flex flex-col justify-between px-5 mb-3 w-full max-w-5xl mx-auto rounded-lg group">
							<div class="relative h-full w-full border-1 rounded-2xl border-token-border-light bg-token-main-surface-primary text-token-text-primary dark:bg-token-main-surface-secondary">
								<div class="flex flex-col gap-3.5 ">
									<div style="opacity: 1; transform: translateY(0px); will-change: auto;">
										<div class="flex w-full items-start gap-4 rounded-3xl border py-4 pl-5 pr-3 text-sm [text-wrap:pretty] dark:border-transparent lg:mx-auto shadow-xxs md:items-center border-token-border-light bg-token-main-surface-primary text-token-text-primary dark:bg-token-main-surface-secondary">
											<div class="flex h-full w-full items-start gap-3 md:items-center">
												<div class="mt-1.5 flex grow items-start gap-4 md:mt-0 md:flex-row md:items-center md:justify-between md:gap-8 flex-col">
													<div class="flex max-w-none flex-col">
														<div class="font-bold text-token-text-primary">You've reached your daily usage limit. You have spent <strong>USD ${$token_cost?.cost}</strong></div>
														<div class="text-token-text-secondary">
															<div>Upgrade to the Plus plan  or try again tomorrow </div>
															<!-- <p>USD ${$token_cost?.cost}</p> -->
														</div>
													</div>
													<div class="flex shrink-0 gap-2 pb-1 md:pb-0">
														<button class="btn relative btn-primary shrink-0">
															<div class="flex items-center justify-center">
																<button class="btn relative btn-primary shrink-0" on:click={() => {
																showSubscriptionModal = true;showPercentage = true;showRelevance = true; showPercentage = true; selectedSubscription = 'plus';
																}}
															
														>Subscribe to Plus and Get more wirh <strong>$15</strong></button></div>
														</button>
													</div>
												</div>
												<div class="flex shrink-0 items-center gap-2">
													
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					{/if}
				</div>
				
				<div class="pb-12" />
				{#if bottomPadding}
					<div class="  pb-6" />
				{/if}
			{/key}
			 
		</div>
	{/if}
</div> 
