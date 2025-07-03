"""Configuration management for Interactive Data Dashboard.

This module handles all configuration settings for the application,
including environment variables, default values, and validation.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Environment(Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ChartTheme(Enum):
    """Available chart themes."""
    PLOTLY = "plotly"
    PLOTLY_WHITE = "plotly_white"
    PLOTLY_DARK = "plotly_dark"
    GGPLOT2 = "ggplot2"
    SEABORN = "seaborn"
    SIMPLE_WHITE = "simple_white"
    PRESENTATION = "presentation"
    XGRIDOFF = "xgridoff"
    YGRIDOFF = "ygridoff"
    GRIDON = "gridon"
    NONE = "none"


@dataclass
class StreamlitConfig:
    """Streamlit-specific configuration."""
    server_port: int = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    server_address: str = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    server_headless: bool = os.getenv("STREAMLIT_SERVER_HEADLESS", "true").lower() == "true"
    server_run_on_save: bool = os.getenv("STREAMLIT_SERVER_RUN_ON_SAVE", "false").lower() == "true"
    server_file_watcher_type: str = os.getenv("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "auto")
    browser_gather_usage_stats: bool = os.getenv("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false").lower() == "true"
    server_enable_cors: bool = os.getenv("STREAMLIT_SERVER_ENABLE_CORS", "false").lower() == "true"
    server_enable_xsrf_protection: bool = os.getenv("STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION", "true").lower() == "true"
    server_max_upload_size: int = int(os.getenv("STREAMLIT_SERVER_MAX_UPLOAD_SIZE", "200"))
    
    # Theme settings
    theme_base: str = os.getenv("STREAMLIT_THEME_BASE", "light")
    theme_primary_color: str = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#FF6B6B")
    theme_background_color: str = os.getenv("STREAMLIT_THEME_BACKGROUND_COLOR", "#FFFFFF")
    theme_secondary_background_color: str = os.getenv("STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR", "#F0F2F6")
    theme_text_color: str = os.getenv("STREAMLIT_THEME_TEXT_COLOR", "#262730")
    theme_font: str = os.getenv("STREAMLIT_THEME_FONT", "sans serif")


@dataclass
class DataConfig:
    """Data processing configuration."""
    max_data_points: int = int(os.getenv("MAX_DATA_POINTS", "10000"))
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "200"))
    supported_file_types: List[str] = field(default_factory=lambda: os.getenv("SUPPORTED_FILE_TYPES", "csv,xlsx,json,parquet").split(","))
    data_cache_ttl: int = int(os.getenv("DATA_CACHE_TTL", "3600"))
    enable_data_validation: bool = os.getenv("ENABLE_DATA_VALIDATION", "true").lower() == "true"
    auto_detect_encoding: bool = os.getenv("AUTO_DETECT_ENCODING", "true").lower() == "true"
    default_encoding: str = os.getenv("DEFAULT_ENCODING", "utf-8")
    data_sample_size: int = int(os.getenv("DATA_SAMPLE_SIZE", "1000"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "10000"))
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024


@dataclass
class ChartConfig:
    """Chart configuration settings."""
    default_theme: ChartTheme = ChartTheme(os.getenv("DEFAULT_THEME", "plotly_white"))
    height: int = int(os.getenv("CHART_HEIGHT", "500"))
    width: int = int(os.getenv("CHART_WIDTH", "700"))
    margin_top: int = int(os.getenv("CHART_MARGIN_TOP", "50"))
    margin_bottom: int = int(os.getenv("CHART_MARGIN_BOTTOM", "50"))
    margin_left: int = int(os.getenv("CHART_MARGIN_LEFT", "50"))
    margin_right: int = int(os.getenv("CHART_MARGIN_RIGHT", "50"))
    enable_animations: bool = os.getenv("ENABLE_CHART_ANIMATIONS", "true").lower() == "true"
    
    # Export settings
    export_format: str = os.getenv("CHART_EXPORT_FORMAT", "png")
    export_width: int = int(os.getenv("CHART_EXPORT_WIDTH", "1200"))
    export_height: int = int(os.getenv("CHART_EXPORT_HEIGHT", "800"))
    export_scale: int = int(os.getenv("CHART_EXPORT_SCALE", "2"))
    
    @property
    def margin_dict(self) -> Dict[str, int]:
        """Return margin settings as a dictionary."""
        return {
            "t": self.margin_top,
            "b": self.margin_bottom,
            "l": self.margin_left,
            "r": self.margin_right
        }


@dataclass
class PerformanceConfig:
    """Performance and optimization settings."""
    enable_caching: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    max_memory_usage_mb: int = int(os.getenv("MAX_MEMORY_USAGE_MB", "2048"))
    enable_lazy_loading: bool = os.getenv("ENABLE_LAZY_LOADING", "true").lower() == "true"
    max_concurrent_operations: int = int(os.getenv("MAX_CONCURRENT_OPERATIONS", "4"))
    enable_profiling: bool = os.getenv("ENABLE_PROFILING", "false").lower() == "true"
    profiling_output_dir: str = os.getenv("PROFILING_OUTPUT_DIR", "./profiling")
    
    @property
    def max_memory_usage_bytes(self) -> int:
        """Convert max memory usage from MB to bytes."""
        return self.max_memory_usage_mb * 1024 * 1024


@dataclass
class UIConfig:
    """User interface configuration."""
    show_sidebar: bool = os.getenv("SHOW_SIDEBAR", "true").lower() == "true"
    show_footer: bool = os.getenv("SHOW_FOOTER", "true").lower() == "true"
    show_header: bool = os.getenv("SHOW_HEADER", "true").lower() == "true"
    enable_dark_mode: bool = os.getenv("ENABLE_DARK_MODE", "false").lower() == "true"
    show_data_preview: bool = os.getenv("SHOW_DATA_PREVIEW", "true").lower() == "true"
    data_preview_rows: int = int(os.getenv("DATA_PREVIEW_ROWS", "10"))
    show_chart_controls: bool = os.getenv("SHOW_CHART_CONTROLS", "true").lower() == "true"
    enable_fullscreen_charts: bool = os.getenv("ENABLE_FULLSCREEN_CHARTS", "true").lower() == "true"
    show_download_buttons: bool = os.getenv("SHOW_DOWNLOAD_BUTTONS", "true").lower() == "true"
    enable_chart_sharing: bool = os.getenv("ENABLE_CHART_SHARING", "true").lower() == "true"


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: LogLevel = LogLevel(os.getenv("LOG_LEVEL", "INFO"))
    format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file: Optional[str] = os.getenv("LOG_FILE")
    max_size_mb: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    enable_console_logging: bool = os.getenv("ENABLE_CONSOLE_LOGGING", "true").lower() == "true"
    enable_file_logging: bool = os.getenv("ENABLE_FILE_LOGGING", "false").lower() == "true"
    log_requests: bool = os.getenv("LOG_REQUESTS", "false").lower() == "true"
    log_performance: bool = os.getenv("LOG_PERFORMANCE", "false").lower() == "true"


@dataclass
class SecurityConfig:
    """Security configuration."""
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    session_timeout: int = int(os.getenv("SESSION_TIMEOUT", "3600"))
    enable_rate_limiting: bool = os.getenv("ENABLE_RATE_LIMITING", "false").lower() == "true"
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    allowed_hosts: List[str] = field(default_factory=lambda: os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(","))
    enable_https: bool = os.getenv("ENABLE_HTTPS", "false").lower() == "true"
    csrf_protection: bool = os.getenv("CSRF_PROTECTION", "true").lower() == "true"


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str = os.getenv("DATABASE_URL", "sqlite:///./dashboard.db")
    echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
    pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    pool_timeout: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
    pool_recycle: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))


@dataclass
class RedisConfig:
    """Redis configuration."""
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    db: int = int(os.getenv("REDIS_DB", "0"))
    password: Optional[str] = os.getenv("REDIS_PASSWORD")
    socket_timeout: int = int(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))
    connection_pool_max_connections: int = int(os.getenv("REDIS_CONNECTION_POOL_MAX_CONNECTIONS", "10"))


@dataclass
class APIConfig:
    """External API configuration."""
    timeout: int = int(os.getenv("API_TIMEOUT", "30"))
    retry_attempts: int = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
    retry_delay: int = int(os.getenv("API_RETRY_DELAY", "1"))
    enable_caching: bool = os.getenv("ENABLE_API_CACHING", "true").lower() == "true"
    cache_ttl: int = int(os.getenv("API_CACHE_TTL", "300"))
    
    # Specific API keys
    alpha_vantage_api_key: Optional[str] = os.getenv("ALPHA_VANTAGE_API_KEY")
    quandl_api_key: Optional[str] = os.getenv("QUANDL_API_KEY")
    yahoo_finance_enabled: bool = os.getenv("YAHOO_FINANCE_ENABLED", "true").lower() == "true"


@dataclass
class FileStorageConfig:
    """File storage configuration."""
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", "./uploads"))
    export_dir: Path = Path(os.getenv("EXPORT_DIR", "./exports"))
    temp_dir: Path = Path(os.getenv("TEMP_DIR", "./temp"))
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
    logs_dir: Path = Path(os.getenv("LOGS_DIR", "./logs"))
    cache_dir: Path = Path(os.getenv("CACHE_DIR", "./cache"))
    static_dir: Path = Path(os.getenv("STATIC_DIR", "./static"))
    templates_dir: Path = Path(os.getenv("TEMPLATES_DIR", "./templates"))
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        for directory in [self.upload_dir, self.export_dir, self.temp_dir, 
                         self.data_dir, self.logs_dir, self.cache_dir, 
                         self.static_dir, self.templates_dir]:
            directory.mkdir(parents=True, exist_ok=True)


@dataclass
class FeatureFlags:
    """Feature flags for enabling/disabling functionality."""
    enable_experimental_features: bool = os.getenv("ENABLE_EXPERIMENTAL_FEATURES", "false").lower() == "true"
    enable_beta_features: bool = os.getenv("ENABLE_BETA_FEATURES", "false").lower() == "true"
    enable_advanced_charts: bool = os.getenv("ENABLE_ADVANCED_CHARTS", "true").lower() == "true"
    enable_data_export: bool = os.getenv("ENABLE_DATA_EXPORT", "true").lower() == "true"
    enable_chart_export: bool = os.getenv("ENABLE_CHART_EXPORT", "true").lower() == "true"
    enable_real_time_updates: bool = os.getenv("ENABLE_REAL_TIME_UPDATES", "false").lower() == "true"
    enable_collaborative_features: bool = os.getenv("ENABLE_COLLABORATIVE_FEATURES", "false").lower() == "true"
    enable_ai_insights: bool = os.getenv("ENABLE_AI_INSIGHTS", "false").lower() == "true"


@dataclass
class Config:
    """Main configuration class that aggregates all settings."""
    # Application metadata
    app_name: str = os.getenv("APP_NAME", "Interactive Data Dashboard")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: Environment = Environment(os.getenv("ENVIRONMENT", "development"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    testing: bool = os.getenv("TESTING", "false").lower() == "true"
    
    # Configuration sections
    streamlit: StreamlitConfig = field(default_factory=StreamlitConfig)
    data: DataConfig = field(default_factory=DataConfig)
    charts: ChartConfig = field(default_factory=ChartConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    api: APIConfig = field(default_factory=APIConfig)
    file_storage: FileStorageConfig = field(default_factory=FileStorageConfig)
    feature_flags: FeatureFlags = field(default_factory=FeatureFlags)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == Environment.TESTING or self.testing
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate required settings
        if not self.app_name:
            errors.append("APP_NAME is required")
        
        if not self.app_version:
            errors.append("APP_VERSION is required")
        
        # Validate port ranges
        if not (1 <= self.streamlit.server_port <= 65535):
            errors.append("STREAMLIT_SERVER_PORT must be between 1 and 65535")
        
        # Validate file sizes
        if self.data.max_file_size_mb <= 0:
            errors.append("MAX_FILE_SIZE_MB must be positive")
        
        # Validate cache TTL
        if self.data.data_cache_ttl < 0:
            errors.append("DATA_CACHE_TTL must be non-negative")
        
        # Validate chart dimensions
        if self.charts.height <= 0 or self.charts.width <= 0:
            errors.append("Chart dimensions must be positive")
        
        # Validate security settings in production
        if self.is_production:
            if self.security.secret_key == "change-me-in-production":
                errors.append("SECRET_KEY must be changed in production")
            
            if self.debug:
                errors.append("DEBUG should be disabled in production")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if hasattr(value, '__dict__'):
                result[key] = value.__dict__
            else:
                result[key] = value
        return result


# Global configuration instance
config = Config()

# Validate configuration on import
validation_errors = config.validate()
if validation_errors:
    logger = logging.getLogger(__name__)
    for error in validation_errors:
        logger.error(f"Configuration error: {error}")
    
    if config.is_production:
        raise ValueError(f"Configuration validation failed: {validation_errors}")


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def reload_config() -> Config:
    """Reload configuration from environment variables."""
    global config
    load_dotenv(override=True)
    config = Config()
    return config


# Export commonly used configurations
__all__ = [
    "Config",
    "Environment",
    "LogLevel",
    "ChartTheme",
    "config",
    "get_config",
    "reload_config",
]