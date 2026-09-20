// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\HostsAutoDesktopService.java
// # 📌 Amac: Desktop tarafindan agent hosts auto endpointlerini cagirir
// # 📌 Modul - Java
// # Version: 3.68.0
// # Aciklama: Hosts inspect, repair-plan ve repair islemlerini HTTP tool uzerinden calistirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.HostsAutoSummary;
import com.jhoster.desktop.tools.HttpRequestTool;

public final class HostsAutoDesktopService {
    private final HttpRequestTool httpRequestTool;
    private final HostsAutoResultFormatterService hostsAutoResultFormatterService;

    public HostsAutoDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.hostsAutoResultFormatterService = new HostsAutoResultFormatterService();
    }

    public HostsAutoSummary inspectSummary() {
        DesktopHttpResult result = httpRequestTool.get(
            DesktopApiConfig.resolveUrl(DesktopApiConfig.HOSTS_AUTO_INSPECT_ROUTE + DesktopApiConfig.HOSTS_AUTO_REAL_WRITE_QUERY)
        );
        return hostsAutoResultFormatterService.format(result);
    }

    public HostsAutoSummary repairPlanSummary() {
        DesktopHttpResult result = httpRequestTool.get(
            DesktopApiConfig.resolveUrl(DesktopApiConfig.HOSTS_AUTO_REPAIR_PLAN_ROUTE + DesktopApiConfig.HOSTS_AUTO_REPAIR_PLAN_REAL_QUERY)
        );
        return hostsAutoResultFormatterService.format(result);
    }

    public HostsAutoSummary repairSummary() {
        DesktopHttpResult result = httpRequestTool.post(
            DesktopApiConfig.resolveUrl(DesktopApiConfig.HOSTS_AUTO_REPAIR_ROUTE + DesktopApiConfig.HOSTS_AUTO_REPAIR_REAL_QUERY)
        );
        return hostsAutoResultFormatterService.format(result);
    }
}
