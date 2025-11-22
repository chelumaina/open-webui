<script>
import { WEBUI_BASE_URL, WEBUI_HOSTNAME } from '$lib/constants';

import { onMount, tick, setContext, onDestroy } from 'svelte';
	import {
		config,
		user,
		settings,
		theme,
		WEBUI_NAME,
		WEBUI_VERSION,
		mobile,
		socket,
		chatId,
		chats,
		currentChatPage,
		tags,
		temporaryChatEnabled,
		isLastActiveTab,
		isApp,
		appInfo,
		toolServers,
		playingNotificationSound,
		
	} from '$lib/stores';
  export let data;
  let email = '';
  let password = '';

  async function submit(e) {
    e.preventDefault();
    // send credentials to your auth endpoint (client call)
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({ email, password })
    });
    if (res.ok) {
      // handle success (redirect to dashboard in (app) group)
      window.location.href = '/dashboard';
    } else {
      alert('Login failed');
    }
  }
</script>

<svelte:head>
	<title>{$WEBUI_NAME}</title>
	<link crossorigin="anonymous" rel="icon" href="{WEBUI_BASE_URL}/static/favicon-dark.png" />

	<meta name="apple-mobile-web-app-title" content={$WEBUI_NAME} />
	<meta name="description" content={$WEBUI_NAME} />
	<link
		rel="search"
		type="application/opensearchdescription+xml"
		title={$WEBUI_NAME}
		href="/opensearch.xml"
		crossorigin="use-credentials"
	/>
</svelte:head>
<h2>{data.title}</h2>
<form on:submit|preventDefault={submit}>
  <input placeholder="Email" bind:value={email} />
  <input type="password" placeholder="Password" bind:value={password} />
  <button type="submit">Sign in</button>
</form>