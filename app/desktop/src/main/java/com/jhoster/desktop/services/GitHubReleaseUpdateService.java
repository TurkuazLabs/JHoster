// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\GitHubReleaseUpdateService.java
// # 📌 Amac: GitHub latest release endpoint uzerinden JHoster surum kontrolu yapar
// # 📌 Modul - Java
// # Version: 3.61.0
// # Aciklama: Launcher splash akisi icin non-blocking update check saglar, repo tanimsizsa guvenli sekilde atlar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.UpdateCheckResult;
import com.jhoster.desktop.tools.SemanticVersionCompareTool;
import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class GitHubReleaseUpdateService {
    private static final String ENV_UPDATE_REPO = "JHOSTER_UPDATE_REPO";
    private static final String PROPERTY_UPDATE_REPO = "jhoster.update.repo";
    private static final String PROPERTY_UPDATE_ENABLED = "jhoster.update.enabled";
    private static final String ENV_UPDATE_ENABLED = "JHOSTER_UPDATE_ENABLED";
    private static final String GITHUB_API_BASE = "https://api.github.com/repos/";
    private static final String LATEST_RELEASE_SUFFIX = "/releases/latest";
    private static final String HEADER_ACCEPT = "Accept";
    private static final String HEADER_API_VERSION = "X-GitHub-Api-Version";
    private static final String HEADER_USER_AGENT = "User-Agent";
    private static final String VALUE_ACCEPT = "application/vnd.github+json";
    private static final String VALUE_API_VERSION = "2022-11-28";
    private static final String VALUE_USER_AGENT = "JHoster-Launcher";
    private static final String KEY_TAG_NAME = "tag_name";
    private static final String KEY_HTML_URL = "html_url";
    private static final long TIMEOUT_SECONDS = 3L;

    private final HttpClient httpClient;
    private final SemanticVersionCompareTool semanticVersionCompareTool;

    public GitHubReleaseUpdateService() {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(2))
            .build();
        this.semanticVersionCompareTool = new SemanticVersionCompareTool();
    }

    public CompletableFuture<UpdateCheckResult> checkLatestRelease(String currentVersion) {
        Optional<String> repo = resolveRepository();
        if (repo.isEmpty()) {
            return CompletableFuture.completedFuture(UpdateCheckResult.skipped(
                currentVersion,
                "GitHub release check skipped because JHOSTER_UPDATE_REPO is not configured."
            ));
        }

        if (!isUpdateCheckEnabled()) {
            return CompletableFuture.completedFuture(UpdateCheckResult.skipped(
                currentVersion,
                "GitHub release check is disabled."
            ));
        }

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(buildLatestReleaseUrl(repo.get())))
            .timeout(Duration.ofSeconds(TIMEOUT_SECONDS))
            .header(HEADER_ACCEPT, VALUE_ACCEPT)
            .header(HEADER_API_VERSION, VALUE_API_VERSION)
            .header(HEADER_USER_AGENT, VALUE_USER_AGENT)
            .GET()
            .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .orTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
            .thenApply(response -> parseResponse(currentVersion, response))
            .exceptionally(exception -> UpdateCheckResult.failed(
                currentVersion,
                "GitHub release check failed or timed out; starting local desktop."
            ));
    }

    private UpdateCheckResult parseResponse(String currentVersion, HttpResponse<String> response) {
        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            return UpdateCheckResult.failed(currentVersion, "GitHub release check returned HTTP " + response.statusCode() + ".");
        }

        String body = response.body() == null ? "" : response.body();
        String latestVersion = extractJsonString(body, KEY_TAG_NAME);
        String releaseUrl = extractJsonString(body, KEY_HTML_URL);
        if (latestVersion.isBlank()) {
            return UpdateCheckResult.failed(currentVersion, "GitHub latest release response did not contain tag_name.");
        }

        if (semanticVersionCompareTool.isNewer(latestVersion, currentVersion)) {
            return UpdateCheckResult.available(currentVersion, latestVersion, releaseUrl);
        }

        return UpdateCheckResult.current(currentVersion, latestVersion, releaseUrl);
    }

    private Optional<String> resolveRepository() {
        String propertyRepo = System.getProperty(PROPERTY_UPDATE_REPO, "").trim();
        if (!propertyRepo.isBlank()) {
            return Optional.of(propertyRepo);
        }
        String envRepo = System.getenv(ENV_UPDATE_REPO);
        if (envRepo != null && !envRepo.trim().isBlank()) {
            return Optional.of(envRepo.trim());
        }
        return Optional.empty();
    }

    private boolean isUpdateCheckEnabled() {
        String propertyValue = System.getProperty(PROPERTY_UPDATE_ENABLED, "").trim();
        if (!propertyValue.isBlank()) {
            return Boolean.parseBoolean(propertyValue);
        }
        String envValue = System.getenv(ENV_UPDATE_ENABLED);
        if (envValue != null && !envValue.trim().isBlank()) {
            return "1".equals(envValue.trim()) || Boolean.parseBoolean(envValue.trim());
        }
        return true;
    }

    private String buildLatestReleaseUrl(String repo) {
        String[] tokens = repo.split("/", 2);
        if (tokens.length != 2) {
            return GITHUB_API_BASE + URLEncoder.encode(repo, StandardCharsets.UTF_8) + LATEST_RELEASE_SUFFIX;
        }
        return GITHUB_API_BASE
            + URLEncoder.encode(tokens[0], StandardCharsets.UTF_8)
            + "/"
            + URLEncoder.encode(tokens[1], StandardCharsets.UTF_8)
            + LATEST_RELEASE_SUFFIX;
    }

    private String extractJsonString(String json, String key) {
        Pattern pattern = Pattern.compile("\\\"" + Pattern.quote(key) + "\\\"\\s*:\\s*\\\"([^\\\"]*)\\\"");
        Matcher matcher = pattern.matcher(json);
        if (matcher.find()) {
            return unescapeJson(matcher.group(1));
        }
        return "";
    }

    private String unescapeJson(String value) {
        return value == null ? "" : value.replace("\\/", "/").replace("\\\"", "\"").trim();
    }
}
