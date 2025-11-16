import { base } from '$app/paths';

export async function GET({ url }) {
  const baseUrl = 'https://lexluma.com';

  // Get all your pages - you might want to fetch this from a CMS or generate dynamically
  const pages = [
    { slug: '', priority: 1.0, changefreq: 'weekly' },
    { slug: 'features/ai-conversational-legal-research', priority: 0.8, changefreq: 'weekly' },
    { slug: 'features/legislation-gazette-navigator', priority: 0.9, changefreq: 'weekly' },
    { slug: 'features/case-law-qa', priority: 0.7, changefreq: 'weekly' },
    { slug: 'features/drafting-assistant', priority: 0.7, changefreq: 'weekly' },
    { slug: 'features/compliance-checklists', priority: 0.7, changefreq: 'weekly' },
    { slug: 'features/knowledge-base-dms-integration', priority: 0.7, changefreq: 'weekly' },

 
    {
      slug: "help/getting-started",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/getting-started/introduction-to-lexluma",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/getting-started/first-login-account-creation",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/getting-started/basic-layout-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/getting-started/your-first-chat",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/getting-started/quick-tour-of-interface",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/getting-started/basic-navigation",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/chats-section-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/starting-new-chats",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/managing-chat-history",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/searching-and-filtering-chats",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/pinning-and-organizing-chats",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/workspaces-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/creating-and-managing-workspaces",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/models-quick-access-panel",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/sidebar-navigation/sidebar-customization",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/main-chat-area-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/reading-conversations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/composing-messages",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/text-formatting-and-multi-line-input",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/attaching-files-to-chats",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/supported-file-types",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/message-actions-menu",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/regenerating-responses",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/editing-previous-messages",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/copying-and-sharing-messages",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/chat-management-options",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/renaming-and-organizing-chats",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/exporting-conversations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/chat-interface/clearing-conversation-history",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/model-selection-guide",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/understanding-different-model-types",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/text-only-models",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/vision-and-multimodal-models",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/specialized-models",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/accessing-model-information",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/switching-models-mid-conversation",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/model-parameters-and-settings",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/temperature-and-creativity-controls",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/response-length-settings",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/context-window-management",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/working-with-models/model-performance-optimization",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/document-chat-rag-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/uploading-and-managing-documents",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/chatting-with-pdf-files",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/working-with-text-documents",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/image-and-vision-file-support",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/web-search-integration",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/enabling-and-using-web-search",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/understanding-search-results",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/voice-features-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/voice-input-speech-to-text",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/text-to-speech-output",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/voice-settings-and-preferences",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/prompt-presets-introduction",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/using-pre-made-prompts",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/creating-custom-prompt-presets",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/managing-your-prompt-library",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/vision-and-image-analysis",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/uploading-images-for-analysis",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/best-practices-for-image-prompts",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/advanced-features/multi-modal-conversations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/profile-management-overview",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/updating-account-information",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/changing-display-name-and-avatar",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/security-and-password-management",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/appearance-customization",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/theme-selection",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/font-size-and-layout-adjustments",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/color-scheme-preferences",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/interface-density-options",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/notification-settings",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/chat-notification-preferences",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/email-notification-settings",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/update-and-alert-preferences",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/api-keys-management",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/web-search-api-configuration",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/other-service-integrations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/personal-settings/key-security-best-practices",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/keyboard-shortcuts-guide",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/navigation-shortcuts",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/chat-management-shortcuts",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/text-editing-shortcuts",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/status-indicators-reference",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/connection-status-indicators",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/model-status-indicators",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/upload-and-progress-indicators",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/common-icons-guide",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/toolbar-icons-reference",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/message-action-icons",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/status-and-notification-icons",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/troubleshooting-common-issues",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/connection-problems",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/file-upload-issues",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/performance-optimization",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/quick-reference/feature-specific-troubleshooting",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices",
      priority: 0.9,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/confidentiality-considerations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ethical-use-of-ai-in-law",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/verifying-ai-outputs",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/documenting-ai-usage",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/compliance-with-legal-standards",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/risk-management-strategies",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/client-communication-best-practices",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/continuing-legal-education-on-ai",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/integrating-ai-into-legal-workflows",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/future-trends-in-legal-ai",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/resources-for-legal-professionals",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/responsible-use-of-ai-in-legal-research",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/avoiding-common-pitfalls-in-legal-ai-use",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/balancing-ai-assistance-with-human-judgment",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/training-and-onboarding-for-legal-ai-tools",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/measuring-the-impact-of-ai-on-legal-practice",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/customizing-ai-tools-for-specific-legal-needs",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/building-client-trust-when-using-ai",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ai-and-legal-research-efficiency",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/maintaining-data-integrity-with-ai-tools",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ai-in-contract-review-and-analysis",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/legal-precedent-and-ai-recommendations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ai-assisted-legal-writing-best-practices",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ensuring-compliance-with-data-protection-laws",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ai-and-intellectual-property-considerations",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/best-practices-for-document-chat-rag",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/optimizing-voice-features-for-legal-use",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/ethical-considerations-for-legal-ai-use",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/leveraging-prompt-presets-for-legal-tasks",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/utilizing-vision-and-image-analysis-in-legal-contexts",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/maximizing-personal-settings-for-productivity",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/quick-reference-for-legal-ai-features",
      priority: 0.8,
      changefreq: "weekly"
    },
    {
      slug: "help/legal-ai-best-practices/maintaining-accuracy-in-ai-legal-research",
      priority: 0.8,
      changefreq: "weekly"
    }

  ];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${pages.map(page => `
  <url>
    <loc>${baseUrl}/${page.slug}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'max-age=0, s-maxage=3600'
    }
  });
}