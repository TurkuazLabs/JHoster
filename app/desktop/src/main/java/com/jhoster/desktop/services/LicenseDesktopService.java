// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\LicenseDesktopService.java
// # 📌 Amac: Desktop tarafindan agent lisans endpointini okur
// # 📌 Modul - Java
// # Version: 3.65.0
// # Aciklama: License status ve feature registry verisini HTTP tool ile alir ve UI ozet modeline cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.LicensePlanSummary;
import com.jhoster.desktop.tools.HttpRequestTool;

public final class LicenseDesktopService {
    private final HttpRequestTool httpRequestTool;
    private final LicenseResultFormatterService licenseResultFormatterService;

    public LicenseDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.licenseResultFormatterService = new LicenseResultFormatterService();
    }

    public LicensePlanSummary currentSummary() {
        DesktopHttpResult result = httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.LICENSE_ROUTE));
        return licenseResultFormatterService.format(result);
    }
}
