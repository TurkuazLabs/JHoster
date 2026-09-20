// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\HostsAutoResultFormatterService.java
// # 📌 Amac: Agent hosts auto HTTP cevabini desktop ozet modeline cevirir
// # 📌 Modul - Java
// # Version: 3.68.0
// # Aciklama: Inspect, repair-plan ve repair cevaplarini UI tarafinda okunabilir hale getirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.HostsAutoSummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class HostsAutoResultFormatterService {
    private static final String TITLE_HOSTS_AUTO = "Hosts Auto";
    private static final String KEY_SUCCESS = "success";
    private static final String KEY_STATUS = "status";
    private static final String KEY_MESSAGE = "message";
    private static final String KEY_EXPECTED_COUNT = "expected_count";
    private static final String KEY_MANAGED_COUNT = "managed_count";
    private static final String KEY_MISSING_COUNT = "missing_count";
    private static final String KEY_STALE_COUNT = "stale_count";
    private static final String KEY_WRONG_IP_COUNT = "wrong_ip_count";
    private static final String KEY_DUPLICATE_COUNT = "duplicate_count";
    private static final String KEY_EXTERNAL_CONFLICT_COUNT = "external_conflict_count";
    private static final String KEY_REPAIR_REQUIRED = "repair_required";
    private static final String KEY_SAFE_TO_REPAIR = "safe_to_repair";
    private static final String KEY_APPLY_MODE = "apply_mode";
    private static final String KEY_TARGET_FILE = "target_file";
    private static final String KEY_ENTRY_COUNT = "entry_count";

    private final JsonTextExtractorTool jsonTextExtractorTool;

    public HostsAutoResultFormatterService() {
        this.jsonTextExtractorTool = new JsonTextExtractorTool();
    }

    public HostsAutoSummary format(DesktopHttpResult result) {
        if (result == null) {
            return HostsAutoSummary.empty();
        }

        String body = result.getBody();
        boolean success = result.isSuccess()
            && jsonTextExtractorTool.extractBoolean(body, KEY_SUCCESS, result.isSuccess());
        int expectedCount = jsonTextExtractorTool.extractInt(body, KEY_EXPECTED_COUNT,
            jsonTextExtractorTool.extractInt(body, KEY_ENTRY_COUNT, 0));
        int managedCount = jsonTextExtractorTool.extractInt(body, KEY_MANAGED_COUNT, 0);

        return new HostsAutoSummary(
            TITLE_HOSTS_AUTO,
            success,
            jsonTextExtractorTool.extractString(body, KEY_STATUS),
            jsonTextExtractorTool.extractString(body, KEY_MESSAGE),
            expectedCount,
            managedCount,
            jsonTextExtractorTool.extractInt(body, KEY_MISSING_COUNT, 0),
            jsonTextExtractorTool.extractInt(body, KEY_STALE_COUNT, 0),
            jsonTextExtractorTool.extractInt(body, KEY_WRONG_IP_COUNT, 0),
            jsonTextExtractorTool.extractInt(body, KEY_DUPLICATE_COUNT, 0),
            jsonTextExtractorTool.extractInt(body, KEY_EXTERNAL_CONFLICT_COUNT, 0),
            jsonTextExtractorTool.extractBoolean(body, KEY_REPAIR_REQUIRED, false),
            jsonTextExtractorTool.extractBoolean(body, KEY_SAFE_TO_REPAIR, success),
            jsonTextExtractorTool.extractString(body, KEY_APPLY_MODE),
            jsonTextExtractorTool.extractString(body, KEY_TARGET_FILE),
            result.toLogBlock()
        );
    }
}
