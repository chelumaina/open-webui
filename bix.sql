PGDMP  1    :                }            bix    17.4    17.0 |    F           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            G           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            H           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            I           1262    16388    bix    DATABASE     n   CREATE DATABASE bix WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE bix;
                     postgres    false                        3079    17083 	   uuid-ossp 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
    DROP EXTENSION "uuid-ossp";
                        false            J           0    0    EXTENSION "uuid-ossp"    COMMENT     W   COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
                             false    2            �            1259    16490    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    16396    auth    TABLE     �   CREATE TABLE public.auth (
    id character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password text NOT NULL,
    active boolean NOT NULL
);
    DROP TABLE public.auth;
       public         heap r       postgres    false            �            1259    16560    channel    TABLE     �   CREATE TABLE public.channel (
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
    DROP TABLE public.channel;
       public         heap r       postgres    false            �            1259    16581    channel_member    TABLE     �   CREATE TABLE public.channel_member (
    id text NOT NULL,
    channel_id text NOT NULL,
    user_id text NOT NULL,
    created_at bigint
);
 "   DROP TABLE public.channel_member;
       public         heap r       postgres    false            �            1259    16402    chat    TABLE     G  CREATE TABLE public.chat (
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
    folder_id text,
    response_token double precision DEFAULT 0.0,
    prompt_token double precision DEFAULT 0.0,
    cost_per_prompt_token double precision DEFAULT 0.001,
    cost_per_response_token double precision DEFAULT 0.001
);
    DROP TABLE public.chat;
       public         heap r       postgres    false            �            1259    16408 	   chatidtag    TABLE     �   CREATE TABLE public.chatidtag (
    id character varying(255) NOT NULL,
    tag_name character varying(255) NOT NULL,
    chat_id character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    "timestamp" bigint NOT NULL
);
    DROP TABLE public.chatidtag;
       public         heap r       postgres    false            �            1259    17155    checkout_sessions    TABLE     �  CREATE TABLE public.checkout_sessions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paypal_session_id character varying(255) NOT NULL,
    customer_id uuid NOT NULL,
    subscription_id uuid,
    status character varying(50) NOT NULL,
    amount numeric(10,2) NOT NULL,
    currency character varying(10) DEFAULT 'USD'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
 %   DROP TABLE public.checkout_sessions;
       public         heap r       postgres    false    2            �            1259    16496    config    TABLE     �   CREATE TABLE public.config (
    id integer NOT NULL,
    data json NOT NULL,
    version integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now()
);
    DROP TABLE public.config;
       public         heap r       postgres    false            �            1259    16495    config_id_seq    SEQUENCE     �   CREATE SEQUENCE public.config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.config_id_seq;
       public               postgres    false    236            K           0    0    config_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.config_id_seq OWNED BY public.config.id;
          public               postgres    false    235            �            1259    16415    document    TABLE     .  CREATE TABLE public.document (
    id integer NOT NULL,
    collection_name character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    title text NOT NULL,
    filename text NOT NULL,
    content text,
    user_id character varying(255) NOT NULL,
    "timestamp" bigint NOT NULL
);
    DROP TABLE public.document;
       public         heap r       postgres    false            �            1259    16414    document_id_seq    SEQUENCE     �   CREATE SEQUENCE public.document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.document_id_seq;
       public               postgres    false    224            L           0    0    document_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.document_id_seq OWNED BY public.document.id;
          public               postgres    false    223            �            1259    16533    feedback    TABLE     �   CREATE TABLE public.feedback (
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
    DROP TABLE public.feedback;
       public         heap r       postgres    false            �            1259    16477    file    TABLE     �   CREATE TABLE public.file (
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
    DROP TABLE public.file;
       public         heap r       postgres    false            �            1259    16518    folder    TABLE     �   CREATE TABLE public.folder (
    id text NOT NULL,
    parent_id text,
    user_id text NOT NULL,
    name text NOT NULL,
    items json,
    meta json,
    is_expanded boolean NOT NULL,
    created_at bigint NOT NULL,
    updated_at bigint NOT NULL
);
    DROP TABLE public.folder;
       public         heap r       postgres    false            �            1259    16483    function    TABLE     F  CREATE TABLE public.function (
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
    DROP TABLE public.function;
       public         heap r       postgres    false            �            1259    16552    group    TABLE     �   CREATE TABLE public."group" (
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
    DROP TABLE public."group";
       public         heap r       postgres    false            �            1259    17139    invoices    TABLE     <  CREATE TABLE public.invoices (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    customer_id uuid,
    subscription_id uuid,
    amount numeric(10,2) NOT NULL,
    currency character varying(10) DEFAULT 'USD'::character varying NOT NULL,
    status character varying(50) NOT NULL,
    issue_date timestamp without time zone NOT NULL,
    due_date timestamp without time zone,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    paypal_order_id character varying(200),
    captured_json json
);
    DROP TABLE public.invoices;
       public         heap r       postgres    false    2            �            1259    16506 	   knowledge    TABLE     �   CREATE TABLE public.knowledge (
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
    DROP TABLE public.knowledge;
       public         heap r       postgres    false            �            1259    16459    memory    TABLE     �   CREATE TABLE public.memory (
    id character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    content text NOT NULL,
    updated_at bigint NOT NULL,
    created_at bigint NOT NULL
);
    DROP TABLE public.memory;
       public         heap r       postgres    false            �            1259    16567    message    TABLE     �   CREATE TABLE public.message (
    id text NOT NULL,
    user_id text,
    channel_id text,
    content text,
    data json,
    meta json,
    created_at bigint,
    updated_at bigint,
    parent_id text
);
    DROP TABLE public.message;
       public         heap r       postgres    false            �            1259    16574    message_reaction    TABLE     �   CREATE TABLE public.message_reaction (
    id text NOT NULL,
    user_id text NOT NULL,
    message_id text NOT NULL,
    name text NOT NULL,
    created_at bigint
);
 $   DROP TABLE public.message_reaction;
       public         heap r       postgres    false            �            1259    16390    migratehistory    TABLE     �   CREATE TABLE public.migratehistory (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    migrated_at timestamp without time zone NOT NULL
);
 "   DROP TABLE public.migratehistory;
       public         heap r       postgres    false            �            1259    16389    migratehistory_id_seq    SEQUENCE     �   CREATE SEQUENCE public.migratehistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.migratehistory_id_seq;
       public               postgres    false    219            M           0    0    migratehistory_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.migratehistory_id_seq OWNED BY public.migratehistory.id;
          public               postgres    false    218            �            1259    16465    model    TABLE     7  CREATE TABLE public.model (
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
    DROP TABLE public.model;
       public         heap r       postgres    false            �            1259    17094    plans    TABLE     &  CREATE TABLE public.plans (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paypal_plan_id character varying(255),
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    currency character varying(10) DEFAULT 'USD'::character varying NOT NULL,
    billing_cycle character varying(50) NOT NULL,
    status character varying(50) DEFAULT 'ACTIVE'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
    DROP TABLE public.plans;
       public         heap r       postgres    false    2            �            1259    16436    prompt    TABLE        CREATE TABLE public.prompt (
    id integer NOT NULL,
    command character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    "timestamp" bigint NOT NULL,
    access_control json
);
    DROP TABLE public.prompt;
       public         heap r       postgres    false            �            1259    16435    prompt_id_seq    SEQUENCE     �   CREATE SEQUENCE public.prompt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.prompt_id_seq;
       public               postgres    false    226            N           0    0    prompt_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.prompt_id_seq OWNED BY public.prompt.id;
          public               postgres    false    225            �            1259    17108    subscriptions    TABLE     �  CREATE TABLE public.subscriptions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    customer_id uuid NOT NULL,
    plan_id uuid,
    status character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    next_billing_date timestamp without time zone,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
 !   DROP TABLE public.subscriptions;
       public         heap r       postgres    false    2            �            1259    16445    tag    TABLE     �   CREATE TABLE public.tag (
    id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    meta json
);
    DROP TABLE public.tag;
       public         heap r       postgres    false            �            1259    16471    tool    TABLE       CREATE TABLE public.tool (
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
    DROP TABLE public.tool;
       public         heap r       postgres    false            �            1259    17123    transactions    TABLE       CREATE TABLE public.transactions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paypal_transaction_id character varying(255) NOT NULL,
    subscription_id uuid NOT NULL,
    amount numeric(10,2) NOT NULL,
    currency character varying(10) DEFAULT 'USD'::character varying NOT NULL,
    status character varying(50) NOT NULL,
    transaction_date timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);
     DROP TABLE public.transactions;
       public         heap r       postgres    false    2            �            1259    16451    user    TABLE     �  CREATE TABLE public."user" (
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
    oauth_sub text
);
    DROP TABLE public."user";
       public         heap r       postgres    false            8           2604    16499 	   config id    DEFAULT     f   ALTER TABLE ONLY public.config ALTER COLUMN id SET DEFAULT nextval('public.config_id_seq'::regclass);
 8   ALTER TABLE public.config ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    236    235    236            5           2604    16418    document id    DEFAULT     j   ALTER TABLE ONLY public.document ALTER COLUMN id SET DEFAULT nextval('public.document_id_seq'::regclass);
 :   ALTER TABLE public.document ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    223    224            /           2604    16393    migratehistory id    DEFAULT     v   ALTER TABLE ONLY public.migratehistory ALTER COLUMN id SET DEFAULT nextval('public.migratehistory_id_seq'::regclass);
 @   ALTER TABLE public.migratehistory ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    219    218    219            6           2604    16439 	   prompt id    DEFAULT     f   ALTER TABLE ONLY public.prompt ALTER COLUMN id SET DEFAULT nextval('public.prompt_id_seq'::regclass);
 8   ALTER TABLE public.prompt ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    225    226            4          0    16490    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    234   O�       &          0    16396    auth 
   TABLE DATA           ;   COPY public.auth (id, email, password, active) FROM stdin;
    public               postgres    false    220   y�       ;          0    16560    channel 
   TABLE DATA           {   COPY public.channel (id, user_id, name, description, data, meta, access_control, created_at, updated_at, type) FROM stdin;
    public               postgres    false    241   ^�       >          0    16581    channel_member 
   TABLE DATA           M   COPY public.channel_member (id, channel_id, user_id, created_at) FROM stdin;
    public               postgres    false    244   {�       '          0    16402    chat 
   TABLE DATA           �   COPY public.chat (id, user_id, title, share_id, archived, created_at, updated_at, chat, pinned, meta, folder_id, response_token, prompt_token, cost_per_prompt_token, cost_per_response_token) FROM stdin;
    public               postgres    false    221   ��       (          0    16408 	   chatidtag 
   TABLE DATA           P   COPY public.chatidtag (id, tag_name, chat_id, user_id, "timestamp") FROM stdin;
    public               postgres    false    222   ��      C          0    17155    checkout_sessions 
   TABLE DATA           �   COPY public.checkout_sessions (id, paypal_session_id, customer_id, subscription_id, status, amount, currency, created_at, updated_at) FROM stdin;
    public               postgres    false    249   ��      6          0    16496    config 
   TABLE DATA           K   COPY public.config (id, data, version, created_at, updated_at) FROM stdin;
    public               postgres    false    236   ܞ      *          0    16415    document 
   TABLE DATA           m   COPY public.document (id, collection_name, name, title, filename, content, user_id, "timestamp") FROM stdin;
    public               postgres    false    224   ,�      9          0    16533    feedback 
   TABLE DATA           l   COPY public.feedback (id, user_id, version, type, data, meta, snapshot, created_at, updated_at) FROM stdin;
    public               postgres    false    239   I�      2          0    16477    file 
   TABLE DATA           u   COPY public.file (id, user_id, filename, meta, created_at, hash, data, updated_at, path, access_control) FROM stdin;
    public               postgres    false    232   f�      8          0    16518    folder 
   TABLE DATA           p   COPY public.folder (id, parent_id, user_id, name, items, meta, is_expanded, created_at, updated_at) FROM stdin;
    public               postgres    false    238   ��      3          0    16483    function 
   TABLE DATA           �   COPY public.function (id, user_id, name, type, content, meta, created_at, updated_at, valves, is_active, is_global) FROM stdin;
    public               postgres    false    233   ޱ      :          0    16552    group 
   TABLE DATA           |   COPY public."group" (id, user_id, name, description, data, meta, permissions, user_ids, created_at, updated_at) FROM stdin;
    public               postgres    false    240   ��      B          0    17139    invoices 
   TABLE DATA           �   COPY public.invoices (id, customer_id, subscription_id, amount, currency, status, issue_date, due_date, created_at, updated_at, paypal_order_id, captured_json) FROM stdin;
    public               postgres    false    248   �      7          0    16506 	   knowledge 
   TABLE DATA           w   COPY public.knowledge (id, user_id, name, description, data, meta, created_at, updated_at, access_control) FROM stdin;
    public               postgres    false    237   0�      /          0    16459    memory 
   TABLE DATA           N   COPY public.memory (id, user_id, content, updated_at, created_at) FROM stdin;
    public               postgres    false    229   M�      <          0    16567    message 
   TABLE DATA           r   COPY public.message (id, user_id, channel_id, content, data, meta, created_at, updated_at, parent_id) FROM stdin;
    public               postgres    false    242   j�      =          0    16574    message_reaction 
   TABLE DATA           U   COPY public.message_reaction (id, user_id, message_id, name, created_at) FROM stdin;
    public               postgres    false    243   ��      %          0    16390    migratehistory 
   TABLE DATA           ?   COPY public.migratehistory (id, name, migrated_at) FROM stdin;
    public               postgres    false    219   ��      0          0    16465    model 
   TABLE DATA           �   COPY public.model (id, user_id, base_model_id, name, meta, params, created_at, updated_at, access_control, is_active) FROM stdin;
    public               postgres    false    230   �      ?          0    17094    plans 
   TABLE DATA           �   COPY public.plans (id, paypal_plan_id, name, description, price, currency, billing_cycle, status, created_at, updated_at) FROM stdin;
    public               postgres    false    245   ��      ,          0    16436    prompt 
   TABLE DATA           c   COPY public.prompt (id, command, user_id, title, content, "timestamp", access_control) FROM stdin;
    public               postgres    false    226   p�      @          0    17108    subscriptions 
   TABLE DATA           �   COPY public.subscriptions (id, customer_id, plan_id, status, start_date, end_date, next_billing_date, created_at, updated_at) FROM stdin;
    public               postgres    false    246   ��      -          0    16445    tag 
   TABLE DATA           6   COPY public.tag (id, name, user_id, meta) FROM stdin;
    public               postgres    false    227   {�      1          0    16471    tool 
   TABLE DATA           w   COPY public.tool (id, user_id, name, content, specs, meta, created_at, updated_at, valves, access_control) FROM stdin;
    public               postgres    false    231   ��      A          0    17123    transactions 
   TABLE DATA           �   COPY public.transactions (id, paypal_transaction_id, subscription_id, amount, currency, status, transaction_date, created_at, updated_at) FROM stdin;
    public               postgres    false    247   �      .          0    16451    user 
   TABLE DATA           �   COPY public."user" (id, name, email, role, profile_image_url, api_key, created_at, updated_at, last_active_at, settings, info, oauth_sub) FROM stdin;
    public               postgres    false    228   1�      O           0    0    config_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.config_id_seq', 1, true);
          public               postgres    false    235            P           0    0    document_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.document_id_seq', 1, false);
          public               postgres    false    223            Q           0    0    migratehistory_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.migratehistory_id_seq', 18, true);
          public               postgres    false    218            R           0    0    prompt_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.prompt_id_seq', 1, false);
          public               postgres    false    225            g           2606    16494 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    234            y           2606    16587 "   channel_member channel_member_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.channel_member
    ADD CONSTRAINT channel_member_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.channel_member DROP CONSTRAINT channel_member_pkey;
       public                 postgres    false    244            s           2606    16566    channel channel_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.channel DROP CONSTRAINT channel_pkey;
       public                 postgres    false    241            �           2606    17165 9   checkout_sessions checkout_sessions_paypal_session_id_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.checkout_sessions
    ADD CONSTRAINT checkout_sessions_paypal_session_id_key UNIQUE (paypal_session_id);
 c   ALTER TABLE ONLY public.checkout_sessions DROP CONSTRAINT checkout_sessions_paypal_session_id_key;
       public                 postgres    false    249            �           2606    17163 (   checkout_sessions checkout_sessions_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.checkout_sessions
    ADD CONSTRAINT checkout_sessions_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.checkout_sessions DROP CONSTRAINT checkout_sessions_pkey;
       public                 postgres    false    249            i           2606    16505    config config_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.config
    ADD CONSTRAINT config_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.config DROP CONSTRAINT config_pkey;
       public                 postgres    false    236            X           2606    16422    document document_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.document DROP CONSTRAINT document_pkey;
       public                 postgres    false    224            o           2606    16539    feedback feedback_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.feedback DROP CONSTRAINT feedback_pkey;
       public                 postgres    false    239            m           2606    16526    folder folder_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.folder
    ADD CONSTRAINT folder_pkey PRIMARY KEY (id, user_id);
 <   ALTER TABLE ONLY public.folder DROP CONSTRAINT folder_pkey;
       public                 postgres    false    238    238            q           2606    16558    group group_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public."group" DROP CONSTRAINT group_pkey;
       public                 postgres    false    240            �           2606    17147    invoices invoices_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.invoices DROP CONSTRAINT invoices_pkey;
       public                 postgres    false    248            k           2606    16512    knowledge knowledge_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.knowledge
    ADD CONSTRAINT knowledge_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.knowledge DROP CONSTRAINT knowledge_pkey;
       public                 postgres    false    237            u           2606    16573    message message_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.message DROP CONSTRAINT message_pkey;
       public                 postgres    false    242            w           2606    16580 &   message_reaction message_reaction_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.message_reaction
    ADD CONSTRAINT message_reaction_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.message_reaction DROP CONSTRAINT message_reaction_pkey;
       public                 postgres    false    243            P           2606    16395 "   migratehistory migratehistory_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.migratehistory
    ADD CONSTRAINT migratehistory_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.migratehistory DROP CONSTRAINT migratehistory_pkey;
       public                 postgres    false    219            ]           2606    16517    tag pk_id_user_id 
   CONSTRAINT     X   ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_id_user_id PRIMARY KEY (id, user_id);
 ;   ALTER TABLE ONLY public.tag DROP CONSTRAINT pk_id_user_id;
       public                 postgres    false    227    227            |           2606    17107    plans plans_paypal_plan_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_paypal_plan_id_key UNIQUE (paypal_plan_id);
 H   ALTER TABLE ONLY public.plans DROP CONSTRAINT plans_paypal_plan_id_key;
       public                 postgres    false    245            ~           2606    17105    plans plans_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.plans DROP CONSTRAINT plans_pkey;
       public                 postgres    false    245            [           2606    16443    prompt prompt_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.prompt
    ADD CONSTRAINT prompt_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.prompt DROP CONSTRAINT prompt_pkey;
       public                 postgres    false    226            �           2606    17115     subscriptions subscriptions_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.subscriptions DROP CONSTRAINT subscriptions_pkey;
       public                 postgres    false    246            �           2606    17133 3   transactions transactions_paypal_transaction_id_key 
   CONSTRAINT        ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_paypal_transaction_id_key UNIQUE (paypal_transaction_id);
 ]   ALTER TABLE ONLY public.transactions DROP CONSTRAINT transactions_paypal_transaction_id_key;
       public                 postgres    false    247            �           2606    17131    transactions transactions_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.transactions DROP CONSTRAINT transactions_pkey;
       public                 postgres    false    247            Q           1259    16401    auth_id    INDEX     =   CREATE UNIQUE INDEX auth_id ON public.auth USING btree (id);
    DROP INDEX public.auth_id;
       public                 postgres    false    220            R           1259    16407    chat_id    INDEX     =   CREATE UNIQUE INDEX chat_id ON public.chat USING btree (id);
    DROP INDEX public.chat_id;
       public                 postgres    false    221            S           1259    16457    chat_share_id    INDEX     I   CREATE UNIQUE INDEX chat_share_id ON public.chat USING btree (share_id);
 !   DROP INDEX public.chat_share_id;
       public                 postgres    false    221            T           1259    16413    chatidtag_id    INDEX     G   CREATE UNIQUE INDEX chatidtag_id ON public.chatidtag USING btree (id);
     DROP INDEX public.chatidtag_id;
       public                 postgres    false    222            U           1259    16423    document_collection_name    INDEX     _   CREATE UNIQUE INDEX document_collection_name ON public.document USING btree (collection_name);
 ,   DROP INDEX public.document_collection_name;
       public                 postgres    false    224            V           1259    16424    document_name    INDEX     I   CREATE UNIQUE INDEX document_name ON public.document USING btree (name);
 !   DROP INDEX public.document_name;
       public                 postgres    false    224            d           1259    16482    file_id    INDEX     =   CREATE UNIQUE INDEX file_id ON public.file USING btree (id);
    DROP INDEX public.file_id;
       public                 postgres    false    232            e           1259    16488    function_id    INDEX     E   CREATE UNIQUE INDEX function_id ON public.function USING btree (id);
    DROP INDEX public.function_id;
       public                 postgres    false    233            �           1259    17175    idx_checkout_sessions_status    INDEX     \   CREATE INDEX idx_checkout_sessions_status ON public.checkout_sessions USING btree (status);
 0   DROP INDEX public.idx_checkout_sessions_status;
       public                 postgres    false    249            �           1259    17174    idx_invoices_status    INDEX     J   CREATE INDEX idx_invoices_status ON public.invoices USING btree (status);
 '   DROP INDEX public.idx_invoices_status;
       public                 postgres    false    248            z           1259    17171    idx_plans_status    INDEX     D   CREATE INDEX idx_plans_status ON public.plans USING btree (status);
 $   DROP INDEX public.idx_plans_status;
       public                 postgres    false    245                       1259    17172    idx_subscriptions_status    INDEX     T   CREATE INDEX idx_subscriptions_status ON public.subscriptions USING btree (status);
 ,   DROP INDEX public.idx_subscriptions_status;
       public                 postgres    false    246            �           1259    17173    idx_transactions_status    INDEX     R   CREATE INDEX idx_transactions_status ON public.transactions USING btree (status);
 +   DROP INDEX public.idx_transactions_status;
       public                 postgres    false    247            a           1259    16464 	   memory_id    INDEX     A   CREATE UNIQUE INDEX memory_id ON public.memory USING btree (id);
    DROP INDEX public.memory_id;
       public                 postgres    false    229            b           1259    16470    model_id    INDEX     ?   CREATE UNIQUE INDEX model_id ON public.model USING btree (id);
    DROP INDEX public.model_id;
       public                 postgres    false    230            Y           1259    16444    prompt_command    INDEX     K   CREATE UNIQUE INDEX prompt_command ON public.prompt USING btree (command);
 "   DROP INDEX public.prompt_command;
       public                 postgres    false    226            c           1259    16476    tool_id    INDEX     =   CREATE UNIQUE INDEX tool_id ON public.tool USING btree (id);
    DROP INDEX public.tool_id;
       public                 postgres    false    231            ^           1259    16458    user_api_key    INDEX     I   CREATE UNIQUE INDEX user_api_key ON public."user" USING btree (api_key);
     DROP INDEX public.user_api_key;
       public                 postgres    false    228            _           1259    16456    user_id    INDEX     ?   CREATE UNIQUE INDEX user_id ON public."user" USING btree (id);
    DROP INDEX public.user_id;
       public                 postgres    false    228            `           1259    16489    user_oauth_sub    INDEX     M   CREATE UNIQUE INDEX user_oauth_sub ON public."user" USING btree (oauth_sub);
 "   DROP INDEX public.user_oauth_sub;
       public                 postgres    false    228            �           2606    17166 8   checkout_sessions checkout_sessions_subscription_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.checkout_sessions
    ADD CONSTRAINT checkout_sessions_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id) ON DELETE SET NULL;
 b   ALTER TABLE ONLY public.checkout_sessions DROP CONSTRAINT checkout_sessions_subscription_id_fkey;
       public               postgres    false    249    246    3457            �           2606    17150 &   invoices invoices_subscription_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id) ON DELETE SET NULL;
 P   ALTER TABLE ONLY public.invoices DROP CONSTRAINT invoices_subscription_id_fkey;
       public               postgres    false    248    246    3457            �           2606    17118 (   subscriptions subscriptions_plan_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.subscriptions DROP CONSTRAINT subscriptions_plan_id_fkey;
       public               postgres    false    246    3454    245            �           2606    17134 .   transactions transactions_subscription_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.transactions DROP CONSTRAINT transactions_subscription_id_fkey;
       public               postgres    false    247    246    3457            4      x�36�0L52J�H20����� '��      &   �   x�Mͻr�@ ���v�
��vf����Jel�޽�5��a��X�:��ԁ@$�NY&�Q�:A�$�PJ���<t�;���m��&��&I�9.�ݪ<��KA����۰���]�n��KyXԲ+���;e�0�K�):0	2�H�	���	Ӓ@si��I��Cc}k��w����&�
������)Ɵm��xS�.�s��U�"�A��6�z��q�%�J�      ;      x������ � �      >      x������ � �      '      x����֕ �����gY�*0�_*�dɊ�'��Y������� 8`�	 ������� ��߾�� (B%E.'pw�"����g_�(�s/��8v��B�q�f9YJ���I�f����L�@����<iJ_�pݕ�?�V��nD���o?�?�Cύ��������]�]�ڢ-%~�?�/7U&����Gͦ*ˍsm���ѿõ����������i���mdӈ��k��ȱ��f�{��y^j�yb����8S7u2���2�v~�ܶ��7�}Y�7�MQf���l�Q��vh�Q��^�Xf�6]�	,'��cI�+����5>:��-<��Z�;c#���g�JE�/E}�6�ꢕ�0�7��ȫ�l+#/��(�F{#���7W��f�����>�-�"}C�Ӫ�e�ծ-���k�f�q�6d �g��< �l`3jf��C��:�v�������o�F���<�	�YW��g�ܟڞ2�!�_�t_����A�Հ��m!��"܅ {�ą�b�-r�6ߋ�����������y�oeY6���D��,w-3c�	@���6��"'JR;��)������2^� �Q����
��5�rq��v��3�V.�_����?iO=����d*���,0=�fZ���ifE���<��Y����$������$'�f 1��u-�	 4�%�}%��6ȥ50`�1������H�}K�}�[��ͮ���)�\R�V;Vs���W܏K�,�O�W#`7"3��DY+k J�]� ��u������ݠDk�T2���
�x0 -^���X�7FY����׏^����˪�o����+���_�e!�+�twS�7�HX9�@�`�wվ̌�[V Bs�����ZK�I-B�MedE�����j+W��~ml��w[��G�>���Xp�m[y+kc7��q��ݛ���m��!,���~�Q_O��hڗJ#< <�]�D! B�U�F�G[���_!�ھ��]�
5@�^����jE�پm��Dqh;>¨�D6����|M=S����jO�Y��5�/����е����I�O��ٕo�FƏ���1b���؈A�#M|cmlݼ��q�=����d+��Q�M���?��Rڵ2��]-�"=^&�P��9w�w�|h�<5�f	�s��?��X��E�(�_�"��f)Z�	7���a?�9 ��Z�>z^ޑ�Z��T��g� �,ό �f"����$J��9����O?����	�bGz��2p�E {�Qn:��-E��l9p�f�>K�J?�%h���yh�<�Ly��V�>>)�2,)M��>��E
��@Ce���x �wC/4�4�I{�?�d�Lc��Q���d���/�]�1� M�8�����Ms!�哊i� �<����V�ef �-u�<���е37��)Njz9�"q�Ȍ�ąkp�%F���V�#!1�N䧁i�q�I�ر�)������i�K\L�s	��
���� D+�C�'ݦ�Oz��Ɛ?�:-�C��T(�d;A�!j�-;�%��Ѵ�w�������KRx�Vu��-	L���R��.�I�ޮ��'%XYFOj�Z�B�������[���x5��2��m���f[��we췙�$�`Û�.�
�?���	mlo��ff�	�*��<�[�����{QD`O	 @<ui�F�ǯjF_������6B�����`ٗmk�Fp��b#���'e檟{H��mX��%<&#�?�WUve�K�2E��$��$������'`�2 0�h�� �)�7-�ӷ�2���w��7�ȉn���)V�czS�躱������0�]��AX1��9ѵ�p"]81����$'F�b�Y���1�\�XV��C���DM���6%/s�c�<���G��e �����ʟv%hI��T�84����Fs#���@J���ZB?����*���Vz�k��� hk�/;�����5��gpK�̋;x�Q�=!���@%�
7jcy�CY�?��NŞ�i�EI�P�|
����"�'L���/��5m��"��D(�!���~"�\���`B�L!����)A��<p�T��꽧2ӛ��Tz��啡��g��]- ){$Wƺ��[V�pC�мA遲����A����d0��Ӵ���W��O�E�"9_��k��+��'I���%1�����˦��D��,'��&S�����G���-�G�$����������榨[�o ���[�%��w�GU�O���3���gJ����r�I�꺑�`4�vŁ>4��n��	�:�B�Δ\<�]�j�������չѷ{��oF.n+��4�7��6-��4T���@6�㠽26��H9nV�W������p4E��a�������"������X�q�X0��H��Y��Ĥj%��~T+�ie���"�>���J�[��vu��#xd����3��؂\�����c�*e�"����O)qe���T;�}ԫ�T-�x�Oyr�ak<��=QP�?��z����
���=�J�}�몗�hڢ�bO��)nD�F��k��D�w($�;�TUe�v4�2>
<g���S29p��3y`����>
X��3u�i�lۓ&hwe��лw,,��P�s�By�Q�}\p�?��O�)��� [
����?�R��i�F�-��������;��<�;Qt��<�#X'����N5O�-�	�Н�#}?�m׳��]�|���9g�8SȐ{F����uv���9�8�G��=�tCx�%�����gI�Y�'}!��@L��(��W��Wc`���o�=�P倊��R���гo�M�DN_���)b���+��+􂀑T��x�>�	e�ǔ"�qߐ�&I�Ww�[ �����k�=��ѥ�o;��c��3q���ދ]ǶC�ύ����Q�J�S����*5���z{2��sŵ��|��1������{�#ǋ�H�Њ��$��P>�<	��KYk	�+�<)�5�1j��ӱ!�7�i
~`_,ɚ�ܱ`�O���W��hB��c���$j��8�$A������b�E�g�7b�t�=����گoP���ڪנuu�Xt� +�)]��&��䊳9w�N���7]*�D[Y$�(M%�}��h��_�:Ǽ2�28u{<��R��xA��i��g67t>ڢs��D$F�8<�)���d}����ߴ�8�p����p�m���{#���v0GK�+�`f��L��u��RL3� �� �OY r��k�2Y;3U� �!�W7՝F���6}�+��> rpw/����?�~ ��������I|#������[h�b:8чшD>A(U��h�RP��a�Y����s���wH V˃>K`��[��;g���-��j���۽c�1Ћl�e,|˷�c���Tt�C��t�i8�Zl��r@A�0���*ۧ�˚ ��x�b������Tu�2|7�T��=s�Q�[7@������V��u�C)ހ4[�kR7���G*��a6˝,K��F�C�QE���=�F��P0"u]��9@DI����Tf�T�b�������j$u�G2Ą"�ZK�Rl�����>���N�"���d��R����^��Ƌ�ʙ�D��{�"�F��cϢ-n%�:��� ��]��(�X'�N�؆l����Plo��Vf�~�iZ��wL2��>�ğ>(}#�C���B��q򶲢���
�����)*��p�*1�(��q��g�C��Rp^��4�s��%i��5pC&$#����#rR7���ۆ�ɝ����e�v��D���Ӟ���>�0"ɢUI��"(��`%��f 4:-�r莥E���=~ �Z����2?{n|�����d`�^��Z�e_ 2�P6�|34Ĉ�Y1�P!c`y�
�R��H�[d��s5���C���V�R��,3�b�m���kI7�J,���>��]��V?9WO�!��<C'�j;1�m��N�- U��S�H�TCJ@Y    ���	1��c[�x�$����רG1k�»j��(o��P� vGW�`j�>�W �
[#z�(��&GNR�cT�5ǤAY
J�4 �}��|��G�zkd[������	qD�M�R��ЭX1zQ01B4,��]�=w���U@[�0�i����dTz��f�������G��Pv��'�mqhs��i.�gۘNF1��d�8r��u���e��ۓH��qq�s7�r��:�u��u������{R	8ˍ:W	�T-,U3�����]�K��o�]���qh��.��%޺�[�x�o]�K�u��.��%޺�[�x�Gl�C�3�"	ok��vw���j�c� ���c�Gmx����m����/l3�0c�N\7�}���������������c��=L3v�Č� <�4Ȅ���Y��
h[Rz2Js3�p��w�y�N�$�V�:��Nƌ�K�^�v;���l��x�+�x��+�O��uA!�-4\@���A�������6��=�}հe��h+?������z]��7d�q�G�v�o��[�׭,6����[��\�ϔ�գ��Ʊ�~�([ݨ��34|���b7�SWڍ�
Gٕ��2��v�q�Kf�(Ĥ�l, ����B����E�Wd��'ת�=Ո�E��_rH�j�Rz	�S�:�:V�e>�'�-q�&~^K�G�^����3���&��G59z���M��ZMW`�(�)�vB?Ĳҩ�"��đ�
�=;�{�u���{�#���w}�~�}2���a��#fϝ/��^�sQ��Z\����P��q$L�Vd��mw�O���s�[�?ٱ#��<3y����$�V��vne�;�O�0%V�ؤ �nj�2p�-+��Oߞv��<���"r2+�e�8�+�c3N|i�ve��|������g�+��v,�.h� ���af� ����
.���ϐ@KtZ�M��CcYo��F�s�N��N���Ŀ�{��AȺ������Sճq�+�gk<߈u��}���?�z� ��<�y���`\�
r�v ��)}o<.��H�1뢥�<�'� E�I#�Q��S��o��z�]N�����ϣ������G}�Ͽ�����Q����_��W8+�%�T`�[Q6i<��z�ex�VB@�Q��0(��6C���Gą�D�K�nD7�̩���;�/Rxf���J6xF�]�9����Jj��=(TU�#R��L`:|�C�u�G~5���# Z�/p^��O��oT�[\AKa	0SqG�A���|�l�ƥ����WSl������ck�?�R�Llǂ=�������B��c8�����x�ɛ�r��;{-]��$i*l�7vdj��$�Yu�f��{�;��jq�*4�zd=�n�ˆ���G�8�nF��4�!�2��cڟ`��.ꪥ{�� 1������Ө�<dt9:� Ye�0��x��苫x��l�#w��5��8��e�6�W�d#YǳVԈ�Ħu�[�5����";���i�)��{[{10ӂ0�O�m�����vqZ��g�Zgʨu��O�t
�}~.ֳ�c�C:����Y����Y����Y���wnf]�u�a|!v8��G��tmK3�j/��E�0� �H�Ib�����*^�:l�Y����(�?=���Q>���¢e)6�]9�x�մ�M�������5���f���z`7"��n�e�G�$p|3
h����ϰ�'�dd^����F�R=i���P�ؙ�q@u.*q�^1�&/p�(�=3�$����)���4O�Pdi�hVq+N��uɸc��	0�a���*Ɨ:�SVW�Hd��I�{3�/�C��I�%���"��o�Lqj\c��~�xr8�U�m��y�-ڃ:�����LU;wtO�����D�՝Z��'8Ч�9���Z�[Bo�=1X/�Ͽb`d�^�l�+&Ѿ�o�iO���(pZT��|�*�h�!Ѫ#q:���rn��xri��=�jYm�=���p7Sv��?�rU�s��xV�j5��Pky ��*L|��R/9e����)��oV�Sh7��Pa�l����Y�W��\�&�:�݉F�_�\��Km��� oeC��7�U��[��4ԫ�������xZ� ��p��`�'k^�q ��IO�K�V������"��.?�
��q;���B���. �]��v���_�-��]��X���h��-�bMEb7GҮ���U�ޯ1DX��yM���Pe 6��� S�	K%��>y�r�d9\���S���č�Xo�l'�3� y+�^蠞�KA��N�xt�\Q�*壣��&� G�&�n�KX��$�ށ3�t� ,`_S��" ���IV�2�#ڊ*<�B��@�A]���:L�pGA�u]�����y� 
�6%����>v�?�|ȴ[�i����!}5�h�1u�b˺�\�١����-�N�V,b�\�3.�I���y�J����%&�(D���6o�jOS��xT絮n�HW �b+K��H|=~���3�WG8�oH`��b8���$��F��Ij��(=� �s�R9��O��J��Q�����o�s�g��Dr�M��Rm⥪Q+�<�j-є���a�~}�x���[+�����M�åְ�)���=��i�6�V�
^Hԫj���6�8����@��5dG\���ߴ�Ь����٠��6˹!���d�ǚ���-Z��p���A�ќ�(�,���/\+�T1L�C�"Ux&A&f�9A�_D��̜A�ט���z��S$����`�x�b�oȄ,�5�7�V4�{>��t�mB-�m��f��Ho��d�ݰ���WO���Y�z��O1U��GE�h *��2e���]��瀙���w������qҦ�=W �adm7���]��A�K�v��� �\�?l6F��C|��oQy!�O�;Af�A45v��7�V��ë �-7�	뜯��y?�k0�玂�&EB�eô����>��TuO���F�)�}B�?����__&�m��"PQ�z(���-f��#�1��40J��]����VH��%�f�E���������~O�V��ND}V�oPA��,
,�d�7���/���7K��R�jS�є[��#����Z�S�+'�ƾT�ێ��_`�D�bR :��Kö!/��Ȇ�6���a7�g�G.W���C�&��V5���]ǏZ��(lH��Cd8(��-A"���9W�9Z����n��2?3�κ!u�[�5B?�Z�#�mE�'�5����i��)�ڂP#M�ۀ�*�����]���f4��+9ê��������9����M:N���q"�&��ЖQ��>?Oj��@�&S�[�ƴC9έ(�J-?��ƛ���nn�$ΈR��g�x8�O�H��ˊ��C糙��N�M3�`WGL0��/ kF�X#4~c�������jve˨3�z��Rs"lC>9��jPD�!ڀd����n���T��^
�R��s��I�L���>"@D��KN��j�̣�!�(��oo��4<"	�L��3����*��q���S�s�����b���_4f/����䐓/X+ߝ:Pu=+��ȳ�`�D5��؍��3�«�b����� 4
�ƌ�����IV>���7Y�ay�}��,�N=�S�Y�����@&�E���7I#�˒�L�e���&q`K����0��O?4��}^j�q�fX^*��E|�|����7���z�+��p�Z���k.XU.�L��#��+Id`t���@�z��}�����{��fI|� ��h,5�S��  {5�����f�9���>�=0̯5�>;����'~�p�Ċ;#|�zgǹ�a����G��x�������),����[��s,����Q��)�)�m��5l�'k<z�Wg��'Ch]r,��S�մ7�O~���|Wg>~�y7�x<�={r�T]H��2������xS[�G�	�	�.�2�^��|*�{#�8��L�>�'���97-    ~gO�\v� ��jsa�0�b�sp*���8��3&�mMV`=6�}۞��ݳ�����i�ؽh��/�4����bϵ���J���	�}��B =�f䁻`�����e���ٲ���iʰ�򠭎��1�q��v�5��q�V�۩�z����gLC��7?�	���/��egܝ1ٞ~8�m���l�|���d���4J���ǉ�猉�I$z��㆏g~�q��Fu�Vљ�H��-�t���?�M�١m]��^��/y���xœf�ﯜ`�J�l7|;��	#яР�k�J�7N���ѳ�6ބ��]a/ǆ��ذ�Z�H�e����Y��b��5�܏�8���^j
+�MWرHb�q��Q_���`@�_ϱ]{F�w�RƦ�\X1dg��~�Q�=���=�"��8�7��H�5�-D��#����TA̐x���?l�4|�)2|kgS� u�:B��p8��,iNMՏQ��<.�4m�~.��[	ٻ�/?HΣ�ԖMj`���'��������w��"ʳ��Qn��o��
M�x���Cc��8�	�ˊ<Z����&�[n��d�l�D���ι^���%����'��u��ʷ���ݕ���x3��7/~0��'Jfi�sJ��ȿAY�R���61�rǥ�q)w\��rǥ�q)w\��rǥ�q)w\��rǥ�q)w\��rǥ�q)w\��r�_f�rǿ�rǥ�qf���$~/��K�����$~/��K����������н$j/��K�����$j/��iƑ����h4�f9���ߞ�ƃ£G %�}ߴ'�K�RjfI�ٖk%��|��i��NjZ�5&}G+:f��$��Xf�S!s�mϲ]��Y�C�.<o4(�r�H�Ƭ�{���X� �7+E���
�N�%�x�W�ͺ}Vһp�4�q`z� �mFi������Kr'H)n��E�$2Кp፩eZ��F"˝4���1�w�/c�2�z��PcTgB�f�o�`0��N�w0w:� ��G���>+)���1�뷠���߾���u�b�������W�:��[�78���s�#�%����w��D�4SS��>���\���z��qb�eҠ!o��|�4kD3+Z��+�y�����ѧ�8���G��Q~i�d��`Wvy��A�[u*��)0USO@,�� ��+E�$� cf�J'��U�ۻ�0� ���y�=v+��S@D�êlX|�g��e�̩FE���W�lӕ�Y���T��]��A�L����gE�w��}4��2b�Kf:��'	v�$���muwu���`����[X*P�����*P#�F�����U.@_��Sە2�S�b���º�e0�R�wZ�j���f�t#khj���Hk^�F�be|��s�մ������zX(
��� ��r��Q&�w
n_��HJ`�����o$�o���yW������`<�R��A�O�?���a��6��v��� ����8��-zXR�h���=x�֐Ȥzl�ǘe�F�'�8:SC^#o<�/Xh�OУl�W �(A����o"�(��ⱹ&�j4})����S�<$$��~����}=��ީg��i�a�/ʹ�B�?�M�e��hh2����o1���%Jc>��^ً* )E4p �80�6�~c<�~�*[�&i7�MI �*�ъ�[ӈ�ˢ�i��ϕk1$[
�O� �vt�/�Rl)��3�����`��S^���9Z-��ѧ!��P�Q��Ke��@"����͌��9���!� �".U����q�X�7-�I���O����X�yBbTDU"��E���1$�M�7(G����+$���:0�)P0p�A펲T0Gx_R��<`�G�|+ �~/�@��EK^:A��U�C(�	���&�VOK�%��Q`��\��~��M�_�,��3�^{d�t��.�|;&X �͡[�2gZ�L�u���m��c,("'\P��!%�Ҿ�	ҿ{�+���BV�f������ �`���zA���k��1%��J��u��Eh�0�hNT��I�<o�*�8	DP�������M�P��G�K	@��m^=#��h�����hɀ��i��X��Df2���;ϸ>�qN�5�^�`R>�2�v�9M�/�Gp~���d���k�*�k<,����;��'>���y����� �tV �ZS�*�>"���քk&����l�Ͼ�2�1^_�M��W]bA���������(+��UT�����jy��C��]+����� �TE��[m`��7�ʽ��,�?����@4���W�	�$. -��Vki���K��-|~I7��;�`��ᅩ�YG���J����g|[����.c������E�3�T.t�j��8~8��s�z�A����aE�ٱR���F�Zrq2����%��3��n��&����!h0����^(!���ޱlo,��E�K՞Q�T �s$s���P<�EyMoD�7�>�ޏ'��@p����^l�O�x�^P���d6o(	��ްHS�Ʋv<���Ӳ���U�<��e|[�!ӄnO>��T�o*�s&ڑ%F����؁���A���?W@�@+�u�2���䭝NT���%�p��[b��gfʳ��	er�*G+�5݋���X'f����E��γ� �{L�l�� C"a�!>���ڛ3[U�oF�%e��67T=D'(2:cH(e�б*
��3Z��񓕔n�%�k�3ŀ	��3�e�"��*�h�OL�H#}4˾��(Ơ���|��o���i���
�o)�@��]�uw��z��h(��Ah��t�lS�X!�mo� ���9d��Mk�K�A��BGᝍ*Och`LZS 'X��v��o~�B����4�. z�۶�J~$`��kT(���!�� ����cı�Q��il����ѧK��>��Ō�ۮ�W���4��������ςW<�;�w|���{��ByfG��8rT��7;��)�I�x�����C�C��tQ�Q��@eR�P�t.��{6(�� ��G͋k�E�kcm�-��=��m�Uef��rm|q1�Q��_�ݳ�i�)�����������o��*�%�TPCAN�b�
r]@��A��?;�@eG��+NЦ�1�?�D���p#���Ȗ��Ch9��#��O����!)b:�36b�����E)?�$v�tT��>BA T8c�dB�L�B���������1�"<�F?���-ٯ��n�
ȡT�ޞH����J�^h�g�0���/N��L��&*<�P@ZzR�5*�;u	�{�轳�R�!���i���=ڱ�;��U�W9�0�`���Y�,�>����E.I	3m{�%3�"�����= A���8rV'1�ٌ�e��Fr��0�U��ޚC�	�2���]��a��h�
 2�El�+��d��XO�%���e$���=̅>Fgs60�q�I4��bf�c���lhc��0.��T��<�������~�T������
�W�JG)8p���K%��S����v8{�s(�a�^��tj;76;O��+699_``tj��u���F��r��>�X�ǖ��(�L��:��>tg�spO��1�4�`�[��/-�6��жx,�MO���h�S����c�J��.NU�JA��F�/�,H ���T;�S��	�uxs��$�SJ$��^����<�\Ry3,`5��űX�űX�űX�űX�űX�űX�ws,~�+:>��[|UWE-��Jֽ�eDP�q� \���wcq7wcq7wcq7wcq7.�/wcq7w��n��O�����-����kX���?/�/����*����Y�S��a�G�c�>Ȕ���0�b.��*������ۓ�n�z�kE]ۜ���������B�v���y������d�L��g��:����*�g��cWB���*���R%4�di
84Tu��Ò�q��^'Vρtm� �$%�h�r�WT�    �i��\
*���>_#o<�$PV4[��!?iT@Pu�����]"0�]�(;5�	y7.Y�g�t�uq�U����D}T����2OSX�7␨�*`��k]i1��w����T7j�y[�r=,���<}5�䢃��P�9&���	�a�� Sm�"^	�E���I�TR���Ep�`�G�7p���5U��(�
-ӛ-�=���>�<��wC�yfi����'8��VyVe��J�
�07B����X�}3��'�~�6��y�4͆}E�S�G��]�e�<�jPw�{��)rהJ��S���١�ǥ%�E�V[�t��[q8�C��S*.�QT����"�	vw�*��j\ty?���f�*�I�B�N)H�����.�K��-坣� &ۭ.�<�~\֙i���v�T�%��K��#ڈBuzRD�kM$��p�H��D	!"7�N:�p�u!�g�*+�D��k'?ୁ�S�A�#�Ǌd����L�@ �9������7�Y����՞`��wń�֮/��_���~�^M�&2�hT�Ď����TC3��^��z�f
��>,45Fg�zl�Ǣţ�1/�g�MT�wqO���=6��Έ�&���w�(�&���#�R��ͤ)��s�螁�������&y��-�2��Zw  ��������?�n\*���x9s�����K��G�3�>����%��m�e�e_>����.����*
棠�{�ʞM]qD�I����mўz��ۍPH{m���*�T��(�5���K������7�^`šީmY����j�M���oa�������@7�s��-����� uB)Tc?z�WvLQ�	���Z$m(Їq����anK�t��,���v��T{|��P�k����B�꧶&��5F�wH��`����]}8���t��j��2������b��}��N�!K�I���HE�#=�����N���`%�>��s�s�����/���ʞ�� �75�;��ġX��C7��3>����6�v�(���u�v@!�)�����~h;q���=S�u�N��aL=��	��z�4�8��� n	g,�%���3�p��X�K8c	g,�%���3�p��X�����o���� �|�X4@���g:���3�8KM��}3��c:N�:���k}��Y��n�4���q`�̓��e�'ҕ�?�����/0�Q�|��Q�jl��pB����3��� ���En��I�xꑣ9 ͦ*ˍs�߼��D
)\W�yn��)"/1�\:��DA���	 �n� �����5��M/�
7��<ax"����9���V`�A�9�o
ief�[2υcǑs) �5�j�H?R�ڸ��"�YA��Q��][(Ĺ����|l�Y�o�MZc��NꝞ8��҈��@e�
3)�¹��G��)������2�%�S�tc�;�P�]�/X�t/y<J���r-j�f�g��w�"�������=hAC���x�n#/nA4��6T〲Lޒ�Lʃ<���~���v��`l�sx��/�~�U�*�S�Gh+�ɋ�<[Z��XI�l ��Z=o8��5�V���4M`Y������ ��z�COͼ{��;':3wǛ���/�hVǟ1tgz$�Q�s��{J�9����y��%ne���H1��V�TE��-��-fi�����-Hftje�s�mT�Q�
�0�x�V��%"�c5�
C������~|�Z�9�e�<��0Wa4i�`����JX���R���:���N�U�N�ޛ1#krDVl?n=9ӛ�X�����oj�-s���|�Q��!�9���ʢ�~p4C0� N���d�,B�wy�^�[���{^��[`�g��8�oǡ��D�q��H3�{��L[3=׶M�Uh�ҍ/��4KрY��R��}?�=�
3	 t\3�AuXv,�L�`�g�T�3:�pw�ާ�!�Hb5QÑ���Ok�"J�56x��·��>�r��t�Pcc1�H"�h7���<�Y;��s�h�������,�5D����X�g�u!h�<�aPJl���zf�F��
�gA��TXj�u�,j�s�r3�2�$���C���V��R�z���6ir��PT�5g�cj�x=[|�+~�LP;�Л��s��B��M�q�иh9�D��s�-�'֑�$S���X����p�Jm;�%�X�3�>�؛f`�{����N�f?���L��q��r��s-[@N$pAS�ŎH��9��Y���ĉ��̜3`�+��$1s�$p�G��/!*��q�웵۱��lFͬW�Ou-�vܑ�)W�燳y0_n�[0,�i��K���� 8ЍFJYB�D#C�z\�_?�6;����� �q/яI��-�VE��U �q��*Y����į�$��u-�=5o���P��U<���Xm]�q�"���_J��e�D�]׶�E]m�' m05��`�]~��E:�&��
�P�q�G�o���*t���:V�3��m<��7L�8Qd;��k���G<a<��M�@���1���{��D%rbf����E��K�/�|�8_���>��8�]��c��u`_��LD�C'�r/��0I}��oF��� e���<w�R%��t#�#�l�Ea��	����>�7}Ͽ?ZacD�'�rʾ����3�D̤�<��� U�`��0��"G�	N��/w�����p�ٓn`��a4âs3�@%N�i�~���Y������,ã�<�q��1�L,��0
��
7r\�p!�P�f���<��%^Be��텖��920�ԲM�1����^Cy1X��|zT�{ɻ�ޱw9��fb��@�>�@Ū�V���]_� V�F�wm�	
[ĝ~(���8�љ�ȩ��(J�T��dnUk�s�U]wL�`�T�I�}�������2������z=����ﮯ���SZ`��d�z�q[|��H���\��8M�=�K���H?X���������p��ӄH�R���?e^�W��+Ǟ6��s	�Tg�;!�j!�y5W�������'C_Z����n��Rf/���锾���L:VN'	۱�����we	�
�x��)���@L�5?;̲�ޏf��~��j(���Sx�)X���t�\7� _v��YR���jE�	l �X?�k0l�[b!@z8Rg� ��ͅ/�5��s&>e���6��n�۹7�93)���-]�����IlSx��,���,W�(�N��c�W��1z��A,p5{�Šݤ�����U�[�Z���Gl�������@���	��1��͟���~��[�-�lX��7�ק/�H?w��;c<�&ŧ��9��\�|q�n���]��E��}����(-�6:9�~�P�9�������'��ɂt��"�c�Ha��-^��jɋef{v�%�;�d�9��7�����q�2v�x�X�[V����(:��y�<������6L/��&�0�<	C/s����^��g�Y
?Hli�Yv���K�/;��0N}l�K*~�N3�/(�y�;�sa�j��bn�g�i{�:�ώ@�iE"t� w�T<���_�k�)i�nR���;H5Q���s�M�z��"�s���z���c�W|(�O��/��K�%���k�+j����o��s�5�����UX���(Ɗ�����.��`*�`�'�����~o����x�Q*��۬���x��;i}�;����k����ݎ��`�7��Eym<5�a����cU��&�G�����g����  ���C�L��qwƓj��C+�k���,�����,�:���Y��eA����!�~R|. O�1	��T��;����>�A�Θu��θ�t̥%�̒f�9hj�Iyf��An{q�ȋY\Y-��H�nI�j�*�>?�X��b����b�@��WL�.	D�������J�Û��r� � Kx�b����JdӒSC}Ŏ`���;�Hc]�~��n�A\�v�^�^5]    EI�Q�?.�m� r�S���<z�Ϊ`�p��v�����Ԥ��R$q%�������`���%p2�����+N�C�LR_X�:�$����>ҟj^#s*qT�T՞��]���Fl���r�������z�넿o�8A�V�d��c��ʝ�)�{���6��(��?;�����J8�JO� ����n�dޘ�p�f��9��&��91r���gI�Ao�9����}����"��ȌS�5�$LL��)mƏ�����__�������������k�jOz���2��~�J�]|�5LBac"l��������:;L�?��c{�*����k�+kR{�q�Y."O������������l/�U������w�	���G50}7��z�e�ɉ�,u���#|���M�w�)�����f,��`	c=�(���;G���;c-�w�6K�iq&�3�����Ӈ�/C�)���w�aeq����� $]��I�\�Q���2�v�癖�m���Y�X!���<M�����I ��3��oκ}V�.�-?��x�؍�kAf
���8�,q��b��h�#����/l:H���9(,��*6\A��)��3���\U3$լ����A�'��hBO,���� �h �d�:!������!�\�3�f���ZtC	�Gԟ�)��{�p�r��eѶب�n�A���°&L���C=$Q�\�@�1�﷔���"��mV8��n�����Mo���g�A�j����?7��{���GpZ�k��Z����e�z0�vuC��vX� ����^"Q�O� �\�VT�������H߬k��5gG��F�Ѵ��WUVr���o�m!�X�]��f���Utgl��
2
~�-v��\y�`�R�[cW���� �8B�&K*�����
�7��{�H�>�	����7�"��t���n���3�ǥ��:��H��nk� 鎞�`s��S��N]O����f�=s ��<w���
UG�Y�|:F��
���&��R�l�/���Ł֊M�����Tm���
�R$�4� D^��Po�(���v�U{n`0"R�r`3xöU1��D7F����H�x�t�f�67Z��8{���g�a�h��x $���E� �#����ҋ��_�Pn��1G�8F��@B%6�~]�Oӽ<M`�~��9�SG<OYR�(���<�)��ѴjPe�(~�Ө����>�m~�3�E�+��,�@Jm�z�Q��=}��8kռn�2|6�,�)�ת��j��~Z͛G��]�zE⎦@����E�����{ w�I�u��=i�;N�n4=�����8_�r2��}ybG�tq�kM�C讜V����g�8��''����s'��U�^V�b-.��b-.��b-.��b-.�⃳/V3���Dԙ���5p�º�/Q;��ة��Ma[6|t� t��	�'��fI������o�q�;f��$��Xf�W�ysm���T��ܮj���W�k�����*y�/Z�E�z���e{(��*`p�+����#uGx�}��
n���O;	rB�/^o�(��������������__��揃�i ]���t��+?��K�8���N޶���o����q\/�M����%IfF.���O�c�Q,�hΞu�,��}�~������Aꘉ� �qdi&Ҿ�x<t�����]
yς�I]�L���3^q?'�j�R�Y9u*����~��m@}�����A�܌�45��)���9PLxT��%����Tb���/�z�:�U�[���چT����$����7�Lh�:燃u�=.�[<�f���_="���R�P�=�=vF�9,���J"e�ފ�:�gE��ime��3���ã�U�ϼ�ev~qN��� �M�[�-<�����d� ,��?�d�VX>�)�9Ȕ�p�/�{��)�0��΀Ǚ�'H�V���Ed��*A͊�/���*���8w��U��m=��;�OSl�O}M��6b��������|����I1Nd9 ������G�(��#g�ۆ�"=澳Uۑ�T8��D2j���Mˆ9i���Q_�aݙ�o���$��N��j@xDo+�(�/��U^vn�24b�W�g4{�K3p��@����;�8��;�meWc�ܔh�QA�3� T�ǁ6v�-."a�P4�)�ҿ���[�h�x �"��烽��j΄fW�z2a5Gw�L�=	b���~�hf�k� :�`��=�+���l�+î�@z���!����+r^;�*fsW�Ez@/	﹓L.��".��r��!1X�\��'{��<��ZuZ�������J8��Ӫ��8R�Ӫ�Ɓ ��q��h��H�W�H�'�&����r���v��K�DP�d<њ���p�l[Q�sc_��v,w�M?Vp�Fv�On3�a�I[ND("!���4B?ϫ�'h���vl��+Ȋ������àk��VX�Ta"�2
�&��LnNM�U,���?�8Jno�� 2�"�\���F�>JMR(�U�j�61��x�)�$5�i�$�v[�r��N%*����l��bZ��F!I�C�����g����~�n;� P)� 15�d��T��äb�U���Y��K�A�B�o�5Y��ؔCPw� ��3[pM�6�x��Z�#�0@0�Ke��!`]+C*Xߨ�ML�qŏ�i��œ���HDh��qmG"�hO�w�0���	���F������l�~y�0<#�8Eē�!ݕ�ّ;V�Ρ�R�D(���j��p��j������.~��.~��.~��.~��.~����/�{�/�����#j}40�$�iu0m9��8i�g�"�I1x(��v��y;¶�yG��;����(t][���3g����sײᮜ��ڵ�r�*,;�B+7� �M/�-S�KES [ [z���Y��r���Xydf�K�	}i�O�K�
�LZBD�K�-�y���p_�
3�)�Y��Tz^�K.6M��3��y��X۲�\`n�����Te�%��Nh��l�����OB���Y���΅���2���?r�����,�x?�z����`<w��!�9�����M|?2=��ѓ\�Bd�i�V��^��x�>r����ND�Y�$I�]S"Б�2��0H������d�@m�zξ��8�����E� ����m���.�z�P��b�#����[�.���BH0���U�ef���~n۹ts?�9ם�V0/�Ss\�!�p#U�ttнG�<��ި�%+�*���>{������s��6+���5�f��F��v��������q�(1s �efZ9"�qB3	����/#��g�>K�����NMF����\`,�E^n�V_l|�s�����%;x���js.�M�^1���EJ3��g�y���̌�H$���kO��*��đj7�評]�
�4E�\�����b}�b�T��l��Cl�U�QMԟ��~���"5�P�����k��࠴�_�C���&�1K�EDB���pɰ�r#�+��KnT��#�Y_�y�"�+�hp�g�����U���!�]7`S�e����:���.��������*���"GZoJ)w�事�qvm��O:dz�P\)��&�[X�K٪����Ff�R"��a�����4|�B�8S�I5-'HDܕ�Q�p��I�@����\�H`���Q�6�!�"�q�SS��d����D*Q��v�謬�)K֘�Ei��ъ��l�> �1��Ȣ�4j"Iop��
׵��!h_�V����7��%ځ���3�A�4O��Ti�⯺��i�P˧�:"EV���Ȥ�)��F2��HF���E�)�'��q�~��	<�K��)N�$�#�̐�Q���� ��&C
84b�O	�Ι���r"�6�G�k�o�V��'Tk�
��2�1�Az�wȱ��I�4�Ft��c�iD)A����N�c��8��T_FX.�+�N(*&�cV�i<kE��h�>    �-�)��`h����.ʲ"�'�!Ш�c�D �F����"Z������J<�����h
p��y@�hA�6�����o�b:x
� .�cX�68�J.e�jVcV�W�!�i�\c���ز�8�I��<Q����p�@~L��n��T��*��B�|��CK�� �6�ℶ�������gHޙ����qK6��D�G����$�:�~���ߊ�����?v���(��F���<D��u�H	�*��(i��A�7Z+\a�7�	!_��s%a$��(�a���J��J`m#VK�>Ǩ�9�WQ�1%�+��PC�XCH�@x`L�e]W5I�{?>�W����?�B�+u��#�)�U�>��+ �ە�1���1Y"��$\jJ��J�f��}y$�k�����!�fw��e�����->�N�u#Q�ƺ���-c��C�Hhl�@i+N~�d5��>4��}{C�i�����'bQ��Œhiu�ټ;�V䴕k.��u�{���S�Z�
�����/D�]j��tǪ)��0I)���9��>���2� ��(V
X�-u�%��O��L(�p��v�Z	�*I�N���_i%�# �Yj|��A��4P'͟�Қ�o�hz@�L�`�|r�īĢ9�ahcp�ꗣ��)vFU�t_��"��A�)�V̈�å�s��Ѱ26��N�h��\J8S�-������� 7Dl���W�Az	W����wWӖ
��)�4���uR���N�-����fR[�F���t�ϒ��=� �u��P��a�R>\O\����x=�G��g�$%w4Ɣ'0���R��k ��l�e����s��Q���#&���qD�j0b/��ʙ��]{MϦ�l;v��ϝO
����������������!��^�v��ɑ�ݕ�6�<'�o�����-8���#.s�}�k���A�{G\'��Ă�~jzq����8d%��(�r'���)��<#y�
�ᨹ RM��b8q�;IPL�(L/� �ap�ė�E���Q�ZEg��A'��u���=�$Ŗ�'��9��+U�a�+T�d�"��B*�b�R
���1�Q'���o*
���,ѭ��xJ�X�[�������=)z:�J?	-�i�l�ig�B}���D��wWg032���;��n��Kh�O+a�����7[ND��P�{�t�mD����������h��!�����.�=v{�]Ԉ��`�#�����-�����R�C��0ɐ%��G��dft���0`�m���fn=��v�
i$�tʤ��Gk���^���?���5�$��W�H����t���7(�\Ό'Ph��.T�;t��ݏ�뼃���C��Z��	~�\�
8�Z��ʕ��^S���(���J{�d�������(�j�2hÙ���(�r�9�?��v.5B��Cv����xlNGG^��;��r��,Qm�zY!T��o����}��9d竫�d���!��l��f�� Nv* P` =D�)����N���3Ɓ������d �þhx�ݪ�Y-'lc��3%�'�}�E���b�ajڈ��ʁRS�,5-��pG>B�v��E%Z#���#�!qHs�sE�����YzD����gٜ��a��z��ު��� =L;�hL�8��?�y�O��Ğx�2�;U$�����0�@���샺�JΝ2)R	F��{�"� %��. �ۉM�X�w ���3?����X:#e�\0^r �pg�j>�u��=
�OG��!��_����"'�d�h$�+�VaxD�b�B}L@ �b�%7ud'���#��S���"��q�#�w*�K� 
EvR�,��>���u<�2���y<]���)=�A�͊���/���f�|�H(b���>B:	r�gJP���� ���)�"?�i�2���N��7^~j��%�m˴}�������X��i���@��>�
� ܞ��%��o|�:������ P=��V�����鐶7o�X�Mp�T \�"��ك�M!�+�NtǱ�	r?6Ύɸ���ɬ>����V� �)3�x'���b�{/+����8���E����b�(�W��\.�r�O�����BO�\N[���[Z���daE��
��,5f�8X����W��aՑ�F4��l�(��蹓���)V4+��Ǌf�>��7%a���c��3�2�$GigI�a�^���u����"����}.ȜU��Es��:=�y�����"ϱM��$)��(�m���"
�(IfόlЯU�;:���Nl�����F�����6 h��d�
U3XS���7��o脩}�8t6Z�I�O_<���:�PQ��cnA��`Th)�wkR�)�s�?�r2�
�i����8�J���C!����U�/�:s�?�G�D]����+\��7�ں�����dV��"�|6��zY��CБ��tg�@� �ϲ.G!��0ݴ�Ou�.v�^I�e�Ћ�>���kI���+O�gc��K���C;ZE�δ|����F��ء�P�	]�xAxd�L��NJ���O������AȶunP%_9цV���2��IȾ����,��+�Y����}e}�9��ܔ��MO&�)D��K'O��2��dI
`��^�2^�{NfC��md�YK����v'��T5e���%5:k�c5:��0d�+&@��2�S+�$��!�'Yf����r2Ϻ��\��o3�J�ńl�Kڴ�S�jOWY
r ��{�XT"O�� R��1J�Qe�]��ԫ�?Aa{~�#捧�<Y�T8�`A�D��H1�Sn�bW�޽9�H�~t��$;�H��P��;3�.<W�S?u�,���X[�zvpN[�Qp5�-��>�^�6{<�1�8�e�삽ۘK;�LM:|�%5z]1������@Kc;vR�1��KL�ͤ)���CzIl���_p���b�ǬU�%�\0)<�� ��,�������)�v���#>���%9���-@p�#��/�>��}r�O_��2�U܊�i]�@=�{S��
�h��@Y|'��kFb���j(q��������=��5����Yԝ�@��~<������:�Zc��Fz���r�)%šڋ��I�v��g����u���'IZv`E�&u19��hr��0~L�:���ѻi%z�CQB'eճ�Ṳ���K�ƥ�q)a\J�ƥ�q)a\J�ƥ�q)a\J��P鶔0.%�K	�/����4q)9\J��å��$���.%�K��Rr��.%�K��Rr��.%�K�ᣥ��Yr�[J��.%�K��R"���rK�ҿw.�[J������o)�{�%}���zK	�R����-%xK	��MNivv��,iN����hy�9yعfI`ziꚱ��f���d�&�'��f	_ӊd:Ƿ�8�3�eZ~,3x &5\?��+$e��UM�z����5F�7x�!J��h�)����ۗ�������M��c�E]�/�#��ۧ��2��/cB}�z�G�]�7׆oYx����3Q���ׯ���'�-ϑ�_�$3=�q���M_��H�DfN��S:�mYݟљ�g6zi��[����6;���펆WfR�)ߘ�}�i��Q,L?P�2+���<# 	������ۯf�ufy�Qhڶ�ގS ���s��	En%�l����&⻌>�0>'��g�G�C�y�����(�I������^�b�
=��}V��s"��o��i�����}uSQ�r'2	�ɚ��J_�{k<-��,�f}�;^�ˍ;�Ϣ`R���;���#�G�Áɥ#�D�C����~������:�-:��E����R`����0|�$�k�e%�&�t��7�N���bKT� �\��__�Q&�o��v��G1N	g�^�2���CqWg�ַ���*�S���U���%ݒ����I�rW@��x�,�x/(q��2K�,Y^;���"N"�@bY@	�
�R��.��ݾ    �aQ\��\���-ؙC�i�4ӖjO�x���X>XO1��U�9��7��'s���Qݜ����p	�*��Z�ێ�ŘCzH8���S���V� kq&�G�H����:��n8G)"*���US(�7K� �E�Uw[�>���,��>s��n��@.7��
X=��yM�$b�f `J��"����b��{���r	:I�E�s�h�`�K<���'��\��^Eq�$E<��[gd�˶K��wY���A:"����
a�:Z�3l�
䇮[q��s>V�Wh�3A�?�uI�=o�sȀ(T]<a7�c�%�#��VǕt`U������b��(��x����bMu�͆3�U�f=0
:97�V�@��@Vw�8��P�!m(�>�8�V�G�����TbC<��Ѻ��T5��r�1A��PFmW ����i����MQ�4U�5����x+�d z@?�M]xq\G2 �PJ`f�^�I��+�/R�g:�_}nˍ�K �TѨ�U�xN�sI�Ct`�=��7`*Pe�[�U�*�H���qc��[_1P�(A��~�0�4��d��k�n�R������=cff���w���sfqMڪ\�ӆ-3.������9��#�j�cRpʋ�J��Td��X�RG��-��8��$%���+U�	[/]À��F*����h㜡G�
����=�+0�t�=S��Ϭ�j��2S`*�6�F@Ra>t����^�Tl0A��C]FI�&��^J�s�+�)�B�&��u�џꮔDf]x>���M�j'O�aF!g#j�"��"�X}�)�WD��k
�,v������C��iy���(��"�ʪ��[qKb��Y�]G�Z����J�d�~����/��vS�7�)��r�MX��À~��' �k�x۟^}ejc�n ���f׵����s1q��q9rX�$�'���?�?I���|����!f.6Ey��`3�bۘ`���Gw��^�F"��O�
���C����O�k�5�$��ߥUY���?;�+}���˴H����?���Tm[m0a�-/wN ���z^���v��l���Qx��]�k��a��� �G��7�Ҵ��j���-��}���޷n�m$i��>�Y]�@�~���Ȳ�֌����ӧO��THT�"	@V��O?����W�Gظd �PY��qzz�"$"#�_H0Z�>�Np3��[{��UͶ>�"�7�nE��,��ėD`u��v�2��t%���٥YQ�x�虣bc�>�ؐ=��c�u��� �רO�ͳ���]��$�lF���Dz�i~6��7P�2K^�v��#+[N�x����z�÷���ޑ��w.A	���Ǫ�7�وo{˔�+HŶ���4�\SZ{�� =��zz��G��l�m꭪�cB��EX�uR����~6ЅǨ�G��r(;-�� Q�?��S�{���zs��?�ۍ\�{Jߌܣ�x����������Nh���;�_�)�B��� G����i���X滥�7���<�/�0����|���0�����B8�_�O8o�6����)�(��t ��)n�����ĸ�jnj7�����q0~�f�s}Y�������in{h¸R�&v�9�9T���/�-zz�q�Ok�?�x5`�]�q�O]����T��%w��RJ���a掯`Z;�}�F�s�>ţUR��w��!�N \�[�X`��*��G�ko��:.{��n�ɢc��"J��t��h!�o�}V�h	ff`�dA��X��J�HTtg�ΜiYE�H�n�D��8�)��T��w#�/�%���$S� ����#_>�M'�y��)��(z�c2���]Z��8F�J��O�gI�o��$C)�Q�w-x�:���KUX��~�������5wD}�d������^(��v�һ��/��3�RX8!���b*/8��=חX���
��_I\��r�𔈕U$���p���oD�S*q����:Jz�dOC	{B_�S�i��k��������m7����G�T�&N��<��_"�X���x��<su�f_��i�/��X0�WK;�~;�&�_^�}a_d��������f�M�J}HMI�^����bMoa����c"�(b�N+۰Ԥvʄ](�=�P)d����^��0"ӛo2���8���y�bEN)�R-UY�_��Q�j��
�a�%������:n]���>зd�iFY�GP4v(��.=z�]"������W�2��׫�Kn]��s�Z��}?O���g\��8�d�L$��(�����ƅ"Q;�:���q�z;�㸼�O�0�/�N�d�|��h|��u�$uÄ�����+/��}����Z� �yV:�`�I쿧ľI؛��I؛��I؛��I؛��I؛��I؛��e�&ao�&ao�&ao�&ao�&ao�&ao�&ao�&ao����Ixb����; }>
����9E�pE�v��A��d�2e'e�Q�Y �c�⤅id�"��e\fҗ��?z�i��}5fx��f#���e�V�د*uC�ry��/��{��������$�L���ݣG���D�a
��zv'�$"�S/��p�X����b �0��Y�`K'�Gv��dXةȄ�q�A��Ix�wK���-=5�=��s��D����UC|���U�dt{K��ܡ���PԅlD�l)nZ�R��!Y�v��-L,Ȇ?(AVo�r)Ur#
��A�l^⎙�_]4��ut�,)��ȅZ/?��*��|��S��t���w��!}MG��Oկ�mu�4�y��w�?_s��#��0UQr�9��-��偵�:���6�7<���p��FKZ�H���'�i+�&��'�w�{�8��FOP;��L*u��D-��e����*���djHպƼ-���պ��N�^^�l�^S9�u~���4Is'nC$M5�X���T���Chh^��.�'�{���������.�W4���҅rqT"�WV�Y���L�=>���.�ȸ𸔮$G_�L���'�+;Ծ��1��P�]q��h�aE���)8j�z�]���޸Ux�[�ï��vm���DÎR�fc�K�U[z�X�
�G��,����P$C�����to��M��7<�W����c+�	�ܣ�{%�i+Q�&�@G-hf⁝�ŉ�$���n&����ܙ�㹒����N��?c+�#F6rp#���t@͛�����<���e!��56��=��fl5c�[��j�V3�����m0T�b@��S�Pg��@��"�u��,(���Ja����@!ou�uh���5��?�.@[�g��L��3�q�?��Ǚ�8�g��L��3�q�?��Ǚ�8�7u�g��L��3�q�?��Ǚ�8�g��L��3����ľI؛��I؛��I؛��I؛��I؛��I؛��e�&ao�&ao�&ao�&ao�&ao�&ao�&ao�&ao����O�u����lK���G��=iq��iP
�s�R�^*�L��>��$�>�(Z
�!�E����(���(����^�nXQv�u�ں@%�RQ�vwj�%4����A�}6���S�O�o��\�;̍�Pfi�ھz�)~l�@�v���X�Q4�]�u���?�B�F(;p��N��l7s�
ᝪ���� ~Bls�mޛ����i�#nW��$k��}���G&��z�z�)��u�Jk�MY��MQ�����/�N��s.XӃ�5�̟���Cv����`i��%�(9��6��(��ODa8Hg��`�f�V-���3���b/�� I*K#���#6Z����/�Bn,P��K,v��\�τ���\��$:��~y���±���/���'�旲�-ɽ���W��+*���o�[S�Z6,����bی��,���h��@`�}�~��Cn&����>xC_U�ދ?z�����~+x�ۆp���bK��à�yE-����ʜ�I[,?"/$�#�ER7#��,>�DNe8�����U�$����3�T\�    YGA�<g��l�:5�|�/R�2�;��,D�*� �pԵ�:���~�^r�r�gw��y��7H��O�R!FNԽ�����v؍;�cn�Xw[D��# �����~)�pF�U+o��[M؛%�w�0#�퀅�\Z�(��v �A֋��HO���GT��z]2{�7���8ّ��5!+���F0���<�-�}]I�6H��!����Uhk��=1X��g��Z�_�f��R���U[n�*c�N�_B�X����\x��L�����aݴ6��?�6���#o���0@���){�M?N'p'�}�i���#�~LX��?�-t0���ڼ89b��'7�]�4V�;���{��P�;�,8V�kL��l��ΘtƤ3&�1�IgL:cҽ�Эb��w��naa�6��w��G䉴���� ��E^J[�Y&�Ta93��ym=��#�&Q��8L�_6�K��»�l�xy��*Ef��;���J7M�����6�\>��-s7�r?��(���\[x�o'N�^y���ܯ�,!ct�rz;C��!u"q�����6,sհ�K�~�iI��J�o*кܚ�XU����D o׉��-���!͙��ݙ���ٿ{:`�~c5p��L�1i]�Y�y�E3|K6�9��SIB�,
�IB�a�,��ėvg�a�8�����J�,
/�D�b�.�	#/�~�_ɼK7pb�R;��"��2׵�8;,˥�7��Y"���0���I��O���Hĉ�|7w�/:��4>����c�5��J*�y��䃞�4��!Y12ƞi��Z�m?�CO5�$��$&]�SV�e��Y���A��.�M�:��_�sD�=��?���S������X�: o��Ww?��m��I�!G��
��A�P�7�;O��|�u�M˧��P.��[Mp:�ǝ��?������O_�91�}E��]�Ԙ"�.$t�~O�.?��~�7Ҷ���h��B��^򔠮Y�w����t�]_��>��߆�I��������0hq!�������;�Ew�}��	��X�w�����}��nvۖ���}�'�s�(���j�n ��2e�s��-��{�FVi�V��|V�U�V�Ȱܔ�r#U=��d����Dء�*���B����EKt�y(�:g*b��9W�5O2L���ޡ��GS���>�.��!�`�������U�h��wH�~W��/x���n A��>�X���?� �(�5�����QhC�-��Ugc5p)R��uޟ�s,�k*�'
z�ԫ�|�Q,���)	��W
��J�i�����n�T���uC�D9�2E���׸��F�3+Q��-)��!`]r^�8K���˺h�i�uN� ��I�,i68o	�G���u��Փiޚu��h����x�=��R���{�io�����Cs��C��;�K��ջ��/���e���)/�j��+QbAd?׌�P1�l�(Y��Ǘ��s�=�cr8��'�eb}fQ]YU��k�$?�m�m+�R��O��c��{����868&�l
�(�t�;��y*.x��=7�/��7����0p��t�.�'��?͊|���A89����FQ�D^�`���?*�z���DFw�my,\`��7�g��o�|c�+�X���7V���o��!ɯx(��#���G�?j�J�8t���,p���"[ #۞�`��'�y��^SX�F�h��S�����x$�r�>�(3�yXa��8����Iء�9A�G� 32��Y�P���D���"�!���Ob[z��*b7�ů u�v�T�d�ێ�'s��[3�������z��);�Q_�z�ILi�j�����
5�-��u`H'�~k˺�:Q�.f���u?^x�=�����x>� b��E�d��x�{;����#_�U@�{���j/gJ�L��A�g�I8�1�V�H.#���z�e���>m�t��p�j�WD�9��zN筈0Ț��%
�y��Q�3b_J�Q�8�p��ݚ�Rzp���8��V�jh��q�Q�c2mݾ�ޑ�+/J�ܳ)=;�2a�L |�(.�8Us9/y�峔B&R�#aG~ �..\;����H8q�8��i���D4l�)�u�j�f�\b�	sq;��R���Ĺ�v����ߟ�o�K����n8�
g#/:���	�\aGΖ���ю㰲i	|�[�?R�U�2+�Y˲�.�'8ʁ`�x���*�C�v����n�h�	l�Tx�Wm�0k�|����{x��%���0Nh��F�a�D��(5��hvZ�rI����z�� ̫�`Яj�g4���2�$H�+r�d�;nČ�3V�a�x��Z�a#��Pu�x7J�UwtLuGS�ۏ�[�����>�c� ;�u�F�QFq�a�oIq��M������뾇?�(����>HTv
]�������O���;LBܽ$�Syv�8��h�O�������֋m��ѼY��k���_���v?�δ����"��O��S�|G�^(3�2��$Ķ�,�����,�J��Q���^��g)cϏ#�t[�ni��i���G��'	���l�w��yCNy{�V;���KEW�<�'*mE�;�r	qO��ɊC����3���� �;���qa}���1z@�'�Xջ�jvK��g����Ys��]#��>�jQ]�=(޵d���?���7 $m��߰,��/Iծ���@�i�3�֘�� ��.޳�����|�>��Bi�\�Ro�Vo^y^�$��zs0ǩ�۫�ؙVo�Ro���z�o�����|nѬ�-��Jb#a��5�H�[��R�s��|�ޡ~.��#� DF���Y��B
of��35�S�-�R��-����֖���,��V��s�َ��pt��������B�����<R8�3���$e�ze���+�_A���p�Җ^��A��H}�Y��҄�C�wY�:	� 6�Gu�v�E(�YxJ���=@Y��>��z���2���se�#n�X���А4V{)%DTQ�]T�p!�j*$��r�<���u#��FuW��� ��X@ͣ��!���r VwQ#�����W$C|4�I"o��Z�5r�k�,�k%jU���-��������OT"�U%#��X��(mz ��h�/�:���5-���`f%*E�H�o���7`-�-G�Q7�	*����6M����̬=�0N���8axR�׬\ax�@Sy<·I��9��{$Ԕئ���+
vb��}�.=+h��8�cY��QE��p�+6:P E�1�V[�B���T�-&k>���ĺ�������~h}�7ú
�"��T�t\��մm9��Eo�1U��� '�bi�4�?�#8�ǟ�o��`^��
Ϧ���;K�s`�ڞ��ul��#Ս:6�ب�_^��E<�xH����X��5��&0�w�2��/s�-Y"�D��
?*�@�e(��B�w�~����4v��G�H��h0x'���H�Ե�iY�Bf�.\���PF�p>��θ|��x�Qڥ+��k�AT�q*���8�M���*�����w�ykf=�vv܋]V	6KR7GGT��M�r{���J6�R�jzu��!���g=���v8�us{��a��O��hi3ၠ�5�V�Xj-�`24-�Ex���&V��~	��_Zp
�<�%�Ly��~��� ��I5���5)�Z���8!��~0dlu_ݠ�^��y��D9�Hв��Gz����*����{Z��X~݃��n���$	R'#�߾��=���Gt6}0�M�Ʒ-pr?���z�?^kD�-D��F$�lD�1�yM4���K���CB���i��12��o�Q�G� A��7'�Ď�1��_7#^S���t;�%��G�e�SF�d�p ��gi��/]��g�y�ځ(B;)ca�V�f2���#�2��D��_ډ oV�~��"<����G�N{�M�D�Y��-h�~��/����/�{�ڱb4�L�@�"��f�[    JˈT��Ahg%�qR2;��df�m����5��;s��㣬%�}���@�Đ |���*4�߬RgLμ��`�S�!����tj`R�i0bѤz�?��?������X�m*���G��A��{�%T�\Q���ƬGLH;_�`�����y
�kڙv����ǅ��'���ȭ%�R�l�!B"^(�芪$����u'�~����֛Ϛ�,�I[4�D.�(H�pz8Y�N�h��Qs�x�������qo��}0��:��{�a����íO[��Yf�)X-���2����D����t�4v�1�9:O�����D�K)���<b�FY�EY(l?��-�W�g'y��|�H�D�R
<ڗH+�F��e�b��
�����.zh�}I��}ˢC9�L2�.w�ʉ�aY F�+`s8��zy���Ck�ϖ�S}�W*�z�r�ݴ<(�]\���R.�0=@G������Ħ�_ɛ�=��g~|����{p�o��;:� m�w��z��M��ȍ�x�Nz�����2 ���c�a�`E�go������M�dn���~���_H��:��Нu�H��V��Q.r�\)J���NK/�p�c�ȃ<HO
�憻�����?� �Z�X�Υ�2�<��үӼ�y��	܅;�J�q�/�Ii�(�xҗ�R/r���g�I`Z�Mȴ�;1��������9H~�b�c�6�e�F��5.�qy���[ve��j\T�u������ƥ4.�q)o_���L���T�K�u)|�  ���p���8�͎�3pR�ag�L��)Gέ��B^�e��:�o���O2�ce��e<�V{v�jL���#<|��c��GE ���V�Wv�>Ħ�v�6� @)'�ώc���][H�څ/�2��,�� �.���{��F�%[�gA��I�v�iȢ=��~+�M@�����%���Y�8�8�V
�f�#n��sO&!����>v��i�?�q�ߕ ¿������a�����K��F�������s�����+l�kk빵���n
�U8����C��� &q7q3�/��V+=}���4x�f���ȕ\e�~&����R�v��gY_�I���ͬl����8��W�E��e�3�agb�fӻ���O�2��
��W" )�A�S^S�"X��V<?�E���j��w�1�f���Eo�}xCj�����<�
��%�Ⓕ�x�����ڙuU�k5��J��E��;�f��'7����{l;xT.��#�Ѫ�[�%A��t>l�{��p�)ҳ��5ސf�����G����s܀�U	<�h��FO��ȤK�q�@�u�ˁ(�>��5x7�Q�[�];cDXƖ�-�
N:r�mZ�^��^��bo�gSW.� ҥ(�P��<�{U��.����&c�b�-�g˚�p������7��ߺ���r`������> �
d���j�V��B�PQ�p#�=�$��;�x�����˛3ni�9�K���ߛ3ܜj˭�5ǖ��#�#��&vЬ:b������T�9d����r����X��;�\�>M�Y�q�I��$��%m����zd{�L<ru��#�nמ����,f���;���nL[���;�x ϐ��+&���Lœ'��w��#��d�Bn��EwP�N^A>ǁ�ݷ5ի����K"�����l�� �i�A�*���ITx���������E$���`��t"�P�k�S�r�&q��bKQh.�����%��N��U�PO�E��K��W�HzX�5?-��A�Ze%����>A�ڃ��u�Ɨ�?7�T���
�tw��fhQ�Z�W�0��@�R�W�;g�n"@�oE���i���M����"��bU����h�e �F=�vN��P<
�B�\}�Ra��*�̓��/]็���������[-�(��t,^@z�"P��*#��صĞ�2pLO{�Cخ�׼D��%�hgh1E���:�� �W��,��>��dx����|llov$�u� �X󾤉�̜��=`��3�M>��V0::�M�ֲ�t���1B�#q:����a���z��r�"���CT�!!���U��܅��v����-�?�����.�����G�kg�,~�}��e*=�Y�Ŏ�0i�D{�£����X��� �A���CI$�lb8��n���bpʙ�\6����l[=���T~X� �c�R����қp����{�OS'�I�Ӆ
�d��Ǩ��!�֬v
�Y7�E˛��_Ul�5o�<���Я��UO��8�8us!�H����+f׃��w�F��QL��N��!�1�M�
�	0�8�8��_�6R��i�ֽ�j'OE �H"-��ϒ��s-���}�0���Q�Z���h"R�����C7Fu��Hj�ed�����m/��W��K6�e�ИveQ;��4�u0��*��N��>U>#K-H1���9��85��#��]<�@�0b�i{e�TC���+ِ��U�"�{\�<8�ז�b��`�+�%����?x��s�T�,r=n(�D��e��� �I)9�4�$.0d���䃵+�?i�	gG.`�S���(�B�������.,{O� ���*
\S+I���������q��Hp�>����H?��\�ƸhD)z�e|��l*/��P�9h/D�R��{.�M��%vT~O���]��^V���*�=�`�e��س0���F��&�	���z���k���ё�5x�V�A��'�b�ʣB�"�԰�x"��1�{���3�hNj��jB��1�ϴ	���C�� Y�f?܁'�>a���#_�`X�tl4��K�{[K߀ま�r��:��̧�t]�`��IG�-ZT�R�p�/���^I�s�����r�??x`=�l�����|)`�^�/}K�SZP� ��=���w�u� ŏ�'ϴ��)/W]��2I�yKI��Yw��xgt�.[�h����?�{�g��w�htf��ڛ{���W)����+w��s�����������~���uw\����E��Nm�rXd5R��6�)Z��k�޻���L�ȣݙ
-��&-~��Q�;�Q��i�)����lV"�Z��7b�����݈�%F���x�����$�v��w߾����[�#%�P�i������[>R�a-V�u���|��h��(��s�~�ܵ*z�q�:����~j����A������{�i���uK��ނ�;h�
\��Ukq|}GW�B|oe�Q��d}�f�p��/�{	JJ^u��Ǟx���},�@scQ�M�۶G	������ګv��d�%��x�**n�Ϫx�ǧ�M��q���%���{�n �I��D�؋R�����<�s�N�4opѺ�1Egl�E:��<BH~/��/�fY��*^�#��c��n^!
�|��e�)����K*q�AsW�QTĥS���{Om.��o)�O2�l���Mg�kk���Tv ���&�݀Aj�w��_������E��y���+��R9�{5(�q%�.y�|�">��|w�>����-B��%��$	7�[���GG��S�-�qm�p,E�*q}��������E��ʋ&�^���A~<�$4'����Yua�)L5���0����TS�j
SMa�)L5���0����TS�j
SMa�)L5���0����TS�7����TS�j
SMa�)L5���0���j�� "�Y�?"B !�"��q�QA�0�bQ�E����2�Sv��Y�gY �7������4�����F��  ��Q��O����.�v����-����Y�g��@����e��^�NT�i1�g]>�%ς0H��v<+3��vq�4�˲�Y�9�F'��	��y�#���޻Y��	0SY���+ ��s��JVH�3��p�6�G0@�w�����[OŦ�Da4��*.�<��B�<���!�����HƺO �r�(q��º���hy4����4ǜ�f"�R�^��������c<`�Q����6�'T�H����u!A���`ͻVe��!;R\����N�    +.~�s�:����L�����$XXH����>�R7���-B'}7@��j���舦�Ʒ���N�q�D�br��:V1i��ϣ��2z��!�����S�&s�G��S���pS�1�AI���"�� Y���n�n.w&�K�DI�A 8��
�bV)���}�.}��T�ᣉ�Q�~L\ߟvB��#�t�+�/�[�Qz~���@�8
qkn�Q
%�#�8.so��κ|��r!c7��(OK�M���ybg�_����pN#��=�����O�I8k�c�q.����q;}�W���S���� ��jM�b@-L��/��P���ӇE�˥,t�HԀ�?}f}���a�]���Ô�C.G��^ؤW��ح������gٞ��P�ڸ�F;{(B)t-��W��B�o�2��e0uWm�NY-�� �b��:�詻c���]~I#ĭ����n��Yc���Q\�����Vb)���s1�Z��\�)��
[�7j�ں{]���D����z��'�yes�"�z��<}����s�Mz��J/�����]`�t���V\S���l_�E�K)��K��搜([yMW�2SU���1�P\	��]��R�%t]7��c�E}��� H�X%XK�[-��R9l
q�_V���T�nTlCu|��x��l*r�u�uN�,��ZV����k�$F���2blk��m�--�B�?��,[z�b�݅?�Φ\�p'1Ɠ {�F�l��{���駌���D;��і���L'���d|�Vu�pK�7��`��Y��X �kZ����d0&�1�����d8�!�� 㛆��CI��n7�����ߏeA��S�"|;~f�e��,2�=P��XЅ\K���GI|��cc�e�ل̃'ϻ���~��ݏ�������rQ�e�%���L� ��M��Y��Q�xN���Ϭ�gYg��e�H]�,=�b�"�-S��n;�99E�mh5b1�'�.�V9���%�t�#ng�=yn�}�l����s� T�*�{��iĦ*���/#$t�M�ʞ4���թ���,v� KaU7�����a-�j�QO�E�ŀd�l`�tl � ��5ZQ��t��+�e��H������a+��u��/��^�/qY�J��-h0Y���h��i������RY9�WxG��Kn-"X͓����&�+���[��@��-|Bv��Vhz�����ӤX�Z���c,D���BQ)T/y��b�e�͘ ��]6���E���&N��xB(!EM���9�q�gl�V�H�������5�<\�<zE���-o�&�P1�PQQ�	m�G:bR^n��T�Y�������X)�z��G�6���{`J��Ka��"!�	��2,�5���Y�����-7#czP��;+���A\C��uE����w #WЀM-u�7C�RJ�xɥ���z����A�-��nm��~4�J�{���{���LAg����}�ppk�F�θ�\k����P4�'�S�j��cU��vk.إ�T͓DBӨV;�1���A���#�j�'�c���m��A)eA�o׈�7���nw��T��x{ʐV|V�	߆�G]�m���Z�����(��������z����)�IW������]E_݂��No��Bpw��5~�@n	.�V�,��
�O �E7��HXb�r۟���A{�)��źn�ɵC7Ψl:��%�h+"M���J�n��_���/w�~��=�;�I�� ��s��G9�'�G��7�7��<�H��^���9�Iy�x�aw��:���V˵�ȃ�|;ɡ���Y�.y�u�^��g�J(,��c8���d�~6�.���CHn.oZ<��o�9�p׭����dn\U�ҭ�x}���V��#)��>	��DFq?a�T9<�?q����c��^���B;�!�Z����`�[@�V���v=�B�6Cw�������\� n4����N� b����ck;��+@R�����O��<<n�=�J?�2�
�\��ʱ�Oހ�Æ�5 ��n3�F���zŮY�hblo�M@}�m���U-gT���n�!Pm�X��)�I+��]c5я��X��*с%��T�E��!�S՚w���H]#&66�Kq�&Ww�)���V���l�akP�J#���c)
�
ؕ��M`��vk�
%%
j.�[ w�F�XYǚ���]K�%�Y�3÷�Z�i��V�؍$��ba�Tl�*TpA@�S�>�Ȳ"�) �U�+0������M�g˥�b$ȓ�K�j7�S�����+�3� �rj+	��!c�Z��C9�K��mq����.� \d�
wU�<�@����d3�-�R�>���G���u���b�"I�J���=�ZIQZմ�
.��i,��}��F��6e}XD>����d�*IӅ�N��b't?����0������a�*_=�_Ei��8F�bT���lm�K9<�h�*��Q��S�t�֚�Kk��'& b"& b"& b"& b"& b"& b"��n"& b"�hG1%��a��'�����+�	��ze(�B���Ai'2�,Y�'�b^Q�SR X�ס񊖎8��.Қ�e-�$x#�>�=�\���z/Pg�T�ڞ�jL���(}�7{Ů��^���M����}G�C��d����ư)"q��tr;-�ď�,	
1(�u��X����-�̷�"��$�_�W$e��nP�������Cls� i֛�����i�#n�Z�H�k��TG�ؒW������5`8����ΊL�\l[+Ou�\]�#o����ɳ�
�79\�kO��)����΢	�P���l1��E�d����߿��,Im�d]v�I��R��ң&t�]�@ w^�f�R �D6����=򓍮�Z�L`�4dR2��0魗�M��L��K�\H����#)���X��"&��Ws�:<��K�	`�˪`�b�u�Ocƕ���?g�\�B����!q�T��^��E�
)�jEg�f'w�<�����s]<W)��[Y猉���;h$�鶮ĩG��_��Ϟ���h�!��(	B��J�=��|�[����2���P]"�7
(�6A����5 6��dy�i����M376PlX�SV�+n�R`��u%)j��7���g�.r�L�#p�[��k
q������5
؛�����\U�z.e�RF� R��Vt��C �/�ht��n���	��N�:B�X�pe�Ad_����Ӧ�*K��[�����ga1Ée�G7{�ax��N^c\��.Gp{�;���U���@�,�IH��*�\O���`7��3�<.wg��F����>U�#��t���q-(����`��Xٖ�	�O5�B��x�(�g�Q��N��0�	�d@C\�:b�y%�vt	��k����-���5�����9p��I�U���(��T_�sK8��̸׃! ��ס��?�P�8I��< z�HC�
Z*g�R�h�6|O���睽��A�,1�(V�p�������Ӏ�w��#��zI�Χ�'Y�u���%�O��ԐdO4j�j5��~3l-���YN�ha�'�n�꬐�t���t��#H��V�E��Ia�;[>љzK�	�Ѯ�T�{P����Qԛ�2I%�4�z���2��G�JL"p�}�b�Q:�b�~~��&�:����]`���r
��5��C���y�!��bhE|��f�s-m�S>0쀛G��܂G��(D�W�EtҶ<ŐCu���
�I7��foiQJ�YOm��k��6:�5<��x�I�.����"�y`ƼCN����+A��k�����V�,��I��P҄�Ę��6$}{�
4�[���������p@�@13�a/H��\Yk��(a[�M��c� u6It}��M���W�e��Бq<�� ;c�,��V�����9�Z�H?1H$%����*��q.��ш�D��Ը���b�F���|	� ��W��{���A�%�}��    N�Nj��M.�\И9PT\�ǟR��RWeЏ�� �-%Kt�5BE��倹�b/�����	�}R�ds?:��|�9i56�0Rt{��E��j�Z �i!0uz*5+'縢 +E�qj*,K��hC;!�F��ܗPח7�z��T�i)�I��S�qcy�
��K�]�J:��-q���+������<�=����ɘf�,�q������>jza�F�t3��8~����FND5�<hFL��^D��
k�'a�8�O�"N�5c�	k�y͊��21���2�+�2�+�2�+�2�+�2�+�2�+�2�+�2�+�2�����\�!�.����0Ӄ}���	�p��xN`N\��]�A)<��i���������ς�~�1^���@���|���a�da�X�:(}�u����_��)����"���'A��q�pЄa�~PMq{N���Z������b��z��B~/Gt hG򲩋�20jB�:c���� �芆��a��%�M(��ؽģQQ���-Q'Bp��4TȆ֏!xUU���D ]�>=���u����)ȃ<Edٍ��C�$*���C4���A��Cg�N*�4I�0wRq�1`�`jjd0�^��r��GArD��'��hr�G2��"�2�`�#���FAh�[������hz���F�'�o�'yGرE�v�9���~j�N�ǹ/}7~Em2~���t?zG��_:��|��(�<�e�9�����e����|�Y��R}2t�4�#;���\��ΤpE���/�_Y	�b�S~Ǭ7�s	��4�?���c�����aɠ��\-�]{6�g���;�N�e*=2H�,,5�AX��Ĭ橇A�?�9>��O!6����n��J��vk��q��߻��
����b��v����6���tƑ�(�8�&�s��5��"�@��t:ZlZ���M�R?+�j��^l�BNW��^���i^�JShx�y�D�uX_�qx�챀�l� O\ȾN���(*�|P�_F秪:�U�!�V|v�ץ��(ďiB���c4���P8��Z�l�˨�>�D{d6�gSq��~Q�m�$��d��M��W8�H5���\5�P��c�0ri�{e�ک?2�ȶ�5�zmM[��$( W`b�W�[LA�4���#�)2Ja����R�_��r�1��"��_�S+-*U�B[�������䢄����ZՐ�Q����2��-���Ƶ��w��-������9]>N�ǜ� �v��ZL�w�����%%���P��/�y���{�#��Zb5�U%��D�g�B �U�s��t��P&0����F:�ɭA�\��c�B�mޗ�â��w������5`ޯ�}C�,4u�A��%*�j�KY����8�@���l�[�P�ɦ�!�#�.�0���"{?/]��Rl�����j�⻕�%�t�3f�TS0:F�N�[?�7��X����4b<-���k�����YGqͺ�3q8b3�<b��K�J#zI�e<�E��/DC,�T���$#x`�6���.{��"7x�r�ʱ�BZxo#�,M�������@���e��&������ˏ�Me9-�V���WXrQ��%�����)���Vl|���i�Q~����Mg|���5��?�����
^��ë��uX&s�}�&p�>��\�@��rj~�1N��ԙ{,��H�{S�I�dJ��P��ЪK�ZE����5������:g��?r_��ð��BEY�,h��<��9u�+�d��>i*�M��Y��l���0x�j����%;[��K`(>J+���dT��t-�}H���M��^C%M���0��Otm�ԫ��:f�}yΪ������'aA@LU�qYH�e���AzK��˩.\3L�#n��Ę��� ���b��iIHTK��da׾jް<	�O�q�����%#�,�e	"����).ķ�;O��SU{�����Ƶ�!���SO�lt�kU����W�ZE��
��`����E�����)]�t�N�J��3��s����$O�zA���d���c7��a������ܔÖ����X��?9@���q��I�h&�����DR.�b�R.&����N&�d�I&�d�I&�d�I&�d�I&�d�I&�d�I&�d�I&�d�Ix<��33W�L�e��5��G��D��9���EZ_v"�kqT�"J�)��Ɋ���h^�ڋ����ps8V��6�Z��e�V[�8`L��)����t,�M\�ySm����$�����LW���G���2��<���r�ف��6������]d�Ԕͺ|VlO��W�i`�~
;��=E��v�R:I�É:�{���W򖞪���
��d�3�f<�v����mA[fuqc�~�H]�`h?�.����O-�_��v����v�i>x���E��wE��	< ����`�%���f#*mk��O�����k�����������Q�
h�T}���$��/�+�*��7�it����w�Kv��C��=��+�ϬV�[������~�Bz������3\���浾5z���X��<���(��f��@�p�Qa�~�P���E���a��@��V�������^��#r�hQ�.��Ů!
��o��f}qO���,�́�}�'C-���y���vb	)�EC��Ғ=x�-��!و�֛�.
_��ixS�R�sp�8VF�]���un?�p�4W�4$N )��ɷ��Z�H���C&��p}K���X]�4�p�c%Nw��0:���m�~�Q�>�|ϖԩ�������;���}/i����%�Cl��:�hԗ�Sl��p��U;|4��y�V�d��{g�����,���K��|@��@a"2����{���[���Χ�Gå,��^�������8��_����,�{���@��kY�?�`]_�/V��as��Ї��Y�o}�1������]O}�k�(�u��oE���{89�-� \$��n�?e!�~��i�΄��8N3<j�uc�S}��q9>�p퇓fk�Ʉ��n��,d?���Ad\g��cWc��1j�-cmk�X[��2֖��~��֩NZ��=�t17��^+m�$��;�]����;qq༛�nE��̄�y��ġe�Cs)��؞�R�X��a<AP��4�'����,H��?���o��;����j��,6�@�Q��o��f�n������[��Z�~����(8�\����C�mk�o5�N���k� ����IϳCǉ<ON�8����gY�~
2Q�E��ve����k���C���'k?�}>�c'6�0��P�`d��Q�sq;����b7��@A��)o���!
���:*��lO���3���>;%�����,���h�hR�~��7�c/�G�N��tJ�gGu�����`��c�9w*5�q��)���NNC�}a�YtF�v?��3B�1#�neͫw��5�&騸 A<a��ہ+=;9���(d�� Hgh���²_��)8���88A�c<mS��;J�g2-�dD���e�iP�R%�BY������u�,I�ky��(�b��Hci�-�,vJ/?��0��9`��cct.��q;9����� 0�W/��:�Vه.���Cʩ���v���ՕUhF��3��XsQ�I�F��>��ST�f)@+�K���??�Z�b��k<T���eT>kW8���%è��>P}�����ȷӅ�G���c׃������AG�G�Z�����5��״Ų0Mp��Tq��.KY�or�;r�*}g@���ޝ_W���k��-�}��V��a1���5*f���k%_|��>�)&M���c ����ͤ;?������Ϲ��շM��-���M�&tHO�NbUi!K�[n�hPI.�]e%��_R��-�o�`���[P_�� �=�u61\����aM�]ک{:^gx~���I��������x#�u�#(,
�Z�W�!n�l^k0��4)*-ֻ�3h|�V��+�w�    �]%������`���%l��nqƇ��s'���ڽD�"7���ަ>��0`,�7s�F��}�9,*ƞ��T'j/?`�g8��rWR��Zp�	�uK-Oj[�,�.D���\'�i�q����������[����$��>0��(��es���uS?�	Z��ľ#���G���̟�ܱ㜎}{��o��P����Yq��7��+��g<c��Q���3�1���x������9ua�M7H't
�w���8~jg^����a��sg���TH4���s��ax�y��}�]��OEJϱ�ЇW�r0��±sQ�0�̲h�u�,c�(�2-�n�����ܴ����pݸ����/�ӧ�_�(2����޾Y��جX��_&�]��gA���6�YF^Q�,�>��M+�~��j<j���y�M�($���9H��l[�q�H`3���r���@�Ϭ�X"�/7��VMG$ ��C>Q�V�l��=6��p�9��s�XG�+
�T�>��@��-�ɩ~_z��{�?�c�q��hA�[��(}�K�"����p� ��#m�v	��I ¯��p/�g]�/�o/^�\Y�>�.;�J�N�2��2,R��qY�t���$!W`�&�p �E+��'Ϗ�� �!�g�p,��P|�#�iJ?��"��v&Ri��,�,.dųds@A��c��j#��&U���[����9�h	./J��ַ��ح������}U���|ٺ���=`4�^)ȟ��@x��m���.*��0@���uBlUp`4�n^�ѸwX��j�9~ka}�hEW,n��Ea������}����
T�f6<5'!B��y�wS�r����낧�	�n�M��^�
u����[_	B� ��t��l������fa}U_#�����\��ܭd�7��K/�/�P�iD��t�ₜ) 5�m�����T %�< V�S�+��0�)� -���2�#<�Y�����c��0~�J���ܡfmoZq)��u�,��pT��fS�4}����� ��n�D?�q�.��D��5O��d�F�m���?�#��m3�ߙ�J���=� -]e��6��;Zw����Y�ڷ�	ԄY��_w�L����`1�*�.++�,h{�P<�|͸V�.�#�s�ic�P�4q_�"�z��\ �����7�Y�]FZ#Ԣ
��!�6��n:4|[��̹��s��y��H/wK���F4@z�jݾ�Q��1�RS�
� ��.�+e�k� �qe^�h���i k�Z�h�0/5q��U2y���k��,&x��G�I㵷gR��n)m�f���#x���!�� �y��OT�'S*aDT�_�Ί⊑X+MKB��m���o��9�#F���}��O��fIaĚ�vN�Zl'?���"o궝Ng�p`�����?�4}�IS�g��7��3��z�������Զ	)�O¶�p�5Iu���Q�&jA�MA	�Ӄ��B	C����ձ���3�)B�0؉�;��\����,\%�i|�a�ݒ��x��Ps|�4����W��ZE��n�j�O���$=*A���D�ż���i�F��%,�n���b�+)��K�	ak��P^����g˛�IR�9�`_ o��X׌ى�Y�!�}����N'��h<^���ɑ�Z���f���:��좝���%�%�' �A�bLt�~c`��0}��鼃T���&t��iy�� <�"O� �o�QbHzE�$7�B0l���Kd��Fi@�0�r�=aTar=^s����D��x�*l�<E�=\s-Bm�)	x��A�	�p�
��G�&j�$�XB6l�ZYJ���n_�v'����!X�zӞ���������{l%�oj12�� 
)�������-YAt���L�&��B@�X��~b�l����,0�5������(�`�T�_k�#���%g}�G{�z�~1�癊�ݏp1R勁���>f1
�҄��DB�aW	Zv{�b����p?B�2v!����@�}��ꈉ��x��n+Q��wk��! �6�aFv�����o��p��M�՟W�Y��7�Ʒ�8k�"x��'�D�8����J1ݐ	&Ђ�;}���¢l^:�E����W��/Ԓѱ{�N,,��b�6BC4�d�S�b�8��~���-@`����j���Z��:����KBɝ#b����Z�w�T�$&9Cg���>�䭔��#aX�����}�c~���K�<�=�2���<윃�IxV\�8@���V�5��	i�y��*m ��������D'��Ȭ���+	�U&�=��%p �J�ܑ;��޷R"��f�Z��7��HJk�f`�|��ǆ�?��K8M���F(Iyly�%�e�~�0���J�z5ҿ��9�@�H�����8SARQ�`������r]/닛���v������3��iE���Z�u�g��zrB2k>zO�z�i�ȷ��V�����7�� avpp0Yk+	��<�k�P�[#n��}�4�вz��0F�5�}���w����ʱ����YXw�#��i�@}�J�a�d(J�gV����<� �"gA�e��o�5�7N�q�����j� "��z��%l+����;�F�_,ά�i���V���s�nw4l����'gm=�@3�b�� �Hr��������ގXӂ����^��Z���/�^�>@ ��������A�O��N@�
"<��3`fy)�t��UC�����g[o��˓P�w�'�O�D�E8�	�t�N�����8	]������q��c֮�W-��N�� d���{��s$-�w� I"/!L�㉑ɑ㮓�PndV�ύ̺|��mx_���M�bD�Mm�sdYH?Jݓ�^6
u� 2(9�I�����g-j��K5�5����J��x��]�l*24��3HE�ΰ~��H	[F��d.��Av���A��	 ��g D/ĺ����$��n;	T4qjhU**z�ֈ���&ecR6&ecR6&ecR6&ecR6&ecR6&ecR6&ecR6&ecR6�@�����y��	#\o�68CtV���`��l�}��p'� �,�BTf{��^�L0��n��[��9�����&ꑊl$� B���z�7[�]e�=9�Y;��n��Rn�BS�z<jH,	~�����d<�齇����v�����9=��Nf�	�R}���d{3RX86s(Px*7Jc=#r ��N��L�D��RkBj�4�V^�'4vUHF�*�i��т���%�'�Ta���T���N�%�C�M�T�{�{��[�oߑ�K+J9p�N�^N�a��l�J��;y����)��5{��� Ҹ$Kk�ޗ�e�g��wj��О�O�s��(���,O|г�͖/h���C��?�R4+d�j���m��� �,RS�,�4�6ۡ�4�G���Ap(�op�jW�/��>�\�K2Ň�wZ���%Il�YԽL�m:l�v�d�R!�n��/D�PQf�$�@3e��%Y��_ir�^�Mjc`�1���N�Pv����'�?� b0�����[�����u�QEO�d��6�:����:�<�+j��{=_��,�.�����UH�*)�&����`�(��?��Щ�}���;� "V��+`�;��Ó������^��r[��k�vp��5�9Pg�X��q'N��ܗ��;8cӲ���(_H�7r����l��[��>}�Ԇb��5v�+�+{n�ɧ܄/���q;PN��n�.ƦV�zh%j�|��?0��̰�"�
�H<���$��7��k߁�;v�K�K0�04Cf��e�b�TT-҈MU�%E�.�r"�ܡ�{[����&�ڟX�C�"�J��B)�3q�A�Tw7'�}h}�)|s���َ������%����vD�o��%����z�D��,X3�Qf��;L����RZhB��*(r�� ���
�! ���dP�I��6�>b,���%�V3hL����T�����~�.�bejo����    M�>��
?Z��T�W�9A�h8�����h���d�����^���q�����q��$���.lB;N��9|S�W8��E�x>d�YUFǐ���b@Nȉ91 'oY�k�KN�RJb*\M���p5����T��
WS�j*\M���p5����T��
WS�j@I(�%1�$�Ā�| ���:؈1 "&�bR,&�bR,&�bR,&�bR,&�bR,&�bR,&�bR,&��K�"b@D��1 "D����n@D��1 "DĀ�"b@D�ȯD���⢫�F-�=|ͲZ2f�_��Q�������(\������~�.�8��Y�������y\8qd�<.� );)�Ԗq)�,Ob��~��rv^D��4�EH[�pY&}��#e����n� U�Nx&`T����
��
�ƊQ	g�����Q��u��]�����Ɖ�G��D����5���r�ϴ�O����/+��+*Tm� �n�%WC�]����E��na{� z�Ylga�Q�"N��O�O�`�.���'e�$Qn#����v���.d�'�[e����I;�m��7��<������T�y��}7
�X�v�������$�];�Eg�HR��L����3��.`B�^I���/k�_�r	�Ye�	&#<G�\0����mU����8��E����t�++��
�Т�V�ܗ?a��&�f[���VTs-~r����
�WG�6�������".�YmЖ W��͖
�ά]��[����%j�hK��@�V�t��zA�����;
a�Zp=��DYMuq��Ch�a�Z�@��C�T?�w�eP����14��h�ϥh�����}��R���V�誔o��	h,��	�V�f����6���0�(/I1��ƷW+ה<ӸI�!�ߗ��<���Y��6 �$��@�6�W��cb���
���p����?݇�l�K��ubu"�:e"�\I]���k�N�	qɨ���Ǌ�+$�U�����T}���w3�.\͛q��'��q���B��nxE��<p� FFh����*6��yŖ��*��(N<�zH��[�)dtd'ڳWX�G���F���0j��D��뽳�iʊ�X�bP�T�_�
�*X�8�) :("1;��R�	�h8��Z�����2��m�K{Fo/���_ ��y՚��|��e\����M�0�N�*u����i��;��/ƾ��o�HtJj�H�|T:i�q�p'�0�4X�᤹D؃�S/á��Dn9�K*��Ύ��~�i��c[�K�#�>rJ�y�0x#�T8e���ԁ1�X��Y��;5ni�Ĺ��8pl/��ZJ�N���E�R�i�����Y�:?��o�ț����7�D�ț�	��e�x��(�R0%=�N��a$��2O���Sw��B����	?��k2A���t��XXשEAr}ײ��d]Vȷ��b�m�#�ۍ\�ݛB6�?M_�sL��"I�uT$ʪA�,Tkw������ϡsO��O������0��:�W�T,Ρ�o�y��]�"9)jz������TjNo�b����"�l��K���L.��~M7���h��h��/��c>/T��O�偭Up=��I6&���
��Ƣ)0籇c�LR������!\���n���	xg���
�+�7�=�*��ա��|w9�Ćv������k�6����+LҊ������m���L����`3�����0�F���[���D��&D�/�1@$wx^� ����p}�K<ǡ��؆p]ωcg�/���?iB�o�!\�Ic�}�/L�c�B���Fn���9X�N�G"���1K�6Ĭ��6�-�$��p���e³D�IQ&v����K)��$���嚑+)�ne���bU�;��k��z*T��iKc�:ǖ�\B��ޜGL�0ɝ�� /���Iig��ۢ��Xe���~����Yg�NϬ�.1�m)]8qFl`��n�;u�cǑ��,-���0�����xu�2Ǽ:���!|�#n���޹(z�>���������ӄ�M�݄�M�݄�M�݄�M��C��&C�&DnB�&DnB�&DnB���	}ϴLH��C�&T=��~�!�S%���&�]M��;�4����W��yY�d"�sO:p`ca���^楑��e��_`C�4�c�u��H
}
�Zfm�E#L����^������xA���@��țj��'��i�cNG�j��^�f��GeQ$n���/2��|\�$�K��c
#`�O�<լ�g��(�@�:vQ�_D2�	�f&=!�,.��dN��t��$	��F��z�q�j.%��q;1��\�7&�>�ؓ<�\�i���o�~Hm|�����~z�_~L�ޣ������R��,�Ǐ�u���w�������|�@<~� >|�ODjޥ(��D_��^ͣ�]��_0���x� �����)��c۶��컔Z�X�M�
��*p�C\?d��k�fVV�iw+����0#��Jnrw�ߗ[��EQm������v ����Θ��.�C~fQs�[�b�S[���K�}�x�`����R��WO�+��wx�[�5(�x�mw޶�Ã��ŀ�n�a����⤿�s75­`CjY��ŧ��m���?/e��~����%���@���s��s��C�|����ʲ�?lDAxk�+W���z`���R��W��o�˟�8�t���6׎!e4��A�Rв�f<{�x����E���4�n�r�yT��Ơ9�8C�vc��UGV�YY_R�Ac��'���,7m3�ɿ��� }X�7�n�����#���,��;}}Uʯ�wL�#zn8�����D�x�74�f.2y(��x:#-��3�����������?�eY�>�䯤���W��)��mc?�y;��j�j=���u��x��L�i��
����VX��kz����o��nR<���[%VL ����ب�^�j��tl��{�;|���{r�7\<��}D���3j�)n׷�#k�ږB�5���K�ͥ2r��
�5/B�"_`��ۿQ<}�
�͉l�}!M�>���Տo�W�C��䩜��0�ܔ���Y֤�e|a���l�+����p}�f����M�|��|&/�Kĥj1�sA:�b�6�1x�%���\������m!�iDR��|}���@��B����zf����HU�]4,����诠���yr�7],&�'_�~�6��;20�#���O��U��g5�!��P�@d_����r%_=����D�/#��������{�[��`RѸ2��J��e����ܮY�[O'�^S�N��Vy��p�TB=�|D�-Dv��������A�9��&�02��S��C��%: }(n���y�m����_@���I5ʽ
9�Z~] ��5U��.�Y�0����0w�������t�m�m �� n5 /j)wi�x<Qec"�=1D�osT7�����:�2�]��dE�
׍f?8�Y�c�>e�ƻ�����а��T�W�)��r��ط��ul����2;�uB�}(a�$�Y��$CP8W�G
t�@
t�@
t�@
t�@
t�@
t�@
t��A
f�;�h'SA���gsA|���sӶ2L�
3N�<�$ID�o����̜��
�i�C�O�c���y"���{��b�aZ��f������`�fd�$.�(v����1��Y� /?�lӁW�^�Yf��ǩe[p!�}GT`RΞz�Տq~��a�a�9��[����N��h�/�q��0��H�$���`���2��:�i�$�W���,(*v́������%���8=��A�!6X0�slZ�=���T��LWU�z�"�O�x�z�t�T��R%�#�<����á�T0�Oe��t.��`mJ��1���iJ��bT� P����Kn��U�����/��i�w�r_<Xtj'�b(�1-���<�{���S� ���0-�wO�����%}
q�@��t_�=����vc�]�FZ&�`�����j�,�۞BsE�]=y��m�/�h�4"�ߕ    ��$��|ځtj�����lo�E��j�O m_��'���Kvƾ��':/?����x����w:���=Y���K���B0-��@ �zy���K�f����Ri�'�f�G����d8���P>~�Y�?����4-D
d��Cuc�$7~�,oKU��>>��`�j����Ǭi���p�Hg����,��yW�:�t�r��f�����ק���?������Yy[�9KW�3�?��7	�?^Z�$ڎ� �]ۙۮ���D�����vd{��i��	9	S`���uc;pBߺkOAm��A@��=�Yx�Ԟ�F��&�kd���F�jd���F�>hdx>����y�0�(���-r��)74=<̙Da`f0����^�{�w /�B/����{>�w�P�2M2�t�,����L\+v�"����zg�>�gyjYN�I�x����H�(�\�*�0/�9y���\�wV?ơ޹�(����/̰S0�c3[�X5M����� �j")Y�����ύ�RN�(�/���f���7�|R��Yn��(1�H�M5��zn�w+4�WM���?{Vc��ly��D��"���3P��D�q�5W�u�Mj�����o�Ax��*
D`�͝�����Ë�o��A/aL��`#bz��e���#�u)�� _�qw����s{ K|���O�W �{�f(�{n�@`�7�C@��}!zn
:��%0�`��#<,q�H?ρ��_�?�
��j��ы�QW�[^ ,�>n������1W��h؈���b=a�oT���  T�7�i~�.4�,VU[?P�B��A��Y��Ĕ����V�t��]^�LT�%TP�Ȇ$~*E�_�T�EG����%����Y89K��p�|ux�t5�b��[m��-�����$:����L���	
��2��GS`����{'`�q�wzU&[ּ�:���1��؉�f�ہe�*t>�|F�e�O�Q5:�5��Q�F]uiԥQ�F]u}Ĩ�\���Jx2D	c�HF'ex�r>q�8� 7��KM/��_AV�y�~*��.�y�ɿ���S���q]eI�_%;��7���\�|�Hp7�7���d���w��Q��-�ɡ�i?�R��,;
]��g4�|�|G�N�0IaffN�^P����m�n��H�4{��Y��B�a��vB��)�z�%f�Z�Y[~���Y4}c>ZR<�EDg�v�;ؒ9{�'�ͱ����Е"H(����7¸�Mn "���3�9�n�x��"�Wg]�tT�����&`m^��������j�����y��
��N���F�����Ctpf��^z=��;9a�xr�^��N�t�GD�.\�Bf��2���86����A��з����ڲ�&w�|�?��c�I�� b�Vש�֚wҚZjm���Іg|9�A�� 3G��5p�8�c!�4-<�ˊ�L�46]��܍ �K���և�����2'5?wLρ��~`�y�(����g�>�0ى
&)K� ��/�8�}Tv�Y"���s�qJ��Y����(w$�|bj��ql�9Ydz��X&��܏m/�F�J�X��GӔ�I�W�8\�f��$���)�%Y�'L*�ϼܕ��Q'�ڄ�.%�1zŐ~d��1%yL��c�ϟQ������'E�vc�K{\6�C]�����X*�*~�M��<'��`��{��u�`|�
Nٲ`ʖy����cEoo��T�k�Bꕰ�s�PI�y���$��q÷|�}�23I� p�GQ|N�*��	i�zN�j�Qq�C���f|b���lᇩo��OS3��a(�(��T8�\8ة��w��W���_ȄF4Z���K$�Fi-����j��m���3�<�g�[6����u)n�T)�"[�?��{������ �VbU�Β�xa/-��{+�/�F�ϟ���	7�OY��t�h����X���c�o~ē�>/��m����ͳU���~$^�g�2\��%؏g��[F�u�Y�X�i�aV��e����-���~&Đ��z��:�6����6����X�/Ѓ'Oiq{�E�eo*r��������[Rnw�-WvoL�>N]�߶�BU�m�P��M����!���E��� �q����p�Ѽ!�4�9�ù�3`���������P��s����>	XwVfdȏ�>��ѫa�?�r�;'�èd+��~�޸����k����	D�G�F�ڤ�S����顝��{8 u���`c0@Wb�_zS��q\�)�I/:��1���`�_���\;������Nm��#��O�j�����s �d�{��X>f�>w��nj³�	S��{f���q���
[�-z��<���4��H��"�4�"sGLf���	UI�vHc�)A��H�VԌt�����Jv'A��iě�t���W�$�0�z�cR��6|�
�W�WT�4>V��^r'��p}�-���!6�͜�hS��:2��5��H5��_t���[��7x��W�c���S��ŋū��\U�����
jPr9e�{ό>t_簤|�C~ɤ��3:{BϦo��2��F�,��'�(��`��*W���i�����c��{�9~k-ԫ�I_S]8�PNh;`s�[�7��N����د���N�W��;Q:ܧ�}:�����>�0����������Ͻ=X���n:���i:���iq8�<_F
\�4i�e��e��q��M�[Xv���A�)ʱ�2 7ӷ0�4-�D�ˀ��-��ѱ�"�8�\3^�d7Ʈ���C���ٍ�^��2S+��<v�� Z��0Qnf! �,u�8Jw�b�n�����8Ǿ���7S���ZAl�v��^:����	I�ݳ����8��;D<��>11|~�f�#3�\����)�D^�>�[�,����ѐ}}]��|一!�CMm�Zo���B��C��T���������b�UyI��$�S��F
��A�,�L�h��l�u�1ea���]վf~�zi$%�D�f����!�i�����D�z#�טˏo�c�L�HeX6��Ձ}���|��M��_n6�5i͚��Ȯ�\A��K�����X��G���`'�K��֭��Z�ɼ�j�����9���Ȯȴ�Ɂ2�B�I<� �v߈u�nf+�'MB3�n*���-���z���+�+�q�8d��x��_�'ۆ���q�o,�FY��iJVu��ó�O|YMKMe����3��������OB�����d�����rS�xh��2z0� ?dy�T4�eۉ�`�Y���o��+H�P��G��̿F�D�,۶ґyu��f$�뚙j��ޛU����&i�Vr�j��a 3��>xV�� Z:x)\��5�u��!�@Q�)�N�Ô�A����rc�%)��	��X�l��w�	��˴�<r��)���(W�z�N���h����}u�ˌ>k
�r�Ṟ �o��~]B[�,�D��EAlJ
��h���l��%���ڕ?ᚁ����$���:Aj�F�ŝ��s�G���[v���Z����~-v�^�������&pKu`҅�ꆤ<$Xr�-CfS���*���l����&��]�$�Z��,-X�W�g\�hv��k��ciZ�D�R�;à�ݧ?��Z��;�B��R�ʢ���:�>Z�w{�'�d���V�t`��fl�%c��4�Q��;�sQ,}|�	�^��H�$ĵ\�&���X�.�-��*�`)�,k����t ���C� ���Y:�re(��<Be[�9+�u�˥"�ebWR��*O`��@�a�s���XU(	��%/|�Q\����Ck|���U����%�>�O%� \��4VR��{{�+!�=D ��rC�ӆ��`�|vb�ڳ�@ϰH��I��B_�Tw�rw�0p���ľ���'�V L��0-����������@ird�Aާč5u�oX�S����]�W�
�GY��T`y�������D�B^U55~b��0ebא���zFi&����A� ���b�����     xrվ\�y�(v�dl�@�l:%K֍e�&�C�W���U��c�=cbO+5~����Ý�N�`}�兜{:���)-@���`˙�\A5)�vm1�CI"$�u
��$�?�ǰ�Z������8��Ԛ0d�NWӂ8��Z�
����Ī�m;!� �zvɶ��*�0�gN��I��ԭ��W :�C�B���Ŀ��|��	��{sU��S)���=��I�l �ʋ�ԊZ�VK�(���
�dg���'W�\?��qD��a���}�;Y�wh�Z�T ��f���(WMHi\���C��$Y��O_pQ��>�j�D͔���q����%��n2Dn���Dm�W�۸B�<��P �|).B]�mЖT�p�>�&�əX��M.el��E^�7zG�F�N
!A4�$89�C�-?��E�����tz�Hn%��z��+飵$�q��$+k�x.$Q�;�׫��7�ykA�U~�,pM�.��}��!j��QJ�K�7!��y���HJuߖ���P��4qn�`�Z�����R�Bk�@W(�8`=��f�k�#�^dr�ʫC� r�=�V�Ì�9�B�Zd��#;qI�MCn3� ��$5Җ)Ooiv�;�K���A��0J�"_��TZ���E�%����S��>!ˇ��V�:���W�I6t5M(�����{�#�u=��HZ�H���!��v���c�@�d��S��S B��cO��H-+>p>��w��\K������JIV
9�|^Q�_]��d0�H�*oP�9,��'�e��P.��qt��,��g%��	a���ɖpR �� ReX���0�Udo�*K�[�J4��.��}�@#���JG�JC2�h{Ƃ�]U�H��470�+��&iHa��Z�4��'�jCja����9����)B�����aH�q�-�NX�#�S�B�ks��oXb�r	2�P ���n!��e۸KZ�5��*��v3�3���\���q"�|D;��ƃ��WM�6k�n��lۂ�)���O��E�&K�t[*�{�"$;�|V���/��~�[�a)	�0�58�eu��k���5X"�����ʴ4&dD�u��'7	;���/�/J�Jǒ?JvA�XuL��P�6�a�R�is�iH����:)W4yE�ŨV�{cU�����e�-�5KB�l�匑�)7]$/C���ZBHx^%70���H�$�P%g�
K��lW~^�	hm@��eC�c�=t�Q_ۢ/�F4&�h�	��͒b�C����Zu�!A�y��R78ht#��o,$�C��~S�W�4
Bв�a4�R�����uh\����R��o(e�ک텕�Y#xI�"J-����8Y����;�ct��b�49�����Hٰ�
}���W�N"MK�í�nr	�)&�Z���S��qEȃ_g�$�]�V-�0S.�#m��M8�B��X�rGr�BTKl�='c],ͼ�%r[��:� �Qe#o�h�h��4�� ��?��6�zk��6Z�6͝�x�e�9Sq�y�OPP��jQ�����ڝ�.tV+�G�K/��F�j�Fp0��{��&�*rQռ]�/�vP���\�+e���X�U�F��#�m �'P�7�X�.i��� �
.hɨ>5���-�y�뢾"G֮X��D"5,�������M��^��g~���8�C������ܖ \���a�������Ԗ0r|����q��ǧ��(�(��Z��r��q'R[l;����.�*�ȵ���DG;�f�z8t��笝�.�b����Ȼ&8vf�����Ji�# �i�u�,�s/真@�v0#���&�/��s�s���3ο�;`<��>1�\X�m
!2<���s�e�"��"��Y����=�ULl�?�8�I�U���������*P�ƭ�㌆��f'��KJ`{�e�p�ek���K��wI������J�{_f�e�K��0����5��zn��e֠%�wﰽ���e 'lz�t��Sx9�;]mt[P����-_�;�F��g�)x�Q��=�!�brK���;�P���xq/o���"�A������B����G!�.lu�wL�����w[�;:e�TՊ]�V�)�ǉ$�k�Q�%v���m{���]퉕���8���a�At� m���n��v������A8���1���!�6�@�v^�=�oL���Tt��	�M�0�!�F!�{
�)�������ۨ�_ ��r4�1����K�q۟�I��7�� cz'�u�����9է�����~��Zoh��z�=oZ���x�J�����~���v�]�ӻ�~,�xj{1}�q�i7�=ύ�xq�F��S<*��x�ϕa��Ղ"/>���W�/
��
]���N�/Nn/:��>���9S���9����g��a溾mF�盞xf��)|5�,7��"��l/�%(�Sۊ���j�Ѷ�́�T�s>1��X؉]�ܘ�K�ԌEf�H|���r[o+�v��cvt�y_���ֻ���އ���Q�cu8V�_���X՟�ꐬ�Zw<�,9�:,�׶^��am�)�a/{1��<����G�Y��</t��Jv���i��(���1����ډ������O�N�W����nS叓qYo�؇<����^/.;��Q\��AG�JrX�Z�����t���m�IӼ�s�d��Edg��(";s�������x�3?�La�Pz�m&���E�Ya�|nnD6��IF.���$��aL����S@�bfq�����ʚ�� [%uQ���h/q)�(PVl���)�w:��Nv�)�r�`��*
~r�M��2�W�x�}�z)�qS1�x��z�B��1��^�2)����I+�{�|���:ҥ��� �:��4�T���E��_z9��!��W�~�Ǔ�)�E�����<D�������\�W�sLA�'b�c�m��<�ޞ���w"PV�k���2�����i�yӷ'l��o�HKm��;�'+����f�Cx��0&�������`lO�d0�O@�,m �#�hs�����q\��l�"@�n�i�5$��^&{���^Ȥ[��&��	�JI��U#�L��q`��w�|G�(g�hY1����ꦹ�]#���j��e!tp��6_0���᡾"$%GSRs$�*������x�7��x�k��d�����ϖc>�B�r��R���e G2�x��<��PHW�%S����H���l�
{*��aAP@X��R�/b��T&�Z`>7t�	.^J�^�V�|Ő��ۈz����r���%�2C��d�����4��)�誱���c�z���ڑ�������� ��(�@f�hO�Yvq3뽻��,�n��W�}Jf�S��`�z]��K{�|���u#ק#�G���c/�O׶�p2�b��Q1��6`�#�В����C+��#p'q{M��'�>�u�}��#�~Wh�Xv{�m:�� ��4L�������?[�3A��i�Z�s����&����1�'��|bҫI�ʉ�?4�$��$�v��a�N>�#�iVRL����C�l�~g�<�d���t���p����+v!��z�#����{��[���GR�1��p+��FtzQ=�m���I��y�Y�3���p�BK}t���-t٣p÷N~�6��r�Ύ
I�_�6�<�j-�DT��^c����\`��gЮ�2��i�ʡy�(t�ߔMZr�7�gI��`A��-0�˶�'��]`MC{+�v��Z�--$	���%&�(�
���C+����Tu�z��3�o��^�ԃ\��]�fS�Ӟ�:����(��1U#�AXܣx�:(��T^'�!�c�|i��_�����%����Xgy�,& v/���[�]�S�w�$��;=��:��`9��j��� XvdN�e���x���Wa<��G?O�s}Ǣj�÷�S��8q{s�E�?�5�-�Ǒ���,3݋�ι}��zG��EVdfE����D�4���J��s��J��<��:�d�j    �Qtt�@�����}�q������B��=�;�bHO� `��D�PE{Q�v�td��W�P����dv�sАCP��T��r���gf�a~�:�N�X�;&Z���;�����D�j8
o��dN��히�؁��p�F;n��p}z���B��DvV5���~>.�h�A�Xё�vN�hg�F[���ﹾ��vl{���}�h�[�$��o+�^����Qԅua@]P�0�.��R�ua@]Pԅ�)G]Pԅua@]��? ���0�.���0�GS�L� y.ta����҅��u�?]�O3n�B~ ��.��}H�纐_������qNN�Ӆ�4s�f����!R#W��Y����z��)����u���oo]�B~��B~q�>]xOo��{�2�.����G>��S�.iw�cU:��C�Zwh��è��^�zm��{���/��~L�t�<](O�Ӆ�t�<](O�Ӆ�t�<](�=�쏫 �.l����v���é�����v�����Ca�:]�N�Ӆ�t!:]�N�{�6u|�\��~��С0KQ�������Q��???��K/x.=����,���I�D�����z	���IVdf��NX���ѣ��S�cfy��0����0�/�"�����QU�|�`��k���{(�,l�>�����B7/����odz���L���ae̛Em����_>��"������uNj���f�	'���.�F��I,����<R8��}�&�����6d� )Y�Сp���`����y�؅It��� i�i��&�� ��(���qWSx��95	�,M�<L^e��q*l3*D^vn9�{���؏���3po^������������`!���,0u+�>���zV��@��z��P��~m��-�#z�j��AH�������ӯ��&1���������?qC��\&?ѡ�g�vX=9�����W�f��b���tV�'!95 ��fi|���J��My�Ad��0EQV��# @�֊���?0��ce��$���`A;L�ŚBH��}v��-E˔�`7���n�?�*h��*�E�ٯ$����*�5ᮓ~)"�G)�=٫jU�	�b��ӝ�j�'A0�G�?�s溧�p���G�4�����Ӊ'�K 	:c}0�'w0u��Ц�K�`��)�k� ���m�m]fX��Ќ�U��j'���jp���$��6Q(���ͫ�(dHB
"^���B�c��&�A��Lp�<_�;��~��@�:� r�����%�vǬ���ȏ�f&��9Z�E��M�BPT�X����sUݔ�Ta��%xa*Ӏ���+(uI�L��C^%��5xa�$�"��H""7b�S%����K���E�}�'��~�E�TI)?�nK,K�b���Y��.E�H��c��*MK�ȹ�_����U���u��nڎ�'B*Pd;YULi�V�&��z�p 8z�u�v.+������':�2�'`��L�=O�y�"��v/��]q���|Ƕ��v:�|��\"?`2M0ZLd	�����#���bQ�r,��1�sd���o߼t�כ�'}�g��S�5��E`R�D5H� Q�D5H� ��3�g)�0d'��06���b�2�l9��
܂��������N�CK��O���wо����}�;h��#�t���I5H� Q�D5H� Q�ći����D��4��	M+tR�K#�M�1�&�uD��l��
�+���i���z��#y\���������l�"r��t���ۮ�mƱ�{q�8�{A�Y���ё]�c3t��D�c	��M�(�3�N���� H �Tm����-[�:r]c��W��	ScB<�B�G��vS�]���r���\gujs�;�<�>11��v`�܍2�����Yje�7� ��m�Մ���ײ�9�FWd��̔��N���1��k#o�6:c��<ofS!A�Ѽք#6M�L^^�
`0�Ct���7}��w����5�?�ԀE���~�)F��$jK�J�Ka�m%>�F����4h�^VT�T�k��i�%C�$��JW�<�����H�\d��q�q��CP�h�v���w��+4q�}�#��]��X�& Qv��X^.Iv���:��6����>�W#��n�|�k�;�UJ܀u��d+��ҜH����I������Yϥ9l�1rx�p���7���(SuQ�Ut\��	�U�=<��u�-�=M(�B�-Xb�3�y,Ǹ�5c��/$�M��
�
����,ъ�A���GMg���Hw�pݗ������<҈�Co�ံخ�sS��l]6(�}&g��f5cID� T�RƾԼ�7Ҋf�߸����^��(�"�L	��PA����Hԫ���è�#	�8���@9��
�5-=L;�V[K����� ��2�C<�(⏨i�:UFB�m�0$���F���	�ݓ3�Ǹ9rk�eQ�Y@*������EGJ|�F���J(\�F��Y�i�d�Dލx=k���� ��KY6�ފR�'pK�+|w|U��0;ₓg��L�w`e��^
L��t?��>밄�r�A0���,�`�]A������
�2�}�����G?9�g�8.P库$�+GĪ��X���z;bU7�<�y?��PX�g�>��w�V"Ykb�(F��X�����B\����=�j�=�"�Y���$�l����:62,x��9������ VT�B��&�/QY ����X10���/	C�r���2�Z�#�ܱ���S�'ڭ��U�z����xў�Gzɜ	��]�/i;:����H�/�ޜ����%��I��un�ȡS����~�&�%ѯt���Rg��*`˚��:ʍ�'����0���(�����`����`9�r,�YR���zD���+�0vZk�)����;�|�08�paqN��D��G4e<ǁ�1��I�aM�/�혥�:�1������z�BXE꙱�Ƌ�̌E����^j�v�&g9t���
�sdV3�d�8����Զ���	3�0�h�R;,L�S���y��`@.j��=Z~)���û���s�8��=�Ng�ڃi�!�QωV,��e�68X�A*x(&�:)�t�(+�q���13��4�CK��ς�\!37���������pC�����GZRh��ƭ�.Adu�C�`�dK�!�Z��7H؋Q��{aܸ�ZW�I�.7I_���ΰ�z�Cm�Y���v��l�����H��D[9���QT��ݘ$o"`+���	3��T��{�s�M���Y>$飏�}1U H.�V�12T��q(}9d��i�Q�� �e��x㽕[ėTă�,�ա?����:~�w��>&|'�3;�hrf@�xi�����mO%;���c�{;BJ^��v0v�[7;S��_�Y�l�8�Lg��H{�I���a�·c=
�D$8��v`i��#�tW(ॡ�e�cZEa�T����8�"�s���Y���ӊ<��x���iV[ƈi�`In�9�8��p���䪁2�<��mo���f'�36�\MJj�n��2vje~˂���@(	�J���}����F^�J��'�\5�dQ�4F#���]A���5�:�ߓ��{	8��r��9���Ԓ1�̈́Fۡ�	�S?Iq:���Țl�D��.�n��N�e䀬������',w`}�%m��~؎�vV���R�o%�̠~E<��"ٯ�b�T��4j��8m�����ƣ� `4�oD��d6P�O;To=1�w;=8	�:�����+�F�
�5�����d���\&=H�B�U~��0c�J?�����1��V�c#&<���æ���`�`r�Lv��}Uol�n��+�F�-���+�@�Qǉ�Y�M�
�Ĳ�9����7�\f�[���J�$x}h�p�z�қ� �-?^��qB���X8�d]ۊ7>I�:�b=�u�8#�r\�&�{
��� ��� �   �Ʉ6ۚN�{�f��S�t���S:K�a�4,���Ӱt�N��iX:�7���Q�W�)�6�Ӧt��G�6��C�4'��Ӝt��Ns�iN:��7�����/鴤�=�ӒtZ�NK�iI:-I�%鴤ې�OK�QF8�����"ڲ����c���؃���/?�������      (      x������ � �      C      x������ � �      6   @
  x��Xyo��;���"�aɒ;����"5�)rlM���%1spJr$+�������ht%�@$�����'G��{e�6Eo,�ǢWi���%j*��G��e�p��XZ��>r�l���%��}�k�H7�_TV�\	�dEW 0�2iWbj��"6Y�fJ��[Y��q'��-PcSx��2bMc,�V{2N2�U`z#�:˄.��+1�d�Y$��S{�J��ᱱV�^�����EW�Wz���N�t�qYΥ'"�K��"_�T'�o+�oV�s[%=��s]̜x�U��%���)�z��3�sk�$r.�R��Ť�B��N����y�E�U�+��ȵ��9lZb*cO�ȉ����B\奶j[��]8*1yKB���������$�e��R13��RM|	MJq�s%e���OE|��ˏ�����1���;���+3	�1"x��S���δ��Q�j0Su0�v�ĩ�� a���
��N�9.;�G���AZ�V��$����`���^r��L91Y	�RbDff�� d�CЫA�e���q�����s$O�>P�FN��I4+���s�$�U!õ�̞(
k�J�V�+��]e��(-f��V�Y̓��QE@d,>��4X����弜k�.�k=��G����B�"�~"	U!'����U	9�����Z9e#kBm������W8Fnq�cI��%W�ə�,<��Ȣ@A'��>P���jz������&ҩ����ͽ/����A�9�0'���S�
��	\1�3�,����1Fn΍I�v�>d��&�\��!���,�˫��40~d]V�Mj�!��$j�3&�_�>Rw(RD���j	�nW�H�Cy�ys��������q�9�5s{#p��� "*e.7�u4�Z��� Aʣ�Ce\����ٳ����Y`�OTB%�@l��{}�����M��;~��9�%�o�o���\�����)l��G:G�uM?��,⤼��h\�ҹh�9��yj!��}�f����9�>
��N�19��}����ջ�������_^�~�.�z�����FS�S!�Pz�M�d|yy���`�*�"�3��L��OCl?V��ZG�D�����x^i��h8�gT3Y�c�����J7�<y"�Q�ǟ?�+UX�卪��o�0�T���0/0�����vc�)M��B��������Qn��,��ɭ8:2E�
�P~ha?
/A�aV�������QC��` ��yU��;R�/^O��	'-�`�����6+iA��{�dR|���-�cjUkkP��>�1�n4��s��BԂ@{�۳��Q�ԭ�P�Q��#Gi�@R; K���P����P�)\qN����pNd�UA�eM���hDE�ad�L%3d��g�n#P���y��A�,�!�%����A�������ݝ 
���W5���������o!����A�}#���������YѨt $	�!!��`�����i�F�*Nݯ
Wٮ�4Z��b��B٭��ms3�_j��$�v��B/kڔu������R�� ����6�@�)�"����W�,a(�8Ӥ\ۦc�c�֨.Єi"l<����Ni��)����1�ϳ�7�q
f��s�$�A�[��PG�p�h�<�E�l�|s��M
��hhZ��~�M����ÿ�|Yy���u.�Pg:�\��OS�k���Z��J�?�k��?���{nv��r��7ϑ,i@�翮>��F݄q�2e��͜񤝡	S'Î�`�,�7��p=e�W��Qi�y�[�!�b�������p8"�H3_MT��͢��ģ
i�PEw���X����Aq.������F�F꽓d3�]X���R�	���93f9Ku�Avx#��ʅ���}/�3} ��/J����� ^+Q���0�����J }z��>�r�wO�$tx�9����x���� e,�o�t�-�����qf�ö�|0<��g���&��u]~�nG����h�ۂ �h	l�ڳ��ƕ���D���e����b�����rtcv��X�����e���b5?���[`zp�ȯ�N�ofR�2	
,��*Wanw�������IU�qB�D{Y��Bq���𡕉�"TІ���~��N��ga%��a�އe���w�����ܽ7���n��f:����G�V����ey[�ث�㵯ڷ#�3P(��R�z�f��=�r_�p�A��k: 3 ���������b�N46F���)L?/�zl������L����(�`$J��4�ro	��T�+�>�bk�o��)�/.\]vٚe���'7Y���Gg�y�a�߁1���l��`_0�����!���%Q��~Һ ��ڝ����QP�~r8�I��7ȃ͸���=�Czxc���'�]�1�͵s�{�}Y��R�j���kF�_u��.V#@[/ׯu�XM��D;���h�Q�ᇾ҈fBk6�ЃJT�4.u������Dw�kȄ�Jv��:�<VIW����"�5��,h=vE�񭍃&�(\��*�ݞ��T���O��ó��H�����hpvyqq~Y�������r|�b|v1xq~y~������Ǐɋ&�      *      x������ � �      9      x������ � �      2   K  x��X�n�H}v�����u��ycd:Qֲ��� �&ٴS$�MZ��οϩnR��" @��ͪ�S�NUkt����Rv�Ëaw���?v��p,/�?�cy�B����;�L/�"ˮ�ȫȗ#9Wg�n泹�|$�Y�s�"�ϱf-�i~��o˛���zk�`8�F�^Fg��b#���l�C�A��2-?��\y�ā(�,��[T�^��W��R����דD��sN'�;����:\���������j2���h�G�$�/��d8L���H�� -
��-�W2�&�H^]\^L����Z�h@�p����v=�]:�r���k��/�;[�dy�����g����/{�� ��iv�#�h���=���c�Q�2#�5Ve�>��*��X;rw��En.�8�U䭥v��2�
�bG)C��l�@�HC���H��嚲r-��+cAu�ǂ�#�?��F��Tq(�Wz:�:�Ϊ$�����!�ٖ]�B���U\��U���"D�VUy���(���="O��4`�J�� ��I@}:�9��Hޓ����yKzc�mߜ�۱�g;��cϞ��_�-�~�7����r���[�3�\6��G�o����t����8�L(I^!�'��G��Ρ˳4��	�(�$�b��/�RH��3ً�3�i�t�����YIr�m�L�le&�ꓶ�8X���H�#֣"ې �葚<�1�"*�
�G��1�|e���K���H��x�i�G�̗5�7�*)/�g�[}��(Bs�eU�/-�(�z`sB܆�� �<��u�z���庶��C���ӧtأ����ws��Ϭ;����l�7��=�Yw�C�F׳��h�tȔLCQ���s|J�,ℰ���ah���Wyȥ۶�4�� �
.B>7���G��/XKu�uPFO2e�a��x�7��eX%�>��P����7�}�p���$.w�,�)�7]ܶ4���P���0*�V{Jk�Ձ�+Q��DY5[%��Q��9f��4EV�F�W��d��l�.t�3���[ⶨ�M�`7�i�G��T����C���	%La7A݀e;��G"n r�'L,Gr*�4�: ��>�B+��� U��ۇ�{L�Z�	��z2��X!�&º���e	Ee0������t���Ƃ=7^��3c�(�B�%��zt7�0A]��m�[y��$�~�&ۦ�K��t�h�!#��. �J`��o�����T8�Mo˒Q���"�Or�%��aVy��%��R,�I�����E��g����D�3���������+��8�^[W �qⰵ$�Y�U�4X��Y�i�Y;�X�����ߏ�Ň>->x���4~
i(��"
dB#��2��وd�g&�V��_"z�Ђ��}v(j�OA�Ʌ{�-+m�e�3YD�;��gF�V��J �n�Q��YxD�oF��})з���f��K��Rdh(�1�m\�����k/��<}� 'J�<�/'��vǄ�`XH�8ZҲ3�4[k�ꀎU��;�C�bU�ۭpe*�plwޓ���<r�������=Zp�'ȼ����E>`���"id�h�2�7�V�:��Y��kXT�F��"e^k�Y�7��p �z�v�~�$�����[����48eR�A�_kK���>e��0��#Sc^ӺM������fv��FQ��(��P&�HƳAƗ�V"�z0@yt4耄/�@��K��i0��escj߸�'xf�;���yC q�'�K�������}��*�g�6=��P��l��S��{@����JWwxSgE��.����J��H���-=�8�Fh�������\S�c1��$Ӕ��#n�I�XK�!*���EY.��x����sk��f���z�0���[�Q}٪O�nY��
��S��'_�m忾6���8�7�pq��s��Lt��OH�����p�s*T5�k��:�x��H�觐 �0�8C�l.�J�l�=7���ZY�
�E��ȳ5��oM2�-Dg�0���������q}� ���f��>D�I�|W�1�"�/�)�~����I�[�Wq�'i�g��͸����S���;hZ%ɫO�W�^���\      8      x������ � �      3      x������ � �      :      x������ � �      B     x��Y�R[�}����1�}��i��	c�c�d\��� )Br���߳�H �|,�I����٫�ڷ&jZ�T���'<��K�4��R;�v"�:/I��`]��i���G%s6w�RڹxsЙ�q�?t8�PI�ڡ��\��N(�
i�C��V�q�̦@i�$��%g<��6�brCHJ�J����#��b9̈́��-w�H��=*����\�VȈvH�CjE�{���x�9�6qr��Yf��u�uI	'���M��9��(/>��vB�Gi�1i�m��n���]�Fz'R&6$F���x�D�b����K�v�� ��D�1�"&y�1`u~!&��r�6�pm:o}���V�`u6�eb�ϐl�1�x4*�Su��¤,a	B��	b����7�T�@H�.�T���C�a�_�)4Sc�$
ACdκ��q���,��ҢD��c&a��.�p�$c�$��V>����Jm�{,�{H�Ǿ{ =>��]Nв蘭#�UB�Rh�$rkm���U��D8�*(3PGl�H%Q��B���-�LO�CN2Rq��VH|�'��ܺ����y����l���P�b`�W��$
��Xg"��&�Y�3g@�E"��*�ȚRgC�L���V�p�N9ێ�vH�C�#߽e�X�VY�P�^App�
)� jXTĚ�H*Z1�! �dπ��Qd���5�D'�XV�vz��_��Ң������
��W���s�RL!��R��H�p��9G���Tj�-�hb�$�"~� �����l;?��k��[!�A�)�}��jޙdBRC/*?3�^-��2e�AE5Q��.�)�b�r����O�V2���Z	Q��3���0�nzbmP
d ݁F�v��K�W�`էK�g�=��*�����J.ѡ�`24��B�h��-
e�)���`)�\�cے�q5[sj���wJS;���{�aÓ�����������J/�R�:Ӡ�i-5;�x���7�J��u��F�M_�#�$�'��ў�]�-�A+dM;�8)�C����o����R+Kٻʏ{��B�x�,=A��$�YSFx����g���`�E5����B��{��k�-b�op�G6B��q(w�@}��Iӓ����J�ꢭ�(����,�D��t�!S�ʎ5��&�r�$�~%h����em2�D��]I����C�gmx����K��ׇ8 N&*=o]
J���I���%�:�GLVz�'�I�WojR-Z��df-�N�x}rv���Z�Ǽ����RqR����й�;xN����%���:_vGi�������}gw4����/������f�狛����x�?_c��f����K}4�W��|�GWC���|Ӽ{��4SY��J��4�n&c�����U���u���8Y`㥝�����ً�_^��}����~��hi��_/m�0�����w�\�.��ݣ�I޽�����e��y�y'�Y�{{[M������b<�׵���;�%��8敥����CƅT���u�嶋Y]����K>��E��m�>
��?���͋�y��'�ա>u����sέ����q��򧰸��>v�u����8�����}u�p�_�7q6��G�q#�K??<��,��y=�I���Nfu���og��;��v�^/�V)���S�G;u�0���#��UG�����^��h��y�{���w9�N�~���ETWW_ih�[�Y�^���.}9�yg0�)��>�F�z4z�w��S?�M��Ė����
���C�U�S��x\	�O��<ȥ�̾����g.Q���Np����Ѹ���8��l��G��U����<ǕR�<�t������q��4��.�����l��{4�O_�����_�V"5\��������pp��f����������Wg9��'������0��i?�t��ea[_]�|q���l��
��0��q��K$��^��ӛ�ޞ���7~�����Ҵ�{��ޝ,��$��M��U��UY���rҨ�?�v��?���������o��~�?/s�8Y��&�����:���b��5D�����.��:|�c�79h��.�}�lY��������?�泭�t[��v��O>���_qi��ߣm��`�-�z��m	T+��qAK!�,͝�
�'�K��B`.�"<�d�Ck��U��� �f��?��yuZG`���4��7m9��'��$�����[/�����M�:�-%8;��2�s��p)2�̷LU0G�z��4Fr�
}=v|�Vș;��JƤ��:�d3v�a1iL�!���&��f�0�Uҹ�(��S�lt��:]"y�X�Q�'%�*�l�����W�$�!�Ab=���HB�fW��]0-����sc��)���+�Կ-���������Q�Q�$����Ė�1�x�R&V�\�VsD��.�����\C�;�h�4���c�%c�	�O�_�إ�K���R��Ex�H^L}n��9'���a�u*��Ȣ�/Z�?����r���y��������0{�!N�^X#�e�Vz*)�1r#�i�cl4�P.��9i�a��/�O�r�czv8�0]���v=^g<s#k��h�d;�:��8&�:xd���F� ˄��>�`�aB��e/c�>�NH .^oǥw�1g9�W���[��z�D��0L�2�뛧�!���Rsf߁��:Ysi����R�-!O�MȍG0\���s���Wj��f)�3Pk��c�"����:�3�0��V�័C���L�X��X+4=����>{��բ[G      7      x������ � �      /      x������ � �      <      x������ � �      =      x������ � �      %   k  x�}�[n� E��*��Do��J��8A�&28Rw߉]5�d�k�3��^8P
.N�F�\�na�F�<R~d�F�ؙ���o�	C�9��.��i���kC� �pT����ޜ�G�>���K"��1w��}��`4�H˕^���3��$
y��x�v5��T?ދ�S�:�g�!�egR�q��V�0��Ku�����nn#=�zc���	�[-�E�nl�Cj�Gf-z�@nZ�!�P\�����:��)�V��H�� 6�&Ԝ��-� V �k~����+ʍ ��� ��L0~���	3�S�7�����?|z�-�X���W5��2��b�k��riH�(܇�����k���0J��!�����      0   �  x��RMo1=��
�g6�~�{'���@P4�'�U����*���f�T*Q�Śy����o��"�4JD)���	�@V�WM��klw[,��6Y�O�o{{>x�S7�@���k�1~H���(��b�=��� �H9Yv�:��*�Ha8��dH�*�<o�弌�]ztQ<�{���yyv^.��}��c�u�8�T"�:�|8�����ߨ�@~�HCT>�BM�Άt�A?�_�܂�����{��ȱz��_��p�DZA���g�0�dh@��ڮܠD�^?`���-)�L���A��Nc�^�AY�k#��6:E���ThŌ����;�=}�X�\����I���c+�%>;��!ĦJ���1�6E���yt��,�#!����Ft����Y�>��1�؞2��˦���)��"M�G�n      ?      x�E�1
1F�:9E.0��d6N�I!."*���z������8�J�B�"$33M�3qV�����~�7����1~ex�l�������isn_� vЂXB�)dE��� %h��MY�^���~�p      ,      x������ � �      @   �  x���M��6���S�2D���:K6��	�r�<7��*+��x�^4�|�H�X��dj��H���P�i5�L�56�V]+Rk7��lħ`r�n��q�������Q��D�TfSD��l�(����{�����/�ز7V���l|X~��A�'Y"vk��(�Q��T�WӉ����$�٤kW���ީ��d����ib=�%bY�7O�5�-J�I�5޹a�C}O�'�D��p�zAP{v�&oPZ�7��QY��(@;Wo
��쉳h�p���{�Ӥ�����D���(�Q�Z+�1����g�����p��^���vo�u�F���h��/4�IiߒW��e�}B��S/-����;4�Y��&�'���$��g���p�yH�����Ƶ�/^L�ʓ��L*�Л�����V����*v �����
p����ŧ�~�|����T�'���DSџH7��&δ��V��A��P.Y9�!�ެ><�;"
l�%�7(~���ׄt?Z��c�a2���K�tw�CD�v׈���5�5�5rz�U���J�0�ڌ��LZ����xL^�Sv?�$k��)aN7W]l����t���Q����c"E�ۻ{�GD�w���?H������OH����	�O���aFK�C"7����Nم#뚤%zC�%�x�F? +�'�MF{ l7�0�<�ݭ>>|��;Y��]t� ^#�F~�ܙ���و���k��������EN�.��k�(��n��v�V��>�&��I�Y��W�d����/d�&�'JK��J�
kM?|�[���'j r�����ñl��=��5�5�7�'���F����
]�h�l���ܸ_|�����E}�8I<�$�Dә�H��K#�mux#��p��Qk���n�CD�i�4��Dl'C8�����NB[�n�>G�0�
��J���!�VL?���><F/�]/�	]�?������i�cԒ�8B���=��������1{8��_o�	]��	]�	MGv���'��9�`���Ԛ(���bL�w;���v�u*^M�97�����%��tf'�[�ֵ�ar��[�EG3�CB����ǯ�k@>�na���PiB)�;���%��D��b�Z�xi�����p5��P�o6<��A�I^����B��Z���b�a�'e�bk1��2$k�y:�D��k�'�5�5�5r�4��s�\���R2Xi���G�7�xGD�8<�N��7o/H��������mN�����|�\7:j��g�Y��ݿ^9�ݻ���I���-��Z.OH��o9��{��w�8�zt;uFF�u;R��?^�bƻ3/���?ћ����B�iw(���Q�Y��L��w�Y<?,=$�	�%���k�E�P�44�Z�*�A��(N���.Pӛ_b��b�aglR..��5
k��uC�[�7g!������:h�G��Շ�.F������W$k��(n?�۶��_��      -   l   x���1�0k�/b[��_h,�&C���IC��vgv��/���;�c��g� t14���|m[��5�Դt�R�{�^��J)�M*���HG����o��ߙ�K�      1      x������ � �      A      x������ � �      .   �   x�eλn!��}
��m����:y�8����֮Hc�ݳ�&�]�7�џt�&%d)��x�B6��}E�h�#��Xz��[[ K��|��������K_p�v&�w"�Q �4�FX���+�#=���e��j*���n��R֕!锣W��=:f�s��	�|hK�W7��)����O{���O�����N˲�.u*����P�������]�     