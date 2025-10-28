<script lang="ts">
	import { onMount } from 'svelte';
	import TestimonialsCarousel, { type Testimonial } from "$lib/components/common/TestimonialsCarousel.svelte";
	// import HowItWorksFlow, { type HowItWorksSection } from "$lib/components/common/HowItWorksFlow.svelte";
	import HowItWorks from "$lib/components/common/HowItWorksFlow.svelte";

	  // If loading from a file:
  // import data from "$lib/testimonials.json";
  // export let dataFromServer = data; // or fetch via load()
  const dataFromServer: { items: Testimonial[] } =  {
    items: [
    {
      "id": "tst-201",
      "name": "Grace Wanjiku",
      "role": "Senior Associate, Commercial Litigation",
      "organization": "Wanjiku & Partners LLP",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Research time cut by more than half",
      "quote": "Plain-English queries return clean summaries with paragraph-level citations. The citation trail alone saves hours.",
      "features_used": ["RAG", "Paragraph Citations", "Case Law Q&A", "Gazette Navigator"],
      "impact": {
        "avg_research_time_before_minutes": 180,
        "avg_research_time_after_minutes": 75,
        "time_saved_percent": 58
      },
      "rating": 5,
      "date": "2025-08-14",
      "verified": true
    },
    {
      "id": "tst-202",
      "name": "Daniel Otieno",
      "role": "Partner, Public & Administrative Law",
      "organization": "Otieno & Co. Advocates",
      "jurisdiction": "Mombasa, Kenya",
      "headline": "Drafts that cite the right parts",
      "quote": "The drafting assistant produces a solid first pass with authorities I can verify in one click. We finish in one round instead of three.",
      "features_used": ["Drafting Assistant", "RAG", "Version Compare", "Export to Word"],
      "impact": {
        "rounds_of_revision_before": 3,
        "rounds_of_revision_after": 1,
        "turnaround_reduction_percent": 52
      },
      "rating": 5,
      "date": "2025-07-22",
      "verified": true
    },
    {
      "id": "tst-203",
      "name": "Aisha Msuya",
      "role": "Knowledge Manager, Regulatory",
      "organization": "Dar Advocates",
      "jurisdiction": "Dar es Salaam, Tanzania",
      "headline": "Fine-tuned to our voice",
      "quote": "After fine-tuning on our internal notes and templates, the outputs match how we argue and structure submissions.",
      "features_used": ["Firm Fine-Tuning", "Template Conditioning", "Access Controls"],
      "impact": {
        "template_reuse_rate_before_percent": 34,
        "template_reuse_rate_after_percent": 81,
        "editing_time_saved_percent": 45
      },
      "rating": 4,
      "date": "2025-09-05",
      "verified": true
    },
    {
      "id": "tst-204",
      "name": "Devika Ramnarain",
      "role": "In-House Counsel, Fintech",
      "organization": "Port Louis Payments Ltd",
      "jurisdiction": "Port Louis, Mauritius",
      "headline": "Faster answers with auditable sources",
      "quote": "Compliance questions that used to take a day are now done before lunch, with links to the exact sections of the Act and the latest Gazette.",
      "features_used": ["RAG", "Legislation Navigator", "Alerts & Updates"],
      "impact": {
        "avg_turnaround_before_hours": 8,
        "avg_turnaround_after_hours": 2,
        "escalations_reduced_percent": 39
      },
      "rating": 5,
      "date": "2025-06-30",
      "verified": true
    },
    {
      "id": "tst-205",
      "name": "Jean-Paul Henriette",
      "role": "Research Officer, Appellate",
      "organization": "Victoria Legal Research Unit",
      "jurisdiction": "Mahé, Seychelles",
      "headline": "Consistent precedent summaries",
      "quote": "Precedent digests are consistent and traceable. The paragraph-level links reduce back-and-forth validation with the bench.",
      "features_used": ["Case Law Q&A", "Precedent Lists", "Paragraph Citations"],
      "impact": {
        "digest_prep_time_before_hours": 5,
        "digest_prep_time_after_hours": 2,
        "verification_time_saved_percent": 50
      },
      "rating": 4,
      "date": "2025-08-28",
      "verified": true
    },
    {
      "id": "tst-206",
      "name": "Ruth Namatovu",
      "role": "Compliance Lead, Telecom Regulation",
      "organization": "Kampala Digital Networks",
      "jurisdiction": "Kampala, Uganda",
      "headline": "Never miss a Gazette update",
      "quote": "Topic alerts flag new Notices and amendments immediately, and the side-by-side version compare shows exactly what changed.",
      "features_used": ["Alerts & Updates", "Version Compare", "Change Summaries"],
      "impact": {
        "missed_update_incidents_before_per_quarter": 3,
        "missed_update_incidents_after_per_quarter": 0,
        "policy_update_cycle_time_reduction_percent": 41
      },
      "rating": 5,
      "date": "2025-09-18",
      "verified": true
    },
    {
      "id": "tst-207",
      "name": "Ahmed Yusuf",
      "role": "Associate, Litigation",
      "organization": "Coastline Law Chambers",
      "jurisdiction": "Mombasa, Kenya",
      "headline": "Pin-point citations in seconds",
      "quote": "Jump-to-paragraph links make validation painless. I can move from answer to authority instantly.",
      "features_used": ["Source Viewer", "Paragraph Citations", "RAG"],
      "impact": {
        "avg_research_time_before_minutes": 120,
        "avg_research_time_after_minutes": 55,
        "time_saved_percent": 54
      },
      "rating": 5,
      "date": "2025-05-21",
      "verified": true
    },
    {
      "id": "tst-208",
      "name": "Beatrice Njeri",
      "role": "Knowledge Counsel",
      "organization": "Njeri & Kariuki",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "House-style drafts on first pass",
      "quote": "Template conditioning keeps tone consistent. Less rewriting, more reviewing.",
      "features_used": ["Template Conditioning", "Drafting Assistant", "Research Trails"],
      "impact": {
        "first_draft_quality_score_before_100": 64,
        "first_draft_quality_score_after_100": 90,
        "editing_time_saved_percent": 42
      },
      "rating": 5,
      "date": "2025-04-12",
      "verified": true
    },
    {
      "id": "tst-209",
      "name": "Charles Oloo",
      "role": "Registrar’s Clerk",
      "organization": "Kisumu High Court",
      "jurisdiction": "Kisumu, Kenya",
      "headline": "Quicker checks on citations",
      "quote": "Finding the exact paragraph in cited decisions is now a one-click job.",
      "features_used": ["Case Law Q&A", "Source Viewer", "Bibliography Export"],
      "impact": {
        "verification_time_before_minutes": 40,
        "verification_time_after_minutes": 12,
        "time_saved_percent": 70
      },
      "rating": 4,
      "date": "2025-06-08",
      "verified": true
    },
    {
      "id": "tst-210",
      "name": "Diana Kilonzo",
      "role": "Senior State Counsel",
      "organization": "Office of the DPP",
      "jurisdiction": "Nakuru, Kenya",
      "headline": "Grounded summaries for quick briefs",
      "quote": "Summaries come with quotes and anchors; our team trusts the trail.",
      "features_used": ["RAG", "Quote Previews", "Paragraph Citations"],
      "impact": {
        "avg_brief_prep_before_hours": 4,
        "avg_brief_prep_after_hours": 1.5,
        "escalations_reduced_percent": 33
      },
      "rating": 5,
      "date": "2025-05-17",
      "verified": true
    },
    {
      "id": "tst-211",
      "name": "Elphas Mbugua",
      "role": "Partner, Corporate",
      "organization": "Mbugua Legal",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Legislation changes at a glance",
      "quote": "Version compare shows exactly what changed and why it matters for clients.",
      "features_used": ["Version Compare", "Change Summaries", "Alerts & Updates"],
      "impact": {
        "client_update_cycle_before_days": 5,
        "client_update_cycle_after_days": 2,
        "cycle_time_reduction_percent": 60
      },
      "rating": 5,
      "date": "2025-03-29",
      "verified": true
    },
    {
      "id": "tst-212",
      "name": "Faith Achieng",
      "role": "Legal Researcher",
      "organization": "Lakeview Law Group",
      "jurisdiction": "Kisumu, Kenya",
      "headline": "Reliable Gazette mining",
      "quote": "Gazette Navigator groups notices cleanly; I rarely miss an item now.",
      "features_used": ["Gazette Navigator", "RAG", "Research Trails"],
      "impact": {
        "miss_rate_before_percent": 18,
        "miss_rate_after_percent": 3,
        "time_saved_percent": 37
      },
      "rating": 4,
      "date": "2025-07-03",
      "verified": true
    },
    {
      "id": "tst-213",
      "name": "George Kariuki",
      "role": "General Counsel",
      "organization": "Savanna Energy PLC",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Board-ready memos in hours",
      "quote": "Drafts come with defensible citations; we ship faster without risking accuracy.",
      "features_used": ["Drafting Assistant", "Bibliography Export", "RAG"],
      "impact": {
        "avg_memo_turnaround_before_hours": 24,
        "avg_memo_turnaround_after_hours": 6,
        "time_saved_percent": 75
      },
      "rating": 5,
      "date": "2025-04-22",
      "verified": true
    },
    {
      "id": "tst-214",
      "name": "Halima Noor",
      "role": "Policy Analyst",
      "organization": "Northern Counties Assembly",
      "jurisdiction": "Garissa, Kenya",
      "headline": "Fewer false positives in search",
      "quote": "Hybrid retrieval with filters is night-and-day vs. keyword search.",
      "features_used": ["Hybrid Retrieval", "Filters", "RAG"],
      "impact": {
        "search_noise_before_percent": 45,
        "search_noise_after_percent": 15,
        "precision_gain_percent": 30
      },
      "rating": 4,
      "date": "2025-08-08",
      "verified": true
    },
    {
      "id": "tst-215",
      "name": "Isaac Mwangi",
      "role": "Senior Associate, Banking",
      "organization": "Equator Legal",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Checklists straight from statute",
      "quote": "Turns statutory requirements into actionable steps with links to sections.",
      "features_used": ["Compliance Checklists", "Legislation Navigator", "RAG"],
      "impact": {
        "policy_draft_time_before_hours": 6,
        "policy_draft_time_after_hours": 2.5,
        "time_saved_percent": 58
      },
      "rating": 5,
      "date": "2025-06-02",
      "verified": true
    },
    {
      "id": "tst-216",
      "name": "Jane Nduta",
      "role": "Paralegal, Litigation Support",
      "organization": "Nduta & Co.",
      "jurisdiction": "Thika, Kenya",
      "headline": "Better bundles with fewer gaps",
      "quote": "Precedent lists and source manifests reduce back-and-forth with counsel.",
      "features_used": ["Precedent Lists", "Citation Manifest", "Source Viewer"],
      "impact": {
        "bundle_corrections_before_per_case": 5,
        "bundle_corrections_after_per_case": 2,
        "rework_reduction_percent": 60
      },
      "rating": 4,
      "date": "2025-07-19",
      "verified": true
    },
    {
      "id": "tst-217",
      "name": "Kelvin Kiptoo",
      "role": "Advocate, Appellate",
      "organization": "Rift Valley Law",
      "jurisdiction": "Eldoret, Kenya",
      "headline": "Issue spotter that actually cites",
      "quote": "The issue list is grounded with authorities I can jump into immediately.",
      "features_used": ["Issue Spotter", "Case Law Q&A", "Paragraph Citations"],
      "impact": {
        "issue_list_prep_before_hours": 3,
        "issue_list_prep_after_hours": 1,
        "time_saved_percent": 67
      },
      "rating": 5,
      "date": "2025-09-01",
      "verified": true
    },
    {
      "id": "tst-218",
      "name": "Lydia Nanziri",
      "role": "Knowledge Manager",
      "organization": "Buganda Chambers",
      "jurisdiction": "Kampala, Uganda",
      "headline": "Cleaner internal knowledge search",
      "quote": "Access controls and dedupe keep house materials tidy and findable.",
      "features_used": ["Access Controls", "De-duplication", "RAG"],
      "impact": {
        "duplicate_docs_before_percent": 22,
        "duplicate_docs_after_percent": 5,
        "time_saved_percent": 31
      },
      "rating": 4,
      "date": "2025-05-27",
      "verified": true
    },
    {
      "id": "tst-219",
      "name": "Moses Musoke",
      "role": "Senior Counsel, Public Law",
      "organization": "Musoke & Partners",
      "jurisdiction": "Kampala, Uganda",
      "headline": "Grounded answers win trust",
      "quote": "Fail-closed grounding keeps outputs credible in sensitive matters.",
      "features_used": ["Grounding Controls", "RAG", "Quote Previews"],
      "impact": {
        "review_cycles_before": 3,
        "review_cycles_after": 1,
        "approval_rate_increase_percent": 28
      },
      "rating": 5,
      "date": "2025-04-04",
      "verified": true
    },
    {
      "id": "tst-220",
      "name": "Njeri Thiong’o",
      "role": "Head of Legal Ops",
      "organization": "Sahara Capital",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "From search to memo in one pane",
      "quote": "Split view lets me chat, read sources, and draft without context switching.",
      "features_used": ["Source Viewer", "Drafting Assistant", "RAG"],
      "impact": {
        "context_switches_before_per_memo": 15,
        "context_switches_after_per_memo": 6,
        "time_saved_percent": 34
      },
      "rating": 5,
      "date": "2025-05-02",
      "verified": true
    },
    {
      "id": "tst-221",
      "name": "Olivia Mbatha",
      "role": "Legal Librarian",
      "organization": "Metropolitan Law Library",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Metadata that actually helps",
      "quote": "Court, year, and topic filters make discovery precise for attorneys.",
      "features_used": ["Metadata Filters", "Hybrid Retrieval", "RAG"],
      "impact": {
        "avg_query_refinements_before": 4,
        "avg_query_refinements_after": 1,
        "precision_gain_percent": 40
      },
      "rating": 4,
      "date": "2025-03-31",
      "verified": true
    },
    {
      "id": "tst-222",
      "name": "Peter Kimani",
      "role": "Head of Litigation",
      "organization": "Kimani & Mworia",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Confidence notes prevent overreach",
      "quote": "The system flags low-grounding answers, so juniors know when to dig deeper.",
      "features_used": ["Confidence Notes", "RAG", "Source Viewer"],
      "impact": {
        "post_review_corrections_before_percent": 19,
        "post_review_corrections_after_percent": 7,
        "risk_reduction_percent": 63
      },
      "rating": 5,
      "date": "2025-07-26",
      "verified": true
    },
    {
      "id": "tst-223",
      "name": "Pooja Bheekhee",
      "role": "Regulatory Counsel",
      "organization": "Blue Lagoon Bank",
      "jurisdiction": "Port Louis, Mauritius",
      "headline": "Regulatory watch without the noise",
      "quote": "Weekly digests capture the right Gazettes and amendments—no inbox flooding.",
      "features_used": ["Alerts & Updates", "Change Summaries", "Legislation Navigator"],
      "impact": {
        "irrelevant_alerts_before_percent": 40,
        "irrelevant_alerts_after_percent": 10,
        "time_saved_percent": 28
      },
      "rating": 4,
      "date": "2025-09-22",
      "verified": true
    },
    {
      "id": "tst-224",
      "name": "Quentin Radegonde",
      "role": "Judicial Researcher",
      "organization": "Court of Appeal",
      "jurisdiction": "Victoria, Seychelles",
      "headline": "Better ratio/obiter separation",
      "quote": "Case Q&A helps isolate holdings vs. commentary reliably.",
      "features_used": ["Case Law Q&A", "Paragraph Citations", "Research Trails"],
      "impact": {
        "misclassification_rate_before_percent": 17,
        "misclassification_rate_after_percent": 6,
        "accuracy_gain_percent": 35
      },
      "rating": 5,
      "date": "2025-06-20",
      "verified": true
    },
    {
      "id": "tst-225",
      "name": "Rosette Uwase",
      "role": "Associate, Commercial",
      "organization": "Kigali Law Group",
      "jurisdiction": "Kigali, Rwanda",
      "headline": "Precedents in one prompt",
      "quote": "I can pull a usable precedent list and jump straight into drafting.",
      "features_used": ["Precedent Lists", "Drafting Assistant", "RAG"],
      "impact": {
        "precedent_hunt_before_hours": 2.5,
        "precedent_hunt_after_hours": 0.7,
        "time_saved_percent": 72
      },
      "rating": 5,
      "date": "2025-08-03",
      "verified": true
    },
    {
      "id": "tst-226",
      "name": "Samuel Mugisha",
      "role": "Senior Associate",
      "organization": "Nyamirambo Chambers",
      "jurisdiction": "Kigali, Rwanda",
      "headline": "Citations you can trust",
      "quote": "The bibliography export is gold for review and audit.",
      "features_used": ["Bibliography Export", "RAG", "Source Viewer"],
      "impact": {
        "citation_errors_before_percent": 12,
        "citation_errors_after_percent": 3,
        "risk_reduction_percent": 75
      },
      "rating": 4,
      "date": "2025-07-08",
      "verified": true
    },
    {
      "id": "tst-227",
      "name": "Said Juma",
      "role": "Advocate, Maritime",
      "organization": "Zanzibar Legal",
      "jurisdiction": "Zanzibar, Tanzania",
      "headline": "Maritime notices at fingertips",
      "quote": "Topic filters surface the right Gazette items for ports and shipping.",
      "features_used": ["Gazette Navigator", "Filters", "Alerts & Updates"],
      "impact": {
        "avg_notice_search_before_minutes": 50,
        "avg_notice_search_after_minutes": 18,
        "time_saved_percent": 64
      },
      "rating": 5,
      "date": "2025-05-10",
      "verified": true
    },
    {
      "id": "tst-228",
      "name": "Thandiwe Dlamini",
      "role": "Litigation Support Manager",
      "organization": "Harbor & Reed",
      "jurisdiction": "Durban, South Africa",
      "headline": "One-click source trails",
      "quote": "Bundles now include a clean trail of authorities with anchors—review is faster.",
      "features_used": ["Citation Manifest", "Source Viewer", "Precedent Lists"],
      "impact": {
        "bundle_review_before_hours": 3.5,
        "bundle_review_after_hours": 1.8,
        "time_saved_percent": 49
      },
      "rating": 4,
      "date": "2025-06-14",
      "verified": true
    },
    {
      "id": "tst-229",
      "name": "Umaru Ssekandi",
      "role": "Court Clerk",
      "organization": "High Court",
      "jurisdiction": "Gulu, Uganda",
      "headline": "Accurate section pinning",
      "quote": "Section-level anchors reduce filing mistakes during verification.",
      "features_used": ["Paragraph Citations", "Legislation Navigator", "Source Viewer"],
      "impact": {
        "filing_corrections_before_percent": 14,
        "filing_corrections_after_percent": 5,
        "accuracy_gain_percent": 36
      },
      "rating": 4,
      "date": "2025-05-30",
      "verified": true
    },
    {
      "id": "tst-230",
      "name": "Valentine Nkurunziza",
      "role": "Policy Counsel",
      "organization": "Eastlake Telecom",
      "jurisdiction": "Bujumbura, Burundi",
      "headline": "Version-aware answers",
      "quote": "Answers default to current law, with a toggle for historical research.",
      "features_used": ["Version Compare", "RAG", "Change Summaries"],
      "impact": {
        "policy_misreferences_before_percent": 10,
        "policy_misreferences_after_percent": 2,
        "risk_reduction_percent": 80
      },
      "rating": 5,
      "date": "2025-09-10",
      "verified": true
    },
    {
      "id": "tst-231",
      "name": "Wycliffe Ochieng",
      "role": "Senior Associate, Energy",
      "organization": "Ochieng & Co.",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "From question to export faster",
      "quote": "We go from query to cited memo in a single sitting.",
      "features_used": ["Drafting Assistant", "Bibliography Export", "RAG"],
      "impact": {
        "avg_cycle_before_hours": 10,
        "avg_cycle_after_hours": 4,
        "time_saved_percent": 60
      },
      "rating": 5,
      "date": "2025-08-19",
      "verified": true
    },
    {
      "id": "tst-232",
      "name": "Xolani Mthembu",
      "role": "Attorney, Admin Law",
      "organization": "Mthembu Attorneys",
      "jurisdiction": "Johannesburg, South Africa",
      "headline": "Cleaner retrieval than keyword search",
      "quote": "Hybrid retrieval dramatically improves relevance for older regulations.",
      "features_used": ["Hybrid Retrieval", "Filters", "RAG"],
      "impact": {
        "irrelevant_hits_before_percent": 38,
        "irrelevant_hits_after_percent": 14,
        "precision_gain_percent": 24
      },
      "rating": 4,
      "date": "2025-04-26",
      "verified": true
    },
    {
      "id": "tst-233",
      "name": "Yvonne Gathoni",
      "role": "Senior Legal Officer",
      "organization": "Nairobi Securities",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Cited summaries for briefings",
      "quote": "Board briefings now include linkable authorities for each claim.",
      "features_used": ["Quote Previews", "Paragraph Citations", "RAG"],
      "impact": {
        "briefing_prep_before_hours": 6,
        "briefing_prep_after_hours": 2.5,
        "time_saved_percent": 58
      },
      "rating": 5,
      "date": "2025-07-30",
      "verified": true
    },
    {
      "id": "tst-234",
      "name": "Zachary Kiplagat",
      "role": "Associate, Employment",
      "organization": "Highlands Legal",
      "jurisdiction": "Nakuru, Kenya",
      "headline": "Fewer revision rounds",
      "quote": "House-style and citations mean partners sign off quicker.",
      "features_used": ["Template Conditioning", "Drafting Assistant", "RAG"],
      "impact": {
        "rounds_of_revision_before": 3,
        "rounds_of_revision_after": 2,
        "turnaround_reduction_percent": 29
      },
      "rating": 4,
      "date": "2025-03-18",
      "verified": true
    },
    {
      "id": "tst-235",
      "name": "Brenda Mutesi",
      "role": "In-House Counsel",
      "organization": "Kivu Fintech",
      "jurisdiction": "Kigali, Rwanda",
      "headline": "Alerts that matter",
      "quote": "We’re notified of changes that actually affect our products.",
      "features_used": ["Alerts & Updates", "Change Summaries", "Legislation Navigator"],
      "impact": {
        "missed_changes_before_per_quarter": 2,
        "missed_changes_after_per_quarter": 0,
        "time_saved_percent": 32
      },
      "rating": 5,
      "date": "2025-06-06",
      "verified": true
    },
    {
      "id": "tst-236",
      "name": "Collins Odhiambo",
      "role": "Senior Prosecutor",
      "organization": "ODPP",
      "jurisdiction": "Kisumu, Kenya",
      "headline": "Rapid validation for filings",
      "quote": "Paragraph anchors reduce clerical errors when cross-checking exhibits.",
      "features_used": ["Paragraph Citations", "Source Viewer", "RAG"],
      "impact": {
        "filing_error_rate_before_percent": 9,
        "filing_error_rate_after_percent": 3,
        "risk_reduction_percent": 67
      },
      "rating": 5,
      "date": "2025-08-01",
      "verified": true
    },
    {
      "id": "tst-237",
      "name": "Deogratius Byaruhanga",
      "role": "Research Fellow",
      "organization": "Makerere Law Centre",
      "jurisdiction": "Kampala, Uganda",
      "headline": "Historical views when needed",
      "quote": "Easy toggle between current and historic versions of statutes.",
      "features_used": ["Version Compare", "Legislation Navigator", "RAG"],
      "impact": {
        "historic_lookup_before_minutes": 35,
        "historic_lookup_after_minutes": 10,
        "time_saved_percent": 71
      },
      "rating": 4,
      "date": "2025-05-06",
      "verified": true
    },
    {
      "id": "tst-238",
      "name": "Eddah Chebet",
      "role": "Associate, Tax",
      "organization": "Rift Tax Law",
      "jurisdiction": "Eldoret, Kenya",
      "headline": "Tax amendments made obvious",
      "quote": "Diff summaries explain rate and scope changes with links.",
      "features_used": ["Change Summaries", "Version Compare", "RAG"],
      "impact": {
        "amendment_analysis_before_hours": 4,
        "amendment_analysis_after_hours": 1.5,
        "time_saved_percent": 62
      },
      "rating": 5,
      "date": "2025-09-27",
      "verified": true
    },
    {
      "id": "tst-239",
      "name": "Farah Abdullahi",
      "role": "Policy Lead",
      "organization": "Horn Digital",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Cleaner sourcing for policy notes",
      "quote": "Every assertion links to a paragraph. Reviewers love it.",
      "features_used": ["Paragraph Citations", "Bibliography Export", "RAG"],
      "impact": {
        "review_cycles_before": 2,
        "review_cycles_after": 1,
        "approval_rate_increase_percent": 22
      },
      "rating": 5,
      "date": "2025-10-02",
      "verified": true
    },
    {
      "id": "tst-240",
      "name": "Gideon Wachira",
      "role": "Head of Compliance",
      "organization": "Kifaru Microfinance",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Audit-ready trails",
      "quote": "Research trails and manifests keep our audits straightforward.",
      "features_used": ["Research Trails", "Citation Manifest", "RAG"],
      "impact": {
        "audit_findings_before_per_year": 4,
        "audit_findings_after_per_year": 1,
        "risk_reduction_percent": 75
      },
      "rating": 5,
      "date": "2025-07-11",
      "verified": true
    },
    {
      "id": "tst-241",
      "name": "Hannah Mugo",
      "role": "Assistant Lecturer",
      "organization": "Mount Kenya Law School",
      "jurisdiction": "Nyeri, Kenya",
      "headline": "Teaching with live citations",
      "quote": "Students explore the source material directly from the answer pane.",
      "features_used": ["Source Viewer", "Paragraph Citations", "RAG"],
      "impact": {
        "prep_time_before_hours": 3,
        "prep_time_after_hours": 1.2,
        "time_saved_percent": 60
      },
      "rating": 4,
      "date": "2025-03-25",
      "verified": true
    },
    {
      "id": "tst-242",
      "name": "Ian Oduor",
      "role": "Senior Associate, IP",
      "organization": "Oduor IP Law",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Better synonym handling",
      "quote": "Query expansion catches older terminology in IP statutes.",
      "features_used": ["Query Expansion", "Hybrid Retrieval", "RAG"],
      "impact": {
        "missed_results_before_percent": 20,
        "missed_results_after_percent": 6,
        "accuracy_gain_percent": 35
      },
      "rating": 5,
      "date": "2025-05-19",
      "verified": true
    },
    {
      "id": "tst-243",
      "name": "Josephine Kendi",
      "role": "Legal Officer",
      "organization": "Safari Foods Ltd",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Faster contract notes with cites",
      "quote": "Draft notes include statutory hooks—saves me from manual lookups.",
      "features_used": ["Drafting Assistant", "Legislation Navigator", "RAG"],
      "impact": {
        "note_prep_before_hours": 2.2,
        "note_prep_after_hours": 0.9,
        "time_saved_percent": 59
      },
      "rating": 5,
      "date": "2025-06-23",
      "verified": true
    },
    {
      "id": "tst-244",
      "name": "Khalid Abdalla",
      "role": "Advocate, Public Procurement",
      "organization": "Abdalla Chambers",
      "jurisdiction": "Mombasa, Kenya",
      "headline": "Procurement regs tracked cleanly",
      "quote": "Alerts and diffs keep us aligned with fast-moving rules.",
      "features_used": ["Alerts & Updates", "Version Compare", "Change Summaries"],
      "impact": {
        "noncompliance_incidents_before_per_year": 3,
        "noncompliance_incidents_after_per_year": 1,
        "risk_reduction_percent": 66
      },
      "rating": 4,
      "date": "2025-08-25",
      "verified": true
    },
    {
      "id": "tst-245",
      "name": "Linet Cherono",
      "role": "Senior Paralegal",
      "organization": "Cherono & Kiplangat",
      "jurisdiction": "Eldoret, Kenya",
      "headline": "Cleaner bundles, fewer returns",
      "quote": "The manifest plus anchors reduced registry returns for incomplete cites.",
      "features_used": ["Citation Manifest", "Paragraph Citations", "Precedent Lists"],
      "impact": {
        "registry_returns_before_percent": 15,
        "registry_returns_after_percent": 6,
        "rework_reduction_percent": 60
      },
      "rating": 5,
      "date": "2025-09-12",
      "verified": true
    },
    {
      "id": "tst-246",
      "name": "Maryanne Wairimu",
      "role": "Corporate Counsel",
      "organization": "Lake Victoria Shipping",
      "jurisdiction": "Kisumu, Kenya",
      "headline": "Maritime Gazette focus",
      "quote": "Topic tagging makes maritime notices trivial to track.",
      "features_used": ["Gazette Navigator", "Filters", "Alerts & Updates"],
      "impact": {
        "topic_filtering_time_before_minutes": 45,
        "topic_filtering_time_after_minutes": 15,
        "time_saved_percent": 67
      },
      "rating": 4,
      "date": "2025-07-07",
      "verified": true
    },
    {
      "id": "tst-247",
      "name": "Nelson Wafula",
      "role": "Head of Legal",
      "organization": "Western Grain",
      "jurisdiction": "Bungoma, Kenya",
      "headline": "Summaries we can stand behind",
      "quote": "Citations and quotes make internal approvals straightforward.",
      "features_used": ["Quote Previews", "Paragraph Citations", "RAG"],
      "impact": {
        "approval_time_before_hours": 12,
        "approval_time_after_hours": 5,
        "time_saved_percent": 58
      },
      "rating": 5,
      "date": "2025-08-05",
      "verified": true
    },
    {
      "id": "tst-248",
      "name": "Osman Ali",
      "role": "Research Attorney",
      "organization": "Coastal Justice Initiative",
      "jurisdiction": "Lamu, Kenya",
      "headline": "Better recall for old Acts",
      "quote": "Retrieval handles historic titles and synonyms gracefully.",
      "features_used": ["Query Expansion", "Hybrid Retrieval", "RAG"],
      "impact": {
        "historic_recall_before_percent": 62,
        "historic_recall_after_percent": 84,
        "accuracy_gain_percent": 22
      },
      "rating": 4,
      "date": "2025-05-14",
      "verified": true
    },
    {
      "id": "tst-249",
      "name": "Patricia Waceke",
      "role": "Senior Associate, Competition",
      "organization": "Waceke & Co.",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Competition regs—no surprises",
      "quote": "Weekly digest captures amendments before they hit the headlines.",
      "features_used": ["Alerts & Updates", "Change Summaries", "RAG"],
      "impact": {
        "surprise_amendments_before_per_quarter": 2,
        "surprise_amendments_after_per_quarter": 0,
        "risk_reduction_percent": 100
      },
      "rating": 5,
      "date": "2025-09-07",
      "verified": true
    },
    {
      "id": "tst-250",
      "name": "Queen Mwende",
      "role": "Litigator",
      "organization": "Mwende & Co. Advocates",
      "jurisdiction": "Machakos, Kenya",
      "headline": "Case trends in minutes",
      "quote": "Trends across courts since 2019 show up with the right citations.",
      "features_used": ["Case Law Q&A", "Precedent Lists", "RAG"],
      "impact": {
        "trend_review_before_hours": 4,
        "trend_review_after_hours": 1.2,
        "time_saved_percent": 70
      },
      "rating": 5,
      "date": "2025-06-01",
      "verified": true
    },
    {
      "id": "tst-251",
      "name": "Ronald Karanja",
      "role": "Regulatory Affairs Lead",
      "organization": "Nyika Telco",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Telecom rules diffed cleanly",
      "quote": "Side-by-side diffs and short AI notes are perfect for exec updates.",
      "features_used": ["Version Compare", "Change Summaries", "Bibliography Export"],
      "impact": {
        "exec_brief_prep_before_hours": 3,
        "exec_brief_prep_after_hours": 1,
        "time_saved_percent": 67
      },
      "rating": 4,
      "date": "2025-04-30",
      "verified": true
    },
    {
      "id": "tst-252",
      "name": "Stella Aoko",
      "role": "Assistant Counsel",
      "organization": "Harbor Logistics",
      "jurisdiction": "Mombasa, Kenya",
      "headline": "Better memos for port ops",
      "quote": "Cited answers reduce back-and-forth with operations.",
      "features_used": ["RAG", "Quote Previews", "Export to Word"],
      "impact": {
        "ops_queries_before_per_month": 9,
        "ops_queries_after_per_month": 4,
        "friction_reduction_percent": 56
      },
      "rating": 4,
      "date": "2025-07-15",
      "verified": true
    },
    {
      "id": "tst-253",
      "name": "Tom Otiende",
      "role": "Clerk of Works (Legal)",
      "organization": "County Infrastructure Fund",
      "jurisdiction": "Kakamega, Kenya",
      "headline": "Procurement checklist from law",
      "quote": "The generated checklist maps directly to statutory sections.",
      "features_used": ["Compliance Checklists", "Legislation Navigator", "RAG"],
      "impact": {
        "noncompliance_risk_before_percent": 16,
        "noncompliance_risk_after_percent": 6,
        "risk_reduction_percent": 63
      },
      "rating": 5,
      "date": "2025-03-20",
      "verified": true
    },
    {
      "id": "tst-254",
      "name": "Umbere Amolo",
      "role": "Lecturer, Legal Tech",
      "organization": "Eastern University",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Students engage with primary sources",
      "quote": "Anchored answers encourage direct reading of Acts and cases.",
      "features_used": ["Source Viewer", "Paragraph Citations", "RAG"],
      "impact": {
        "primary_source_use_before_percent": 46,
        "primary_source_use_after_percent": 73,
        "engagement_gain_percent": 27
      },
      "rating": 5,
      "date": "2025-10-10",
      "verified": true
    },
    {
      "id": "tst-255",
      "name": "Victor Wekesa",
      "role": "Associate, Energy & Mining",
      "organization": "Savannah Legal",
      "jurisdiction": "Kitale, Kenya",
      "headline": "Gazette mining that scales",
      "quote": "Bulk uploads with OCR make legacy notices searchable.",
      "features_used": ["Ingestion OCR", "Gazette Navigator", "RAG"],
      "impact": {
        "legacy_search_before_hours": 7,
        "legacy_search_after_hours": 2,
        "time_saved_percent": 71
      },
      "rating": 4,
      "date": "2025-06-18",
      "verified": true
    },
    {
      "id": "tst-256",
      "name": "Winnie Njoki",
      "role": "Senior Counsel, Health",
      "organization": "Kijani Hospitals",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Health regs updated weekly",
      "quote": "Digest keeps our SOPs aligned with new rules.",
      "features_used": ["Alerts & Updates", "Change Summaries", "RAG"],
      "impact": {
        "sop_updates_before_per_quarter": 2,
        "sop_updates_after_per_quarter": 4,
        "compliance_improvement_percent": 35
      },
      "rating": 5,
      "date": "2025-08-11",
      "verified": true
    },
    {
      "id": "tst-257",
      "name": "Xavier Mutuku",
      "role": "Litigation Associate",
      "organization": "Mutuku & Co.",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Bench-ready skeletons",
      "quote": "Skeleton arguments come with authorities and pin cites.",
      "features_used": ["Drafting Assistant", "Precedent Lists", "Paragraph Citations"],
      "impact": {
        "skeleton_draft_before_hours": 5,
        "skeleton_draft_after_hours": 2,
        "time_saved_percent": 60
      },
      "rating": 5,
      "date": "2025-05-03",
      "verified": true
    },
    {
      "id": "tst-258",
      "name": "Yusuf Abdinasir",
      "role": "Policy Advocate",
      "organization": "Digital Rights EA",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Data protection tracked well",
      "quote": "Alerts highlight impactful Gazette changes first.",
      "features_used": ["Alerts & Updates", "Filters", "RAG"],
      "impact": {
        "noise_in_alerts_before_percent": 35,
        "noise_in_alerts_after_percent": 12,
        "signal_gain_percent": 23
      },
      "rating": 4,
      "date": "2025-07-01",
      "verified": true
    },
    {
      "id": "tst-259",
      "name": "Zena Wairimu",
      "role": "Associate, Real Estate",
      "organization": "Hilltop Law",
      "jurisdiction": "Naivasha, Kenya",
      "headline": "Commencement dates made clear",
      "quote": "We no longer misread effective dates for subsidiary legislation.",
      "features_used": ["Legislation Navigator", "Change Summaries", "RAG"],
      "impact": {
        "date_errors_before_percent": 11,
        "date_errors_after_percent": 2,
        "risk_reduction_percent": 82
      },
      "rating": 5,
      "date": "2025-09-29",
      "verified": true
    },
    {
      "id": "tst-260",
      "name": "Abel Karanja",
      "role": "Head of Chambers",
      "organization": "Karanja Litigation",
      "jurisdiction": "Nairobi, Kenya",
      "headline": "Team moves faster with trust",
      "quote": "Strict grounding and review trails keep quality high while speeding delivery.",
      "features_used": ["Grounding Controls", "Research Trails", "RAG"],
      "impact": {
        "avg_case_prep_before_days": 7,
        "avg_case_prep_after_days": 4,
        "time_saved_percent": 43
      },
      "rating": 5,
      "date": "2025-10-18",
      "verified": true
    }
  ]
  };
 
 
  // (Optional) override steps/content/colors
  const steps = [
    {
      title: "Create Your Workspace",
      description:
        "Sign up, choose local (Ollama) or provider models via LiteLLM, and set RBAC & retention.",
      gradientFrom: "from-indigo-500",
      gradientTo: "to-purple-600",
      pingColor: "bg-yellow-400"
    },
    {
      title: "Connect Law Sources & Configure RAG",
      description:
        "Upload Gazette Notices, Acts, subsidiary legislation, and court decisions; configure Top-K, filters, and citations.",
      gradientFrom: "from-purple-500",
      gradientTo: "to-pink-600",
      pingColor: "bg-green-400",
      pingDelay: "delay-500"
    },
    {
      title: "Chat, Cite & Export",
      description:
        "Ask in plain language, get grounded answers with paragraph-level citations, draft, and export to Word/Docs.",
      gradientFrom: "from-pink-500",
      gradientTo: "to-rose-600",
      pingColor: "bg-blue-400",
      pingDelay: "delay-1000"
    }
  ];
  
	let isVisible = false;
	
	onMount(() => {
		isVisible = true;
	});
 


</script>

<div class="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
	 

    <!-- Features Section -->
    <section id="features" class="py-20 bg-gray-50 dark:bg-gray-900">
        <div class="container mx-auto px-4">
            <div class="text-center mb-16">
				<h2 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">
					Powerful Features for Smart AI Legal Research
				</h2>
				<p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
					Everything you need to make Smart and informed legal decisions
				</p>
			</div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">AI-Powered Conversational Legal Research</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Ask questions across Gazette Notices, statutes, regulations, and case law. Get concise answers with citations and confidence notes.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-pink-500 to-rose-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Legislation & Gazette Navigator</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Trace amendments, subsidiary legislation, and commencement dates. Compare versions and see change summaries.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Case Law Q&A</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Query holdings, ratio decidendi, and trends across courts. Pull precedent lists with one prompt and filter by year, court level, or topic.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Drafting Assistant</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Get help with legal drafting, including contracts, pleadings, and other documents. Improve your writing with AI suggestions.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Compliance & Checklists</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Create step-by-step procedures from statutory requirements; export as checklists with linked provisions.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Knowledge Base & DMS Integration</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Connect your document management system or knowledge repository to chat over internal materials, with strict access controls..</p>
                </div>
            </div>
        </div>
    </section>

 
		<!-- <HowItWorksFlow sections={extra} /> -->
	<HowItWorks heading="How It Works" subheading="Get started in three simple steps" />


	<TestimonialsCarousel items={dataFromServer.items} title="What Our Users Say" subtitle="See how we've helped our clients succeed." />



	<!-- CTA Section -->
	<section class="py-20 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-800 dark:via-purple-800 dark:to-pink-800 relative overflow-hidden">
		<div class="absolute inset-0 opacity-10">
			<div class="absolute top-0 left-1/4 w-96 h-96 bg-white rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
			<div class="absolute bottom-0 right-1/4 w-96 h-96 bg-yellow-200 rounded-full mix-blend-multiply filter blur-3xl animate-pulse delay-1000"></div>
		</div>
		
		<div class="container mx-auto px-4 text-center relative z-10">
			<h2 class="text-4xl md:text-5xl font-extrabold text-white mb-6">
				Turn days of research into minutes of answers.
			</h2>
			<p class="text-xl text-gray-100 mb-10 max-w-2xl mx-auto">
				Join thousands of legal researchers who trust our platform for smarter legal research.

				Chat with your law library—Gazette, legislation, and case law—with citations you can trust.
				
				An AI legal copilot that answers with sources, drafts with authority, and learns your firm’s style.
			</p>
			<a href="/auth" class="inline-block bg-white text-indigo-600 px-12 py-5 rounded-xl font-bold text-lg hover:bg-gray-50 transition-all duration-300 shadow-2xl hover:shadow-xl hover:scale-105 transform">
				Get Started Today - It's Free
			</a>
			<p class="text-sm text-gray-200 mt-6">No credit card required • Cancel anytime</p>
		</div>
	</section>

   
</div>

<style>
	@keyframes pulse {
		0%, 100% {
			opacity: 0.6;
		}
		50% {
			opacity: 1;
		}
	}
	
	.delay-500 {
		animation-delay: 500ms;
	}
	
	.delay-1000 {
		animation-delay: 1000ms;
	}
	
	.delay-2000 {
		animation-delay: 2000ms;
	}
</style>
