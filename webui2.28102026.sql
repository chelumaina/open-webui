--
-- PostgreSQL database dump
--

\restrict oylqjiPcL6KMekq05wsHPKfkxXczgWH9J9VbHsAqoKPAeB75bfdktBpRlkvltHa

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO transcription;

--
-- Name: auth; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.auth (
    id character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password text NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public.auth OWNER TO transcription;

--
-- Name: channel; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.channel (
    id text NOT NULL,
    user_id text,
    name text,
    description text,
    data json,
    meta json,
    access_control json,
    created_at bigint,
    updated_at bigint,
    type text
);


ALTER TABLE public.channel OWNER TO transcription;

--
-- Name: channel_member; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.channel_member (
    id text NOT NULL,
    channel_id text NOT NULL,
    user_id text NOT NULL,
    created_at bigint
);


ALTER TABLE public.channel_member OWNER TO transcription;

--
-- Name: chat; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.chat (
    id character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    title text NOT NULL,
    share_id character varying(255),
    archived boolean NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL,
    chat json,
    pinned boolean,
    meta json DEFAULT '{}'::json NOT NULL,
    folder_id text
);


ALTER TABLE public.chat OWNER TO transcription;

--
-- Name: chatidtag; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.chatidtag (
    id character varying(255) NOT NULL,
    tag_name character varying(255) NOT NULL,
    chat_id character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    "timestamp" bigint NOT NULL
);


ALTER TABLE public.chatidtag OWNER TO transcription;

--
-- Name: config; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.config (
    id integer NOT NULL,
    data json NOT NULL,
    version integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.config OWNER TO transcription;

--
-- Name: config_id_seq; Type: SEQUENCE; Schema: public; Owner: transcription
--

CREATE SEQUENCE public.config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.config_id_seq OWNER TO transcription;

--
-- Name: config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: transcription
--

ALTER SEQUENCE public.config_id_seq OWNED BY public.config.id;


--
-- Name: document; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.document (
    id integer NOT NULL,
    collection_name character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    title text NOT NULL,
    filename text NOT NULL,
    content text,
    user_id character varying(255) NOT NULL,
    "timestamp" bigint NOT NULL
);


ALTER TABLE public.document OWNER TO transcription;

--
-- Name: document_id_seq; Type: SEQUENCE; Schema: public; Owner: transcription
--

CREATE SEQUENCE public.document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_id_seq OWNER TO transcription;

--
-- Name: document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: transcription
--

ALTER SEQUENCE public.document_id_seq OWNED BY public.document.id;


--
-- Name: feedback; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.feedback (
    id text NOT NULL,
    user_id text,
    version bigint,
    type text,
    data json,
    meta json,
    snapshot json,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL
);


ALTER TABLE public.feedback OWNER TO transcription;

--
-- Name: file; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.file (
    id text NOT NULL,
    user_id text NOT NULL,
    filename text NOT NULL,
    meta json,
    created_at bigint NOT NULL,
    hash text,
    data json,
    updated_at bigint,
    path text,
    access_control json
);


ALTER TABLE public.file OWNER TO transcription;

--
-- Name: folder; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.folder (
    id text NOT NULL,
    parent_id text,
    user_id text NOT NULL,
    name text NOT NULL,
    items json,
    meta json,
    is_expanded boolean NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL,
    data json
);


ALTER TABLE public.folder OWNER TO transcription;

--
-- Name: function; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.function (
    id text NOT NULL,
    user_id text NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    content text NOT NULL,
    meta text NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL,
    valves text,
    is_active boolean NOT NULL,
    is_global boolean NOT NULL
);


ALTER TABLE public.function OWNER TO transcription;

--
-- Name: group; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public."group" (
    id text NOT NULL,
    user_id text,
    name text,
    description text,
    data json,
    meta json,
    permissions json,
    user_ids json,
    created_at bigint,
    updated_at bigint
);


ALTER TABLE public."group" OWNER TO transcription;

--
-- Name: knowledge; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.knowledge (
    id text NOT NULL,
    user_id text NOT NULL,
    name text NOT NULL,
    description text,
    data json,
    meta json,
    created_at bigint NOT NULL,
    updated_at bigint,
    access_control json
);


ALTER TABLE public.knowledge OWNER TO transcription;

--
-- Name: memory; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.memory (
    id character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    content text NOT NULL,
    updated_at bigint NOT NULL,
    created_at bigint NOT NULL
);


ALTER TABLE public.memory OWNER TO transcription;

--
-- Name: message; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.message (
    id text NOT NULL,
    user_id text,
    channel_id text,
    content text,
    data json,
    meta json,
    created_at bigint,
    updated_at bigint,
    parent_id text,
    reply_to_id text
);


ALTER TABLE public.message OWNER TO transcription;

--
-- Name: message_reaction; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.message_reaction (
    id text NOT NULL,
    user_id text NOT NULL,
    message_id text NOT NULL,
    name text NOT NULL,
    created_at bigint
);


ALTER TABLE public.message_reaction OWNER TO transcription;

--
-- Name: migratehistory; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.migratehistory (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    migrated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.migratehistory OWNER TO transcription;

--
-- Name: migratehistory_id_seq; Type: SEQUENCE; Schema: public; Owner: transcription
--

CREATE SEQUENCE public.migratehistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.migratehistory_id_seq OWNER TO transcription;

--
-- Name: migratehistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: transcription
--

ALTER SEQUENCE public.migratehistory_id_seq OWNED BY public.migratehistory.id;


--
-- Name: model; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.model (
    id text NOT NULL,
    user_id text NOT NULL,
    base_model_id text,
    name text NOT NULL,
    meta text NOT NULL,
    params text NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL,
    access_control json,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.model OWNER TO transcription;

--
-- Name: modelfile; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.modelfile (
    id integer NOT NULL,
    tag_name character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    modelfile text NOT NULL,
    "timestamp" bigint NOT NULL
);


ALTER TABLE public.modelfile OWNER TO transcription;

--
-- Name: modelfile_id_seq; Type: SEQUENCE; Schema: public; Owner: transcription
--

CREATE SEQUENCE public.modelfile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.modelfile_id_seq OWNER TO transcription;

--
-- Name: modelfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: transcription
--

ALTER SEQUENCE public.modelfile_id_seq OWNED BY public.modelfile.id;


--
-- Name: note; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.note (
    id text NOT NULL,
    user_id text,
    title text,
    data json,
    meta json,
    access_control json,
    created_at bigint,
    updated_at bigint
);


ALTER TABLE public.note OWNER TO transcription;

--
-- Name: oauth_session; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.oauth_session (
    id text NOT NULL,
    user_id text NOT NULL,
    provider text NOT NULL,
    token text NOT NULL,
    expires_at bigint NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL
);


ALTER TABLE public.oauth_session OWNER TO transcription;

--
-- Name: payment_transactions; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.payment_transactions (
    id uuid NOT NULL,
    user_id character varying NOT NULL,
    reference character varying NOT NULL,
    amount double precision NOT NULL,
    currency character varying NOT NULL,
    plan_id character varying NOT NULL,
    plan_name character varying NOT NULL,
    billing_cycle character varying,
    status character varying,
    paystack_reference character varying,
    paystack_status character varying,
    gateway_response text,
    gateway_response_data text,
    group_id character varying,
    paid_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.payment_transactions OWNER TO transcription;

--
-- Name: prompt; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.prompt (
    id integer NOT NULL,
    command character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    "timestamp" bigint NOT NULL,
    access_control json
);


ALTER TABLE public.prompt OWNER TO transcription;

--
-- Name: prompt_id_seq; Type: SEQUENCE; Schema: public; Owner: transcription
--

CREATE SEQUENCE public.prompt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.prompt_id_seq OWNER TO transcription;

--
-- Name: prompt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: transcription
--

ALTER SEQUENCE public.prompt_id_seq OWNED BY public.prompt.id;


--
-- Name: tag; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.tag (
    id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    meta json
);


ALTER TABLE public.tag OWNER TO transcription;

--
-- Name: tool; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.tool (
    id text NOT NULL,
    user_id text NOT NULL,
    name text NOT NULL,
    content text NOT NULL,
    specs text NOT NULL,
    meta text NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL,
    valves text,
    access_control json
);


ALTER TABLE public.tool OWNER TO transcription;

--
-- Name: user; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public."user" (
    id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    role character varying(255) NOT NULL,
    profile_image_url text NOT NULL,
    api_key character varying(255),
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL,
    last_active_at bigint NOT NULL,
    settings text,
    info text,
    oauth_sub text,
    username character varying(50),
    bio text,
    gender text,
    date_of_birth date
);


ALTER TABLE public."user" OWNER TO transcription;

--
-- Name: user_subscriptions; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.user_subscriptions (
    id uuid NOT NULL,
    user_id character varying NOT NULL,
    plan_id character varying NOT NULL,
    plan_name character varying NOT NULL,
    status character varying,
    amount double precision NOT NULL,
    currency character varying NOT NULL,
    group_id character varying,
    billing_cycle character varying,
    started_at timestamp without time zone,
    expires_at timestamp without time zone,
    trial_end timestamp with time zone,
    current_period_end timestamp with time zone,
    transaction_reference character varying NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.user_subscriptions OWNER TO transcription;

--
-- Name: config id; Type: DEFAULT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.config ALTER COLUMN id SET DEFAULT nextval('public.config_id_seq'::regclass);


--
-- Name: document id; Type: DEFAULT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.document ALTER COLUMN id SET DEFAULT nextval('public.document_id_seq'::regclass);


--
-- Name: migratehistory id; Type: DEFAULT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.migratehistory ALTER COLUMN id SET DEFAULT nextval('public.migratehistory_id_seq'::regclass);


--
-- Name: modelfile id; Type: DEFAULT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.modelfile ALTER COLUMN id SET DEFAULT nextval('public.modelfile_id_seq'::regclass);


--
-- Name: prompt id; Type: DEFAULT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.prompt ALTER COLUMN id SET DEFAULT nextval('public.prompt_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.alembic_version (version_num) FROM stdin;
a5c220713937
\.


--
-- Data for Name: auth; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.auth (id, email, password, active) FROM stdin;
\.


--
-- Data for Name: channel; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.channel (id, user_id, name, description, data, meta, access_control, created_at, updated_at, type) FROM stdin;
\.


--
-- Data for Name: channel_member; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.channel_member (id, channel_id, user_id, created_at) FROM stdin;
\.


--
-- Data for Name: chat; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.chat (id, user_id, title, share_id, archived, created_at, updated_at, chat, pinned, meta, folder_id) FROM stdin;
\.


--
-- Data for Name: chatidtag; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.chatidtag (id, tag_name, chat_id, user_id, "timestamp") FROM stdin;
\.


--
-- Data for Name: config; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.config (id, data, version, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: document; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.document (id, collection_name, name, title, filename, content, user_id, "timestamp") FROM stdin;
\.


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.feedback (id, user_id, version, type, data, meta, snapshot, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: file; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.file (id, user_id, filename, meta, created_at, hash, data, updated_at, path, access_control) FROM stdin;
\.


--
-- Data for Name: folder; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.folder (id, parent_id, user_id, name, items, meta, is_expanded, created_at, updated_at, data) FROM stdin;
\.


--
-- Data for Name: function; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.function (id, user_id, name, type, content, meta, created_at, updated_at, valves, is_active, is_global) FROM stdin;
\.


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public."group" (id, user_id, name, description, data, meta, permissions, user_ids, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: knowledge; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.knowledge (id, user_id, name, description, data, meta, created_at, updated_at, access_control) FROM stdin;
\.


--
-- Data for Name: memory; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.memory (id, user_id, content, updated_at, created_at) FROM stdin;
\.


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.message (id, user_id, channel_id, content, data, meta, created_at, updated_at, parent_id, reply_to_id) FROM stdin;
\.


--
-- Data for Name: message_reaction; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.message_reaction (id, user_id, message_id, name, created_at) FROM stdin;
\.


--
-- Data for Name: migratehistory; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.migratehistory (id, name, migrated_at) FROM stdin;
1	001_initial_schema	2025-10-28 12:41:31.699174
2	002_add_local_sharing	2025-10-28 12:41:31.703263
3	003_add_auth_api_key	2025-10-28 12:41:31.705325
4	004_add_archived	2025-10-28 12:41:31.707789
5	005_add_updated_at	2025-10-28 12:41:31.718398
6	006_migrate_timestamps_and_charfields	2025-10-28 12:41:31.726931
7	007_add_user_last_active_at	2025-10-28 12:41:31.738426
8	008_add_memory	2025-10-28 12:41:31.742509
9	009_add_models	2025-10-28 12:41:31.747139
10	010_migrate_modelfiles_to_models	2025-10-28 12:41:31.751228
11	011_add_user_settings	2025-10-28 12:41:31.754393
12	012_add_tools	2025-10-28 12:41:31.757948
13	013_add_user_info	2025-10-28 12:41:31.759081
14	014_add_files	2025-10-28 12:41:31.763157
15	015_add_functions	2025-10-28 12:41:31.767698
16	016_add_valves_and_is_active	2025-10-28 12:41:31.769971
17	017_add_user_oauth_sub	2025-10-28 12:41:31.772243
18	018_add_function_is_global	2025-10-28 12:41:31.774457
\.


--
-- Data for Name: model; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, access_control, is_active) FROM stdin;
\.


--
-- Data for Name: modelfile; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.modelfile (id, tag_name, user_id, modelfile, "timestamp") FROM stdin;
\.


--
-- Data for Name: note; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.note (id, user_id, title, data, meta, access_control, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: oauth_session; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.oauth_session (id, user_id, provider, token, expires_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: payment_transactions; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.payment_transactions (id, user_id, reference, amount, currency, plan_id, plan_name, billing_cycle, status, paystack_reference, paystack_status, gateway_response, gateway_response_data, group_id, paid_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: prompt; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.prompt (id, command, user_id, title, content, "timestamp", access_control) FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.tag (id, name, user_id, meta) FROM stdin;
\.


--
-- Data for Name: tool; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.tool (id, user_id, name, content, specs, meta, created_at, updated_at, valves, access_control) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public."user" (id, name, email, role, profile_image_url, api_key, created_at, updated_at, last_active_at, settings, info, oauth_sub, username, bio, gender, date_of_birth) FROM stdin;
\.


--
-- Data for Name: user_subscriptions; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.user_subscriptions (id, user_id, plan_id, plan_name, status, amount, currency, group_id, billing_cycle, started_at, expires_at, trial_end, current_period_end, transaction_reference, created_at, updated_at) FROM stdin;
\.


--
-- Name: config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.config_id_seq', 1, false);


--
-- Name: document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.document_id_seq', 1, false);


--
-- Name: migratehistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.migratehistory_id_seq', 4, true);


--
-- Name: modelfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.modelfile_id_seq', 1, false);


--
-- Name: prompt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.prompt_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: channel_member channel_member_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.channel_member
    ADD CONSTRAINT channel_member_pkey PRIMARY KEY (id);


--
-- Name: channel channel_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_pkey PRIMARY KEY (id);


--
-- Name: config config_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.config
    ADD CONSTRAINT config_pkey PRIMARY KEY (id);


--
-- Name: document document_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: folder folder_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.folder
    ADD CONSTRAINT folder_pkey PRIMARY KEY (id, user_id);


--
-- Name: group group_id_key; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_id_key UNIQUE (id);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: knowledge knowledge_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.knowledge
    ADD CONSTRAINT knowledge_pkey PRIMARY KEY (id);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: message_reaction message_reaction_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.message_reaction
    ADD CONSTRAINT message_reaction_pkey PRIMARY KEY (id);


--
-- Name: migratehistory migratehistory_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.migratehistory
    ADD CONSTRAINT migratehistory_pkey PRIMARY KEY (id);


--
-- Name: modelfile modelfile_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.modelfile
    ADD CONSTRAINT modelfile_pkey PRIMARY KEY (id);


--
-- Name: note note_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.note
    ADD CONSTRAINT note_pkey PRIMARY KEY (id);


--
-- Name: oauth_session oauth_session_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.oauth_session
    ADD CONSTRAINT oauth_session_pkey PRIMARY KEY (id);


--
-- Name: payment_transactions payment_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.payment_transactions
    ADD CONSTRAINT payment_transactions_pkey PRIMARY KEY (id);


--
-- Name: tag pk_id_user_id; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_id_user_id PRIMARY KEY (id, user_id);


--
-- Name: prompt prompt_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.prompt
    ADD CONSTRAINT prompt_pkey PRIMARY KEY (id);


--
-- Name: user user_oauth_sub_key; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_oauth_sub_key UNIQUE (oauth_sub);


--
-- Name: user_subscriptions user_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.user_subscriptions
    ADD CONSTRAINT user_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: auth_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX auth_id ON public.auth USING btree (id);


--
-- Name: chat_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX chat_id ON public.chat USING btree (id);


--
-- Name: chat_share_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX chat_share_id ON public.chat USING btree (share_id);


--
-- Name: chatidtag_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX chatidtag_id ON public.chatidtag USING btree (id);


--
-- Name: document_collection_name; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX document_collection_name ON public.document USING btree (collection_name);


--
-- Name: document_name; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX document_name ON public.document USING btree (name);


--
-- Name: file_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX file_id ON public.file USING btree (id);


--
-- Name: folder_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX folder_id_idx ON public.chat USING btree (folder_id);


--
-- Name: folder_id_user_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX folder_id_user_id_idx ON public.chat USING btree (folder_id, user_id);


--
-- Name: function_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX function_id ON public.function USING btree (id);


--
-- Name: idx_oauth_session_expires_at; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX idx_oauth_session_expires_at ON public.oauth_session USING btree (expires_at);


--
-- Name: idx_oauth_session_user_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX idx_oauth_session_user_id ON public.oauth_session USING btree (user_id);


--
-- Name: idx_oauth_session_user_provider; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX idx_oauth_session_user_provider ON public.oauth_session USING btree (user_id, provider);


--
-- Name: is_global_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX is_global_idx ON public.function USING btree (is_global);


--
-- Name: ix_payment_transactions_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_payment_transactions_id ON public.payment_transactions USING btree (id);


--
-- Name: ix_payment_transactions_reference; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX ix_payment_transactions_reference ON public.payment_transactions USING btree (reference);


--
-- Name: ix_payment_transactions_user_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_payment_transactions_user_id ON public.payment_transactions USING btree (user_id);


--
-- Name: ix_user_subscriptions_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_user_subscriptions_id ON public.user_subscriptions USING btree (id);


--
-- Name: ix_user_subscriptions_user_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_user_subscriptions_user_id ON public.user_subscriptions USING btree (user_id);


--
-- Name: memory_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX memory_id ON public.memory USING btree (id);


--
-- Name: model_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX model_id ON public.model USING btree (id);


--
-- Name: modelfile_tag_name; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX modelfile_tag_name ON public.modelfile USING btree (tag_name);


--
-- Name: prompt_command; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX prompt_command ON public.prompt USING btree (command);


--
-- Name: tag_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX tag_id ON public.tag USING btree (id);


--
-- Name: tool_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX tool_id ON public.tool USING btree (id);


--
-- Name: updated_at_user_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX updated_at_user_id_idx ON public.chat USING btree (updated_at, user_id);


--
-- Name: user_api_key; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX user_api_key ON public."user" USING btree (api_key);


--
-- Name: user_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX user_id ON public."user" USING btree (id);


--
-- Name: user_id_archived_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX user_id_archived_idx ON public.chat USING btree (user_id, archived);


--
-- Name: user_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX user_id_idx ON public.tag USING btree (user_id);


--
-- Name: user_id_pinned_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX user_id_pinned_idx ON public.chat USING btree (user_id, pinned);


--
-- Name: user_oauth_sub; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX user_oauth_sub ON public."user" USING btree (oauth_sub);


--
-- Name: oauth_session oauth_session_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.oauth_session
    ADD CONSTRAINT oauth_session_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict oylqjiPcL6KMekq05wsHPKfkxXczgWH9J9VbHsAqoKPAeB75bfdktBpRlkvltHa

