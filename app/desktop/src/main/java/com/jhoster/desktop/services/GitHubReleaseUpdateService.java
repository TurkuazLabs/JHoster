// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\GitHubReleaseUpdateService.java
// # 📌 Amac: GitHub latest release endpoint uzerinden JHoster surum ve setup asset kontrolu yapar
// # 📌 Modul - Java
// # Version: 3.80.0
// # Aciklama: Latest release tag, NSIS setup EXE ve SHA-256 asset URL bilgilerini non-blocking olarak cozer
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.UpdateCheckResult;
import com.jhoster.desktop.tools.DesktopMetadataTool;
import com.jhoster.desktop.tools.SemanticVersionCompareTool;
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
    private static final String ENV_UPDATE_ENABLED = "JHOSTER_UPDATE_ENABLED";
    private static final String ENV_GITHUB_TOKEN = "JHOSTER_GITHUB_TOKEN";
    private static final String PROPERTY_UPDATE_REPO = "jhoster.update.repo";
    private static final String PROPERTY_UPDATE_ENABLED = "jhoster.update.enabled";
    private static final String PROPERTY_GITHUB_TOKEN = "jhoster.update.token";
    private static final String GITHUB_API_BASE = "https://api.github.com/repos/";
    private static final String LATEST_RELEASE_SUFFIX = "/releases/latest";
    private static final String HEADER_ACCEPT = "Accept";
    private static final String HEADER_API_VERSION = "X-GitHub-Api-Version";
    private static final String HEADER_USER_AGENT = "User-Agent";
    private static final String HEADER_AUTHORIZATION = "Authorization";
    private static final String VALUE_ACCEPT = "application/vnd.github+json";
    private static final String VALUE_API_VERSION = "2022-11-28";
    private static final String VALUE_USER_AGENT = "JHoster-Launcher";
    private static final String KEY_TAG_NAME = "tag_name";
    private static final long TIMEOUT_SECONDS = 6L;
    private static final Pattern ASSET_PATTERN = Pattern.compile(
        "\\"name\\"\\s*:\\s*\\"([^\\"]+)\\"(?:(?!\\"name\\").)*?"
            + "\\"browser_download_url\\"\\s*:\\s*\\"([^\\"]+)\\"",
        Pattern.DOTALL
    );

    private final HttpClient httpClient;
    private final SemanticVersionCompareTool semanticVersionCompareTool;
    private final DesktopMetadataTool desktopMetadataTool;

    public GitHubReleaseUpdateService() {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(3))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .build();
        this.semanticVersionCompareTool = new SemanticVersionCompareTool();
        this.desktopMetadataTool = new DesktopMetadataTool();
    }

    public CompletableFuture<UpdateCheckResult> checkLatestRelease(String currentVersion) {
        Optional<String> repo = resolveRepository();
        if (repo.isEmpty()) {
            return CompletableFuture.completedFuture(UpdateCheckResult.skipped(
                currentVersion,
                "GitHub release check skipped because update repository is not configured."
            ));
        }

        if (!isUpdateCheckEnabled()) {
            return CompletableFuture.completedFuture(UpdateCheckResult.skipped(
                currentVersion,
                "GitHub release check is disabled."
            ));
        }

        HttpRequest.Builder builder = HttpRequest.newBuilder()
            .uri(URI.create(buildLatestReleaseUrl(repo.get())))
            .timeout(Duration.ofSeconds(TIMEOUT_SECONDS))
            .header(HEADER_ACCEPT, VALUE_ACCEPT)
            .header(HEADER_API_VERSION, VALUE_API_VERSION)
            .header(HEADER_USER_AGENT, VALUE_USER_AGENT)
            .GET();
        resolveGitHubToken().ifPresent(token -> builder.header(HEADER_AUTHORIZATION, "Bearer " + token));

        return httpClient.sendAsync(builder.build(), HttpResponse.BodyHandlers.ofString())
            .orTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
            .thenApply(response -> parseResponse(currentVersion, repo.get(), response))
            .exceptionally(exception -> UpdateCheckResult.failed(
                currentVersion,
                "GitHub release check failed or timed out; starting local desktop."
            ));
    }

    private UpdateCheckResult parseResponse(
        String currentVersion,
        String repository,
        HttpResponse<String> response
    ) {
        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            return UpdateCheckResult.failed(
                currentVersion,
                "GitHub release check returned HTTP " + response.statusCode() + "."
            );
        }

        String body = response.body() == null ? "" : response.body();
        String latestVersion = extractJsonString(body, KEY_TAG_NAME);
        if (latestVersion.isBlank()) {
            return UpdateCheckResult.failed(
                currentVersion,
                "GitHub latest release response did not contain tag_name."
            );
        }

        String releaseUrl = buildReleaseWebUrl(repository, latestVersion);
        if (!semanticVersionCompareTool.isNewer(latestVersion, currentVersion)) {
            return UpdateCheckResult.current(currentVersion, latestVersion, releaseUrl);
        }

        ReleaseAssets assets = resolveReleaseAssets(body);
        return UpdateCheckResult.available(
            currentVersion,
            latestVersion,
            releaseUrl,
            assets.installerAssetName(),
            assets.installerDownloadUrl(),
            assets.checksumDownloadUrl()
        );
    }

    private ReleaseAssets resolveReleaseAssets(String body) {
        String prefix = desktopMetadataTool.installerAssetPrefix();
        String installerName = "";
        String installerUrl = "";
        String checksumUrl = "";

        Matcher matcher = ASSET_PATTERN.matcher(body);
        while (matcher.find()) {
            String name = unescapeJson(matcher.group(1));
            String url = unescapeJson(matcher.group(2));
            if (name.startsWith(prefix) && name.toLowerCase().endsWith(".exe")) {
                installerName = name;
                installerUrl = url;
            }
            if (name.startsWith(prefix) && name.toLowerCase().endsWith(".exe.sha256")) {
                checksumUrl = url;
            }
        }

        if (installerName.isBlank() || installerUrl.isBlank()) {
            return new ReleaseAssets("", "", "");
        }
        return new ReleaseAssets(installerName, installerUrl, checksumUrl);
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
        String metadataRepo = desktopMetadataTool.updateRepository();
        return metadataRepo.isBlank() ? Optional.empty() : Optional.of(metadataRepo);
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
        return desktopMetadataTool.updateEnabled();
    }

    private Optional<String> resolveGitHubToken() {
        String propertyValue = System.getProperty(PROPERTY_GITHUB_TOKEN, "").trim();
        if (!propertyValue.isBlank()) {
            return Optional.of(propertyValue);
        }
        String envValue = System.getenv(ENV_GITHUB_TOKEN);
        if (envValue != null && !envValue.trim().isBlank()) {
            return Optional.of(envValue.trim());
        }
        return Optional.empty();
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

    private String buildReleaseWebUrl(String repository, String tagName) {
        return "https://github.com/" + repository + "/releases/tag/"
            + URLEncoder.encode(tagName, StandardCharsets.UTF_8).replace("+", "%20");
    }

    private String extractJsonString(String json, String key) {
        Pattern pattern = Pattern.compile("\\"" + Pattern.quote(key) + "\\"\\s*:\\s*\\"([^\\"]*)\\"");
        Matcher matcher = pattern.matcher(json);
        if (matcher.find()) {
            return unescapeJson(matcher.group(1));
        }
        return "";
    }

    private String unescapeJson(String value) {
        return value == null ? "" : value.replace("\\/", "/").replace("\\"", "\"").trim();
    }

    private record ReleaseAssets(
        String installerAssetName,
        String installerDownloadUrl,
        String checksumDownloadUrl
    ) {
    }
}
