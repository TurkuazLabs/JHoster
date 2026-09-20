// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\ServiceManagerSummary.java
// # 📌 Amac: Desktop service manager aksiyon sonucunu standart model olarak tasir
// # 📌 Modul - Java
// # Version: 3.40.0
// # Aciklama: Apache, Nginx, MySQL ve PHP servisleri icin status, operation ve log bilgisini View katmanina aktarir
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

public final class ServiceManagerSummary {
    private static final String EMPTY_VALUE = "";
    private static final String LOG_SEPARATOR = "\n";
    private static final String LABEL_TITLE = "title=";
    private static final String LABEL_SUCCESS = "success=";
    private static final String LABEL_SERVICE = "service=";
    private static final String LABEL_OPERATION = "operation=";
    private static final String LABEL_STATUS = "status=";
    private static final String LABEL_MESSAGE = "message=";
    private static final int VALUE_NOT_AVAILABLE = -1;

    private final String title;
    private final boolean success;
    private final String serviceCode;
    private final String operation;
    private final String status;
    private final String message;
    private final int recordCount;
    private final String rawLog;

    public ServiceManagerSummary(
        String title,
        boolean success,
        String serviceCode,
        String operation,
        String status,
        String message,
        int recordCount,
        String rawLog
    ) {
        this.title = normalize(title);
        this.success = success;
        this.serviceCode = normalize(serviceCode);
        this.operation = normalize(operation);
        this.status = normalize(status);
        this.message = normalize(message);
        this.recordCount = recordCount;
        this.rawLog = normalize(rawLog);
    }

    public static ServiceManagerSummary empty(String title, String rawLog) {
        return new ServiceManagerSummary(title, false, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, VALUE_NOT_AVAILABLE, rawLog);
    }

    public String getTitle() {
        return title;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getServiceCode() {
        return serviceCode;
    }

    public String getOperation() {
        return operation;
    }

    public String getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }

    public int getRecordCount() {
        return recordCount;
    }

    public boolean hasServiceCode() {
        return !serviceCode.isBlank();
    }

    public boolean hasStatus() {
        return !status.isBlank();
    }

    public boolean hasRecordCount() {
        return recordCount >= 0;
    }

    public String toLogBlock() {
        return LABEL_TITLE + title
            + LOG_SEPARATOR + LABEL_SUCCESS + success
            + LOG_SEPARATOR + LABEL_SERVICE + serviceCode
            + LOG_SEPARATOR + LABEL_OPERATION + operation
            + LOG_SEPARATOR + LABEL_STATUS + status
            + LOG_SEPARATOR + LABEL_MESSAGE + message
            + LOG_SEPARATOR + rawLog;
    }

    private String normalize(String value) {
        return value == null ? EMPTY_VALUE : value;
    }
}
