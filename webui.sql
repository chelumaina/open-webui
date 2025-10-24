--
-- PostgreSQL database dump
--

\restrict pgc5GXmp9hpUiz4X5w9ZhjdoDqpMdiElULPJ7MEUr9ZknA1yBfVJqCJyDUjd6eU

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

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: set_updated_at(); Type: FUNCTION; Schema: public; Owner: transcription
--

CREATE FUNCTION public.set_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END$$;


ALTER FUNCTION public.set_updated_at() OWNER TO transcription;

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
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    reference character varying(64) NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character varying(8) NOT NULL,
    plan_id character varying(64) NOT NULL,
    plan_name character varying(128) NOT NULL,
    status character varying(32) DEFAULT 'pending'::character varying NOT NULL,
    paystack_reference character varying(128),
    paystack_status character varying(64),
    gateway_response character varying(200),
    paid_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    gateway_response_data text,
    group_id character varying(200),
    billing_cycle character varying(200)
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
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    plan_id character varying(64) NOT NULL,
    plan_name character varying(128) NOT NULL,
    status character varying(32) DEFAULT 'pending'::character varying NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character varying(8) DEFAULT 'USD'::character varying NOT NULL,
    billing_cycle character varying(16) NOT NULL,
    started_at timestamp with time zone,
    expires_at timestamp with time zone,
    transaction_reference character varying(128),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    group_id character varying(200),
    trial_end timestamp without time zone,
    current_period_end timestamp without time zone,
    CONSTRAINT chk_currency_len CHECK (((length((currency)::text) >= 3) AND (length((currency)::text) <= 8))),
    CONSTRAINT user_subscriptions_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'pending'::character varying, 'canceled'::character varying, 'expired'::character varying, 'past_due'::character varying, 'trialing'::character varying])::text[])))
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
4844b2fe-1df4-4f91-a9cf-83b851b8ca06	chelumaina@gmail.com	$2b$12$h1inkjWOgDrlU0eYgZJt2uoooUmGtlCnxgw19kYnE2jjCTY./Ea7e	t
db0a25a5-f2e9-47d1-804a-2004b6b0c3d9	betty@gmail.com	$2b$12$84kSszbjWmAdNdhUDmSB3.BzNoBnZMDye9Qontk6DkAKhWIk0h0Ai	t
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
49cfb513-c406-4138-aef3-9454b0c14509	db0a25a5-f2e9-47d1-804a-2004b6b0c3d9	New Chat	\N	f	1761274433	1761274434	{"id": "", "title": "New Chat", "models": ["gpt-oss:120b"], "params": {}, "history": {"messages": {"62d40c4c-1a41-42b9-bb5a-3a9bfae45ad0": {"id": "62d40c4c-1a41-42b9-bb5a-3a9bfae45ad0", "parentId": null, "childrenIds": ["626acfeb-aff7-4960-a51b-9588d668ef7f"], "role": "user", "content": "Tell me a random fun fact about the Roman Empire", "timestamp": 1761274433, "models": ["gpt-oss:120b"]}, "626acfeb-aff7-4960-a51b-9588d668ef7f": {"parentId": "62d40c4c-1a41-42b9-bb5a-3a9bfae45ad0", "id": "626acfeb-aff7-4960-a51b-9588d668ef7f", "childrenIds": [], "role": "assistant", "content": "", "model": "gpt-oss:120b", "modelName": "gpt-oss:120b", "modelIdx": 0, "timestamp": 1761274433, "error": {"content": "401: unauthorized"}}}, "currentId": "626acfeb-aff7-4960-a51b-9588d668ef7f"}, "messages": [{"id": "62d40c4c-1a41-42b9-bb5a-3a9bfae45ad0", "parentId": null, "childrenIds": ["626acfeb-aff7-4960-a51b-9588d668ef7f"], "role": "user", "content": "Tell me a random fun fact about the Roman Empire", "timestamp": 1761274433, "models": ["gpt-oss:120b"]}, {"parentId": "62d40c4c-1a41-42b9-bb5a-3a9bfae45ad0", "id": "626acfeb-aff7-4960-a51b-9588d668ef7f", "childrenIds": [], "role": "assistant", "content": "", "model": "gpt-oss:120b", "modelName": "gpt-oss:120b", "modelIdx": 0, "timestamp": 1761274433}], "tags": [], "timestamp": 1761274433954, "files": []}	f	{}	\N
31217890-b3ec-48fc-878a-ee24033db297	db0a25a5-f2e9-47d1-804a-2004b6b0c3d9	New Chat	\N	f	1761278075	1761278075	{"id": "", "title": "New Chat", "models": ["gpt-oss:120b"], "params": {}, "history": {"messages": {"43d2f041-00a5-4230-a457-9491c6333714": {"id": "43d2f041-00a5-4230-a457-9491c6333714", "parentId": null, "childrenIds": ["b529af03-11ea-4325-88b1-672b770d56f2"], "role": "user", "content": "Show me a code snippet of a website's sticky header in CSS and JavaScript.", "timestamp": 1761278075, "models": ["gpt-oss:120b"]}, "b529af03-11ea-4325-88b1-672b770d56f2": {"parentId": "43d2f041-00a5-4230-a457-9491c6333714", "id": "b529af03-11ea-4325-88b1-672b770d56f2", "childrenIds": [], "role": "assistant", "content": "", "model": "gpt-oss:120b", "modelName": "gpt-oss:120b", "modelIdx": 0, "timestamp": 1761278075, "error": {"content": "401: unauthorized"}}}, "currentId": "b529af03-11ea-4325-88b1-672b770d56f2"}, "messages": [{"id": "43d2f041-00a5-4230-a457-9491c6333714", "parentId": null, "childrenIds": ["b529af03-11ea-4325-88b1-672b770d56f2"], "role": "user", "content": "Show me a code snippet of a website's sticky header in CSS and JavaScript.", "timestamp": 1761278075, "models": ["gpt-oss:120b"]}, {"parentId": "43d2f041-00a5-4230-a457-9491c6333714", "id": "b529af03-11ea-4325-88b1-672b770d56f2", "childrenIds": [], "role": "assistant", "content": "", "model": "gpt-oss:120b", "modelName": "gpt-oss:120b", "modelIdx": 0, "timestamp": 1761278075}], "tags": [], "timestamp": 1761278075129, "files": []}	f	{}	\N
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
1	{"version": 0, "ui": {"enable_signup": true, "default_user_role": "user", "enable_community_sharing": false, "enable_message_rating": true, "enable_user_webhooks": true, "pending_user_overlay_title": "", "pending_user_overlay_content": "", "watermark": ""}, "webhook_url": "", "auth": {"admin": {"show": true}, "api_key": {"enable": true, "endpoint_restrictions": false, "allowed_endpoints": ""}, "jwt_expiry": "4w"}, "webui": {"url": "http://localhost:8080"}, "channels": {"enable": true}, "notes": {"enable": true}, "ldap": {"enable": false}}	0	2025-10-23 11:25:44.99629	2025-10-24 05:50:05.08201
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
6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	Basic	Basic Plan Users	null	null	{"workspace": {"models": false, "knowledge": false, "prompts": false, "tools": false}, "sharing": {"public_models": false, "public_knowledge": false, "public_prompts": false, "public_tools": false, "public_notes": false}, "chat": {"controls": true, "valves": true, "system_prompt": true, "params": true, "file_upload": true, "delete": true, "delete_message": true, "continue_response": true, "regenerate_response": true, "rate_response": true, "edit": true, "share": true, "export": true, "stt": true, "tts": true, "call": true, "multiple_models": true, "temporary": true, "temporary_enforced": false}, "features": {"direct_tool_servers": false, "web_search": true, "image_generation": true, "code_interpreter": true, "notes": true}}	["db0a25a5-f2e9-47d1-804a-2004b6b0c3d9", "4844b2fe-1df4-4f91-a9cf-83b851b8ca06"]	1761232952	1761295572
8ca4c096-2b16-4e19-9586-4a162448fd63	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	Pro 	Pro Plan Users	null	null	{"workspace": {"models": false, "knowledge": false, "prompts": false, "tools": false}, "sharing": {"public_models": false, "public_knowledge": false, "public_prompts": false, "public_tools": false, "public_notes": false}, "chat": {"controls": true, "valves": true, "system_prompt": true, "params": true, "file_upload": true, "delete": true, "delete_message": true, "continue_response": true, "regenerate_response": true, "rate_response": true, "edit": true, "share": true, "export": true, "stt": true, "tts": true, "call": true, "multiple_models": true, "temporary": true, "temporary_enforced": false}, "features": {"direct_tool_servers": false, "web_search": true, "image_generation": true, "code_interpreter": true, "notes": true}}	["4844b2fe-1df4-4f91-a9cf-83b851b8ca06"]	1761232971	1761273709
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
1	001_initial_schema	2025-10-23 11:20:11.362182
2	002_add_local_sharing	2025-10-23 11:20:11.36633
3	003_add_auth_api_key	2025-10-23 11:20:11.368421
4	004_add_archived	2025-10-23 11:20:11.370851
5	005_add_updated_at	2025-10-23 11:20:11.387034
6	006_migrate_timestamps_and_charfields	2025-10-23 11:20:11.395267
7	007_add_user_last_active_at	2025-10-23 11:20:11.404286
8	008_add_memory	2025-10-23 11:20:11.408218
9	009_add_models	2025-10-23 11:20:11.413172
10	010_migrate_modelfiles_to_models	2025-10-23 11:20:11.416695
11	011_add_user_settings	2025-10-23 11:20:11.426635
12	012_add_tools	2025-10-23 11:20:11.429732
13	013_add_user_info	2025-10-23 11:20:11.431651
14	014_add_files	2025-10-23 11:20:11.434522
15	015_add_functions	2025-10-23 11:20:11.437431
16	016_add_valves_and_is_active	2025-10-23 11:20:11.44034
17	017_add_user_oauth_sub	2025-10-23 11:20:11.44235
18	018_add_function_is_global	2025-10-23 11:20:11.444154
\.


--
-- Data for Name: model; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, access_control, is_active) FROM stdin;
qwen3-coder:480b	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	qwen3-coder:480b	{"profile_image_url": "/static/favicon.png", "description": null, "capabilities": null}	{}	1761272459	1761272459	{}	f
kimi-k2:1t	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	kimi-k2:1t	{"profile_image_url": "/static/favicon.png", "description": null, "capabilities": null}	{}	1761272465	1761272465	{}	f
gpt-oss:20b	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	gpt-oss:20b	{"profile_image_url": "/static/favicon.png", "description": null, "capabilities": null}	{}	1761272467	1761272467	{}	f
glm-4.6	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	glm-4.6	{"profile_image_url": "/static/favicon.png", "description": null, "capabilities": null}	{}	1761272471	1761272471	{}	f
gpt-oss:120b	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	gpt-oss:120b	{"profile_image_url": "http://localhost:8080/static/favicon.png", "description": null, "capabilities": {"vision": true, "file_upload": true, "web_search": true, "image_generation": true, "code_interpreter": true, "citations": true, "status_updates": true}, "suggestion_prompts": null, "tags": []}	{}	1761273964	1761273964	{"read": {"group_ids": ["6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98", "8ca4c096-2b16-4e19-9586-4a162448fd63"], "user_ids": []}, "write": {"group_ids": [], "user_ids": []}}	t
qwen3-vl:235b	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	qwen3-vl:235b	{"profile_image_url": "http://localhost:8080/static/favicon.png", "description": null, "capabilities": {"vision": true, "file_upload": true, "web_search": true, "image_generation": true, "code_interpreter": true, "citations": true, "status_updates": true}, "suggestion_prompts": null, "tags": []}	{}	1761273977	1761273977	{"read": {"group_ids": ["8ca4c096-2b16-4e19-9586-4a162448fd63"], "user_ids": []}, "write": {"group_ids": [], "user_ids": []}}	t
deepseek-v3.1:671b	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	\N	deepseek-v3.1:671b	{"profile_image_url": "http://localhost:8080/static/favicon.png", "description": null, "capabilities": {"vision": true, "file_upload": true, "web_search": true, "image_generation": true, "code_interpreter": true, "citations": true, "status_updates": true, "usage": true}, "suggestion_prompts": null, "tags": []}	{}	1761233002	1761233002	{"read": {"group_ids": ["8ca4c096-2b16-4e19-9586-4a162448fd63"], "user_ids": []}, "write": {"group_ids": [], "user_ids": []}}	t
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

COPY public.payment_transactions (id, user_id, reference, amount, currency, plan_id, plan_name, status, paystack_reference, paystack_status, gateway_response, paid_at, created_at, updated_at, gateway_response_data, group_id, billing_cycle) FROM stdin;
336aec08-e430-49cf-8e79-80c6cd433baf	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	ref_1761211462_6ca5a11a	10.00	USD	basic	Basic Plan	success	\N	success	Successful	2025-10-23 15:33:08.304621+00	2025-10-23 12:24:23.508677+00	2025-10-23 15:33:07.602964+00	{'id': 5458072403, 'domain': 'test', 'status': 'success', 'reference': 'ref_1761211462_6ca5a11a', 'receipt_number': None, 'amount': 1000, 'message': None, 'gateway_response': 'Successful', 'paid_at': '2025-10-23T12:24:50.000Z', 'created_at': '2025-10-23T12:24:23.000Z', 'channel': 'card', 'currency': 'USD', 'ip_address': '41.215.58.26', 'metadata': {'user_id': '4844b2fe-1df4-4f91-a9cf-83b851b8ca06', 'plan_id': 'basic', 'plan_name': 'Basic Plan', 'custom_fields': [{'display_name': 'Plan', 'variable_name': 'plan', 'value': 'Basic Plan'}], 'referrer': 'http://localhost:5173/'}, 'log': {'start_time': 1761222267, 'time_spent': 24, 'attempts': 1, 'errors': 0, 'success': True, 'mobile': False, 'input': [], 'history': [{'type': 'action', 'message': 'Attempted to pay with card', 'time': 22}, {'type': 'success', 'message': 'Successfully paid with card', 'time': 24}]}, 'fees': 38, 'fees_split': None, 'authorization': {'authorization_code': 'AUTH_gs0tdb29fy', 'bin': '408408', 'last4': '4081', 'exp_month': '12', 'exp_year': '2030', 'channel': 'card', 'card_type': 'visa ', 'bank': 'TEST BANK', 'country_code': 'NG', 'brand': 'visa', 'reusable': True, 'signature': 'SIG_B854Q0ttEtcqRxBJAxJ8', 'account_name': None, 'receiver_bank_account_number': None, 'receiver_bank': None}, 'customer': {'id': 301188820, 'first_name': None, 'last_name': None, 'email': 'chelumaina@gmail.com', 'customer_code': 'CUS_1txmfn5hi2f23po', 'phone': None, 'metadata': None, 'risk_action': 'default', 'international_format_phone': None}, 'plan': None, 'split': {}, 'order_id': None, 'paidAt': '2025-10-23T12:24:50.000Z', 'createdAt': '2025-10-23T12:24:23.000Z', 'requested_amount': 1000, 'pos_transaction_data': None, 'source': None, 'fees_breakdown': None, 'connect': None, 'transaction_date': '2025-10-23T12:24:23.000Z', 'plan_object': {}, 'subaccount': {}}	\N	\N
05a00aa4-fae4-4c31-865f-0670de52021c	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	ref_1761261540_ae650359	20.00	USD	enterprise	Enterprise Plan	success	\N	success	Successful	2025-10-24 02:19:12.032646+00	2025-10-24 02:19:01.488614+00	2025-10-24 02:19:11.418858+00		8ca4c096-2b16-4e19-9586-4a162448fd63	\N
a1d8ec71-d840-4f05-a235-c4af43193e1f	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	ref_1761262873_1125a442	20.00	USD	enterprise2	Enterprise Plan	success	\N	success	[Test] Approved	2025-10-24 02:41:49.771989+00	2025-10-24 02:41:14.483043+00	2025-10-24 02:41:49.184349+00		8ca4c096-2b16-4e19-9586-4a162448fd63	\N
10fc4280-3d71-40d9-8327-d0346077a157	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	ref_1761260477_dd6b4f4d	10.00	USD	basic	Basic Plan	success	\N	success	Successful	2025-10-24 02:42:58.730602+00	2025-10-24 02:01:18.777112+00	2025-10-24 02:42:58.037429+00	{'id': 5459670902, 'domain': 'test', 'status': 'success', 'reference': 'ref_1761260477_dd6b4f4d', 'receipt_number': None, 'amount': 1000, 'message': None, 'gateway_response': 'Successful', 'paid_at': '2025-10-24T02:01:32.000Z', 'created_at': '2025-10-24T02:01:19.000Z', 'channel': 'card', 'currency': 'USD', 'ip_address': '41.209.3.219', 'metadata': {'user_id': '4844b2fe-1df4-4f91-a9cf-83b851b8ca06', 'plan_id': 'basic', 'plan_name': 'Basic Plan', 'custom_fields': [{'display_name': 'Plan', 'variable_name': 'plan', 'value': 'Basic Plan', 'group_id': '6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98'}], 'referrer': 'http://localhost:5173/'}, 'log': {'start_time': 1761271282, 'time_spent': 10, 'attempts': 1, 'errors': 0, 'success': True, 'mobile': False, 'input': [], 'history': [{'type': 'action', 'message': 'Attempted to pay with card', 'time': 9}, {'type': 'success', 'message': 'Successfully paid with card', 'time': 10}]}, 'fees': 38, 'fees_split': None, 'authorization': {'authorization_code': 'AUTH_514rf1uydo', 'bin': '408408', 'last4': '4081', 'exp_month': '12', 'exp_year': '2030', 'channel': 'card', 'card_type': 'visa ', 'bank': 'TEST BANK', 'country_code': 'NG', 'brand': 'visa', 'reusable': True, 'signature': 'SIG_B854Q0ttEtcqRxBJAxJ8', 'account_name': None, 'receiver_bank_account_number': None, 'receiver_bank': None}, 'customer': {'id': 301188820, 'first_name': None, 'last_name': None, 'email': 'chelumaina@gmail.com', 'customer_code': 'CUS_1txmfn5hi2f23po', 'phone': None, 'metadata': None, 'risk_action': 'default', 'international_format_phone': None}, 'plan': None, 'split': {}, 'order_id': None, 'paidAt': '2025-10-24T02:01:32.000Z', 'createdAt': '2025-10-24T02:01:19.000Z', 'requested_amount': 1000, 'pos_transaction_data': None, 'source': None, 'fees_breakdown': None, 'connect': None, 'transaction_date': '2025-10-24T02:01:19.000Z', 'plan_object': {}, 'subaccount': {}}	6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98	\N
06503b2c-b25d-46c6-a765-a7df8d98e650	db0a25a5-f2e9-47d1-804a-2004b6b0c3d9	ref_1761282508_310907f9	10.00	USD	basic	Basic Plan	success	\N	success	Successful	2025-10-24 08:46:12.02737+00	2025-10-24 08:08:30.107744+00	2025-10-24 08:46:11.238264+00		6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98	monthly
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
4844b2fe-1df4-4f91-a9cf-83b851b8ca06	Chelule Maina	chelumaina@gmail.com	admin	data:image/png;base64,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	\N	1761218744	1761218744	1761274423	{"ui": {"version": "0.6.34", "models": ["glm-4.6"]}}	null	\N	\N	\N	\N	\N
db0a25a5-f2e9-47d1-804a-2004b6b0c3d9	betty	betty@gmail.com	user	data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAE40lEQVR4Aeya228UVRzHv2dm270VxZZYjaSKlwceKg/GRkNMxGA1QYlKNBqJPuib6X9gjNH4om8aYzQoUSMJxktsjNFoAl4ekFAayjUQCBB4gBYKdLvL3mY4U66zO5ywJ5wzv5n+Nnu6c87Zc85vPp/8urtnxplZ1+tzocPAAT9IEWAhpHQALISFECNALBzOEBZCjACxcDhDWAgxAsTC4QyZF0KInWSSwuEMIWaLhbAQYgSIhcMZwkKIESAWDmcICyFGgFg4nCEshBgBYuEkKUOIoTMTDgsxw1V7Vhaijc7MQBZihqv2rCxEG52ZgSzEDFftWVmINjozA1mIGa7as7IQbXRmBrIQM1y1Z2Uh2ujMDGQhZrhqz8pCtNGZGUhaiCj0w71jeUfFuW2pGVKWZiUtJPf4F8ivGu2oFF74Dz1vTKG49iAKz21C99C7llDenGVIC9E/RQGRXQin70F0D46g8NJ2We/Vn87iyJQKCRN0FtyN4iu74N7+cLiDYC1ZQnwPzRNbosvkGLwz++FXTkrMviwtTzeL3JPftTTSqyZKiF+dRuXXVdFldBjlHx/F7IalKK2/E42jv7fRFrk+ZO5b09ZOqSFRQm4YnFfH+T9fRX3vV21DMvc829ZGqSGdQi4Rrm17/9LR1RfnlnuvVswdac+caiF+7Rz8RjkMx82F68RqqRYSsBYtAvyZI0Ez2ZJqIe5dKwARPsXmqQlQfoSjpRxph7E5i5YhP7whPMproL7zk3AbsVqyhAgBZPKRRWR75S/zwbmvtfmnNqKw+i/A6Q7hrk18DL96JtRGreJQC0gVTwC95/VjiCrFtQfk3tVmBPtf7uKVQOhflY/a+IeojX0A6o9ECdGF6VdOoXl8s+5wq+PmhRCRX4T8M79d3DoRrlXAnS6WLCFyL8ubHEdkmdoBb3oP/NIxoFGJ5JAZeBq5Fesi+6g0JkpIsJdVHl2JyPLLEyj/9BhmNy5D6evFKH//ELyzB9s4Z5ashtv/SFs7lQalECpB6sThzRxG+Ych1Pe3fPWVk2WXfyT/0nymVshl3NV/R9C6fSJ6Bi53k3tNvZCAuDc1HrxcKaKreOWY2sH8EDK9r4W7IHtJd14IcW69PyxEflvzq6fDbURqqRciuhbM3UZ0LW+/Rnf7JNVCRE7+IHz+b8DJXOtDXpPfGqpTqqRSiLPwAXQNvoXiyxMI7jgJAZf/rqr/jISaKFUSJSS4SaH42mFcvxyZu0musGYLskPvAW62jXV99+dyx5fm50cQbKKEBAEHnwnXLz3yLUKW6Gfj0M+o/v92dCeR1hiExHDmzSqqW9/B+U1vxrB4Z0s6nb3d8rubNb0F5ZVBvz6L5uTYXEaUvl0irxR+qjeX5VGkhVT+eBGlL/s6L+v7MfvNACqjw6jv+gyQGWKZq/ZypIVon1WCB7IQYvJYCAshRoBYOJwhLIQYAWLhcIawEDME0jIrZwgxkyyEhRAjQCwczhAWQowAsXA4Q1gIMQLEwuEMYSHECBALhzNEKcR+Jwuxz1y5IgtR4rHfyULsM1euyEKUeOx3shD7zJUrshAlHvudLMQ+c+WKLESJx34nC7HPXLkiC1HiMdOpmpWFqOjE0MdCYoCuWpKFqOjE0MdCYoCuWpKFqOjE0MdCYoCuWpKFqOjE0MdCYoCuWvICAAAA///eqF2iAAAABklEQVQDAPfKQmcgco+aAAAAAElFTkSuQmCC	\N	1761272277	1761272277	1761295720	null	null	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_subscriptions; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.user_subscriptions (id, user_id, plan_id, plan_name, status, amount, currency, billing_cycle, started_at, expires_at, transaction_reference, created_at, updated_at, group_id, trial_end, current_period_end) FROM stdin;
15cfe064-27c1-4473-a566-465392ae0a76	4844b2fe-1df4-4f91-a9cf-83b851b8ca06	basic	Basic Plan	active	10.00	USD	monthly	2025-10-23 12:44:02.848883+00	\N	ref_1761260477_dd6b4f4d	2025-10-23 12:44:02.848893+00	2025-10-24 02:42:58.037429+00	\N	\N	\N
da4a6d4e-aac7-4497-8466-9f7afe42897a	db0a25a5-f2e9-47d1-804a-2004b6b0c3d9	basic	Basic Plan	active	10.00	USD	monthly	2025-10-24 08:08:41.088988+00	2026-04-22 08:25:04.936993+00	ref_1761282508_310907f9	2025-10-24 08:08:41.089035+00	2025-10-24 08:46:11.238264+00	\N	2026-05-22 08:25:04.936993	\N
\.


--
-- Name: config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.config_id_seq', 1, true);


--
-- Name: document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.document_id_seq', 1, false);


--
-- Name: migratehistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: transcription
--

SELECT pg_catalog.setval('public.migratehistory_id_seq', 18, true);


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
-- Name: payment_transactions payment_transactions_reference_key; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.payment_transactions
    ADD CONSTRAINT payment_transactions_reference_key UNIQUE (reference);


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
-- Name: ix_payment_transactions_paystack_ref; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_payment_transactions_paystack_ref ON public.payment_transactions USING btree (paystack_reference);


--
-- Name: ix_payment_transactions_status; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_payment_transactions_status ON public.payment_transactions USING btree (status);


--
-- Name: ix_payment_transactions_user_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_payment_transactions_user_id ON public.payment_transactions USING btree (user_id);


--
-- Name: ix_user_subscriptions_status; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_user_subscriptions_status ON public.user_subscriptions USING btree (status);


--
-- Name: ix_user_subscriptions_user_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_user_subscriptions_user_id ON public.user_subscriptions USING btree (user_id);


--
-- Name: ix_user_subscriptions_user_status; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX ix_user_subscriptions_user_status ON public.user_subscriptions USING btree (user_id, status);


--
-- Name: memory_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX memory_id ON public.memory USING btree (id);


--
-- Name: model_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX model_id ON public.model USING btree (id);


--
-- Name: prompt_command; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX prompt_command ON public.prompt USING btree (command);


--
-- Name: tool_id; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX tool_id ON public.tool USING btree (id);


--
-- Name: updated_at_user_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX updated_at_user_id_idx ON public.chat USING btree (updated_at, user_id);


--
-- Name: uq_user_active_subscription; Type: INDEX; Schema: public; Owner: transcription
--

CREATE UNIQUE INDEX uq_user_active_subscription ON public.user_subscriptions USING btree (user_id) WHERE ((status)::text = 'active'::text);


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
-- Name: payment_transactions trg_payment_transactions_updated_at; Type: TRIGGER; Schema: public; Owner: transcription
--

CREATE TRIGGER trg_payment_transactions_updated_at BEFORE UPDATE ON public.payment_transactions FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: user_subscriptions trg_user_subscriptions_updated_at; Type: TRIGGER; Schema: public; Owner: transcription
--

CREATE TRIGGER trg_user_subscriptions_updated_at BEFORE UPDATE ON public.user_subscriptions FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: oauth_session oauth_session_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.oauth_session
    ADD CONSTRAINT oauth_session_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict pgc5GXmp9hpUiz4X5w9ZhjdoDqpMdiElULPJ7MEUr9ZknA1yBfVJqCJyDUjd6eU

