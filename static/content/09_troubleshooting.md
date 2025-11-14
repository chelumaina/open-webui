Troubleshooting Guide

Even with a polished UI, occasional issues may arise. This troubleshooting guide offers solutions to common UI and navigation problems encountered in OpenWebUI.

Sidebar not loading or icons missing:
Try refreshing the browser, clearing cache, or disabling conflicting browser extensions. Ensure your installation folder structure hasn’t been modified.

Model selector not showing models:
Verify that your models directory is correctly indexed. If using remote endpoints, ensure network connectivity and API credentials.

Chat panel freezes during generation:
Large output generations may temporarily stall the UI. Lower max tokens or refresh the session. Check if server logs show memory pressure.

Right panel not appearing:
Your theme or layout preferences may hide the right panel. Re-enable it in Settings → UI Layout.

Settings not saving:
File permissions or Docker volume mounts may be blocking write operations. Ensure the OpenWebUI config directory is writable.

If issues persist, reviewing logs or restarting the application typically resolves most UI-related problems.