// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\AutomaticReleaseUpdateService.java
// # 📌 Amac: GitHub release NSIS setup paketini indirir, SHA-256 dogrular ve sessiz update baslatir
// # 📌 Modul - Java
// # Version: 3.80.0
// # Aciklama: Splash otomatik update akisinda setup EXE + SHA256 assetlerini guvenli sekilde indirir ve /S /UPDATE=1 ile baslatir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.UpdateCheckResult;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.time.Duration;
import java.util.HexFormat;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

public final class AutomaticReleaseUpdateService {
    private static final String ENV_GITHUB_TOKEN = "JHOSTER_GITHUB_TOKEN";
    private static final String PROPERTY_GITHUB_TOKEN = "jhoster.update.token";
    private static final String HEADER_ACCEPT = "Accept";
    private static final String HEADER_USER_AGENT = "User-Agent";
    private static final String HEADER_AUTHORIZATION = "Authorization";
    private static final String VALUE_USER_AGENT = "JHoster-AutoUpdater";
    private static final Duration REQUEST_TIMEOUT = Duration.ofSeconds(90);

    private final HttpClient httpClient;

    public AutomaticReleaseUpdateService() {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .followRedirects(HttpClient.Redirect.ALWAYS)
            .build();
    }

    public CompletableFuture<Boolean> downloadVerifyAndLaunch(UpdateCheckResult result) {
        return CompletableFuture.supplyAsync(() -> {
            if (result == null || !result.isUpdateAvailable() || !result.hasVerifiedInstallerAssets()) {
                return false;
            }

            try {
                Path updateDirectory = resolveUpdateDirectory(result.getLatestVersion());
                Files.createDirectories(updateDirectory);

                Path installerPath = updateDirectory.resolve(safeFileName(result.getInstallerAssetName()));
                Path checksumPath = updateDirectory.resolve(installerPath.getFileName().toString() + ".sha256");

                download(result.getInstallerDownloadUrl(), installerPath, "application/octet-stream");
                download(result.getChecksumDownloadUrl(), checksumPath, "text/plain");

                String expectedHash = readExpectedSha256(checksumPath);
                String actualHash = sha256(installerPath);
                if (expectedHash.isBlank() || !expectedHash.equalsIgnoreCase(actualHash)) {
                    Files.deleteIfExists(installerPath);
                    return false;
                }

                new ProcessBuilder(installerPath.toString(), "/S", "/UPDATE=1")
                    .directory(updateDirectory.toFile())
                    .start();
                return true;
            } catch (Exception exception) {
                return false;
            }
        });
    }

    private void download(String url, Path target, String accept) throws IOException, InterruptedException {
        HttpRequest.Builder builder = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .timeout(REQUEST_TIMEOUT)
            .header(HEADER_ACCEPT, accept)
            .header(HEADER_USER_AGENT, VALUE_USER_AGENT)
            .GET();
        resolveGitHubToken().ifPresent(token -> builder.header(HEADER_AUTHORIZATION, "Bearer " + token));

        HttpResponse<Path> response = httpClient.send(
            builder.build(),
            HttpResponse.BodyHandlers.ofFile(target)
        );
        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            Files.deleteIfExists(target);
            throw new IOException("Update asset download returned HTTP " + response.statusCode());
        }
    }

    private Path resolveUpdateDirectory(String version) {
        String safeVersion = version == null ? "unknown" : version.replaceAll("[^A-Za-z0-9._-]", "_");
        return Path.of(System.getProperty("java.io.tmpdir"), "JHoster", "updates", safeVersion);
    }

    private String safeFileName(String value) {
        String normalized = value == null ? "" : value.replaceAll("[^A-Za-z0-9._-]", "_");
        return normalized.isBlank() ? "JHoster-Setup.exe" : normalized;
    }

    private String readExpectedSha256(Path checksumPath) throws IOException {
        String text = Files.readString(checksumPath, StandardCharsets.UTF_8).trim();
        if (text.isBlank()) {
            return "";
        }
        String firstToken = text.split("\\s+", 2)[0].trim();
        return firstToken.matches("(?i)[0-9a-f]{64}") ? firstToken : "";
    }

    private String sha256(Path filePath) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (var stream = Files.newInputStream(filePath)) {
            byte[] buffer = new byte[64 * 1024];
            int read;
            while ((read = stream.read(buffer)) >= 0) {
                if (read > 0) {
                    digest.update(buffer, 0, read);
                }
            }
        }
        return HexFormat.of().formatHex(digest.digest());
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
}
