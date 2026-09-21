// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java
// # 📌 Amac: Desktop uygulamadan agent HTTP endpointlerine erisim adaptorudur
// # 📌 Modul - Java
// # Version: 3.79.0
// # Aciklama: Java HttpClient ile GET ve POST isteklerini Tool katmaninda izole eder
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import com.jhoster.desktop.models.DesktopHttpResult;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class HttpRequestTool {
    private static final int TIMEOUT_SECONDS = 6;
    private static final int LONG_RUNNING_TIMEOUT_SECONDS = 300;
    private static final String GET_METHOD = "GET";
    private static final String POST_METHOD = "POST";
    private static final String CONTENT_TYPE_HEADER = "Content-Type";
    private static final String JSON_CONTENT_TYPE = "application/json; charset=UTF-8";

    private final HttpClient httpClient;

    public HttpRequestTool() {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(TIMEOUT_SECONDS))
            .build();
    }

    public DesktopHttpResult get(String url) {
        return send(url, GET_METHOD, "", "", TIMEOUT_SECONDS);
    }

    public DesktopHttpResult post(String url) {
        return send(url, POST_METHOD, "", "", TIMEOUT_SECONDS);
    }

    public DesktopHttpResult postJson(String url, String jsonBody) {
        return send(url, POST_METHOD, jsonBody, JSON_CONTENT_TYPE, LONG_RUNNING_TIMEOUT_SECONDS);
    }

    private DesktopHttpResult send(String url, String method, String body, String contentType, int timeoutSeconds) {
        String safeBody = body == null ? "" : body;
        HttpRequest.BodyPublisher bodyPublisher = safeBody.isBlank()
            ? HttpRequest.BodyPublishers.noBody()
            : HttpRequest.BodyPublishers.ofString(safeBody, StandardCharsets.UTF_8);

        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .timeout(Duration.ofSeconds(timeoutSeconds));

        if (contentType != null && !contentType.isBlank()) {
            requestBuilder.header(CONTENT_TYPE_HEADER, contentType);
        }

        HttpRequest request = requestBuilder
            .method(method, bodyPublisher)
            .build();

        try {
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            return DesktopHttpResult.success(response.statusCode(), response.body());
        } catch (IOException exception) {
            return DesktopHttpResult.failure(exception.getMessage());
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            return DesktopHttpResult.failure(exception.getMessage());
        } catch (IllegalArgumentException exception) {
            return DesktopHttpResult.failure(exception.getMessage());
        }
    }
}
