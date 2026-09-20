// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java
// # 📌 Amac: Desktop uygulamadan agent HTTP endpointlerine erisim adaptorudur
// # 📌 Modul - Java
// # Version: 3.35.0
// # Aciklama: Java HttpClient ile GET ve POST isteklerini Tool katmaninda izole eder
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import com.jhoster.desktop.models.DesktopHttpResult;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public final class HttpRequestTool {
    private static final int TIMEOUT_SECONDS = 6;
    private static final String GET_METHOD = "GET";
    private static final String POST_METHOD = "POST";

    private final HttpClient httpClient;

    public HttpRequestTool() {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(TIMEOUT_SECONDS))
            .build();
    }

    public DesktopHttpResult get(String url) {
        return send(url, GET_METHOD);
    }

    public DesktopHttpResult post(String url) {
        return send(url, POST_METHOD);
    }

    private DesktopHttpResult send(String url, String method) {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .timeout(Duration.ofSeconds(TIMEOUT_SECONDS))
            .method(method, HttpRequest.BodyPublishers.noBody())
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
