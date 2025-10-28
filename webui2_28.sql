--
-- PostgreSQL database dump
--

\restrict xzpp2bTNO1W4aD7jzeqDM88wq59ATUlDg7J78UCl3bvWPlPcJG1grNFLGZHE5cs

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
    email character varying(255),
    password text,
    active boolean
);


ALTER TABLE public.auth OWNER TO transcription;

--
-- Name: chat; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.chat (
    id character varying(255) NOT NULL,
    user_id character varying(255),
    title text,
    share_id2 text,
    archived2 boolean,
    created_at2 bigint,
    updated_at2 bigint,
    chat json,
    pinned boolean,
    meta json DEFAULT '{}'::json,
    folder_id text,
    share_id character varying(255),
    archived boolean NOT NULL
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
-- Name: file; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public.file (
    id character varying NOT NULL,
    user_id character varying,
    filename text,
    meta json,
    created_at bigint,
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
    is_expanded boolean,
    created_at bigint,
    updated_at bigint,
    data json
);


ALTER TABLE public.folder OWNER TO transcription;

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
    "timestamp" bigint NOT NULL
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
    name character varying(255),
    user_id character varying(255) NOT NULL,
    meta json
);


ALTER TABLE public.tag OWNER TO transcription;

--
-- Name: user; Type: TABLE; Schema: public; Owner: transcription
--

CREATE TABLE public."user" (
    id character varying(255) NOT NULL,
    name character varying(255),
    email character varying(255),
    role character varying(255),
    profile_image_url text,
    api_key2 character varying(255),
    created_at bigint,
    updated_at bigint,
    last_active_at bigint,
    settings text,
    info text,
    oauth_sub text,
    username character varying(50),
    bio text,
    gender text,
    date_of_birth date,
    api_key character varying(255)
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
20251028_payments_autogen
\.


--
-- Data for Name: auth; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.auth (id, email, password, active) FROM stdin;
\.


--
-- Data for Name: chat; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.chat (id, user_id, title, share_id2, archived2, created_at2, updated_at2, chat, pinned, meta, folder_id, share_id, archived) FROM stdin;
\.


--
-- Data for Name: chatidtag; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.chatidtag (id, tag_name, chat_id, user_id, "timestamp") FROM stdin;
\.


--
-- Data for Name: document; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.document (id, collection_name, name, title, filename, content, user_id, "timestamp") FROM stdin;
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
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public."group" (id, user_id, name, description, data, meta, permissions, user_ids, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: migratehistory; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.migratehistory (id, name, migrated_at) FROM stdin;
1	001_initial_schema	2025-10-28 11:09:01.398968
2	002_add_local_sharing	2025-10-28 11:13:23.40207
3	003_add_auth_api_key	2025-10-28 11:13:59.563638
4	004_add_archived	2025-10-28 11:17:55.052389
\.


--
-- Data for Name: modelfile; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.modelfile (id, tag_name, user_id, modelfile, "timestamp") FROM stdin;
\.


--
-- Data for Name: payment_transactions; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.payment_transactions (id, user_id, reference, amount, currency, plan_id, plan_name, billing_cycle, status, paystack_reference, paystack_status, gateway_response, gateway_response_data, group_id, paid_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: prompt; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.prompt (id, command, user_id, title, content, "timestamp") FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.tag (id, name, user_id, meta) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public."user" (id, name, email, role, profile_image_url, api_key2, created_at, updated_at, last_active_at, settings, info, oauth_sub, username, bio, gender, date_of_birth, api_key) FROM stdin;
\.


--
-- Data for Name: user_subscriptions; Type: TABLE DATA; Schema: public; Owner: transcription
--

COPY public.user_subscriptions (id, user_id, plan_id, plan_name, status, amount, currency, group_id, billing_cycle, started_at, expires_at, trial_end, current_period_end, transaction_reference, created_at, updated_at) FROM stdin;
\.


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
-- Name: chat chat_share_id_key; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.chat
    ADD CONSTRAINT chat_share_id_key UNIQUE (share_id2);


--
-- Name: document document_pkey; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id);


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
-- Name: user user_api_key_key; Type: CONSTRAINT; Schema: public; Owner: transcription
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_api_key_key UNIQUE (api_key2);


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
-- Name: folder_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX folder_id_idx ON public.chat USING btree (folder_id);


--
-- Name: folder_id_user_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX folder_id_user_id_idx ON public.chat USING btree (folder_id, user_id);


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
-- Name: updated_at_user_id_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX updated_at_user_id_idx ON public.chat USING btree (updated_at2, user_id);


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

CREATE INDEX user_id_archived_idx ON public.chat USING btree (user_id, archived2);


--
-- Name: user_id_pinned_idx; Type: INDEX; Schema: public; Owner: transcription
--

CREATE INDEX user_id_pinned_idx ON public.chat USING btree (user_id, pinned);


--
-- PostgreSQL database dump complete
--

\unrestrict xzpp2bTNO1W4aD7jzeqDM88wq59ATUlDg7J78UCl3bvWPlPcJG1grNFLGZHE5cs

