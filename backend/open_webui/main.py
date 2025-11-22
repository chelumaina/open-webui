import asyncio
import inspect
import json
import logging
import mimetypes
import os
import shutil
import sys
import time
import random
import re
from uuid import uuid4


from contextlib import asynccontextmanager
from urllib.parse import urlencode, parse_qs, urlparse
from pydantic import BaseModel
from sqlalchemy import text

from typing import Optional
from aiocache import cached
import aiohttp
import anyio.to_thread
import requests
from redis import Redis


from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
    applications,
    BackgroundTasks,
)
from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from starlette_compress import CompressMiddleware

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response, StreamingResponse
from starlette.datastructures import Headers

from starsessions import (
    SessionMiddleware as StarSessionsMiddleware,
    SessionAutoloadMiddleware,
)
from starsessions.stores.redis import RedisStore

from open_webui.utils import logger
from open_webui.utils.audit import AuditLevel, AuditLoggingMiddleware
from open_webui.utils.logger import start_logger
from open_webui.models.payments import Payments
from open_webui.socket.main import (
    app as socket_app,
    periodic_usage_pool_cleanup,
    get_event_emitter,
    get_models_in_use,
    get_active_user_ids,
)
from open_webui.routers import (
    audio,
    images,
    ollama,
    openai,
    retrieval,
    pipelines,
    tasks,
    auths,
    channels,
    chats,
    notes,
    folders,
    configs,
    groups,
    files,
    functions,
    memories,
    models,
    knowledge,
    prompts,
    evaluations,
    tools,
    users,
    utils,
    scim,
    payments,
    features,
    user_guide,
   
)

from open_webui.routers.retrieval import (
    get_embedding_function,
    get_reranking_function,
    get_ef,
    get_rf,
)

from open_webui.internal.db import Session, engine

from open_webui.models.functions import Functions
from open_webui.models.models import Models
from open_webui.models.users import UserModel, Users
from open_webui.models.chats import Chats

from open_webui.config import (
    # Ollama
    ENABLE_OLLAMA_API,
    OLLAMA_BASE_URLS,
    OLLAMA_API_CONFIGS,
    # OpenAI
    ENABLE_OPENAI_API,
    OPENAI_API_BASE_URLS,
    OPENAI_API_KEYS,
    OPENAI_API_CONFIGS,
    # Direct Connections
    ENABLE_DIRECT_CONNECTIONS,
    # Model list
    ENABLE_BASE_MODELS_CACHE,
    # Thread pool size for FastAPI/AnyIO
    THREAD_POOL_SIZE,
    # Tool Server Configs
    TOOL_SERVER_CONNECTIONS,
    # Code Execution
    ENABLE_CODE_EXECUTION,
    CODE_EXECUTION_ENGINE,
    CODE_EXECUTION_JUPYTER_URL,
    CODE_EXECUTION_JUPYTER_AUTH,
    CODE_EXECUTION_JUPYTER_AUTH_TOKEN,
    CODE_EXECUTION_JUPYTER_AUTH_PASSWORD,
    CODE_EXECUTION_JUPYTER_TIMEOUT,
    ENABLE_CODE_INTERPRETER,
    CODE_INTERPRETER_ENGINE,
    CODE_INTERPRETER_PROMPT_TEMPLATE,
    CODE_INTERPRETER_JUPYTER_URL,
    CODE_INTERPRETER_JUPYTER_AUTH,
    CODE_INTERPRETER_JUPYTER_AUTH_TOKEN,
    CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD,
    CODE_INTERPRETER_JUPYTER_TIMEOUT,
    # Image
    AUTOMATIC1111_API_AUTH,
    AUTOMATIC1111_BASE_URL,
    AUTOMATIC1111_PARAMS,
    COMFYUI_BASE_URL,
    COMFYUI_API_KEY,
    COMFYUI_WORKFLOW,
    COMFYUI_WORKFLOW_NODES,
    ENABLE_IMAGE_GENERATION,
    ENABLE_IMAGE_PROMPT_GENERATION,
    IMAGE_GENERATION_ENGINE,
    IMAGE_GENERATION_MODEL,
    IMAGE_SIZE,
    IMAGE_STEPS,
    IMAGES_OPENAI_API_BASE_URL,
    IMAGES_OPENAI_API_VERSION,
    IMAGES_OPENAI_API_KEY,
    IMAGES_GEMINI_API_BASE_URL,
    IMAGES_GEMINI_API_KEY,
    IMAGES_GEMINI_ENDPOINT_METHOD,
    IMAGE_EDIT_ENGINE,
    IMAGE_EDIT_MODEL,
    IMAGE_EDIT_SIZE,
    IMAGES_EDIT_OPENAI_API_BASE_URL,
    IMAGES_EDIT_OPENAI_API_KEY,
    IMAGES_EDIT_OPENAI_API_VERSION,
    IMAGES_EDIT_GEMINI_API_BASE_URL,
    IMAGES_EDIT_GEMINI_API_KEY,
    IMAGES_EDIT_COMFYUI_BASE_URL,
    IMAGES_EDIT_COMFYUI_API_KEY,
    IMAGES_EDIT_COMFYUI_WORKFLOW,
    IMAGES_EDIT_COMFYUI_WORKFLOW_NODES,
    # Audio
    AUDIO_STT_ENGINE,
    AUDIO_STT_MODEL,
    AUDIO_STT_SUPPORTED_CONTENT_TYPES,
    AUDIO_STT_OPENAI_API_BASE_URL,
    AUDIO_STT_OPENAI_API_KEY,
    AUDIO_STT_AZURE_API_KEY,
    AUDIO_STT_AZURE_REGION,
    AUDIO_STT_AZURE_LOCALES,
    AUDIO_STT_AZURE_BASE_URL,
    AUDIO_STT_AZURE_MAX_SPEAKERS,
    AUDIO_STT_MISTRAL_API_KEY,
    AUDIO_STT_MISTRAL_API_BASE_URL,
    AUDIO_STT_MISTRAL_USE_CHAT_COMPLETIONS,
    AUDIO_TTS_ENGINE,
    AUDIO_TTS_MODEL,
    AUDIO_TTS_VOICE,
    AUDIO_TTS_OPENAI_API_BASE_URL,
    AUDIO_TTS_OPENAI_API_KEY,
    AUDIO_TTS_OPENAI_PARAMS,
    AUDIO_TTS_API_KEY,
    AUDIO_TTS_SPLIT_ON,
    AUDIO_TTS_AZURE_SPEECH_REGION,
    AUDIO_TTS_AZURE_SPEECH_BASE_URL,
    AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT,
    PLAYWRIGHT_WS_URL,
    PLAYWRIGHT_TIMEOUT,
    FIRECRAWL_API_BASE_URL,
    FIRECRAWL_API_KEY,
    WEB_LOADER_ENGINE,
    WEB_LOADER_CONCURRENT_REQUESTS,
    WHISPER_MODEL,
    WHISPER_VAD_FILTER,
    WHISPER_LANGUAGE,
    DEEPGRAM_API_KEY,
    WHISPER_MODEL_AUTO_UPDATE,
    WHISPER_MODEL_DIR,
    # Retrieval
    RAG_TEMPLATE,
    DEFAULT_RAG_TEMPLATE,
    RAG_FULL_CONTEXT,
    BYPASS_EMBEDDING_AND_RETRIEVAL,
    RAG_EMBEDDING_MODEL,
    RAG_EMBEDDING_MODEL_AUTO_UPDATE,
    RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE,
    RAG_RERANKING_ENGINE,
    RAG_RERANKING_MODEL,
    RAG_EXTERNAL_RERANKER_URL,
    RAG_EXTERNAL_RERANKER_API_KEY,
    RAG_RERANKING_MODEL_AUTO_UPDATE,
    RAG_RERANKING_MODEL_TRUST_REMOTE_CODE,
    RAG_EMBEDDING_ENGINE,
    RAG_EMBEDDING_BATCH_SIZE,
    RAG_TOP_K,
    RAG_TOP_K_RERANKER,
    RAG_RELEVANCE_THRESHOLD,
    RAG_HYBRID_BM25_WEIGHT,
    RAG_ALLOWED_FILE_EXTENSIONS,
    RAG_FILE_MAX_COUNT,
    RAG_FILE_MAX_SIZE,
    FILE_IMAGE_COMPRESSION_WIDTH,
    FILE_IMAGE_COMPRESSION_HEIGHT,
    RAG_OPENAI_API_BASE_URL,
    RAG_OPENAI_API_KEY,
    RAG_AZURE_OPENAI_BASE_URL,
    RAG_AZURE_OPENAI_API_KEY,
    RAG_AZURE_OPENAI_API_VERSION,
    RAG_OLLAMA_BASE_URL,
    RAG_OLLAMA_API_KEY,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CONTENT_EXTRACTION_ENGINE,
    DATALAB_MARKER_API_KEY,
    DATALAB_MARKER_API_BASE_URL,
    DATALAB_MARKER_ADDITIONAL_CONFIG,
    DATALAB_MARKER_SKIP_CACHE,
    DATALAB_MARKER_FORCE_OCR,
    DATALAB_MARKER_PAGINATE,
    DATALAB_MARKER_STRIP_EXISTING_OCR,
    DATALAB_MARKER_DISABLE_IMAGE_EXTRACTION,
    DATALAB_MARKER_FORMAT_LINES,
    DATALAB_MARKER_OUTPUT_FORMAT,
    MINERU_API_MODE,
    MINERU_API_URL,
    MINERU_API_KEY,
    MINERU_PARAMS,
    DATALAB_MARKER_USE_LLM,
    EXTERNAL_DOCUMENT_LOADER_URL,
    EXTERNAL_DOCUMENT_LOADER_API_KEY,
    TIKA_SERVER_URL,
    DOCLING_SERVER_URL,
    DOCLING_PARAMS,
    DOCLING_DO_OCR,
    DOCLING_FORCE_OCR,
    DOCLING_OCR_ENGINE,
    DOCLING_OCR_LANG,
    DOCLING_PDF_BACKEND,
    DOCLING_TABLE_MODE,
    DOCLING_PIPELINE,
    DOCLING_DO_PICTURE_DESCRIPTION,
    DOCLING_PICTURE_DESCRIPTION_MODE,
    DOCLING_PICTURE_DESCRIPTION_LOCAL,
    DOCLING_PICTURE_DESCRIPTION_API,
    DOCUMENT_INTELLIGENCE_ENDPOINT,
    DOCUMENT_INTELLIGENCE_KEY,
    MISTRAL_OCR_API_BASE_URL,
    MISTRAL_OCR_API_KEY,
    RAG_TEXT_SPLITTER,
    TIKTOKEN_ENCODING_NAME,
    PDF_EXTRACT_IMAGES,
    YOUTUBE_LOADER_LANGUAGE,
    YOUTUBE_LOADER_PROXY_URL,
    # Retrieval (Web Search)
    ENABLE_WEB_SEARCH,
    WEB_SEARCH_ENGINE,
    BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL,
    BYPASS_WEB_SEARCH_WEB_LOADER,
    WEB_SEARCH_RESULT_COUNT,
    WEB_SEARCH_CONCURRENT_REQUESTS,
    WEB_SEARCH_TRUST_ENV,
    WEB_SEARCH_DOMAIN_FILTER_LIST,
    OLLAMA_CLOUD_WEB_SEARCH_API_KEY,
    JINA_API_KEY,
    SEARCHAPI_API_KEY,
    SEARCHAPI_ENGINE,
    SERPAPI_API_KEY,
    SERPAPI_ENGINE,
    SEARXNG_QUERY_URL,
    YACY_QUERY_URL,
    YACY_USERNAME,
    YACY_PASSWORD,
    SERPER_API_KEY,
    SERPLY_API_KEY,
    SERPSTACK_API_KEY,
    SERPSTACK_HTTPS,
    TAVILY_API_KEY,
    TAVILY_EXTRACT_DEPTH,
    BING_SEARCH_V7_ENDPOINT,
    BING_SEARCH_V7_SUBSCRIPTION_KEY,
    BRAVE_SEARCH_API_KEY,
    EXA_API_KEY,
    PERPLEXITY_API_KEY,
    PERPLEXITY_MODEL,
    PERPLEXITY_SEARCH_CONTEXT_USAGE,
    SOUGOU_API_SID,
    SOUGOU_API_SK,
    KAGI_SEARCH_API_KEY,
    MOJEEK_SEARCH_API_KEY,
    BOCHA_SEARCH_API_KEY,
    GOOGLE_PSE_API_KEY,
    GOOGLE_PSE_ENGINE_ID,
    GOOGLE_DRIVE_CLIENT_ID,
    GOOGLE_DRIVE_API_KEY,
    ENABLE_ONEDRIVE_INTEGRATION,
    ONEDRIVE_CLIENT_ID_PERSONAL,
    ONEDRIVE_CLIENT_ID_BUSINESS,
    ONEDRIVE_SHAREPOINT_URL,
    ONEDRIVE_SHAREPOINT_TENANT_ID,
    ENABLE_ONEDRIVE_PERSONAL,
    ENABLE_ONEDRIVE_BUSINESS,
    ENABLE_RAG_HYBRID_SEARCH,
    ENABLE_RAG_LOCAL_WEB_FETCH,
    ENABLE_WEB_LOADER_SSL_VERIFICATION,
    ENABLE_GOOGLE_DRIVE_INTEGRATION,
    UPLOAD_DIR,
    EXTERNAL_WEB_SEARCH_URL,
    EXTERNAL_WEB_SEARCH_API_KEY,
    EXTERNAL_WEB_LOADER_URL,
    EXTERNAL_WEB_LOADER_API_KEY,
    # WebUI
    WEBUI_AUTH,
    WEBUI_NAME,
    WEBUI_BANNERS,
    WEBHOOK_URL,
    ADMIN_EMAIL,
    SHOW_ADMIN_DETAILS,
    JWT_EXPIRES_IN,
    ENABLE_SIGNUP,
    ENABLE_LOGIN_FORM,
    ENABLE_API_KEY,
    ENABLE_API_KEY_ENDPOINT_RESTRICTIONS,
    API_KEY_ALLOWED_ENDPOINTS,
    ENABLE_CHANNELS,
    ENABLE_NOTES,
    ENABLE_COMMUNITY_SHARING,
    ENABLE_MESSAGE_RATING,
    ENABLE_USER_WEBHOOKS,
    ENABLE_EVALUATION_ARENA_MODELS,
    BYPASS_ADMIN_ACCESS_CONTROL,
    USER_PERMISSIONS,
    DEFAULT_USER_ROLE,
    PENDING_USER_OVERLAY_CONTENT,
    PENDING_USER_OVERLAY_TITLE,
    DEFAULT_PROMPT_SUGGESTIONS,
    DEFAULT_MODELS,
    DEFAULT_ARENA_MODEL,
    MODEL_ORDER_LIST,
    EVALUATION_ARENA_MODELS,
    # WebUI (OAuth)
    ENABLE_OAUTH_ROLE_MANAGEMENT,
    OAUTH_ROLES_CLAIM,
    OAUTH_EMAIL_CLAIM,
    OAUTH_PICTURE_CLAIM,
    OAUTH_USERNAME_CLAIM,
    OAUTH_ALLOWED_ROLES,
    OAUTH_ADMIN_ROLES,
    # WebUI (LDAP)
    ENABLE_LDAP,
    LDAP_SERVER_LABEL,
    LDAP_SERVER_HOST,
    LDAP_SERVER_PORT,
    LDAP_ATTRIBUTE_FOR_MAIL,
    LDAP_ATTRIBUTE_FOR_USERNAME,
    LDAP_SEARCH_FILTERS,
    LDAP_SEARCH_BASE,
    LDAP_APP_DN,
    LDAP_APP_PASSWORD,
    LDAP_USE_TLS,
    LDAP_CA_CERT_FILE,
    LDAP_VALIDATE_CERT,
    LDAP_CIPHERS,
    # LDAP Group Management
    ENABLE_LDAP_GROUP_MANAGEMENT,
    ENABLE_LDAP_GROUP_CREATION,
    LDAP_ATTRIBUTE_FOR_GROUPS,
    # Misc
    ENV,
    CACHE_DIR,
    STATIC_DIR,
    FRONTEND_BUILD_DIR,
    CORS_ALLOW_ORIGIN,
    DEFAULT_LOCALE,
    OAUTH_PROVIDERS,
    WEBUI_URL,
    RESPONSE_WATERMARK,
    # Admin
    ENABLE_ADMIN_CHAT_ACCESS,
    BYPASS_ADMIN_ACCESS_CONTROL,
    ENABLE_ADMIN_EXPORT,
    # Tasks
    TASK_MODEL,
    TASK_MODEL_EXTERNAL,
    ENABLE_TAGS_GENERATION,
    ENABLE_TITLE_GENERATION,
    ENABLE_FOLLOW_UP_GENERATION,
    ENABLE_SEARCH_QUERY_GENERATION,
    ENABLE_RETRIEVAL_QUERY_GENERATION,
    ENABLE_AUTOCOMPLETE_GENERATION,
    TITLE_GENERATION_PROMPT_TEMPLATE,
    FOLLOW_UP_GENERATION_PROMPT_TEMPLATE,
    TAGS_GENERATION_PROMPT_TEMPLATE,
    IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE,
    TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE,
    QUERY_GENERATION_PROMPT_TEMPLATE,
    AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE,
    AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH,
    AppConfig,
    reset_config,
)
from open_webui.env import (
    LICENSE_KEY,
    AUDIT_EXCLUDED_PATHS,
    AUDIT_LOG_LEVEL,
    CHANGELOG,
    REDIS_URL,
    REDIS_CLUSTER,
    REDIS_KEY_PREFIX,
    REDIS_SENTINEL_HOSTS,
    REDIS_SENTINEL_PORT,
    GLOBAL_LOG_LEVEL,
    MAX_BODY_LOG_SIZE,
    SAFE_MODE,
    SRC_LOG_LEVELS,
    VERSION,
    INSTANCE_ID,
    WEBUI_BUILD_HASH,
    WEBUI_SECRET_KEY,
    WEBUI_SESSION_COOKIE_SAME_SITE,
    WEBUI_SESSION_COOKIE_SECURE,
    ENABLE_SIGNUP_PASSWORD_CONFIRMATION,
    WEBUI_AUTH_TRUSTED_EMAIL_HEADER,
    WEBUI_AUTH_TRUSTED_NAME_HEADER,
    WEBUI_AUTH_SIGNOUT_REDIRECT_URL,
    # SCIM
    SCIM_ENABLED,
    SCIM_TOKEN,
    ENABLE_COMPRESSION_MIDDLEWARE,
    ENABLE_WEBSOCKET_SUPPORT,
    BYPASS_MODEL_ACCESS_CONTROL,
    RESET_CONFIG_ON_START,
    ENABLE_VERSION_UPDATE_CHECK,
    ENABLE_OTEL,
    EXTERNAL_PWA_MANIFEST_URL,
    AIOHTTP_CLIENT_SESSION_SSL,
    ENABLE_STAR_SESSIONS_MIDDLEWARE,
)


from open_webui.utils.models import (
    get_all_models,
    get_all_base_models,
    check_model_access,
    get_filtered_models,
)
from open_webui.utils.chat import (
    generate_chat_completion as chat_completion_handler,
    chat_completed as chat_completed_handler,
    chat_action as chat_action_handler,
)
from open_webui.utils.embeddings import generate_embeddings
from open_webui.utils.middleware import process_chat_payload, process_chat_response
from open_webui.utils.access_control import has_access

from open_webui.utils.auth import (
    get_license_data,
    get_http_authorization_cred,
    decode_token,
    get_admin_user,
    get_verified_user,
)
from open_webui.utils.plugin import install_tool_and_function_dependencies
from open_webui.utils.oauth import (
    get_oauth_client_info_with_dynamic_client_registration,
    encrypt_data,
    decrypt_data,
    OAuthManager,
    OAuthClientManager,
    OAuthClientInformationFull,
)
from open_webui.utils.security_headers import SecurityHeadersMiddleware
from open_webui.utils.redis import get_redis_connection

from open_webui.tasks import (
    redis_task_command_listener,
    list_task_ids_by_item_id,
    create_task,
    stop_task,
    list_tasks,
)  # Import from tasks.py

from open_webui.utils.redis import get_sentinels_from_env


from open_webui.constants import ERROR_MESSAGES


if SAFE_MODE:
    print("SAFE MODE ENABLED")
    Functions.deactivate_all_functions()

logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOG_LEVEL)
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                if path.endswith(".js"):
                    # Return 404 for javascript files
                    raise ex
                else:
                    return await super().get_response("index.html", scope)
            else:
                raise ex


print(
    rf"""
 ██████╗ ██████╗ ███████╗███╗   ██╗    ██╗    ██╗███████╗██████╗ ██╗   ██╗██╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║    ██║    ██║██╔════╝██╔══██╗██║   ██║██║
██║   ██║██████╔╝█████╗  ██╔██╗ ██║    ██║ █╗ ██║█████╗  ██████╔╝██║   ██║██║
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║    ██║███╗██║██╔══╝  ██╔══██╗██║   ██║██║
╚██████╔╝██║     ███████╗██║ ╚████║    ╚███╔███╔╝███████╗██████╔╝╚██████╔╝██║
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝     ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝


v{VERSION} - building the best AI user interface.
{f"Commit: {WEBUI_BUILD_HASH}" if WEBUI_BUILD_HASH != "dev-build" else ""}
https://github.com/open-webui/open-webui
"""
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.instance_id = INSTANCE_ID
    start_logger()

    if RESET_CONFIG_ON_START:
        reset_config()

    if LICENSE_KEY:
        get_license_data(app, LICENSE_KEY)

    # This should be blocking (sync) so functions are not deactivated on first /get_models calls
    # when the first user lands on the / route.
    log.info("Installing external dependencies of functions and tools...")
    install_tool_and_function_dependencies()

    app.state.redis = get_redis_connection(
        redis_url=REDIS_URL,
        redis_sentinels=get_sentinels_from_env(
            REDIS_SENTINEL_HOSTS, REDIS_SENTINEL_PORT
        ),
        redis_cluster=REDIS_CLUSTER,
        async_mode=True,
    )

    if app.state.redis is not None:
        app.state.redis_task_command_listener = asyncio.create_task(
            redis_task_command_listener(app)
        )

    if THREAD_POOL_SIZE and THREAD_POOL_SIZE > 0:
        limiter = anyio.to_thread.current_default_thread_limiter()
        limiter.total_tokens = THREAD_POOL_SIZE

    asyncio.create_task(periodic_usage_pool_cleanup())

    if app.state.config.ENABLE_BASE_MODELS_CACHE:
        await get_all_models(
            Request(
                # Creating a mock request object to pass to get_all_models
                {
                    "type": "http",
                    "asgi.version": "3.0",
                    "asgi.spec_version": "2.0",
                    "method": "GET",
                    "path": "/internal",
                    "query_string": b"",
                    "headers": Headers({}).raw,
                    "client": ("127.0.0.1", 12345),
                    "server": ("127.0.0.1", 80),
                    "scheme": "http",
                    "app": app,
                }
            ),
            None,
        )

    yield

    if hasattr(app.state, "redis_task_command_listener"):
        app.state.redis_task_command_listener.cancel()


app = FastAPI(
    title="Lex Luma AI",
    docs_url="/docs" if ENV == "dev" else None,
    openapi_url="/openapi.json" if ENV == "dev" else None,
    redoc_url=None,
    lifespan=lifespan,
)

# For Lex Luma AI OIDC/OAuth2
oauth_manager = OAuthManager(app)
app.state.oauth_manager = oauth_manager

# For Integrations
oauth_client_manager = OAuthClientManager(app)
app.state.oauth_client_manager = oauth_client_manager

app.state.instance_id = None
app.state.config = AppConfig(
    redis_url=REDIS_URL,
    redis_sentinels=get_sentinels_from_env(REDIS_SENTINEL_HOSTS, REDIS_SENTINEL_PORT),
    redis_cluster=REDIS_CLUSTER,
    redis_key_prefix=REDIS_KEY_PREFIX,
)
app.state.redis = None

app.state.WEBUI_NAME = WEBUI_NAME
app.state.LICENSE_METADATA = None


########################################
#
# OPENTELEMETRY
#
########################################

if ENABLE_OTEL:
    from open_webui.utils.telemetry.setup import setup as setup_opentelemetry

    setup_opentelemetry(app=app, db_engine=engine)


########################################
#
# OLLAMA
#
########################################


app.state.config.ENABLE_OLLAMA_API = ENABLE_OLLAMA_API
app.state.config.OLLAMA_BASE_URLS = OLLAMA_BASE_URLS
app.state.config.OLLAMA_API_CONFIGS = OLLAMA_API_CONFIGS

app.state.OLLAMA_MODELS = {}

########################################
#
# OPENAI
#
########################################

app.state.config.ENABLE_OPENAI_API = ENABLE_OPENAI_API
app.state.config.OPENAI_API_BASE_URLS = OPENAI_API_BASE_URLS
app.state.config.OPENAI_API_KEYS = OPENAI_API_KEYS
app.state.config.OPENAI_API_CONFIGS = OPENAI_API_CONFIGS

app.state.OPENAI_MODELS = {}

########################################
#
# TOOL SERVERS
#
########################################

app.state.config.TOOL_SERVER_CONNECTIONS = TOOL_SERVER_CONNECTIONS
app.state.TOOL_SERVERS = []

########################################
#
# DIRECT CONNECTIONS
#
########################################

app.state.config.ENABLE_DIRECT_CONNECTIONS = ENABLE_DIRECT_CONNECTIONS

########################################
#
# SCIM
#
########################################

app.state.SCIM_ENABLED = SCIM_ENABLED
app.state.SCIM_TOKEN = SCIM_TOKEN

########################################
#
# MODELS
#
########################################

app.state.config.ENABLE_BASE_MODELS_CACHE = ENABLE_BASE_MODELS_CACHE
app.state.BASE_MODELS = []

########################################
#
# WEBUI
#
########################################

app.state.config.WEBUI_URL = WEBUI_URL
app.state.config.ENABLE_SIGNUP = ENABLE_SIGNUP
app.state.config.ENABLE_LOGIN_FORM = ENABLE_LOGIN_FORM

app.state.config.ENABLE_API_KEY = ENABLE_API_KEY
app.state.config.ENABLE_API_KEY_ENDPOINT_RESTRICTIONS = (
    ENABLE_API_KEY_ENDPOINT_RESTRICTIONS
)
app.state.config.API_KEY_ALLOWED_ENDPOINTS = API_KEY_ALLOWED_ENDPOINTS

app.state.config.JWT_EXPIRES_IN = JWT_EXPIRES_IN

app.state.config.SHOW_ADMIN_DETAILS = SHOW_ADMIN_DETAILS
app.state.config.ADMIN_EMAIL = ADMIN_EMAIL


app.state.config.DEFAULT_MODELS = DEFAULT_MODELS
app.state.config.DEFAULT_PROMPT_SUGGESTIONS = DEFAULT_PROMPT_SUGGESTIONS
app.state.config.DEFAULT_USER_ROLE = DEFAULT_USER_ROLE

app.state.config.PENDING_USER_OVERLAY_CONTENT = PENDING_USER_OVERLAY_CONTENT
app.state.config.PENDING_USER_OVERLAY_TITLE = PENDING_USER_OVERLAY_TITLE

app.state.config.RESPONSE_WATERMARK = RESPONSE_WATERMARK

app.state.config.USER_PERMISSIONS = USER_PERMISSIONS
app.state.config.WEBHOOK_URL = WEBHOOK_URL
app.state.config.BANNERS = WEBUI_BANNERS
app.state.config.MODEL_ORDER_LIST = MODEL_ORDER_LIST


app.state.config.ENABLE_CHANNELS = ENABLE_CHANNELS
app.state.config.ENABLE_NOTES = ENABLE_NOTES
app.state.config.ENABLE_COMMUNITY_SHARING = ENABLE_COMMUNITY_SHARING
app.state.config.ENABLE_MESSAGE_RATING = ENABLE_MESSAGE_RATING
app.state.config.ENABLE_USER_WEBHOOKS = ENABLE_USER_WEBHOOKS

app.state.config.ENABLE_EVALUATION_ARENA_MODELS = ENABLE_EVALUATION_ARENA_MODELS
app.state.config.EVALUATION_ARENA_MODELS = EVALUATION_ARENA_MODELS

app.state.config.OAUTH_USERNAME_CLAIM = OAUTH_USERNAME_CLAIM
app.state.config.OAUTH_PICTURE_CLAIM = OAUTH_PICTURE_CLAIM
app.state.config.OAUTH_EMAIL_CLAIM = OAUTH_EMAIL_CLAIM

app.state.config.ENABLE_OAUTH_ROLE_MANAGEMENT = ENABLE_OAUTH_ROLE_MANAGEMENT
app.state.config.OAUTH_ROLES_CLAIM = OAUTH_ROLES_CLAIM
app.state.config.OAUTH_ALLOWED_ROLES = OAUTH_ALLOWED_ROLES
app.state.config.OAUTH_ADMIN_ROLES = OAUTH_ADMIN_ROLES

app.state.config.ENABLE_LDAP = ENABLE_LDAP
app.state.config.LDAP_SERVER_LABEL = LDAP_SERVER_LABEL
app.state.config.LDAP_SERVER_HOST = LDAP_SERVER_HOST
app.state.config.LDAP_SERVER_PORT = LDAP_SERVER_PORT
app.state.config.LDAP_ATTRIBUTE_FOR_MAIL = LDAP_ATTRIBUTE_FOR_MAIL
app.state.config.LDAP_ATTRIBUTE_FOR_USERNAME = LDAP_ATTRIBUTE_FOR_USERNAME
app.state.config.LDAP_APP_DN = LDAP_APP_DN
app.state.config.LDAP_APP_PASSWORD = LDAP_APP_PASSWORD
app.state.config.LDAP_SEARCH_BASE = LDAP_SEARCH_BASE
app.state.config.LDAP_SEARCH_FILTERS = LDAP_SEARCH_FILTERS
app.state.config.LDAP_USE_TLS = LDAP_USE_TLS
app.state.config.LDAP_CA_CERT_FILE = LDAP_CA_CERT_FILE
app.state.config.LDAP_VALIDATE_CERT = LDAP_VALIDATE_CERT
app.state.config.LDAP_CIPHERS = LDAP_CIPHERS

# For LDAP Group Management
app.state.config.ENABLE_LDAP_GROUP_MANAGEMENT = ENABLE_LDAP_GROUP_MANAGEMENT
app.state.config.ENABLE_LDAP_GROUP_CREATION = ENABLE_LDAP_GROUP_CREATION
app.state.config.LDAP_ATTRIBUTE_FOR_GROUPS = LDAP_ATTRIBUTE_FOR_GROUPS


app.state.AUTH_TRUSTED_EMAIL_HEADER = WEBUI_AUTH_TRUSTED_EMAIL_HEADER
app.state.AUTH_TRUSTED_NAME_HEADER = WEBUI_AUTH_TRUSTED_NAME_HEADER
app.state.WEBUI_AUTH_SIGNOUT_REDIRECT_URL = WEBUI_AUTH_SIGNOUT_REDIRECT_URL
app.state.EXTERNAL_PWA_MANIFEST_URL = EXTERNAL_PWA_MANIFEST_URL

app.state.USER_COUNT = None

app.state.TOOLS = {}
app.state.TOOL_CONTENTS = {}

app.state.FUNCTIONS = {}
app.state.FUNCTION_CONTENTS = {}

########################################
#
# RETRIEVAL
#
########################################


app.state.config.TOP_K = RAG_TOP_K
app.state.config.TOP_K_RERANKER = RAG_TOP_K_RERANKER
app.state.config.RELEVANCE_THRESHOLD = RAG_RELEVANCE_THRESHOLD
app.state.config.HYBRID_BM25_WEIGHT = RAG_HYBRID_BM25_WEIGHT


app.state.config.ALLOWED_FILE_EXTENSIONS = RAG_ALLOWED_FILE_EXTENSIONS
app.state.config.FILE_MAX_SIZE = RAG_FILE_MAX_SIZE
app.state.config.FILE_MAX_COUNT = RAG_FILE_MAX_COUNT
app.state.config.FILE_IMAGE_COMPRESSION_WIDTH = FILE_IMAGE_COMPRESSION_WIDTH
app.state.config.FILE_IMAGE_COMPRESSION_HEIGHT = FILE_IMAGE_COMPRESSION_HEIGHT


app.state.config.RAG_FULL_CONTEXT = RAG_FULL_CONTEXT
app.state.config.BYPASS_EMBEDDING_AND_RETRIEVAL = BYPASS_EMBEDDING_AND_RETRIEVAL
app.state.config.ENABLE_RAG_HYBRID_SEARCH = ENABLE_RAG_HYBRID_SEARCH
app.state.config.ENABLE_WEB_LOADER_SSL_VERIFICATION = ENABLE_WEB_LOADER_SSL_VERIFICATION

app.state.config.CONTENT_EXTRACTION_ENGINE = CONTENT_EXTRACTION_ENGINE
app.state.config.DATALAB_MARKER_API_KEY = DATALAB_MARKER_API_KEY
app.state.config.DATALAB_MARKER_API_BASE_URL = DATALAB_MARKER_API_BASE_URL
app.state.config.DATALAB_MARKER_ADDITIONAL_CONFIG = DATALAB_MARKER_ADDITIONAL_CONFIG
app.state.config.DATALAB_MARKER_SKIP_CACHE = DATALAB_MARKER_SKIP_CACHE
app.state.config.DATALAB_MARKER_FORCE_OCR = DATALAB_MARKER_FORCE_OCR
app.state.config.DATALAB_MARKER_PAGINATE = DATALAB_MARKER_PAGINATE
app.state.config.DATALAB_MARKER_STRIP_EXISTING_OCR = DATALAB_MARKER_STRIP_EXISTING_OCR
app.state.config.DATALAB_MARKER_DISABLE_IMAGE_EXTRACTION = (
    DATALAB_MARKER_DISABLE_IMAGE_EXTRACTION
)
app.state.config.DATALAB_MARKER_FORMAT_LINES = DATALAB_MARKER_FORMAT_LINES
app.state.config.DATALAB_MARKER_USE_LLM = DATALAB_MARKER_USE_LLM
app.state.config.DATALAB_MARKER_OUTPUT_FORMAT = DATALAB_MARKER_OUTPUT_FORMAT
app.state.config.EXTERNAL_DOCUMENT_LOADER_URL = EXTERNAL_DOCUMENT_LOADER_URL
app.state.config.EXTERNAL_DOCUMENT_LOADER_API_KEY = EXTERNAL_DOCUMENT_LOADER_API_KEY
app.state.config.TIKA_SERVER_URL = TIKA_SERVER_URL
app.state.config.DOCLING_SERVER_URL = DOCLING_SERVER_URL
app.state.config.DOCLING_PARAMS = DOCLING_PARAMS
app.state.config.DOCLING_DO_OCR = DOCLING_DO_OCR
app.state.config.DOCLING_FORCE_OCR = DOCLING_FORCE_OCR
app.state.config.DOCLING_OCR_ENGINE = DOCLING_OCR_ENGINE
app.state.config.DOCLING_OCR_LANG = DOCLING_OCR_LANG
app.state.config.DOCLING_PDF_BACKEND = DOCLING_PDF_BACKEND
app.state.config.DOCLING_TABLE_MODE = DOCLING_TABLE_MODE
app.state.config.DOCLING_PIPELINE = DOCLING_PIPELINE
app.state.config.DOCLING_DO_PICTURE_DESCRIPTION = DOCLING_DO_PICTURE_DESCRIPTION
app.state.config.DOCLING_PICTURE_DESCRIPTION_MODE = DOCLING_PICTURE_DESCRIPTION_MODE
app.state.config.DOCLING_PICTURE_DESCRIPTION_LOCAL = DOCLING_PICTURE_DESCRIPTION_LOCAL
app.state.config.DOCLING_PICTURE_DESCRIPTION_API = DOCLING_PICTURE_DESCRIPTION_API
app.state.config.DOCUMENT_INTELLIGENCE_ENDPOINT = DOCUMENT_INTELLIGENCE_ENDPOINT
app.state.config.DOCUMENT_INTELLIGENCE_KEY = DOCUMENT_INTELLIGENCE_KEY
app.state.config.MISTRAL_OCR_API_BASE_URL = MISTRAL_OCR_API_BASE_URL
app.state.config.MISTRAL_OCR_API_KEY = MISTRAL_OCR_API_KEY
app.state.config.MINERU_API_MODE = MINERU_API_MODE
app.state.config.MINERU_API_URL = MINERU_API_URL
app.state.config.MINERU_API_KEY = MINERU_API_KEY
app.state.config.MINERU_PARAMS = MINERU_PARAMS

app.state.config.TEXT_SPLITTER = RAG_TEXT_SPLITTER
app.state.config.TIKTOKEN_ENCODING_NAME = TIKTOKEN_ENCODING_NAME

app.state.config.CHUNK_SIZE = CHUNK_SIZE
app.state.config.CHUNK_OVERLAP = CHUNK_OVERLAP

app.state.config.RAG_EMBEDDING_ENGINE = RAG_EMBEDDING_ENGINE
app.state.config.RAG_EMBEDDING_MODEL = RAG_EMBEDDING_MODEL
app.state.config.RAG_EMBEDDING_BATCH_SIZE = RAG_EMBEDDING_BATCH_SIZE

app.state.config.RAG_RERANKING_ENGINE = RAG_RERANKING_ENGINE
app.state.config.RAG_RERANKING_MODEL = RAG_RERANKING_MODEL
app.state.config.RAG_EXTERNAL_RERANKER_URL = RAG_EXTERNAL_RERANKER_URL
app.state.config.RAG_EXTERNAL_RERANKER_API_KEY = RAG_EXTERNAL_RERANKER_API_KEY

app.state.config.RAG_TEMPLATE = RAG_TEMPLATE

app.state.config.RAG_OPENAI_API_BASE_URL = RAG_OPENAI_API_BASE_URL
app.state.config.RAG_OPENAI_API_KEY = RAG_OPENAI_API_KEY

app.state.config.RAG_AZURE_OPENAI_BASE_URL = RAG_AZURE_OPENAI_BASE_URL
app.state.config.RAG_AZURE_OPENAI_API_KEY = RAG_AZURE_OPENAI_API_KEY
app.state.config.RAG_AZURE_OPENAI_API_VERSION = RAG_AZURE_OPENAI_API_VERSION

app.state.config.RAG_OLLAMA_BASE_URL = RAG_OLLAMA_BASE_URL
app.state.config.RAG_OLLAMA_API_KEY = RAG_OLLAMA_API_KEY

app.state.config.PDF_EXTRACT_IMAGES = PDF_EXTRACT_IMAGES

app.state.config.YOUTUBE_LOADER_LANGUAGE = YOUTUBE_LOADER_LANGUAGE
app.state.config.YOUTUBE_LOADER_PROXY_URL = YOUTUBE_LOADER_PROXY_URL


app.state.config.ENABLE_WEB_SEARCH = ENABLE_WEB_SEARCH
app.state.config.WEB_SEARCH_ENGINE = WEB_SEARCH_ENGINE
app.state.config.WEB_SEARCH_DOMAIN_FILTER_LIST = WEB_SEARCH_DOMAIN_FILTER_LIST
app.state.config.WEB_SEARCH_RESULT_COUNT = WEB_SEARCH_RESULT_COUNT
app.state.config.WEB_SEARCH_CONCURRENT_REQUESTS = WEB_SEARCH_CONCURRENT_REQUESTS

app.state.config.WEB_LOADER_ENGINE = WEB_LOADER_ENGINE
app.state.config.WEB_LOADER_CONCURRENT_REQUESTS = WEB_LOADER_CONCURRENT_REQUESTS

app.state.config.WEB_SEARCH_TRUST_ENV = WEB_SEARCH_TRUST_ENV
app.state.config.BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL = (
    BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL
)
app.state.config.BYPASS_WEB_SEARCH_WEB_LOADER = BYPASS_WEB_SEARCH_WEB_LOADER

app.state.config.ENABLE_GOOGLE_DRIVE_INTEGRATION = ENABLE_GOOGLE_DRIVE_INTEGRATION
app.state.config.ENABLE_ONEDRIVE_INTEGRATION = ENABLE_ONEDRIVE_INTEGRATION

app.state.config.OLLAMA_CLOUD_WEB_SEARCH_API_KEY = OLLAMA_CLOUD_WEB_SEARCH_API_KEY
app.state.config.SEARXNG_QUERY_URL = SEARXNG_QUERY_URL
app.state.config.YACY_QUERY_URL = YACY_QUERY_URL
app.state.config.YACY_USERNAME = YACY_USERNAME
app.state.config.YACY_PASSWORD = YACY_PASSWORD
app.state.config.GOOGLE_PSE_API_KEY = GOOGLE_PSE_API_KEY
app.state.config.GOOGLE_PSE_ENGINE_ID = GOOGLE_PSE_ENGINE_ID
app.state.config.BRAVE_SEARCH_API_KEY = BRAVE_SEARCH_API_KEY
app.state.config.KAGI_SEARCH_API_KEY = KAGI_SEARCH_API_KEY
app.state.config.MOJEEK_SEARCH_API_KEY = MOJEEK_SEARCH_API_KEY
app.state.config.BOCHA_SEARCH_API_KEY = BOCHA_SEARCH_API_KEY
app.state.config.SERPSTACK_API_KEY = SERPSTACK_API_KEY
app.state.config.SERPSTACK_HTTPS = SERPSTACK_HTTPS
app.state.config.SERPER_API_KEY = SERPER_API_KEY
app.state.config.SERPLY_API_KEY = SERPLY_API_KEY
app.state.config.TAVILY_API_KEY = TAVILY_API_KEY
app.state.config.SEARCHAPI_API_KEY = SEARCHAPI_API_KEY
app.state.config.SEARCHAPI_ENGINE = SEARCHAPI_ENGINE
app.state.config.SERPAPI_API_KEY = SERPAPI_API_KEY
app.state.config.SERPAPI_ENGINE = SERPAPI_ENGINE
app.state.config.JINA_API_KEY = JINA_API_KEY
app.state.config.BING_SEARCH_V7_ENDPOINT = BING_SEARCH_V7_ENDPOINT
app.state.config.BING_SEARCH_V7_SUBSCRIPTION_KEY = BING_SEARCH_V7_SUBSCRIPTION_KEY
app.state.config.EXA_API_KEY = EXA_API_KEY
app.state.config.PERPLEXITY_API_KEY = PERPLEXITY_API_KEY
app.state.config.PERPLEXITY_MODEL = PERPLEXITY_MODEL
app.state.config.PERPLEXITY_SEARCH_CONTEXT_USAGE = PERPLEXITY_SEARCH_CONTEXT_USAGE
app.state.config.SOUGOU_API_SID = SOUGOU_API_SID
app.state.config.SOUGOU_API_SK = SOUGOU_API_SK
app.state.config.EXTERNAL_WEB_SEARCH_URL = EXTERNAL_WEB_SEARCH_URL
app.state.config.EXTERNAL_WEB_SEARCH_API_KEY = EXTERNAL_WEB_SEARCH_API_KEY
app.state.config.EXTERNAL_WEB_LOADER_URL = EXTERNAL_WEB_LOADER_URL
app.state.config.EXTERNAL_WEB_LOADER_API_KEY = EXTERNAL_WEB_LOADER_API_KEY


app.state.config.PLAYWRIGHT_WS_URL = PLAYWRIGHT_WS_URL
app.state.config.PLAYWRIGHT_TIMEOUT = PLAYWRIGHT_TIMEOUT
app.state.config.FIRECRAWL_API_BASE_URL = FIRECRAWL_API_BASE_URL
app.state.config.FIRECRAWL_API_KEY = FIRECRAWL_API_KEY
app.state.config.TAVILY_EXTRACT_DEPTH = TAVILY_EXTRACT_DEPTH

app.state.EMBEDDING_FUNCTION = None
app.state.RERANKING_FUNCTION = None
app.state.ef = None
app.state.rf = None

app.state.YOUTUBE_LOADER_TRANSLATION = None


try:
    app.state.ef = get_ef(
        app.state.config.RAG_EMBEDDING_ENGINE,
        app.state.config.RAG_EMBEDDING_MODEL,
        RAG_EMBEDDING_MODEL_AUTO_UPDATE,
    )
    if (
        app.state.config.ENABLE_RAG_HYBRID_SEARCH
        and not app.state.config.BYPASS_EMBEDDING_AND_RETRIEVAL
    ):
        app.state.rf = get_rf(
            app.state.config.RAG_RERANKING_ENGINE,
            app.state.config.RAG_RERANKING_MODEL,
            app.state.config.RAG_EXTERNAL_RERANKER_URL,
            app.state.config.RAG_EXTERNAL_RERANKER_API_KEY,
            RAG_RERANKING_MODEL_AUTO_UPDATE,
        )
    else:
        app.state.rf = None
except Exception as e:
    log.error(f"Error updating models: {e}")
    pass


app.state.EMBEDDING_FUNCTION = get_embedding_function(
    app.state.config.RAG_EMBEDDING_ENGINE,
    app.state.config.RAG_EMBEDDING_MODEL,
    embedding_function=app.state.ef,
    url=(
        app.state.config.RAG_OPENAI_API_BASE_URL
        if app.state.config.RAG_EMBEDDING_ENGINE == "openai"
        else (
            app.state.config.RAG_OLLAMA_BASE_URL
            if app.state.config.RAG_EMBEDDING_ENGINE == "ollama"
            else app.state.config.RAG_AZURE_OPENAI_BASE_URL
        )
    ),
    key=(
        app.state.config.RAG_OPENAI_API_KEY
        if app.state.config.RAG_EMBEDDING_ENGINE == "openai"
        else (
            app.state.config.RAG_OLLAMA_API_KEY
            if app.state.config.RAG_EMBEDDING_ENGINE == "ollama"
            else app.state.config.RAG_AZURE_OPENAI_API_KEY
        )
    ),
    embedding_batch_size=app.state.config.RAG_EMBEDDING_BATCH_SIZE,
    azure_api_version=(
        app.state.config.RAG_AZURE_OPENAI_API_VERSION
        if app.state.config.RAG_EMBEDDING_ENGINE == "azure_openai"
        else None
    ),
)

app.state.RERANKING_FUNCTION = get_reranking_function(
    app.state.config.RAG_RERANKING_ENGINE,
    app.state.config.RAG_RERANKING_MODEL,
    reranking_function=app.state.rf,
)

########################################
#
# CODE EXECUTION
#
########################################

app.state.config.ENABLE_CODE_EXECUTION = ENABLE_CODE_EXECUTION
app.state.config.CODE_EXECUTION_ENGINE = CODE_EXECUTION_ENGINE
app.state.config.CODE_EXECUTION_JUPYTER_URL = CODE_EXECUTION_JUPYTER_URL
app.state.config.CODE_EXECUTION_JUPYTER_AUTH = CODE_EXECUTION_JUPYTER_AUTH
app.state.config.CODE_EXECUTION_JUPYTER_AUTH_TOKEN = CODE_EXECUTION_JUPYTER_AUTH_TOKEN
app.state.config.CODE_EXECUTION_JUPYTER_AUTH_PASSWORD = (
    CODE_EXECUTION_JUPYTER_AUTH_PASSWORD
)
app.state.config.CODE_EXECUTION_JUPYTER_TIMEOUT = CODE_EXECUTION_JUPYTER_TIMEOUT

app.state.config.ENABLE_CODE_INTERPRETER = ENABLE_CODE_INTERPRETER
app.state.config.CODE_INTERPRETER_ENGINE = CODE_INTERPRETER_ENGINE
app.state.config.CODE_INTERPRETER_PROMPT_TEMPLATE = CODE_INTERPRETER_PROMPT_TEMPLATE

app.state.config.CODE_INTERPRETER_JUPYTER_URL = CODE_INTERPRETER_JUPYTER_URL
app.state.config.CODE_INTERPRETER_JUPYTER_AUTH = CODE_INTERPRETER_JUPYTER_AUTH
app.state.config.CODE_INTERPRETER_JUPYTER_AUTH_TOKEN = (
    CODE_INTERPRETER_JUPYTER_AUTH_TOKEN
)
app.state.config.CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD = (
    CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD
)
app.state.config.CODE_INTERPRETER_JUPYTER_TIMEOUT = CODE_INTERPRETER_JUPYTER_TIMEOUT

########################################
#
# IMAGES
#
########################################

app.state.config.IMAGE_GENERATION_ENGINE = IMAGE_GENERATION_ENGINE
app.state.config.ENABLE_IMAGE_GENERATION = ENABLE_IMAGE_GENERATION
app.state.config.ENABLE_IMAGE_PROMPT_GENERATION = ENABLE_IMAGE_PROMPT_GENERATION

app.state.config.IMAGE_GENERATION_MODEL = IMAGE_GENERATION_MODEL
app.state.config.IMAGE_SIZE = IMAGE_SIZE
app.state.config.IMAGE_STEPS = IMAGE_STEPS

app.state.config.IMAGES_OPENAI_API_BASE_URL = IMAGES_OPENAI_API_BASE_URL
app.state.config.IMAGES_OPENAI_API_VERSION = IMAGES_OPENAI_API_VERSION
app.state.config.IMAGES_OPENAI_API_KEY = IMAGES_OPENAI_API_KEY

app.state.config.IMAGES_GEMINI_API_BASE_URL = IMAGES_GEMINI_API_BASE_URL
app.state.config.IMAGES_GEMINI_API_KEY = IMAGES_GEMINI_API_KEY
app.state.config.IMAGES_GEMINI_ENDPOINT_METHOD = IMAGES_GEMINI_ENDPOINT_METHOD

app.state.config.AUTOMATIC1111_BASE_URL = AUTOMATIC1111_BASE_URL
app.state.config.AUTOMATIC1111_API_AUTH = AUTOMATIC1111_API_AUTH
app.state.config.AUTOMATIC1111_PARAMS = AUTOMATIC1111_PARAMS

app.state.config.COMFYUI_BASE_URL = COMFYUI_BASE_URL
app.state.config.COMFYUI_API_KEY = COMFYUI_API_KEY
app.state.config.COMFYUI_WORKFLOW = COMFYUI_WORKFLOW
app.state.config.COMFYUI_WORKFLOW_NODES = COMFYUI_WORKFLOW_NODES


app.state.config.IMAGE_EDIT_ENGINE = IMAGE_EDIT_ENGINE
app.state.config.IMAGE_EDIT_MODEL = IMAGE_EDIT_MODEL
app.state.config.IMAGE_EDIT_SIZE = IMAGE_EDIT_SIZE
app.state.config.IMAGES_EDIT_OPENAI_API_BASE_URL = IMAGES_EDIT_OPENAI_API_BASE_URL
app.state.config.IMAGES_EDIT_OPENAI_API_KEY = IMAGES_EDIT_OPENAI_API_KEY
app.state.config.IMAGES_EDIT_OPENAI_API_VERSION = IMAGES_EDIT_OPENAI_API_VERSION
app.state.config.IMAGES_EDIT_GEMINI_API_BASE_URL = IMAGES_EDIT_GEMINI_API_BASE_URL
app.state.config.IMAGES_EDIT_GEMINI_API_KEY = IMAGES_EDIT_GEMINI_API_KEY
app.state.config.IMAGES_EDIT_COMFYUI_BASE_URL = IMAGES_EDIT_COMFYUI_BASE_URL
app.state.config.IMAGES_EDIT_COMFYUI_API_KEY = IMAGES_EDIT_COMFYUI_API_KEY
app.state.config.IMAGES_EDIT_COMFYUI_WORKFLOW = IMAGES_EDIT_COMFYUI_WORKFLOW
app.state.config.IMAGES_EDIT_COMFYUI_WORKFLOW_NODES = IMAGES_EDIT_COMFYUI_WORKFLOW_NODES


########################################
#
# AUDIO
#
########################################

app.state.config.STT_ENGINE = AUDIO_STT_ENGINE
app.state.config.STT_MODEL = AUDIO_STT_MODEL
app.state.config.STT_SUPPORTED_CONTENT_TYPES = AUDIO_STT_SUPPORTED_CONTENT_TYPES

app.state.config.STT_OPENAI_API_BASE_URL = AUDIO_STT_OPENAI_API_BASE_URL
app.state.config.STT_OPENAI_API_KEY = AUDIO_STT_OPENAI_API_KEY

app.state.config.WHISPER_MODEL = WHISPER_MODEL
app.state.config.WHISPER_VAD_FILTER = WHISPER_VAD_FILTER
app.state.config.DEEPGRAM_API_KEY = DEEPGRAM_API_KEY

app.state.config.AUDIO_STT_AZURE_API_KEY = AUDIO_STT_AZURE_API_KEY
app.state.config.AUDIO_STT_AZURE_REGION = AUDIO_STT_AZURE_REGION
app.state.config.AUDIO_STT_AZURE_LOCALES = AUDIO_STT_AZURE_LOCALES
app.state.config.AUDIO_STT_AZURE_BASE_URL = AUDIO_STT_AZURE_BASE_URL
app.state.config.AUDIO_STT_AZURE_MAX_SPEAKERS = AUDIO_STT_AZURE_MAX_SPEAKERS

app.state.config.AUDIO_STT_MISTRAL_API_KEY = AUDIO_STT_MISTRAL_API_KEY
app.state.config.AUDIO_STT_MISTRAL_API_BASE_URL = AUDIO_STT_MISTRAL_API_BASE_URL
app.state.config.AUDIO_STT_MISTRAL_USE_CHAT_COMPLETIONS = (
    AUDIO_STT_MISTRAL_USE_CHAT_COMPLETIONS
)

app.state.config.TTS_ENGINE = AUDIO_TTS_ENGINE

app.state.config.TTS_MODEL = AUDIO_TTS_MODEL
app.state.config.TTS_VOICE = AUDIO_TTS_VOICE

app.state.config.TTS_OPENAI_API_BASE_URL = AUDIO_TTS_OPENAI_API_BASE_URL
app.state.config.TTS_OPENAI_API_KEY = AUDIO_TTS_OPENAI_API_KEY
app.state.config.TTS_OPENAI_PARAMS = AUDIO_TTS_OPENAI_PARAMS

app.state.config.TTS_API_KEY = AUDIO_TTS_API_KEY
app.state.config.TTS_SPLIT_ON = AUDIO_TTS_SPLIT_ON


app.state.config.TTS_AZURE_SPEECH_REGION = AUDIO_TTS_AZURE_SPEECH_REGION
app.state.config.TTS_AZURE_SPEECH_BASE_URL = AUDIO_TTS_AZURE_SPEECH_BASE_URL
app.state.config.TTS_AZURE_SPEECH_OUTPUT_FORMAT = AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT


app.state.faster_whisper_model = None
app.state.speech_synthesiser = None
app.state.speech_speaker_embeddings_dataset = None


########################################
#
# TASKS
#
########################################


app.state.config.TASK_MODEL = TASK_MODEL
app.state.config.TASK_MODEL_EXTERNAL = TASK_MODEL_EXTERNAL


app.state.config.ENABLE_SEARCH_QUERY_GENERATION = ENABLE_SEARCH_QUERY_GENERATION
app.state.config.ENABLE_RETRIEVAL_QUERY_GENERATION = ENABLE_RETRIEVAL_QUERY_GENERATION
app.state.config.ENABLE_AUTOCOMPLETE_GENERATION = ENABLE_AUTOCOMPLETE_GENERATION
app.state.config.ENABLE_TAGS_GENERATION = ENABLE_TAGS_GENERATION
app.state.config.ENABLE_TITLE_GENERATION = ENABLE_TITLE_GENERATION
app.state.config.ENABLE_FOLLOW_UP_GENERATION = ENABLE_FOLLOW_UP_GENERATION


app.state.config.TITLE_GENERATION_PROMPT_TEMPLATE = TITLE_GENERATION_PROMPT_TEMPLATE
app.state.config.TAGS_GENERATION_PROMPT_TEMPLATE = TAGS_GENERATION_PROMPT_TEMPLATE
app.state.config.IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE = (
    IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE
)
app.state.config.FOLLOW_UP_GENERATION_PROMPT_TEMPLATE = (
    FOLLOW_UP_GENERATION_PROMPT_TEMPLATE
)

app.state.config.TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE = (
    TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE
)
app.state.config.QUERY_GENERATION_PROMPT_TEMPLATE = QUERY_GENERATION_PROMPT_TEMPLATE
app.state.config.AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE = (
    AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE
)
app.state.config.AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH = (
    AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH
)


########################################
#
# WEBUI
#
########################################

app.state.MODELS = {}


class RedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the request is a GET request
        if request.method == "GET":
            path = request.url.path
            query_params = dict(parse_qs(urlparse(str(request.url)).query))

            redirect_params = {}

            # Check for the specific watch path and the presence of 'v' parameter
            if path.endswith("/watch") and "v" in query_params:
                # Extract the first 'v' parameter
                youtube_video_id = query_params["v"][0]
                redirect_params["youtube"] = youtube_video_id

            if "shared" in query_params and len(query_params["shared"]) > 0:
                # PWA share_target support

                text = query_params["shared"][0]
                if text:
                    urls = re.match(r"https://\S+", text)
                    if urls:
                        from open_webui.retrieval.loaders.youtube import _parse_video_id

                        if youtube_video_id := _parse_video_id(urls[0]):
                            redirect_params["youtube"] = youtube_video_id
                        else:
                            redirect_params["load-url"] = urls[0]
                    else:
                        redirect_params["q"] = text

            if redirect_params:
                redirect_url = f"/?{urlencode(redirect_params)}"
                return RedirectResponse(url=redirect_url)

        # Proceed with the normal flow of other requests
        response = await call_next(request)
        return response


# Add the middleware to the app
if ENABLE_COMPRESSION_MIDDLEWARE:
    app.add_middleware(CompressMiddleware)

app.add_middleware(RedirectMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.middleware("http")
async def commit_session_after_request(request: Request, call_next):
    response = await call_next(request)
    # log.debug("Commit session after request")
    Session.commit()
    return response


@app.middleware("http")
async def check_url(request: Request, call_next):
    start_time = int(time.time())
    request.state.token = get_http_authorization_cred(
        request.headers.get("Authorization")
    )

    request.state.enable_api_key = app.state.config.ENABLE_API_KEY
    response = await call_next(request)
    process_time = int(time.time()) - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def inspect_websocket(request: Request, call_next):
    if (
        "/ws/socket.io" in request.url.path
        and request.query_params.get("transport") == "websocket"
    ):
        upgrade = (request.headers.get("Upgrade") or "").lower()
        connection = (request.headers.get("Connection") or "").lower().split(",")
        # Check that there's the correct headers for an upgrade, else reject the connection
        # This is to work around this upstream issue: https://github.com/miguelgrinberg/python-engineio/issues/367
        if upgrade != "websocket" or "upgrade" not in connection:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid WebSocket upgrade request"},
            )
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/ws", socket_app)


app.include_router(ollama.router, prefix="/ollama", tags=["ollama"])
app.include_router(openai.router, prefix="/openai", tags=["openai"])


app.include_router(pipelines.router, prefix="/api/v1/pipelines", tags=["pipelines"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(images.router, prefix="/api/v1/images", tags=["images"])

app.include_router(audio.router, prefix="/api/v1/audio", tags=["audio"])
app.include_router(retrieval.router, prefix="/api/v1/retrieval", tags=["retrieval"])

app.include_router(configs.router, prefix="/api/v1/configs", tags=["configs"])

app.include_router(auths.router, prefix="/api/v1/auths", tags=["auths"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


app.include_router(channels.router, prefix="/api/v1/channels", tags=["channels"])
app.include_router(chats.router, prefix="/api/v1/chats", tags=["chats"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])
app.include_router(prompts.router, prefix="/api/v1/prompts", tags=["prompts"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])

app.include_router(memories.router, prefix="/api/v1/memories", tags=["memories"])
app.include_router(folders.router, prefix="/api/v1/folders", tags=["folders"])
app.include_router(groups.router, prefix="/api/v1/groups", tags=["groups"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(functions.router, prefix="/api/v1/functions", tags=["functions"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(features.router, prefix="/api/v1/features", tags=["features"])
app.include_router(user_guide.router, prefix="/api/v1/user_guide", tags=["user_guide"])

app.include_router(
    evaluations.router, prefix="/api/v1/evaluations", tags=["evaluations"]
)
app.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])

# SCIM 2.0 API for identity management
if SCIM_ENABLED:
    app.include_router(scim.router, prefix="/api/v1/scim/v2", tags=["scim"])


try:
    audit_level = AuditLevel(AUDIT_LOG_LEVEL)
except ValueError as e:
    logger.error(f"Invalid audit level: {AUDIT_LOG_LEVEL}. Error: {e}")
    audit_level = AuditLevel.NONE

if audit_level != AuditLevel.NONE:
    app.add_middleware(
        AuditLoggingMiddleware,
        audit_level=audit_level,
        excluded_paths=AUDIT_EXCLUDED_PATHS,
        max_body_size=MAX_BODY_LOG_SIZE,
    )
##################################
#
# Chat Endpoints
#
##################################


@app.get("/api/models")
@app.get("/api/v1/models")  # Experimental: Compatibility with OpenAI API
async def get_models(
    request: Request, refresh: bool = False, user=Depends(get_verified_user)
):
    all_models = await get_all_models(request, refresh=refresh, user=user)

    models = []
    for model in all_models:
        # Filter out filter pipelines
        if "pipeline" in model and model["pipeline"].get("type", None) == "filter":
            continue

        try:
            model_tags = [
                tag.get("name")
                for tag in model.get("info", {}).get("meta", {}).get("tags", [])
            ]
            tags = [tag.get("name") for tag in model.get("tags", [])]

            tags = list(set(model_tags + tags))
            model["tags"] = [{"name": tag} for tag in tags]
        except Exception as e:
            log.debug(f"Error processing model tags: {e}")
            model["tags"] = []
            pass

        models.append(model)

    model_order_list = request.app.state.config.MODEL_ORDER_LIST
    if model_order_list:
        model_order_dict = {model_id: i for i, model_id in enumerate(model_order_list)}
        # Sort models by order list priority, with fallback for those not in the list
        models.sort(
            key=lambda model: (
                model_order_dict.get(model.get("id", ""), float("inf")),
                (model.get("name", "") or ""),
            )
        )

    models = get_filtered_models(models, user)

    log.debug(
        f"/api/models returned filtered models accessible to the user: {json.dumps([model.get('id') for model in models])}"
    )
    return {"data": models}


@app.get("/api/models/base")
async def get_base_models(request: Request, user=Depends(get_admin_user)):
    models = await get_all_base_models(request, user=user)
    return {"data": models}


##################################
# Embeddings
##################################


@app.post("/api/embeddings")
@app.post("/api/v1/embeddings")  # Experimental: Compatibility with OpenAI API
async def embeddings(
    request: Request, form_data: dict, user=Depends(get_verified_user)
):
    """
    OpenAI-compatible embeddings endpoint.

    This handler:
      - Performs user/model checks and dispatches to the correct backend.
      - Supports OpenAI, Ollama, arena models, pipelines, and any compatible provider.

    Args:
        request (Request): Request context.
        form_data (dict): OpenAI-like payload (e.g., {"model": "...", "input": [...]})
        user (UserModel): Authenticated user.

    Returns:
        dict: OpenAI-compatible embeddings response.
    """
    # Make sure models are loaded in app state
    if not request.app.state.MODELS:
        await get_all_models(request, user=user)
    # Use generic dispatcher in utils.embeddings
    return await generate_embeddings(request, form_data, user)


@app.post("/api/chat/completions")
@app.post("/api/v1/chat/completions")  # Experimental: Compatibility with OpenAI API
async def chat_completion(
    request: Request,
    form_data: dict,
    user=Depends(get_verified_user),
):
    if not request.app.state.MODELS:
        await get_all_models(request, user=user)

    model_id = form_data.get("model", None)
    model_item = form_data.pop("model_item", {})
    tasks = form_data.pop("background_tasks", None)

    metadata = {}
    try:
        if not model_item.get("direct", False):
            if model_id not in request.app.state.MODELS:
                raise Exception("Model not found")

            model = request.app.state.MODELS[model_id]
            model_info = Models.get_model_by_id(model_id)

            # Check if user has access to the model
            if not BYPASS_MODEL_ACCESS_CONTROL and (
                user.role != "admin" or not BYPASS_ADMIN_ACCESS_CONTROL
            ):
                try:
                    check_model_access(user, model)
                except Exception as e:
                    raise e
        else:
            model = model_item
            model_info = None

            request.state.direct = True
            request.state.model = model

        model_info_params = (
            model_info.params.model_dump() if model_info and model_info.params else {}
        )

        # Chat Params
        stream_delta_chunk_size = form_data.get("params", {}).get(
            "stream_delta_chunk_size"
        )
        reasoning_tags = form_data.get("params", {}).get("reasoning_tags")

        # Model Params
        if model_info_params.get("stream_delta_chunk_size"):
            stream_delta_chunk_size = model_info_params.get("stream_delta_chunk_size")

        if model_info_params.get("reasoning_tags") is not None:
            reasoning_tags = model_info_params.get("reasoning_tags")

        metadata = {
            "user_id": user.id,
            "chat_id": form_data.pop("chat_id", None),
            "message_id": form_data.pop("id", None),
            "session_id": form_data.pop("session_id", None),
            "filter_ids": form_data.pop("filter_ids", []),
            "tool_ids": form_data.get("tool_ids", None),
            "tool_servers": form_data.pop("tool_servers", None),
            "files": form_data.get("files", None),
            "features": form_data.get("features", {}),
            "variables": form_data.get("variables", {}),
            "model": model,
            "direct": model_item.get("direct", False),
            "params": {
                "stream_delta_chunk_size": stream_delta_chunk_size,
                "reasoning_tags": reasoning_tags,
                "function_calling": (
                    "native"
                    if (
                        form_data.get("params", {}).get("function_calling") == "native"
                        or model_info_params.get("function_calling") == "native"
                    )
                    else "default"
                ),
            },
        }

        if metadata.get("chat_id") and (user and user.role != "admin"):
            if not metadata["chat_id"].startswith("local:"):
                chat = Chats.get_chat_by_id_and_user_id(metadata["chat_id"], user.id)
                if chat is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=ERROR_MESSAGES.DEFAULT(),
                    )

        request.state.metadata = metadata
        form_data["metadata"] = metadata

    except Exception as e:
        log.debug(f"Error processing chat metadata: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    async def process_chat(request, form_data, user, metadata, model):
        try:
            form_data, metadata, events = await process_chat_payload(
                request, form_data, user, metadata, model
            )

            response = await chat_completion_handler(request, form_data, user)
            if metadata.get("chat_id") and metadata.get("message_id"):
                try:
                    if not metadata["chat_id"].startswith("local:"):
                        Chats.upsert_message_to_chat_by_id_and_message_id(
                            metadata["chat_id"],
                            metadata["message_id"],
                            {
                                "model": model_id,
                            },
                        )
                except:
                    pass

            return await process_chat_response(
                request, response, form_data, user, metadata, model, events, tasks
            )
        except asyncio.CancelledError:
            log.info("Chat processing was cancelled")
            try:
                event_emitter = get_event_emitter(metadata)
                await asyncio.shield(
                    event_emitter(
                        {"type": "chat:tasks:cancel"},
                    )
                )
            except Exception as e:
                pass
            finally:
                raise  # re-raise to ensure proper task cancellation handling
        except Exception as e:
            log.debug(f"Error processing chat payload: {e}")
            if metadata.get("chat_id") and metadata.get("message_id"):
                # Update the chat message with the error
                try:
                    if not metadata["chat_id"].startswith("local:"):
                        Chats.upsert_message_to_chat_by_id_and_message_id(
                            metadata["chat_id"],
                            metadata["message_id"],
                            {
                                "error": {"content": str(e)},
                            },
                        )

                    event_emitter = get_event_emitter(metadata)
                    await event_emitter(
                        {
                            "type": "chat:message:error",
                            "data": {"error": {"content": str(e)}},
                        }
                    )
                    await event_emitter(
                        {"type": "chat:tasks:cancel"},
                    )

                except:
                    pass
        finally:
            try:
                if mcp_clients := metadata.get("mcp_clients"):
                    for client in reversed(mcp_clients.values()):
                        await client.disconnect()
            except Exception as e:
                log.debug(f"Error cleaning up: {e}")
                pass

    if (
        metadata.get("session_id")
        and metadata.get("chat_id")
        and metadata.get("message_id")
    ):
        # Asynchronous Chat Processing
        task_id, _ = await create_task(
            request.app.state.redis,
            process_chat(request, form_data, user, metadata, model),
            id=metadata["chat_id"],
        )
        return {"status": True, "task_id": task_id}
    else:
        return await process_chat(request, form_data, user, metadata, model)


# Alias for chat_completion (Legacy)
generate_chat_completions = chat_completion
generate_chat_completion = chat_completion


@app.post("/api/chat/completed")
async def chat_completed(
    request: Request, form_data: dict, user=Depends(get_verified_user)
):
    try:
        model_item = form_data.pop("model_item", {})

        if model_item.get("direct", False):
            request.state.direct = True
            request.state.model = model_item

        return await chat_completed_handler(request, form_data, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.post("/api/chat/actions/{action_id}")
async def chat_action(
    request: Request, action_id: str, form_data: dict, user=Depends(get_verified_user)
):
    try:
        model_item = form_data.pop("model_item", {})

        if model_item.get("direct", False):
            request.state.direct = True
            request.state.model = model_item

        return await chat_action_handler(request, action_id, form_data, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.post("/api/tasks/stop/{task_id}")
async def stop_task_endpoint(
    request: Request, task_id: str, user=Depends(get_verified_user)
):
    try:
        result = await stop_task(request.app.state.redis, task_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/api/tasks")
async def list_tasks_endpoint(request: Request, user=Depends(get_verified_user)):
    return {"tasks": await list_tasks(request.app.state.redis)}


@app.get("/api/tasks/chat/{chat_id}")
async def list_tasks_by_chat_id_endpoint(
    request: Request, chat_id: str, user=Depends(get_verified_user)
):
    chat = Chats.get_chat_by_id(chat_id)
    if chat is None or chat.user_id != user.id:
        return {"task_ids": []}

    task_ids = await list_task_ids_by_item_id(request.app.state.redis, chat_id)

    log.debug(f"Task IDs for chat {chat_id}: {task_ids}")
    return {"task_ids": task_ids}


##################################
#
# Config Endpoints
#
##################################


@app.get("/api/config")
async def get_app_config(request: Request):
    user = None
    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header:
        cred = get_http_authorization_cred(auth_header)
        if cred:
            token = cred.credentials

    if not token and "token" in request.cookies:
        token = request.cookies.get("token")

    if token:
        try:
            data = decode_token(token)
        except Exception as e:
            log.debug(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        if data is not None and "id" in data:
            user = Users.get_user_by_id(data["id"])

    user_count = Users.get_num_users()
    onboarding = True
    subscription = {}
    if user is None:
        onboarding = user_count == 0
    else:
        subscription = Payments.get_user_subscription(user.id)

    return {
        **({"onboarding": True} if onboarding else {}),
        "status": True,
        "name": app.state.WEBUI_NAME,
        "version": VERSION,
        "default_locale": str(DEFAULT_LOCALE),
        "plan_id": subscription.plan_id if subscription else None,
        "oauth": {
            "providers": {
                name: config.get("name", name)
                for name, config in OAUTH_PROVIDERS.items()
            }
        },
        "features": {
            "auth": WEBUI_AUTH,
            "auth_trusted_header": bool(app.state.AUTH_TRUSTED_EMAIL_HEADER),
            "enable_signup_password_confirmation": ENABLE_SIGNUP_PASSWORD_CONFIRMATION,
            "enable_ldap": app.state.config.ENABLE_LDAP,
            "enable_api_key": app.state.config.ENABLE_API_KEY,
            "enable_signup": app.state.config.ENABLE_SIGNUP,
            "enable_login_form": app.state.config.ENABLE_LOGIN_FORM,
            "enable_websocket": ENABLE_WEBSOCKET_SUPPORT,
            "enable_version_update_check": ENABLE_VERSION_UPDATE_CHECK,
            **(
                {
                    "enable_direct_connections": app.state.config.ENABLE_DIRECT_CONNECTIONS,
                    "enable_channels": app.state.config.ENABLE_CHANNELS,
                    "enable_notes": app.state.config.ENABLE_NOTES,
                    "enable_web_search": app.state.config.ENABLE_WEB_SEARCH,
                    "enable_code_execution": app.state.config.ENABLE_CODE_EXECUTION,
                    "enable_code_interpreter": app.state.config.ENABLE_CODE_INTERPRETER,
                    "enable_image_generation": app.state.config.ENABLE_IMAGE_GENERATION,
                    "enable_autocomplete_generation": app.state.config.ENABLE_AUTOCOMPLETE_GENERATION,
                    "enable_community_sharing": app.state.config.ENABLE_COMMUNITY_SHARING,
                    "enable_message_rating": app.state.config.ENABLE_MESSAGE_RATING,
                    "enable_user_webhooks": app.state.config.ENABLE_USER_WEBHOOKS,
                    "enable_admin_export": ENABLE_ADMIN_EXPORT,
                    "enable_admin_chat_access": ENABLE_ADMIN_CHAT_ACCESS,
                    "enable_google_drive_integration": app.state.config.ENABLE_GOOGLE_DRIVE_INTEGRATION,
                    "enable_onedrive_integration": app.state.config.ENABLE_ONEDRIVE_INTEGRATION,
                    **(
                        {
                            "enable_onedrive_personal": ENABLE_ONEDRIVE_PERSONAL,
                            "enable_onedrive_business": ENABLE_ONEDRIVE_BUSINESS,
                        }
                        if app.state.config.ENABLE_ONEDRIVE_INTEGRATION
                        else {}
                    ),
                }
                if user is not None
                else {}
            ),
        },
        **(
            {
                "default_models": app.state.config.DEFAULT_MODELS,
                "default_prompt_suggestions": app.state.config.DEFAULT_PROMPT_SUGGESTIONS,
                "user_count": user_count,
                "code": {
                    "engine": app.state.config.CODE_EXECUTION_ENGINE,
                },
                "audio": {
                    "tts": {
                        "engine": app.state.config.TTS_ENGINE,
                        "voice": app.state.config.TTS_VOICE,
                        "split_on": app.state.config.TTS_SPLIT_ON,
                    },
                    "stt": {
                        "engine": app.state.config.STT_ENGINE,
                    },
                },
                "file": {
                    "max_size": app.state.config.FILE_MAX_SIZE,
                    "max_count": app.state.config.FILE_MAX_COUNT,
                    "image_compression": {
                        "width": app.state.config.FILE_IMAGE_COMPRESSION_WIDTH,
                        "height": app.state.config.FILE_IMAGE_COMPRESSION_HEIGHT,
                    },
                },
                "permissions": {**app.state.config.USER_PERMISSIONS},
                "google_drive": {
                    "client_id": GOOGLE_DRIVE_CLIENT_ID.value,
                    "api_key": GOOGLE_DRIVE_API_KEY.value,
                },
                "onedrive": {
                    "client_id_personal": ONEDRIVE_CLIENT_ID_PERSONAL,
                    "client_id_business": ONEDRIVE_CLIENT_ID_BUSINESS,
                    "sharepoint_url": ONEDRIVE_SHAREPOINT_URL.value,
                    "sharepoint_tenant_id": ONEDRIVE_SHAREPOINT_TENANT_ID.value,
                },
                "ui": {
                    "pending_user_overlay_title": app.state.config.PENDING_USER_OVERLAY_TITLE,
                    "pending_user_overlay_content": app.state.config.PENDING_USER_OVERLAY_CONTENT,
                    "response_watermark": app.state.config.RESPONSE_WATERMARK,
                },
                "license_metadata": app.state.LICENSE_METADATA,
                **(
                    {
                        "active_entries": app.state.USER_COUNT,
                    }
                    if user.role == "admin"
                    else {}
                ),
            }
            if user is not None and (user.role in ["admin", "user"])
            else {
                **(
                    {
                        "ui": {
                            "pending_user_overlay_title": app.state.config.PENDING_USER_OVERLAY_TITLE,
                            "pending_user_overlay_content": app.state.config.PENDING_USER_OVERLAY_CONTENT,
                        }
                    }
                    if user and user.role == "pending"
                    else {}
                ),
                **(
                    {
                        "metadata": {
                            "login_footer": app.state.LICENSE_METADATA.get(
                                "login_footer", ""
                            ),
                            "auth_logo_position": app.state.LICENSE_METADATA.get(
                                "auth_logo_position", ""
                            ),
                        }
                    }
                    if app.state.LICENSE_METADATA
                    else {}
                ),
            }
        ),
    }


class UrlForm(BaseModel):
    url: str


@app.get("/api/webhook")
async def get_webhook_url(user=Depends(get_admin_user)):
    return {
        "url": app.state.config.WEBHOOK_URL,
    }


@app.post("/api/webhook")
async def update_webhook_url(form_data: UrlForm, user=Depends(get_admin_user)):
    app.state.config.WEBHOOK_URL = form_data.url
    app.state.WEBHOOK_URL = app.state.config.WEBHOOK_URL
    return {"url": app.state.config.WEBHOOK_URL}


@app.get("/api/version")
async def get_app_version():
    return {
        "version": VERSION,
    }


@app.get("/api/version/updates")
async def get_app_latest_release_version(user=Depends(get_verified_user)):
    if not ENABLE_VERSION_UPDATE_CHECK:
        log.debug(
            f"Version update check is disabled, returning current version as latest version"
        )
        return {"current": VERSION, "latest": VERSION}
    try:
        timeout = aiohttp.ClientTimeout(total=1)
        async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(
                "https://api.github.com/repos/open-webui/open-webui/releases/latest",
                ssl=AIOHTTP_CLIENT_SESSION_SSL,
            ) as response:
                response.raise_for_status()
                data = await response.json()
                latest_version = data["tag_name"]

                return {"current": VERSION, "latest": latest_version[1:]}
    except Exception as e:
        log.debug(e)
        return {"current": VERSION, "latest": VERSION}


@app.get("/api/changelog")
async def get_app_changelog():
    return {key: CHANGELOG[key] for idx, key in enumerate(CHANGELOG) if idx < 5}


@app.get("/api/usage")
async def get_current_usage(user=Depends(get_verified_user)):
    """
    Get current usage statistics for Lex Luma AI.
    This is an experimental endpoint and subject to change.
    """
    try:
        return {"model_ids": get_models_in_use(), "user_ids": get_active_user_ids()}
    except Exception as e:
        log.error(f"Error getting usage statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


############################
# OAuth Login & Callback
############################


# Initialize OAuth client manager with any MCP tool servers using OAuth 2.1
if len(app.state.config.TOOL_SERVER_CONNECTIONS) > 0:
    for tool_server_connection in app.state.config.TOOL_SERVER_CONNECTIONS:
        if tool_server_connection.get("type", "openapi") == "mcp":
            server_id = tool_server_connection.get("info", {}).get("id")
            auth_type = tool_server_connection.get("auth_type", "none")

            if server_id and auth_type == "oauth_2.1":
                oauth_client_info = tool_server_connection.get("info", {}).get(
                    "oauth_client_info", ""
                )

                try:
                    oauth_client_info = decrypt_data(oauth_client_info)
                    app.state.oauth_client_manager.add_client(
                        f"mcp:{server_id}",
                        OAuthClientInformationFull(**oauth_client_info),
                    )
                except Exception as e:
                    log.error(
                        f"Error adding OAuth client for MCP tool server {server_id}: {e}"
                    )
                    pass

try:
    if ENABLE_STAR_SESSIONS_MIDDLEWARE:
        redis_session_store = RedisStore(
            url=REDIS_URL,
            prefix=(f"{REDIS_KEY_PREFIX}:session:" if REDIS_KEY_PREFIX else "session:"),
        )

        app.add_middleware(SessionAutoloadMiddleware)
        app.add_middleware(
            StarSessionsMiddleware,
            store=redis_session_store,
            cookie_name="owui-session",
            cookie_same_site=WEBUI_SESSION_COOKIE_SAME_SITE,
            cookie_https_only=WEBUI_SESSION_COOKIE_SECURE,
        )
        log.info("Using Redis for session")
    else:
        raise ValueError("No Redis URL provided")
except Exception as e:
    app.add_middleware(
        SessionMiddleware,
        secret_key=WEBUI_SECRET_KEY,
        session_cookie="owui-session",
        same_site=WEBUI_SESSION_COOKIE_SAME_SITE,
        https_only=WEBUI_SESSION_COOKIE_SECURE,
    )


async def register_client(self, request, client_id: str) -> bool:
    server_type, server_id = client_id.split(":", 1)

    connection = None
    connection_idx = None

    for idx, conn in enumerate(request.app.state.config.TOOL_SERVER_CONNECTIONS or []):
        if conn.get("type", "openapi") == server_type:
            info = conn.get("info", {})
            if info.get("id") == server_id:
                connection = conn
                connection_idx = idx
                break

    if connection is None or connection_idx is None:
        log.warning(
            f"Unable to locate MCP tool server configuration for client {client_id} during re-registration"
        )
        return False

    server_url = connection.get("url")
    oauth_server_key = (connection.get("config") or {}).get("oauth_server_key")

    try:
        oauth_client_info = (
            await get_oauth_client_info_with_dynamic_client_registration(
                request,
                client_id,
                server_url,
                oauth_server_key,
            )
        )
    except Exception as e:
        log.error(f"Dynamic client re-registration failed for {client_id}: {e}")
        return False

    try:
        request.app.state.config.TOOL_SERVER_CONNECTIONS[connection_idx] = {
            **connection,
            "info": {
                **connection.get("info", {}),
                "oauth_client_info": encrypt_data(
                    oauth_client_info.model_dump(mode="json")
                ),
            },
        }
    except Exception as e:
        log.error(
            f"Failed to persist updated OAuth client info for tool server {client_id}: {e}"
        )
        return False

    oauth_client_manager.remove_client(client_id)
    oauth_client_manager.add_client(client_id, oauth_client_info)
    log.info(f"Re-registered OAuth client {client_id} for tool server")
    return True


@app.get("/oauth/clients/{client_id}/authorize")
async def oauth_client_authorize(
    client_id: str,
    request: Request,
    response: Response,
    user=Depends(get_verified_user),
):
    # ensure_valid_client_registration
    client = oauth_client_manager.get_client(client_id)
    client_info = oauth_client_manager.get_client_info(client_id)
    if client is None or client_info is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if not await oauth_client_manager._preflight_authorization_url(client, client_info):
        log.info(
            "Detected invalid OAuth client %s; attempting re-registration",
            client_id,
        )

        registered = await register_client(request, client_id)
        if not registered:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to re-register OAuth client",
            )

        client = oauth_client_manager.get_client(client_id)
        client_info = oauth_client_manager.get_client_info(client_id)
        if client is None or client_info is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OAuth client unavailable after re-registration",
            )

        if not await oauth_client_manager._preflight_authorization_url(
            client, client_info
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OAuth client registration is still invalid after re-registration",
            )

    return await oauth_client_manager.handle_authorize(request, client_id=client_id)


@app.get("/oauth/clients/{client_id}/callback")
async def oauth_client_callback(
    client_id: str,
    request: Request,
    response: Response,
    user=Depends(get_verified_user),
):
    return await oauth_client_manager.handle_callback(
        request,
        client_id=client_id,
        user_id=user.id if user else None,
        response=response,
    )


@app.get("/oauth/{provider}/login")
async def oauth_login(provider: str, request: Request):
    return await oauth_manager.handle_login(request, provider)


# OAuth login logic is as follows:
# 1. Attempt to find a user with matching subject ID, tied to the provider
# 2. If OAUTH_MERGE_ACCOUNTS_BY_EMAIL is true, find a user with the email address provided via OAuth
#    - This is considered insecure in general, as OAuth providers do not always verify email addresses
# 3. If there is no user, and ENABLE_OAUTH_SIGNUP is true, create a user
#    - Email addresses are considered unique, so we fail registration if the email address is already taken
@app.get("/oauth/{provider}/login/callback")
@app.get("/oauth/{provider}/callback")  # Legacy endpoint
async def oauth_login_callback(provider: str, request: Request, response: Response):
    return await oauth_manager.handle_callback(request, provider, response)


@app.get("/manifest.json")
async def get_manifest_json():
    if app.state.EXTERNAL_PWA_MANIFEST_URL:
        return requests.get(app.state.EXTERNAL_PWA_MANIFEST_URL).json()
    else:
        return {
            "name": app.state.WEBUI_NAME,
            "short_name": app.state.WEBUI_NAME,
            "description": f"{app.state.WEBUI_NAME} is an open, extensible, user-friendly interface for AI that adapts to your workflow.",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#343541",
            "icons": [
                {
                    "src": "/static/logo.png",
                    "type": "image/png",
                    "sizes": "500x500",
                    "purpose": "any",
                },
                {
                    "src": "/static/logo.png",
                    "type": "image/png",
                    "sizes": "500x500",
                    "purpose": "maskable",
                },
            ],
            "share_target": {
                "action": "/",
                "method": "GET",
                "params": {"text": "shared"},
            },
        }


@app.get("/opensearch.xml")
async def get_opensearch_xml():
    xml_content = rf"""
    <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/" xmlns:moz="http://www.mozilla.org/2006/browser/search/">
    <ShortName>{app.state.WEBUI_NAME}</ShortName>
    <Description>Search {app.state.WEBUI_NAME}</Description>
    <InputEncoding>UTF-8</InputEncoding>
    <Image width="16" height="16" type="image/x-icon">{app.state.config.WEBUI_URL}/static/favicon-dark.png</Image>
    <Url type="text/html" method="get" template="{app.state.config.WEBUI_URL}/?q={"{searchTerms}"}"/>
    <moz:SearchForm>{app.state.config.WEBUI_URL}/</moz:SearchForm>
    </OpenSearchDescription>
    """
    return Response(content=xml_content, media_type="application/xml")

@app.get("/robots.txt")
async def get_robots_txt():
    robots_content = rf"""
    User-agent: *
    Disallow: /api/
    Disallow: /oauth/
    Disallow: /admin/
    Disallow: /static/
    Disallow: /docs/
    Sitemap: {app.state.config.WEBUI_URL}/sitemap.xml
    """
    return Response(content=robots_content, media_type="text/plain")


@app.get("/sitemap.xml")
async def get_sitemap_xml():
    xml_content = rf"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>{app.state.config.WEBUI_URL}/</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>1</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/features/ai-conversational-legal-research</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/features/legislation-gazette-navigator</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/features/case-law-qa</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/features/drafting-assistant</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/features/compliance-checklists</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/features/knowledge-base-dms-integration</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started/introduction-to-lexluma</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started/first-login-account-creation</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started/basic-layout-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started/your-first-chat</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started/quick-tour-of-interface</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/getting-started/basic-navigation</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/chats-section-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/starting-new-chats</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/managing-chat-history</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/searching-and-filtering-chats</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/pinning-and-organizing-chats</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/workspaces-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/creating-and-managing-workspaces</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/models-quick-access-panel</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/sidebar-navigation/sidebar-customization</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/main-chat-area-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/reading-conversations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/composing-messages</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/text-formatting-and-multi-line-input</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/attaching-files-to-chats</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/supported-file-types</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/message-actions-menu</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/regenerating-responses</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/editing-previous-messages</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/copying-and-sharing-messages</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/chat-management-options</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/renaming-and-organizing-chats</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/exporting-conversations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/chat-interface/clearing-conversation-history</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/model-selection-guide</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/understanding-different-model-types</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/text-only-models</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/vision-and-multimodal-models</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/specialized-models</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/accessing-model-information</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/switching-models-mid-conversation</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/model-parameters-and-settings</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/temperature-and-creativity-controls</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/response-length-settings</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/context-window-management</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/working-with-models/model-performance-optimization</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/document-chat-rag-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/uploading-and-managing-documents</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/chatting-with-pdf-files</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/working-with-text-documents</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/image-and-vision-file-support</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/web-search-integration</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/enabling-and-using-web-search</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/understanding-search-results</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/voice-features-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/voice-input-speech-to-text</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/text-to-speech-output</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/voice-settings-and-preferences</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/prompt-presets-introduction</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/using-pre-made-prompts</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/creating-custom-prompt-presets</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/managing-your-prompt-library</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/vision-and-image-analysis</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/uploading-images-for-analysis</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/best-practices-for-image-prompts</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/advanced-features/multi-modal-conversations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/profile-management-overview</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/updating-account-information</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/changing-display-name-and-avatar</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/security-and-password-management</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/appearance-customization</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/theme-selection</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/font-size-and-layout-adjustments</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/color-scheme-preferences</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/interface-density-options</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/notification-settings</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/chat-notification-preferences</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/email-notification-settings</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/update-and-alert-preferences</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/api-keys-management</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/web-search-api-configuration</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/other-service-integrations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/personal-settings/key-security-best-practices</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/keyboard-shortcuts-guide</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/navigation-shortcuts</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/chat-management-shortcuts</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/text-editing-shortcuts</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/status-indicators-reference</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/connection-status-indicators</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/model-status-indicators</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/upload-and-progress-indicators</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/common-icons-guide</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/toolbar-icons-reference</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/message-action-icons</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/status-and-notification-icons</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/troubleshooting-common-issues</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/connection-problems</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/file-upload-issues</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/performance-optimization</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/quick-reference/feature-specific-troubleshooting</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/confidentiality-considerations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ethical-use-of-ai-in-law</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/verifying-ai-outputs</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/documenting-ai-usage</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/compliance-with-legal-standards</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/risk-management-strategies</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/client-communication-best-practices</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/continuing-legal-education-on-ai</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/integrating-ai-into-legal-workflows</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/future-trends-in-legal-ai</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/resources-for-legal-professionals</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/responsible-use-of-ai-in-legal-research</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/avoiding-common-pitfalls-in-legal-ai-use</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/balancing-ai-assistance-with-human-judgment</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/training-and-onboarding-for-legal-ai-tools</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/measuring-the-impact-of-ai-on-legal-practice</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/customizing-ai-tools-for-specific-legal-needs</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/building-client-trust-when-using-ai</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ai-and-legal-research-efficiency</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/maintaining-data-integrity-with-ai-tools</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ai-in-contract-review-and-analysis</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/legal-precedent-and-ai-recommendations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ai-assisted-legal-writing-best-practices</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ensuring-compliance-with-data-protection-laws</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ai-and-intellectual-property-considerations</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/best-practices-for-document-chat-rag</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/optimizing-voice-features-for-legal-use</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/ethical-considerations-for-legal-ai-use</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/leveraging-prompt-presets-for-legal-tasks</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/utilizing-vision-and-image-analysis-in-legal-contexts</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/maximizing-personal-settings-for-productivity</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/quick-reference-for-legal-ai-features</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{app.state.config.WEBUI_URL}/help/legal-ai-best-practices/maintaining-accuracy-in-ai-legal-research</loc>
            <lastmod>2025-11-16</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        </urlset>
        """
    return Response(content=xml_content, media_type="application/xml")
@app.get("/health")
async def healthcheck():
    return {"status": True}

@app.get("/help")
async def help():
    json_data="""[
  {
    "title": "Getting Started",
    "slug": "getting-started",
    "metaTitle": "Getting Started with LexLuma - Your AI Legal Assistant",
    "metaDescription": "Begin your journey with LexLuma. Learn how to create an account, navigate the interface, and start your first AI-powered chat for legal tasks.",
    "keywords": ["LexLuma start", "account creation", "first login", "basic navigation", "AI legal assistant tutorial", "interface overview"],
    "og": {
      "title": "Getting Started with LexLuma - Your AI Legal Assistant",
      "description": "Begin your journey with LexLuma. Learn how to create an account, navigate the interface, and start your first AI-powered chat for legal tasks.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "Getting Started with LexLuma - Your AI Legal Assistant",
      "description": "Begin your journey with LexLuma. Learn how to create an account, navigate the interface, and start your first AI-powered chat for legal tasks."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "Getting Started with LexLuma",
      "description": "A guide to help new users begin using the LexLuma AI legal assistant platform."
    },
    "pages": [
      {
        "title": "Introduction to LexLuma",
        "slug": "introduction-to-lexluma",
        "metaTitle": "What is LexLuma? - AI for Legal Professionals | LexLuma Help",
        "metaDescription": "Discover LexLuma, the AI assistant designed for lawyers and legal professionals. Learn about its core features for research, drafting, and analysis.",
        "keywords": ["LexLuma AI", "legal AI assistant", "what is LexLuma", "AI for lawyers", "legal technology", "law firm software"]
      },
      {
        "title": "First Login & Account Creation",
        "slug": "first-login-account-creation",
        "metaTitle": "Create Your LexLuma Account & First Login Guide",
        "metaDescription": "Step-by-step instructions for creating your LexLuma account and successfully logging in for the first time to access AI legal tools.",
        "keywords": ["sign up LexLuma", "create account", "first login", "account setup", "legal AI login", "onboarding"]
      },
      {
        "title": "Basic Layout Overview",
        "slug": "basic-layout-overview",
        "metaTitle": "LexLuma Interface & Layout Guide for Beginners",
        "metaDescription": "Get familiar with the LexLuma workspace. This guide explains the sidebar, chat area, and settings to help you navigate efficiently.",
        "keywords": ["LexLuma layout", "user interface", "workspace overview", "UI guide", "where to find features"]
      },
      {
        "title": "Your First Chat",
        "slug": "your-first-chat",
        "metaTitle": "How to Start Your First AI Chat in LexLuma",
        "metaDescription": "Learn how to start your first conversation with LexLuma's AI. A simple guide to asking questions and getting legal insights.",
        "keywords": ["first chat", "start conversation", "ask AI a question", "legal AI chat", "beginner tutorial"]
      },
      {
        "title": "Quick Tour of Interface",
        "slug": "quick-tour-of-interface",
        "metaTitle": "Quick Tour: LexLuma's Key Features and Interface",
        "metaDescription": "Take a fast-paced tour of LexLuma's most important features, from the chat history to model selection and settings.",
        "keywords": ["interface tour", "feature overview", "LexLuma walkthrough", "key features", "quick start guide"]
      },
      {
        "title": "Basic Navigation",
        "slug": "basic-navigation",
        "metaTitle": "How to Navigate the LexLuma Platform | Help Guide",
        "metaDescription": "Master the basics of moving around the LexLuma app. Learn how to access different sections, chats, and workspaces with ease.",
        "keywords": ["navigation guide", "how to navigate", "menu navigation", "moving between chats", "basic controls"]
      }
    ]
  },
  {
    "title": "Sidebar Navigation",
    "slug": "sidebar-navigation",
    "metaTitle": "Master LexLuma Sidebar: Chats, Workspaces & Models",
    "metaDescription": "Learn to use the LexLuma sidebar effectively. Manage your chat history, organize workspaces, and quickly switch between AI models.",
    "keywords": ["LexLuma sidebar", "chat history", "workspaces", "model switcher", "sidebar customization", "organize chats"],
    "og": {
      "title": "Master LexLuma Sidebar: Chats, Workspaces & Models",
      "description": "Learn to use the LexLuma sidebar effectively. Manage your chat history, organize workspaces, and quickly switch between AI models.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "Master LexLuma Sidebar: Chats, Workspaces & Models",
      "description": "Learn to use the LexLuma sidebar effectively. Manage your chat history, organize workspaces, and quickly switch between AI models."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "LexLuma Sidebar Navigation Guide",
      "description": "Learn how to use the sidebar to manage chats, workspaces, and AI models in LexLuma."
    },
    "pages": [
      {
        "title": "Chats Section Overview",
        "slug": "chats-section-overview",
        "metaTitle": "LexLuma Chats Section: Manage Conversation History",
        "metaDescription": "Understand the Chats section in LexLuma's sidebar. Learn how to view, search, and access your past and current AI conversations.",
        "keywords": ["chats section", "conversation history", "past chats", "chat list", "sidebar chats"]
      },
      {
        "title": "Starting New Chats",
        "slug": "starting-new-chats",
        "metaTitle": "How to Start a New Chat in LexLuma | Step-by-Step",
        "metaDescription": "Quick guide on initiating a new conversation with LexLuma's AI. Start fresh chats for different legal topics or tasks.",
        "keywords": ["new chat", "start conversation", "begin new chat", "fresh chat", "create new conversation"]
      },
      {
        "title": "Managing Chat History",
        "slug": "managing-chat-history",
        "metaTitle": "How to Manage & Delete Your LexLuma Chat History",
        "metaDescription": "Keep your LexLuma workspace organized. Learn how to review, search, archive, and delete your old chat conversations.",
        "keywords": ["chat history", "delete chats", "manage conversations", "clear history", "organize chats"]
      },
      {
        "title": "Searching and Filtering Chats",
        "slug": "searching-and-filtering-chats",
        "metaTitle": "Find Chats Fast: Search & Filter in LexLuma",
        "metaDescription": "Use LexLuma's powerful search and filter tools to quickly locate specific conversations or topics within your chat history.",
        "keywords": ["search chats", "filter conversations", "find old chat", "search history", "locate conversation"]
      },
      {
        "title": "Pinning and Organizing Chats",
        "slug": "pinning-and-organizing-chats",
        "metaTitle": "Pin Important Chats in LexLuma for Quick Access",
        "metaDescription": "Keep your most important legal research and drafts at your fingertips. Learn how to pin and organize chats in your LexLuma sidebar.",
        "keywords": ["pin chats", "favorite chats", "organize sidebar", "important conversations", "quick access chats"]
      },
      {
        "title": "Workspaces Overview",
        "slug": "workspaces-overview",
        "metaTitle": "Using Workspaces in LexLuma to Organize Legal Work",
        "metaDescription": "Use LexLuma Workspaces to separate chats by case, client, or project. Keep your legal work organized and context-specific.",
        "keywords": ["workspaces", "organize by case", "client workspaces", "project organization", "separate chats"]
      },
      {
        "title": "Creating and Managing Workspaces",
        "slug": "creating-and-managing-workspaces",
        "metaTitle": "Create & Manage LexLuma Workspaces | Guide",
        "metaDescription": "Step-by-step instructions on creating new workspaces, renaming them, and managing chats across different workspaces in LexLuma.",
        "keywords": ["create workspace", "manage workspaces", "rename workspace", "delete workspace", "workspace settings"]
      },
      {
        "title": "Models Quick Access Panel",
        "slug": "models-quick-access-panel",
        "metaTitle": "Quick AI Model Switcher in LexLuma Sidebar",
        "metaDescription": "Learn how to use the quick access panel in the sidebar to swiftly switch between different AI models for various legal tasks.",
        "keywords": ["model switcher", "quick access", "change AI model", "sidebar model panel", "switch GPT model"]
      },
      {
        "title": "Sidebar Customization",
        "slug": "sidebar-customization",
        "metaTitle": "Customize Your LexLuma Sidebar Layout & Preferences",
        "metaDescription": "Tailor the LexLuma sidebar to your workflow. Learn how to show, hide, and resize elements for an optimal user experience.",
        "keywords": ["customize sidebar", "sidebar settings", "hide sidebar", "resize panel", "personalize interface"]
      }
    ]
  },
  {
    "title": "Chat Interface",
    "slug": "chat-interface",
    "metaTitle": "LexLuma Chat Interface: Composing, Managing & Exporting",
    "metaDescription": "Master the LexLuma chat interface. Learn to compose messages, use formatting, attach files, manage conversations, and export your legal work.",
    "keywords": ["LexLuma chat", "compose message", "chat management", "export conversation", "message actions", "file upload"],
    "og": {
      "title": "LexLuma Chat Interface: Composing, Managing & Exporting",
      "description": "Master the LexLuma chat interface. Learn to compose messages, use formatting, attach files, manage conversations, and export your legal work.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "LexLuma Chat Interface: Composing, Managing & Exporting",
      "description": "Master the LexLuma chat interface. Learn to compose messages, use formatting, attach files, manage conversations, and export your legal work."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "LexLuma Chat Interface Guide",
      "description": "A comprehensive guide to using the main chat area in LexLuma, from composing messages to managing conversations."
    },
    "pages": [
      {
        "title": "Main Chat Area Overview",
        "slug": "main-chat-area-overview",
        "metaTitle": "LexLuma Main Chat Area: A Complete Guide",
        "metaDescription": "Get a detailed overview of the LexLuma main chat area. Understand all the components and tools available during your conversation.",
        "keywords": ["main chat", "chat window", "conversation area", "chat UI", "message display"]
      },
      {
        "title": "Reading Conversations",
        "slug": "reading-conversations",
        "metaTitle": "How to Read & Follow AI Conversations in LexLuma",
        "metaDescription": "Learn the best ways to read and follow long conversations with LexLuma's AI, including scrolling, formatting, and distinguishing turns.",
        "keywords": ["read chat", "follow conversation", "chat history view", "scroll messages", "understanding responses"]
      },
      {
        "title": "Composing Messages",
        "slug": "composing-messages",
        "metaTitle": "How to Write Effective Messages to LexLuma AI",
        "metaDescription": "Tips and instructions for composing clear, effective prompts and questions to get the best results from the LexLuma AI for your legal work.",
        "keywords": ["compose message", "write prompt", "asking questions", "effective prompts", "message input"]
      },
      {
        "title": "Text Formatting and Multi-line Input",
        "slug": "text-formattin g-and-multi-line-input",
        "metaTitle": "Use Text Formatting & Multi-line Input in LexLuma",
        "metaDescription": "Make your prompts clear and structured. Learn how to use multi-line input and basic text formatting in LexLuma chat.",
        "keywords": ["text formatting", "multi-line input", "code blocks", "lists in chat", "structured prompts"]
      },
      {
        "title": "Attaching Files to Chats",
        "slug": "attaching-files-to-chats",
        "metaTitle": "How to Attach Files to Your LexLuma Chats",
        "metaDescription": "Upload documents, images, and other files directly to your LexLuma chat for the AI to analyze, summarize, or answer questions about.",
        "keywords": ["attach files", "upload document", "chat with PDF", "file upload", "add attachment"]
      },
      {
        "title": "Supported File Types",
        "slug": "supported-file-types",
        "metaTitle": "LexLuma Supported File Types: PDF, DOCX, TXT & More",
        "metaDescription": "A complete list of file types supported by LexLuma for chat analysis, including documents, images, and data files.",
        "keywords": ["supported files", "file types", "PDF support", "DOCX support", "image upload", "allowed formats"]
      },
      {
        "title": "Message Actions Menu",
        "slug": "message-actions-menu",
        "metaTitle": "LexLuma Message Actions: Copy, Edit, Regenerate",
        "metaDescription": "Learn how to use the message actions menu on each AI response to copy, edit, regenerate, or share specific parts of the conversation.",
        "keywords": ["message actions", "copy message", "edit prompt", "regenerate response", "response menu"]
      },
      {
        "title": "Regenerating Responses",
        "slug": "regenerating-responses",
        "metaTitle": "How to Regenerate AI Responses in LexLuma",
        "metaDescription": "Not satisfied with an answer? Learn how to ask LexLuma to regenerate a response for a different perspective or more detail.",
        "keywords": ["regenerate response", "get new answer", "retry AI", "alternative response", "refresh answer"]
      },
      {
        "title": "Editing Previous Messages",
        "slug": "editing-previous-messages",
        "slug": "editing-previous-messages",
        "metaTitle": "Edit Your Previous Messages in a LexLuma Chat",
        "metaDescription": "Made a mistake in your prompt? Learn how to edit your previous messages to steer the conversation in a new direction without starting over.",
        "keywords": ["edit message", "correct prompt", "change question", "edit history", "revise input"]
      },
      {
        "title": "Copying and Sharing Messages",
        "slug": "copying-and-sharing-messages",
        "metaTitle": "Copy & Share Snippets from LexLuma Conversations",
        "metaDescription": "Easily copy text from your AI conversations or share specific messages and responses with colleagues or for your notes.",
        "keywords": ["copy message", "share chat", "export snippet", "copy text", "share AI output"]
      },
      {
        "title": "Chat Management Options",
        "slug": "chat-management-options",
        "metaTitle": "Manage LexLuma Chats: Rename, Export, Clear",
        "metaDescription": "Access high-level chat management options. Learn how to rename, export, or clear entire conversations in LexLuma.",
        "keywords": ["chat management", "chat settings", "menu options", "manage conversation", "chat tools"]
      },
      {
        "title": "Renaming and Organizing Chats",
        "slug": "renaming-and-organizing-chats",
        "metaTitle": "Rename LexLuma Chats for Better Organization",
        "metaDescription": "Keep your chat history tidy. Learn how to rename your conversations with descriptive titles for easy future reference.",
        "keywords": ["rename chat", "chat title", "organize chats", "label conversation", "change chat name"]
      },
      {
        "title": "Exporting Conversations",
        "slug": "exporting-conversations",
        "metaTitle": "Export Your LexLuma Chat History | PDF & Text",
        "metaDescription": "Save a record of your work. Learn how to export your LexLuma conversations to PDF or text file for your records or reports.",
        "keywords": ["export chat", "save conversation", "PDF export", "text export", "download history"]
      },
      {
        "title": "Clearing Conversation History",
        "slug": "clearing-conversation-history",
        "metaTitle": "How to Clear a Single Chat in LexLuma",
        "metaDescription": "Need a fresh start? Learn how to clear the history of a specific chat conversation while keeping the chat itself open.",
        "keywords": ["clear chat", "delete conversation", "start fresh", "erase history", "reset chat"]
      }
    ]
  },
  {
    "title": "Working with Models",
    "slug": "working-with-models",
    "metaTitle": "Choose the Right AI Model in LexLuma | Model Guide",
    "metaDescription": "Select the best AI model for your legal task. Compare text-only, vision, and specialized models, and learn to adjust parameters for optimal results.",
    "keywords": ["AI models", "model selection", "GPT-4", "Claude", "model parameters", "temperature", "context window"],
    "og": {
      "title": "Choose the Right AI Model in LexLuma | Model Guide",
      "description": "Select the best AI model for your legal task. Compare text-only, vision, and specialized models, and learn to adjust parameters for optimal results.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "Choose the Right AI Model in LexLuma | Model Guide",
      "description": "Select the best AI model for your legal task. Compare text-only, vision, and specialized models, and learn to adjust parameters for optimal results."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "Working with AI Models in LexLuma",
      "description": "A guide to selecting and configuring different AI models for specialized legal tasks in LexLuma."
    },
    "pages": [
      {
        "title": "Model Selection Guide",
        "slug": "model-selection-guide",
        "metaTitle": "How to Choose the Best AI Model in LexLuma",
        "metaDescription": "A practical guide to selecting the right AI model in LexLuma for tasks like legal research, contract review, creative brainstorming, and more.",
        "keywords": ["choose model", "model guide", "which AI to use", "model comparison", "task-specific model"]
      },
      {
        "title": "Understanding Different Model",
        "slug": "understanding-different-model-types",
        "metaTitle": "Text, Vision & Multimodal AI Models in LexLuma",
        "metaDescription": "Understand the difference between text-only, vision, and multimodal AI models available in LexLuma and their applications in law.",
        "keywords": ["model types", "text models", "vision models", "multimodal AI", "GPT-4V", "model capabilities"]
      },
      {
        "title": "Text-Only Models",
        "slug": "text-only-models",
        "metaTitle": "Using Text-Only AI Models for Legal Writing & Research",
        "metaDescription": "Learn when and how to use text-only AI models in LexLuma for powerful legal drafting, research summarization, and analysis.",
        "keywords": ["text models", "GPT-3.5", "Claude Instant", "legal writing", "research models"]
      },
      {
        "title": "Vision and Multimodal Models",
        "slug": "vision-and-multimodal-models",
        "metaTitle": "LexLuma Vision Models: Analyze Images & Documents",
        "metaDescription": "Use LexLuma's vision and multimodal models to analyze scanned documents, charts, graphs, and crime scene photos for legal insights.",
        "keywords": ["vision models", "multimodal", "GPT-4V", "image analysis", "document analysis", "visual AI"]
      },
      {
        "title": "Specialized Models",
        "slug": "specialized-models",
        "metaTitle": "Specialized AI Models for Coding & Creative Tasks",
        "metaDescription": "Explore LexLuma's specialized AI models optimized for specific tasks like code generation, creative writing, and complex reasoning.",
        "keywords": ["specialized models", "coding AI", "creative writing", "reasoning models", "task-specific AI"]
      },
      {
        "title": "Accessing Model Information",
        "slug": "accessing-model-information",
        "metaTitle": "How to Check AI Model Info & Capabilities in LexLuma",
        "metaDescription": "Learn where to find detailed information about each AI model in LexLuma, including its strengths, limitations, and context window size.",
        "keywords": ["model info", "AI capabilities", "model specs", "context window", "token limit"]
      },
      {
        "title": "Switching Models Mid-Conversation",
        "slug": "switching-models-mid-conversation",
        "metaTitle": "Switch AI Models Mid-Chat in LexLuma | Guide",
        "metaDescription": "Change AI models during a conversation to leverage different strengths. Learn how to switch models without losing your chat context.",
        "keywords": ["switch model", "change AI", "mid-conversation", "model switcher", "different model for task"]
      },
      {
        "title": "Model Parameters and Settings",
        "slug": "model-parameters-and-settings",
        "metaTitle": "Configure AI Model Parameters in LexLuma",
        "metaDescription": "Fine-tune how the AI responds by adjusting advanced model parameters like temperature, top-p, and response length in LexLuma.",
        "keywords": ["model parameters", "AI settings", "fine-tuning", "customize responses", "advanced settings"]
      },
      {
        "title": "Temperature and Creativity Controls",
        "slug": "temperature-and-creativity-controls",
        "metaTitle": "AI Temperature Setting: Control Creativity in LexLuma",
        "metaDescription": "Understand how the 'temperature' parameter affects the creativity and determinism of LexLuma's AI responses for legal tasks.",
        "keywords": ["temperature", "creativity control", "deterministic output", "randomness", "AI creativity"]
      },
      {
        "title": "Response Length Settings",
        "slug": "response-length-settings",
        "metaTitle": "Control AI Response Length in LexLuma | Max Tokens",
        "metaDescription": "Learn how to set minimum and maximum response lengths to get detailed analyses or concise summaries from the LexLuma AI.",
        "keywords": ["response length", "max tokens", "short answers", "long answers", "control output length"]
      },
      {
        "title": "Context Window Management",
        "slug": "context-window-management",
        "metaTitle": "Manage AI Context Window for Long Legal Documents",
        "metaDescription": "Understand what the context window is and how to manage it effectively when working with long legal documents and multi-file conversations.",
        "keywords": ["context window", "token limit", "long documents", "memory", "conversation history"]
      },
      {
        "title": "Model Performance Optimization",
        "slug": "model-performance-optimization",
        "metaTitle": "Optimize LexLuma AI Model Performance & Speed",
        "metaDescription": "Get the best performance and fastest response times from LexLuma's AI models with these tips and configuration settings.",
        "keywords": ["performance", "optimization", "speed", "fast responses", "efficient AI", "reduce latency"]
      }
    ]
  },
  {
    "title": "Advanced Features",
    "slug": "advanced-features",
    "metaTitle": "LexLuma Advanced Features: RAG, Web Search, Voice & More",
    "metaDescription": "Unlock the full power of LexLuma with advanced features like Document Chat (RAG), live web search, voice commands, and custom prompt presets.",
    "keywords": ["RAG", "document chat", "web search", "voice AI", "prompt presets", "multimodal", "advanced LexLuma"],
    "og": {
      "title": "LexLuma Advanced Features: RAG, Web Search, Voice & More",
      "description": "Unlock the full power of LexLuma with advanced features like Document Chat (RAG), live web search, voice commands, and custom prompt presets.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "LexLuma Advanced Features: RAG, Web Search, Voice & More",
      "description": "Unlock the full power of LexLuma with advanced features like Document Chat (RAG), live web search, voice commands, and custom prompt presets."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "LexLuma Advanced Features Guide",
      "description": "Explore advanced LexLuma capabilities including document analysis, web search, voice features, and prompt management."
    },
    "pages": [
      {
        "title": "Document Chat & RAG Overview",
        "slug": "document-chat-rag-overview",
        "metaTitle": "Chat with Documents using RAG in LexLuma",
        "metaDescription": "Use Retrieval-Augmented Generation (RAG) to chat with your legal documents. Upload PDFs, DOCX, and more for the AI to analyze and answer questions.",
        "keywords": ["RAG", "document chat", "chat with PDF", "ask document", "retrieval augmented generation"]
      },
      {
        "title": "Uploading and Managing Documents",
        "slug": "uploading-and-managing-documents",
        "metaTitle": "Upload & Manage Documents for AI Analysis in LexLuma",
        "metaDescription": "Learn how to upload, view, and manage the documents in your LexLuma library for use with the Document Chat feature.",
        "keywords": ["upload documents", "document library", "manage files", "delete documents", "document storage"]
      },
      {
        "title": "Chatting with PDF Files",
        "slug": "chatting-with-pdf-files",
        "metaTitle": "Ask Questions About PDFs in LexLuma | Legal Docs",
        "metaDescription": "Extract key information from legal PDFs. Learn how to ask LexLuma questions about case law, contracts, and briefs saved as PDF files.",
        "keywords": ["chat with PDF", "PDF analysis", "ask about PDF", "legal PDF", "contract review PDF"]
      },
      {
        "title": "Working with Text Documents",
        "slug": "working-with-text-documents",
        "metaTitle": "Analyze TXT & DOCX Files with LexLuma AI",
        "metaDescription": "Use LexLuma to summarize, draft, and analyze content from text documents (.txt, .docx) for legal research and drafting.",
        "keywords": ["text documents", "DOCX files", "TXT files", "summarize document", "analyze text"]
      },
      {
        "title": "Image and Vision File Support",
        "slug": "image-and-vision-file-support",
        "metaTitle": "Analyze Images, Charts & Diagrams with LexLuma Vision",
        "metaDescription": "Upload images for the AI to describe and analyze. Ideal for reviewing visual evidence, charts from reports, or crime scene photos.",
        "keywords": ["image analysis", "vision AI", "upload images", "describe photo", "visual evidence analysis"]
      },
      {
        "title": "Web Search Integration",
        "slug": "web-search-integration",
        "metaTitle": "Use Real-Time Web Search in LexLuma Chats",
        "metaDescription": "Enable web search to give LexLuma access to current, real-time information for up-to-date legal research and fact-checking.",
        "keywords": ["web search", "real-time search", "live information", "search internet", "Bing search"]
      },
      {
        "title": "Enabling and Using Web Search",
        "slug": "enabling-and-using-web-search",
        "metaTitle": "How to Enable & Use Web Search in LexLuma | Step-by-Step",
        "metaDescription": "A step-by-step guide on how to turn on the web search feature and use it within your LexLuma conversations.",
        "keywords": ["enable web search", "turn on search", "use web search", "search toggle", "how to search web"]
      },
      {
        "title": "Understanding Search Results",
        "slug": "understanding-search-results",
        "metaTitle": "How LexLuma Uses & Cites Web Search Results",
        "metaDescription": "Learn how LexLuma incorporates and cites information from web searches, and how to interpret the results in your legal context.",
        "keywords": ["search results", "citations", "source links", "interpreting results", "web citations"]
      },
      {
        "title": "Voice Features Overview",
        "slug": "voice-features-overview",
        "metaTitle": "Use Voice Commands & Text-to-Speech in LexLuma",
        "metaDescription": "Go hands-free with LexLuma's voice features. Use speech-to-text for input and text-to-speech to have responses read aloud.",
        "keywords": ["voice features", "speech to text", "text to speech", "voice input", "audio output"]
      },
      {
        "title": "Voice Input (Speech-to-Text)",
        "slug": "voice-input-speech-to-text",
        "metaTitle": "Dictate Messages to LexLuma with Voice Input",
        "metaDescription": "Use your microphone to dictate prompts and questions to LexLuma instead of typing, for faster input and note-taking.",
        "keywords": ["voice input", "speech to text", "dictation", "microphone", "talk to AI"]
      },
      {
        "title": "Text-to-Speech Output",
        "slug": "text-to-speech-output",
        "metaTitle": "Have LexLuma Read Responses Aloud with TTS",
        "metaDescription": "Enable text-to-speech to have LexLuma's AI responses read aloud, perfect for proofreading drafts or multitasking.",
        "keywords": ["text to speech", "TTS", "read aloud", "audio playback", "voice output"]
      },
      {
        "title": "Voice Settings and Preferences",
        "slug": "voice-settings-and-preferences",
        "metaTitle": "Configure Voice Input & Output Settings in LexLuma",
        "metaDescription": "Customize your voice experience by adjusting speech-to-text sensitivity, text-to-speech voice selection, and playback speed.",
        "keywords": ["voice settings", "TTS voice", "STT settings", "playback speed", "microphone settings"]
      },
      {
        "title": "Prompt Presets Introduction",
        "slug": "prompt-presets-introduction",
        "metaTitle": "Save Time with Prompt Presets in LexLuma",
        "metaDescription": "Create and use pre-defined prompt templates for common legal tasks like contract review, deposition preparation, and legal research.",
        "keywords": ["prompt presets", "prompt templates", "saved prompts", "quick prompts", "task templates"]
      },
      {
        "title": "Using Pre-made Prompts",
        "slug": "using-pre-made-prompts",
        "metaTitle": "How to Use LexLuma's Library of Pre-made Prompts",
        "metaDescription": "Access and use LexLuma's curated library of pre-made prompt presets designed for common legal workflows and tasks.",
        "keywords": ["pre-made prompts", "prompt library", "use templates", "curated prompts", "example prompts"]
      },
      {
        "title": "Creating Custom Prompt Presets",
        "slug": "creating-custom-prompt-presets",
        "metaTitle": "Create Your Own Custom Prompt Presets in LexLuma",
        "metaDescription": "Build and save your own custom prompt presets for repetitive legal tasks, ensuring consistency and saving time.",
        "keywords": ["create prompt preset", "custom prompts", "save prompt", "build template", "personal presets"]
      },
      {
        "title": "Managing Your Prompt Library",
        "slug": "managing-your-prompt-library",
        "metaTitle": "Organize, Edit & Delete Your LexLuma Prompt Presets",
        "metaDescription": "Learn how to manage your growing library of prompt presets by organizing, editing, and deleting them as needed.",
        "keywords": ["manage prompts", "prompt library", "edit preset", "delete preset", "organize prompts"]
      },
      {
        "title": "Vision and Image Analysis",
        "slug": "vision-and-image-analysis",
        "metaTitle": "In-Depth Guide to LexLuma's Vision AI Capabilities",
        "metaDescription": "A comprehensive guide to using LexLuma's vision models to analyze images, extract text, identify objects, and understand visual content.",
        "keywords": ["vision AI", "image analysis", "computer vision", "visual AI", "image recognition"]
      },
      {
        "title": "Uploading Images for Analysis",
        "slug": "uploading-images-for-analysis",
        "metaTitle": "Step-by-Step: Upload Images to LexLuma for AI Analysis",
        "metaDescription": "Practical instructions on how to upload image files (JPG, PNG, etc.) to LexLuma for description, analysis, and contextual understanding.",
        "keywords": ["upload images", "image file types", "add picture", "visual upload", "image for analysis"]
      },
      {
        "title": "Best Practices for Image Prompts",
        "slug": "best-practices-for-image-prompts",
        "metaTitle": "How to Write Effective Prompts for Image Analysis",
        "metaDescription": "Learn the best practices for writing prompts that get the most accurate and useful information from LexLuma's vision AI models.",
        "keywords": ["image prompts", "visual prompts", "asking about images", "effective questions", "vision prompts"]
      },
      {
        "title": "Multi-modal Conversations",
        "slug": "multi-modal-conversations",
        "metaTitle": "Combine Text & Images in Multi-modal LexLuma Chats",
        "metaDescription": "Create rich, multi-modal conversations by combining text prompts with image uploads for complex legal analysis and document review.",
        "keywords": ["multi-modal", "text and images", "combined input", "rich conversations", "multi-modal chat"]
      }
    ]
  },
  {
    "title": "Personal Settings",
    "slug": "personal-settings",
    "metaTitle": "LexLuma Personal Settings: Profile, Appearance & API",
    "metaDescription": "Customize your LexLuma experience. Manage your profile, adjust appearance themes, configure notifications, and set up API keys for integrations.",
    "keywords": ["LexLuma settings", "profile", "appearance", "theme", "notifications", "API keys", "personalization"],
    "og": {
      "title": "LexLuma Personal Settings: Profile, Appearance & API",
      "description": "Customize your LexLuma experience. Manage your profile, adjust appearance themes, configure notifications, and set up API keys for integrations.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "LexLuma Personal Settings: Profile, Appearance & API",
      "description": "Customize your LexLuma experience. Manage your profile, adjust appearance themes, configure notifications, and set up API keys for integrations."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "LexLuma Personal Settings and Configuration",
      "description": "Guide to customizing your profile, appearance, notifications, and API settings in LexLuma."
    },
    "pages": [
      {
        "title": "Profile Management Overview",
        "slug": "profile-management-overview",
        "metaTitle": "Manage Your LexLuma User Profile & Account",
        "metaDescription": "An overview of all profile management options in LexLuma, including account info, security, and personal details.",
        "keywords": ["profile management", "user profile", "account settings", "profile overview", "user account"]
      },
      {
        "title": "Updating Account Information",
        "slug": "updating-account-information",
        "metaTitle": "Update Your Email, Name & Account Info in LexLuma",
        "metaDescription": "Learn how to change your primary email address, name, and other basic account information in your LexLuma profile.",
        "keywords": ["update account", "change email", "change name", "account info", "profile details"]
      },
      {
        "title": "Changing Display Name and Avatar",
        "slug": "changing-display-name-and-avatar",
        "metaTitle": "Change Your Display Name & Profile Picture in LexLuma",
        "metaDescription": "Personalize how you appear in LexLuma by changing your display name and uploading a custom profile picture or avatar.",
        "keywords": ["display name", "profile picture", "avatar", "user icon", "personalize profile"]
      },
      {
        "title": "Security and Password Management",
        "slug": "security-and-password-management",
        "metaTitle": "Change Password & Enhance LexLuma Account Security",
        "metaDescription": "Keep your account secure. Learn how to change your password and implement other security best practices for your LexLuma account.",
        "keywords": ["security", "password change", "account security", "strong password", "secure account"]
      },
      {
        "title": "Appearance Customization",
        "slug": "appearance-customization",
        "metaTitle": "Customize LexLuma's Look: Themes, Fonts & Layout",
        "metaDescription": "Make LexLuma work for your eyes. Customize the theme, font size, color scheme, and layout density for optimal comfort.",
        "keywords": ["appearance", "customization", "themes", "font size", "layout", "UI customization"]
      },
      {
        "title": "Theme Selection (Light/Dark/Auto)",
        "slug": "theme-selection",
        "metaTitle": "Choose Light, Dark, or Auto Theme in LexLuma",
        "metaDescription": "Reduce eye strain by selecting a light, dark, or system-matched theme for the LexLuma interface.",
        "keywords": ["theme", "light mode", "dark mode", "auto theme", "dark theme", "light theme"]
      },
      {
        "title": "Font Size and Layout Adjustments",
        "slug": "font-size-and-layout-adjustments",
        "metaTitle": "Adjust Text Size & Interface Layout in LexLuma",
        "metaDescription": "Make text more readable by adjusting the font size and changing the overall density of the LexLuma user interface.",
        "keywords": ["font size", "text size", "layout density", "compact mode", "readability"]
      },
      {
        "title": "Color Scheme Preferences",
        "slug": "color-scheme-preferences",
        "metaTitle": "Customize Color Schemes & Accents in LexLuma",
        "metaDescription": "Personalize the LexLuma interface further by choosing from different color schemes and accent colors.",
        "keywords": ["color scheme", "accent color", "UI colors", "personalize colors", "brand colors"]
      },
      {
        "title": "Interface Density Options",
        "slug": "interface-density-options",
        "metaTitle": "Choose Comfortable, Compact, or Cozy Layout in LexLuma",
        "metaDescription": "Control how much information is displayed on screen by selecting between Comfortable, Compact, and Cozy interface density modes.",
        "keywords": ["interface density", "compact mode", "cozy mode", "comfortable mode", "layout spacing"]
      },
      {
        "title": "Notification Settings",
        "slug": "notification-settings",
        "metaTitle": "Configure LexLuma Notifications & Alerts",
        "metaDescription": "Manage how and when you receive notifications from LexLuma, including in-app alerts and email notifications.",
        "keywords": ["notifications", "alerts", "notification settings", "manage alerts", "push notifications"]
      },
      {
        "title": "Chat Notification Preferences",
        "slug": "chat-notification-preferences",
        "metaTitle": "Set Up Notifications for Chats & AI Responses",
        "metaDescription": "Configure notifications for when long-running AI tasks are complete or when you receive shared chats from colleagues.",
        "keywords": ["chat notifications", "AI response alerts", "task completion", "browser notifications"]
      },
      {
        "title": "Email Notification Settings",
        "slug": "email-notification-settings",
        "metaTitle": "Manage LexLuma Email Notifications & Digest Frequency",
        "metaDescription": "Control the frequency of email digests and promotional emails you receive from LexLuma to avoid inbox clutter.",
        "keywords": ["email notifications", "email digest", "promotional emails", "unsubscribe", "email frequency"]
      },
      {
        "title": "Update and Alert Preferences",
        "slug": "update-and-alert-preferences",
        "metaTitle": "Set Preferences for Feature Updates & Security Alerts",
        "metaDescription": "Choose how you want to be notified about new features, important security updates, and maintenance schedules for LexLuma.",
        "keywords": ["update alerts", "feature updates", "security alerts", "maintenance notifications", "product news"]
      },
      {
        "title": "API Keys Management",
        "slug": "api-keys-management",
        "metaTitle": "Manage API Keys for LexLuma Integrations",
        "metaDescription": "Learn how to view, create, and manage API keys for integrating LexLuma with other legal software and custom workflows.",
        "keywords": ["API keys", "API management", "integrations", "generate API key", "key rotation"]
      },
      {
        "title": "Web Search API Configuration",
        "slug": "web-search-api-configuration",
        "metaTitle": "Configure Web Search API Settings in LexLuma",
        "metaDescription": "If using a custom search API, learn how to configure the endpoint and credentials for the web search feature in LexLuma.",
        "keywords": ["web search API", "search configuration", "Bing API", "custom search", "API endpoint"]
      },
      {
        "title": "Other Service Integrations",
        "slug": "other-service-integrations",
        "metaTitle": "Set Up Integrations with Other Legal Services",
        "metaDescription": "Explore and configure integrations between LexLuma and other legal tech services you use, such as document management systems.",
        "keywords": ["integrations", "service integrations", "third-party apps", "connect services", "legal tech stack"]
      },
      {
        "title": "Key Security Best Practices",
        "slug": "key-security-best-practices",
        "metaTitle": "API Key Security: Best Practices for LexLuma",
        "metaDescription": "Protect your data and account by following these essential security best practices for managing and using API keys in LexLuma.",
        "keywords": ["API security", "key security", "best practices", "secure keys", "data protection"]
      }
    ]
  },
  {
    "title": "Quick Reference",
    "slug": "quick-reference",
    "metaTitle": "LexLuma Quick Reference: Shortcuts, Icons & Troubleshooting",
    "metaDescription": "Your go-to guide for LexLuma keyboard shortcuts, status icon meanings, and solutions to common issues. Boost your productivity.",
    "keywords": ["keyboard shortcuts", "troubleshooting", "status icons", "error messages", "quick reference", "FAQ"],
    "og": {
      "title": "LexLuma Quick Reference: Shortcuts, Icons & Troubleshooting",
      "description": "Your go-to guide for LexLuma keyboard shortcuts, status icon meanings, and solutions to common issues. Boost your productivity.",
      "type": "article"
    },
    "twitter": {
      "card": "summary",
      "title": "LexLuma Quick Reference: Shortcuts, Icons & Troubleshooting",
      "description": "Your go-to guide for LexLuma keyboard shortcuts, status icon meanings, and solutions to common issues. Boost your productivity."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "LexLuma Quick Reference Guide",
      "description": "A quick reference for keyboard shortcuts, icon meanings, and troubleshooting common issues in LexLuma."
    },
    "pages": [
      {
        "title": "Keyboard Shortcuts Guide",
        "slug": "keyboard-shortcuts-guide",
        "metaTitle": "LexLuma Keyboard Shortcuts Cheat Sheet",
        "metaDescription": "A complete list of keyboard shortcuts to navigate and use LexLuma faster, without touching your mouse.",
        "keywords": ["keyboard shortcuts", "hotkeys", "cheat sheet", "productivity", "quick keys"]
      },
      {
        "title": "Navigation Shortcuts",
        "slug": "navigation-shortcuts",
        "metaTitle": "Keyboard Shortcuts for Navigating LexLuma",
        "metaDescription": "Learn the keyboard shortcuts for quickly moving between chats, workspaces, and settings in LexLuma.",
        "keywords": ["navigation shortcuts", "switch chats", "open settings", "go to search", "quick nav"]
      },
      {
        "title": "Chat Management Shortcuts",
        "slug": "chat-management-shortcuts",
        "metaTitle": "Shortcuts for Managing Chats in LexLuma",
        "metaDescription": "Use keyboard shortcuts to quickly create new chats, rename them, pin them, or delete them in LexLuma.",
        "keywords": ["chat shortcuts", "new chat", "rename chat", "pin chat", "delete chat"]
      },
      {
        "title": "Text Editing Shortcuts",
        "slug": "text-editing-shortcuts",
        "metaTitle": "Text Formatting & Editing Shortcuts in LexLuma Input",
        "metaDescription": "Speed up your prompt writing with text editing and formatting shortcuts available in the LexLuma message input box.",
        "keywords": ["text shortcuts", "editing", "formatting", "select all", "copy paste"]
      },
      {
        "title": "Status Indicators Reference",
        "slug": "status-indicators-reference",
        "metaTitle": "LexLuma Status Icons & Indicators: A Complete Guide",
        "metaDescription": "Understand what all the status icons and indicators in LexLuma mean, from connection status to upload progress.",
        "keywords": ["status indicators", "status icons", "what does this icon mean", "connection status", "progress bar"]
      },
      {
        "title": "Connection Status Indicators",
        "slug": "connection-status-indicators",
        "metaTitle": "LexLuma Connection Status: Online, Offline, Error",
        "metaDescription": "Learn how to interpret the connection status indicator and what to do if you see an offline or error state.",
        "keywords": ["connection status", "online", "offline", "error", "connection problem"]
      },
      {
        "title": "Model Status Indicators",
        "slug": "model-status-indicators",
        "metaTitle": "AI Model Status & Availability Indicators in LexLuma",
        "metaDescription": "See if a model is available, busy, or experiencing issues at a glance with the model status indicators in LexLuma.",
        "keywords": ["model status", "AI available", "model busy", "downtime", "status indicator"]
      },
      {
        "title": "Upload and Progress Indicators",
        "slug": "upload-and-progress-indicators",
        "metaTitle": "File Upload & AI Processing Progress Indicators",
        "metaDescription": "Understand the different progress indicators for file uploads and AI response generation in LexLuma.",
        "keywords": ["upload progress", "progress bar", "processing", "AI thinking", "loading indicator"]
      },
      {
        "title": "Common Icons Guide",
        "slug": "common-icons-guide",
        "metaTitle": "LexLuma Icon Dictionary: What Each Icon Means",
        "metaDescription": "A visual guide to the most common icons used throughout the LexLuma interface, with explanations of their functions.",
        "keywords": ["icons guide", "icon dictionary", "what is this icon", "toolbar icons", "button icons"]
      },
      {
        "title": "Toolbar Icons Reference",
        "slug": "toolbar-icons-reference",
        "metaTitle": "LexLuma Main Toolbar Icons & Their Functions",
        "metaDescription": "A reference for all the icons found in the main toolbar of LexLuma, explaining what each one does when clicked.",
        "keywords": ["toolbar icons", "main toolbar", "top bar icons", "menu icons", "action bar"]
      },
      {
        "title": "Message Action Icons",
        "slug": "message-action-icons",
        "metaTitle": "Copy, Regenerate, Edit: Message Action Icons Guide",
        "metaDescription": "Learn what the small icons on each AI response and your messages do, such as copy, regenerate, edit, and more.",
        "keywords": ["message actions", "copy icon", "regenerate icon", "edit icon", "message menu"]
      },
      {
        "title": "Status and Notification Icons",
        "slug": "status-and-notification-icons",
        "metaTitle": "Notification Bell & System Status Icons in LexLuma",
        "metaDescription": "Understand the icons in the status bar, including the notification bell, user menu, and system alerts.",
        "keywords": ["notification icons", "bell icon", "alert icon", "system status", "user menu"]
      },
      {
        "title": "Troubleshooting Common Issues",
        "slug": "troubleshooting-common-issues",
        "metaTitle": "Fix Common LexLuma Problems & Errors",
        "metaDescription": "Step-by-step solutions for the most common issues users face in LexLuma, from login problems to feature errors.",
        "keywords": ["troubleshooting", "common issues", "error fixes", "problem solving", "help desk"]
      },
      {
        "title": "Connection Problems",
        "slug": "connection-problems",
        "metaTitle": "How to Fix LexLuma Connection & Login Issues",
        "metaDescription": "Can't connect or log in? Follow this guide to diagnose and resolve common network and authentication problems.",
        "keywords": ["connection problems", "login issues", "can't connect", "network error", "authentication failed"]
      },
      {
        "title": "File Upload Issues",
        "slug": "file-upload-issues",
        "metaTitle": "Troubleshoot File Upload Failures in LexLuma",
        "metaDescription": "Learn what to do when a file fails to upload, is rejected, or isn't processed correctly by LexLuma's AI.",
        "keywords": ["file upload issues", "upload failed", "file rejected", "processing error", "unsupported file"]
      },
      {
        "title": "Performance Optimization",
        "slug": "performance-optimization",
        "metaTitle": "Speed Up a Slow LexLuma Interface | Performance Tips",
        "metaDescription": "Is LexLuma running slowly? Use these tips to improve performance, from browser cache clearing to model selection.",
        "keywords": ["performance", "slow loading", "speed up", "optimization", "browser cache"]
      },
      {
        "title": "Feature-Specific Troubleshooting",
        "slug": "feature-specific-troubleshooting",
        "metaTitle": "Troubleshoot Specific LexLuma Features Like Web Search & Voice",
        "metaDescription": "Find solutions for issues with specific features like web search not returning results, voice input not working, or RAG failing.",
        "keywords": ["feature troubleshooting", "web search not working", "voice input broken", "RAG issues", "model errors"]
      }
    ]
  },
  {
    "title": "LEGAL AI BEST PRACTICES",
    "slug": "legal-ai-best-practices",
    "metaTitle": "Legal AI Best Practices: Ethical, Effective & Compliant Use",
    "metaDescription": "A comprehensive guide to using AI ethically and effectively in your legal practice. Ensure confidentiality, verify outputs, and maintain compliance.",
    "keywords": ["legal AI ethics", "confidentiality", "AI compliance", "verify AI outputs", "risk management", "ethical AI", "legal best practices"],
    "og": {
      "title": "Legal AI Best Practices: Ethical, Effective & Compliant Use",
      "description": "A comprehensive guide to using AI ethically and effectively in your legal practice. Ensure confidentiality, verify outputs, and maintain compliance.",
      "type": "article"
    },
    "twitter": {
      "card": "summary_large_image",
      "title": "Legal AI Best Practices: Ethical, Effective & Compliant Use",
      "description": "A comprehensive guide to using AI ethically and effectively in your legal practice. Ensure confidentiality, verify outputs, and maintain compliance."
    },
    "jsonLd": {
      "@type": "CollectionPage",
      "name": "Legal AI Best Practices and Ethical Guidelines",
      "description": "Essential guidelines for the responsible and effective use of AI in the legal profession, covering ethics, compliance, and risk management."
    },
    "pages": [
      {
        "title": "Confidentiality Considerations",
        "slug": "confidentiality-considerations",
        "metaTitle": "Maintaining Client Confidentiality with LexLuma AI",
        "metaDescription": "Critical guidelines for protecting client confidentiality and sensitive case information when using LexLuma and other AI tools.",
        "keywords": ["confidentiality", "client data", "sensitive information", "data privacy", "ethical walls", "information barrier"]
      },
      {
        "title": "Ethical Use of AI in Law",
        "slug": "ethical-use-of-ai-in-law",
        "metaTitle": "ABA Rules & Ethical Guidelines for AI in Legal Practice",
        "metaDescription": "Understand how ABA Model Rules of Professional Conduct apply to the use of AI tools like LexLuma in your legal practice.",
        "keywords": ["ethical AI", "ABA rules", "professional conduct", "competence", "diligence", "supervision"]
      },
      {
        "title": "Verifying AI Outputs",
        "slug": "verifying-ai-outputs",
        "metaTitle": "How to Verify & Validate LexLuma AI Outputs for Accuracy",
        "metaDescription": "A lawyer's duty of supervision requires verifying AI-generated content. Learn strategies to check LexLuma's work for accuracy and reliability.",
        "keywords": ["verify AI", "validate outputs", "fact-checking", "accuracy", "hallucinations", "legal research verification"]
      },
      {
        "title": "Documenting AI Usage",
        "slug": "documenting-ai-usage",
        "metaTitle": "Best Practices for Documenting AI Use in Legal Matters",
        "metaDescription": "Why and how to document your use of AI tools like LexLuma in case files, for billing, and for potential malpractice defense.",
        "keywords": ["documenting AI", "usage log", "case file notes", "billing AI time", "malpractice defense", "audit trail"]
      },
      {
        "title": "Compliance with Legal Standards",
        "slug": "compliance-with-legal-standards",
        "metaTitle": "Ensuring AI Compliance with Legal Industry Standards",
        "metaDescription": "Navigate the complex landscape of legal industry standards, data protection laws, and regulations when implementing AI in your practice.",
        "keywords": ["compliance", "legal standards", "data protection", "GDPR", "HIPAA", "regulations", "industry compliance"]
      },
      {
        "title": "Risk Management Strategies",
        "slug": "risk-management-strategies",
        "metaTitle": "Risk Management for AI Integration in Law Firms",
        "metaDescription": "Proactive strategies to identify, assess, and mitigate the risks associated with using AI tools like LexLuma in a legal context.",
        "keywords": ["risk management", "mitigation strategies", "liability", "malpractice risk", "insurance", "due diligence"]
      },
      {
        "title": "Client Communication Best Practices",
        "slug": "client-communication-best-practices",
        "metaTitle": "How to Discuss AI Use with Clients | LexLuma Guide",
        "metaDescription": "Guidance on when and how to inform clients about your use of AI tools, obtaining consent, and setting appropriate expectations.",
        "keywords": ["client communication", "informed consent", "managing expectations", "transparency", "fee disclosure", "engagement letters"]
      },
      {
        "title": "Continuing Legal Education on AI",
        "slug": "continuing-legal-education-on-ai",
        "metaTitle": "CLE Resources for AI in Law & Legal Technology",
        "metaDescription": "Stay ahead of the curve. A curated list of resources for continuing legal education on AI, machine learning, and legal tech.",
        "keywords": ["CLE", "continuing legal education", "AI training", "legal tech education", "professional development", "lawyer training"]
      },
      {
        "title": "Integrating AI into Legal Workflows",
        "slug": "integrating-ai-into-legal-workflows",
        "metaTitle": "Strategies for Integrating LexLuma into Legal Workflows",
        "metaDescription": "Practical steps for seamlessly integrating LexLuma AI into your existing legal workflows for research, drafting, and case analysis.",
        "keywords": ["workflow integration", "legal workflows", "process improvement", "efficiency", "automation", "legal operations"]
      },
      {
        "title": "Future Trends in Legal AI",
        "slug": "future-trends-in-legal-ai",
        "metaTitle": "Future Trends & Developments in Legal AI Technology",
        "metaDescription": "Explore the emerging trends and future developments in legal AI that may impact the practice of law in the coming years.",
        "keywords": ["future trends", "legal tech future", "AI developments", "emerging technology", "predictions", "legal innovation"]
      },
      {
        "title": "Resources for Legal Professionals",
        "slug": "resources-for-legal-professionals",
        "metaTitle": "Curated Resources for Lawyers on AI & Technology",
        "metaDescription": "A collection of essential resources, including books, articles, organizations, and thought leaders in the legal AI space.",
        "keywords": ["resources", "legal professionals", "books on AI", "articles", "organizations", "thought leaders"]
      },
      {
        "title": "Responsible Use of AI in Legal Research",
        "slug": "responsible-use-of-ai-in-legal-research",
        "metaTitle": "Responsible AI Use for Legal Research & Case Law Analysis",
        "metaDescription": "Best practices for using LexLuma responsibly in legal research, including cross-referencing sources and understanding limitations.",
        "keywords": ["legal research", "case law", "responsible use", "cross-referencing", "source validation", "research limitations"]
      },
      {
        "title": "Avoiding Common Pitfalls in Legal AI ",
        "slug": "avoiding-common-pitfalls-in-legal-ai-use",
        "metaTitle": "10 Common Pitfalls When Using AI in Law & How to Avoid Them",
        "metaDescription": "Learn from the mistakes of others. A guide to the most common pitfalls lawyers face with AI and how to steer clear of them.",
        "keywords": ["common pitfalls", "mistakes to avoid", "AI errors", "over-reliance", "bias", "pitfall prevention"]
      },
      {
        "title": "Balancing AI Assistance with Human Judgment",
        "slug": "balancing-ai-assistance-with-human-judgment",
        "metaTitle": "Striking the Right Balance: AI Tools vs. Human Judgment",
        "metaDescription": "The role of the lawyer is more important than ever. Learn how to balance the efficiency of AI with irreplaceable human legal judgment.",
        "keywords": ["human judgment", "AI assistance", "balance", "lawyer discretion", "final authority", "critical thinking"]
      },
      {
        "title": "Training and Onboarding for Legal AI",
        "slug": "training-and-onboarding-for-legal-ai-tools",
        "metaTitle": "Effective Training & Onboarding for LexLuma in Law Firms",
        "metaDescription": "Develop a successful training and onboarding program to ensure your firm adopts LexLuma safely, effectively, and consistently.",
        "keywords": ["training", "onboarding", "law firm training", "adoption", "change management", "staff education"]
      },
      {
        "title": "Measuring the Impact of AI on Legal Practice",
        "slug": "measuring-the-impact-of-ai-on-legal-practice",
        "metaTitle": "How to Measure ROI & Impact of AI Tools in Your Law Firm",
        "metaDescription": "Identify key metrics and methods for measuring the return on investment and overall impact of integrating AI into your legal practice.",
        "keywords": ["measuring impact", "ROI", "key metrics", "efficiency gains", "cost savings", "client satisfaction"]
      },
      {
        "title": "Customizing AI Tools for Specific Legal Needs",
        "slug": "customizing-ai-tools-for-specific-legal-needs",
        "metaTitle": "Customizing LexLuma for Your Specific Legal Practice Area",
        "metaDescription": "Go beyond generic use. Learn how to customize LexLuma's prompts and workflows for specific practice areas like litigation, corporate law, or IP.",
        "keywords": ["customizing AI", "practice area", "litigation", "corporate law", "IP law", "family law", "specialization"]
      },
      {
        "title": "Building Client Trust When Using AI",
        "slug": "building-client-trust-when-using-ai",
        "metaTitle": "Building & Maintaining Client Trust in an AI-Driven Practice",
        "metaDescription": "In an era of AI, client trust is paramount. Learn how to communicate your use of technology in a way that builds confidence and trust.",
        "keywords": ["client trust", "building trust", "transparency", "reassurance", "value proposition", "competitive advantage"]
      },
      {
        "title": "AI and Legal Research Efficiency",
        "slug": "ai-and-legal-research-efficiency",
        "metaTitle": "Maximizing Legal Research Efficiency with LexLuma AI",
        "metaDescription": "Dramatically reduce legal research time while maintaining quality. Techniques for using LexLuma to research cases, statutes, and regulations faster.",
        "keywords": ["research efficiency", "faster research", "case law research", "statutory research", "time savings", "productivity"]
      },
      {
        "title": "Maintaining Data Integrity with AI Tools",
        "slug": "maintaining-data-integrity-with-ai-tools",
        "metaTitle": "Ensuring Data Integrity & Preservation with AI Tools",
        "metaDescription": "Best practices for ensuring the integrity, authenticity, and preservation of legal data when processed and analyzed by AI systems.",
        "keywords": ["data integrity", "data preservation", "chain of custody", "authenticity", "metadata", "legal hold"]
      },
      {
        "title": "AI in Contract Review and Analysis",
        "slug": "ai-in-contract-review-and-analysis",
        "metaTitle": "Best Practices for AI-Powered Contract Review & Analysis",
        "metaDescription": "Leverage LexLuma for contract review. Learn how to identify key clauses, assess risks, and ensure consistency across document sets.",
        "keywords": ["contract review", "contract analysis", "clause identification", "risk assessment", "due diligence", "M&A"]
      },
      {
        "title": "Legal Precedent and AI Recommendations",
        "slug": "legal-precedent-and-ai-recommendations",
        "metaTitle": "Evaluating AI-Generated Legal Precedent & Case Recommendations",
        "metaDescription": "How to critically assess the relevance, authority, and applicability of case law and legal precedents suggested by LexLuma AI.",
        "keywords": ["legal precedent", "case recommendations", "case evaluation", "relevance", "authority", "shepardizing"]
      },
      {
        "title": "AI-Assisted Legal Writing Best Practices",
        "slug": "ai-assisted-legal-writing-best-practices",
        "metaTitle": "AI-Assisted Legal Writing: Drafting Briefs, Memos & Letters",
        "metaDescription": "Enhance your legal writing without sacrificing your voice. Best practices for using LexLuma to draft, edit, and polish legal documents.",
        "keywords": ["legal writing", "drafting", "briefs", "memos", "demand letters", "editing", "polishing"]
      },
      {
        "title": "Ensuring Compliance with Data Protection Laws",
        "slug": "ensuring-compliance-with-data-protection-laws",
        "metaTitle": "GDPR, CCPA & Data Protection Compliance for Legal AI",
        "metaDescription": "A detailed guide to ensuring your use of LexLuma complies with major data protection regulations like GDPR, CCPA, and others.",
        "keywords": ["data protection", "GDPR", "CCPA", "compliance", "data processing", "data subject rights"]
      },
      {
        "title": "AI and Intellectual Property Considerations",
        "slug": "ai-and-intellectual-property-considerations",
        "metaTitle": "IP Law & AI: Ownership, Copyright, and Patent Considerations",
        "metaDescription": "Navigate the complex intellectual property issues surrounding AI, including ownership of AI-generated work and patentability of AI-assisted inventions.",
        "keywords": ["intellectual property", "copyright", "patent", "ownership", "AI-generated work", "invention"]
      },
      {
        "title": "Best Practices for Document Chat",
        "slug": "best-practices-for-document-chat-rag",
        "metaTitle": "Best Practices for Document Chat & RAG in Legal Contexts",
        "metaDescription": "Maximize the value of LexLuma's Document Chat. Learn how to prepare documents, ask effective questions, and interpret results for legal work.",
        "keywords": ["document chat best practices", "RAG best practices", "preparing documents", "effective questions", "legal document analysis"]
      },
      {
        "title": "Optimizing Voice Features for Legal Use",
        "slug": "optimizing-voice-features-for-legal-use",
        "metaTitle": "Optimizing LexLuma Voice Features for Dictation & Review",
        "metaDescription": "Practical tips for using voice input and output in a legal setting, from dictating notes to proofreading drafts via text-to-speech.",
        "keywords": ["voice features optimization", "legal dictation", "proofreading", "hands-free research", "accessibility"]
      },
      {
        "title": "Ethical Considerations for Legal AI Use",
        "slug": "ethical-considerations-for-legal-ai-use",
        "metaTitle": "Core Ethical Considerations for Using AI in a Law Practice",
        "metaDescription": "A deep dive into the core ethical considerations, including bias, fairness, access to justice, and the lawyer's evolving role.",
        "keywords": ["ethical considerations", "AI bias", "fairness", "access to justice", "accountability", "transparency"]
      },
      {
        "title": "Leveraging Prompt Presets for Legal Tasks",
        "slug": "leveraging-prompt-presets-for-legal-tasks",
        "metaTitle": "Creating & Using Prompt Presets for Common Legal Tasks",
        "metaDescription": "Save time and ensure consistency by creating and using prompt presets for repetitive legal tasks like deposition prep or discovery review.",
        "keywords": ["prompt presets", "legal task templates", "deposition prep", "discovery review", "contract clause library"]
      },
      {
        "title": "Utilizing Vision and Image Analysis in Legal Contexts",
        "slug": "utilizing-vision-and-image-analysis-in-legal-contexts",
        "metaTitle": "Using AI Vision Analysis for Evidence, Charts & Documents",
        "metaDescription": "Apply LexLuma's vision capabilities to analyze visual evidence, interpret charts from financial documents, and extract text from scanned images.",
        "keywords": ["vision analysis", "image analysis", "visual evidence", "chart interpretation", "OCR", "document scanning"]
      },
      {
        "title": "Maximizing Personal Settings for Productivity",
        "slug": "maximizing-personal-settings-for-productivity",
        "metaTitle": "Configure LexLuma Settings for Maximum Lawyer Productivity",
        "metaDescription": "Tailor LexLuma's personal settings to create a streamlined, efficient workspace that matches your specific legal workflow and preferences.",
        "keywords": ["personal settings", "productivity", "workspace optimization", "efficiency", "custom workflow"]
      },
      {
        "title": "Quick Reference for Legal AI Features",
        "slug": "quick-reference-for-legal-ai-features",
        "metaTitle": "Quick Reference: LexLuma Features for Legal Professionals",
        "metaDescription": "A handy, at-a-glance reference sheet linking key LexLuma features to common legal tasks and workflows.",
        "keywords": ["quick reference", "legal features", "task-to-feature guide", "cheat sheet", "legal workflow map"]
      },
      {
        "title": "Maintaining Accuracy in AI Legal Research",
        "slug": "maintaining-accuracy-in-ai-legal-research",
        "metaTitle": "Ensuring Accuracy & Reliability in AI-Powered Legal Research",
        "metaDescription": "A focused guide on the specific techniques and checks required to maintain the high accuracy standards demanded in legal research when using AI.",
        "keywords": ["accuracy", "reliability", "legal research", "fact-checking", "source verification", "citation checking"]
      }
    ]
  }
]
"""
    return Response(content=json_data, media_type="application/json")


@app.get("/health/db")
async def healthcheck_with_db():
    Session.execute(text("SELECT 1;")).all()
    return {"status": True}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/cache/{path:path}")
async def serve_cache_file(
    path: str,
    user=Depends(get_verified_user),
):
    file_path = os.path.abspath(os.path.join(CACHE_DIR, path))
    # prevent path traversal
    if not file_path.startswith(os.path.abspath(CACHE_DIR)):
        raise HTTPException(status_code=404, detail="File not found")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


def swagger_ui_html(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon.png",
    )


applications.get_swagger_ui_html = swagger_ui_html

if os.path.exists(FRONTEND_BUILD_DIR):
    mimetypes.add_type("text/javascript", ".js")
    app.mount(
        "/",
        SPAStaticFiles(directory=FRONTEND_BUILD_DIR, html=True),
        name="spa-static-files",
    )
else:
    log.warning(
        f"Frontend build directory not found at '{FRONTEND_BUILD_DIR}'. Serving API only."
    )
