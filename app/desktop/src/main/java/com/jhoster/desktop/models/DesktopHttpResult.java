// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java
// # 📌 Amac: Desktop HTTP istek sonucunu standart model olarak tasir
// # 📌 Modul - Java
// # Version: 3.35.0
// # Aciklama: API client tarafindan donen status code, body ve hata bilgisini View katmanina guvenli sekilde aktarir
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

public final class DesktopHttpResult {
    private static final String EMPTY_BODY_MESSAGE = "empty response body";
    private static final String ERROR_PREFIX = "error: ";
    private static final int HTTP_SUCCESS_MIN = 200;
    private static final int HTTP_SUCCESS_MAX = 299;

    private final int statusCode;
    private final String body;
    private final String errorMessage;

    private DesktopHttpResult(int statusCode, String body, String errorMessage) {
        this.statusCode = statusCode;
        this.body = body == null ? "" : body;
        this.errorMessage = errorMessage == null ? "" : errorMessage;
    }

    public static DesktopHttpResult success(int statusCode, String body) {
        return new DesktopHttpResult(statusCode, body, "");
    }

    public static DesktopHttpResult failure(String errorMessage) {
        return new DesktopHttpResult(0, "", errorMessage);
    }

    public int getStatusCode() {
        return statusCode;
    }

    public String getBody() {
        return body;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public boolean isSuccess() {
        return errorMessage.isBlank() && statusCode >= HTTP_SUCCESS_MIN && statusCode <= HTTP_SUCCESS_MAX;
    }

    public String toLogBlock() {
        if (!errorMessage.isBlank()) {
            return ERROR_PREFIX + errorMessage;
        }

        String responseBody = body.isBlank() ? EMPTY_BODY_MESSAGE : body;
        return "status=" + statusCode + "\n" + responseBody;
    }
}
