"""MCP server for JustWatch streaming availability data using FastMCP."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from simplejustwatchapi import justwatch

DEFAULT_TRANSPORT = "stdio"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_LOG_LEVEL = "INFO"
LOGGER_NAME = "mcp_justwatch"

logger = logging.getLogger(LOGGER_NAME)


@dataclass(frozen=True)
class RuntimeSettings:
    """Runtime settings for local or remote MCP execution."""

    transport: str
    host: str
    port: int
    log_level: str
    log_file: str | None


def _normalize_transport(value: str) -> str:
    transport = value.strip().lower()
    allowed = {"stdio", "http"}
    if transport not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ValueError(f"MCP_JUSTWATCH_TRANSPORT must be one of: {allowed_values}")
    return transport


def _parse_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as exc:
        raise ValueError("MCP_JUSTWATCH_PORT must be an integer") from exc

    if not 1 <= port <= 65535:
        raise ValueError("MCP_JUSTWATCH_PORT must be between 1 and 65535")
    return port


def build_runtime_settings(env: Mapping[str, str] | None = None) -> RuntimeSettings:
    """Build runtime settings from environment variables."""
    values = os.environ if env is None else env

    transport = _normalize_transport(values.get("MCP_JUSTWATCH_TRANSPORT", DEFAULT_TRANSPORT))
    host = values.get("MCP_JUSTWATCH_HOST", DEFAULT_HOST).strip() or DEFAULT_HOST
    port = _parse_port(values.get("MCP_JUSTWATCH_PORT", str(DEFAULT_PORT)))
    log_level = values.get("MCP_JUSTWATCH_LOG_LEVEL", DEFAULT_LOG_LEVEL).strip().upper()
    log_file = values.get("MCP_JUSTWATCH_LOG_FILE", "").strip() or None

    return RuntimeSettings(
        transport=transport,
        host=host,
        port=port,
        log_level=log_level,
        log_file=log_file,
    )


def configure_logging(env: Mapping[str, str] | None = None) -> logging.Logger:
    """Configure logging for local development or managed service execution."""
    settings = build_runtime_settings(env)
    level = getattr(logging, settings.log_level, logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False
    logger.addHandler(stream_handler)

    if settings.log_file:
        log_path = Path(settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, mode="a")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


configure_logging()

# Initialize FastMCP server
mcp = FastMCP("mcp-justwatch")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_: Request) -> PlainTextResponse:
    """Return a simple liveness response for reverse proxies and service managers."""
    return PlainTextResponse("OK")


def format_media_entry(entry, index: Optional[int] = None) -> str:
    """Format a MediaEntry object as a readable string."""
    lines = []

    # Add index if provided
    if index is not None:
        lines.append(f"\n{index}. ")
    else:
        lines.append("\n")

    # Basic information
    lines.append(f"Title: {entry.title}")
    lines.append(f"  Entry ID: {entry.entry_id}")
    lines.append(f"  Type: {entry.object_type}")

    if entry.release_year:
        lines.append(f"  Release Year: {entry.release_year}")

    if entry.release_date:
        lines.append(f"  Release Date: {entry.release_date}")

    # Runtime
    if entry.runtime_minutes:
        hours = entry.runtime_minutes // 60
        minutes = entry.runtime_minutes % 60
        if hours > 0:
            lines.append(f"  Runtime: {hours}h {minutes}m")
        else:
            lines.append(f"  Runtime: {minutes}m")

    # Genres
    if entry.genres:
        genres_str = ", ".join(entry.genres)
        lines.append(f"  Genres: {genres_str}")

    # Scores
    if hasattr(entry, "scoring") and entry.scoring:
        if entry.scoring.imdb_score:
            lines.append(f"  IMDb Score: {entry.scoring.imdb_score}/10")
        if entry.scoring.tmdb_score:
            lines.append(f"  TMDb Score: {entry.scoring.tmdb_score}/10")

    # Streaming offers
    if entry.offers:
        lines.append(f"  Available on {len(entry.offers)} platform(s):")
        for offer in entry.offers:
            offer_line = f"    - {offer.package.name}"
            details_parts = []
            if offer.monetization_type:
                details_parts.append(offer.monetization_type)
            if offer.presentation_type:
                details_parts.append(offer.presentation_type)
            if offer.price_string:
                details_parts.append(f"Price: {offer.price_string}")
            if details_parts:
                offer_line += f" ({', '.join(details_parts)})"
            if offer.url:
                offer_line += f"\n      URL: {offer.url}"
            lines.append(offer_line)
    else:
        lines.append("  No streaming offers available")

    return "\n".join(lines)


@mcp.tool()
def search_content(
    query: str,
    country: str = "US",
    language: str = "en",
    count: int = 5,
    best_only: bool = True,
) -> str:
    """Search for movies and TV shows on JustWatch with streaming availability.

    Args:
        query: The title to search for (movie or TV show)
        country: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB', 'DE')
        language: ISO 639-1 language code (e.g., 'en', 'es', 'fr')
        count: Maximum number of results to return (1-20)
        best_only: Return only best quality offers per platform

    Returns:
        Formatted search results with streaming availability
    """
    try:
        # Normalize country to uppercase and language to lowercase
        country = country.upper()
        language = language.lower()

        # Clamp count to reasonable range
        count = max(1, min(count, 20))

        logger.info("Searching for '%s' in %s (language: %s)", query, country, language)

        results = justwatch.search(
            title=query, country=country, language=language, count=count, best_only=best_only
        )

        if not results:
            return f"No results found for '{query}' in {country}."

        # Format the results
        output_lines = [f"Search results for '{query}' in {country} ({len(results)} result(s)):\n"]

        for idx, entry in enumerate(results, 1):
            output_lines.append(format_media_entry(entry, idx))

        return "\n".join(output_lines)

    except Exception as e:
        logger.error("Error searching for content: %s", e, exc_info=True)
        return f"Error searching for content: {str(e)}"


@mcp.tool()
def get_details(
    node_id: str,
    country: str = "US",
    language: str = "en",
    best_only: bool = True,
) -> str:
    """Get detailed information about a specific movie or TV show using its JustWatch node ID.

    Args:
        node_id: The JustWatch node ID (obtained from search results, e.g., 'tm12345')
        country: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB', 'DE')
        language: ISO 639-1 language code (e.g., 'en', 'es', 'fr')
        best_only: Return only best quality offers per platform

    Returns:
        Detailed information about the content with streaming offers
    """
    try:
        # Normalize country to uppercase and language to lowercase
        country = country.upper()
        language = language.lower()

        logger.info("Getting details for node ID '%s' in %s", node_id, country)

        entry = justwatch.details(
            node_id=node_id, country=country, language=language, best_only=best_only
        )

        if not entry:
            return f"No details found for node ID '{node_id}' in {country}."

        output_lines = [f"Details for content in {country}:\n"]
        output_lines.append(format_media_entry(entry))

        return "\n".join(output_lines)

    except Exception as e:
        logger.error("Error getting details: %s", e, exc_info=True)
        return f"Error getting details: {str(e)}"


@mcp.tool()
def get_offers_for_countries(
    node_id: str,
    countries: list[str],
    language: str = "en",
    best_only: bool = True,
) -> str:
    """Get streaming offers for specific content across multiple countries.

    Args:
        node_id: The JustWatch node ID (from search results)
        countries: List of two-letter country codes (e.g., ['US', 'GB', 'CA', 'AU'])
        language: ISO 639-1 language code (e.g., 'en', 'es', 'fr')
        best_only: Return only best quality offers per platform

    Returns:
        Streaming offers organized by country
    """
    try:
        # Convert list to set and ensure uppercase
        countries_set = {c.upper() for c in countries}
        language = language.lower()

        logger.info("Getting offers for node ID '%s' in countries: %s", node_id, countries_set)

        offers_dict = justwatch.offers_for_countries(
            node_id=node_id, countries=countries_set, language=language, best_only=best_only
        )

        if not offers_dict:
            return f"No offers found for node ID '{node_id}'."

        output_lines = ["Streaming offers across countries:\n"]

        for country in sorted(countries_set):
            offers_list = offers_dict.get(country, [])
            output_lines.append(f"\n{country}:")
            if offers_list:
                for offer in offers_list:
                    offer_line = f"  - {offer.package.name}"
                    details_parts = []
                    if offer.monetization_type:
                        details_parts.append(offer.monetization_type)
                    if offer.presentation_type:
                        details_parts.append(offer.presentation_type)
                    if offer.price_string:
                        details_parts.append(f"Price: {offer.price_string}")
                    if details_parts:
                        offer_line += f" ({', '.join(details_parts)})"
                    if offer.url:
                        offer_line += f"\n    URL: {offer.url}"
                    output_lines.append(offer_line)
            else:
                output_lines.append("  No offers available")

        return "\n".join(output_lines)

    except Exception as e:
        logger.error("Error getting offers: %s", e, exc_info=True)
        return f"Error getting offers: {str(e)}"


def main(env: Mapping[str, str] | None = None):
    """Entry point for the MCP server."""
    settings = build_runtime_settings(env)
    configure_logging(env)

    if settings.transport == "http":
        mcp.run(transport="http", host=settings.host, port=settings.port)
        return

    mcp.run()


if __name__ == "__main__":
    main()
