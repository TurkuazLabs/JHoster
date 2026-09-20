// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\PackageDownloadDesktopService.java
// # 📌 Amac: Desktop package downloader is kurallarini agent API uzerinden yonetir
// # 📌 Modul - Java
// # Version: 3.58.0
// # Aciklama: Katalog, plan, download ve install aksiyonlarini package-downloads endpointine baglar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.PackageDownloadSummary;
import com.jhoster.desktop.tools.HttpRequestTool;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public final class PackageDownloadDesktopService {
    private static final String PATH_SEPARATOR = "/";
    private static final String PLAN_ACTION = "/plan";
    private static final String DOWNLOAD_ACTION = "/download";
    private static final String INSTALL_ACTION = "/install";
    private static final String QUERY_DRY_RUN_FALSE = "?dry_run=false";
    private static final String QUERY_DRY_RUN_TRUE = "?dry_run=true";

    private final HttpRequestTool httpRequestTool;
    private final PackageDownloadResultFormatterService formatterService;

    public PackageDownloadDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.formatterService = new PackageDownloadResultFormatterService();
    }

    public PackageDownloadSummary catalogSummary() {
        return formatterService.format("Package Catalog", "Indirilebilir paket katalog listesi", listPackages());
    }

    public PackageDownloadSummary planSummary(String packageCode) {
        return formatterService.format("Package Plan", packageCode, getPlan(packageCode));
    }

    public PackageDownloadSummary downloadSummary(String packageCode) {
        return formatterService.format("Package Download", packageCode, downloadPackage(packageCode, false));
    }

    public PackageDownloadSummary installSummary(String packageCode) {
        return formatterService.format("Package Install", packageCode, installPackage(packageCode, false));
    }

    public DesktopHttpResult listPackages() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.PACKAGE_DOWNLOADS_ROUTE));
    }

    public DesktopHttpResult getPlan(String packageCode) {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(buildPackageRoute(packageCode) + PLAN_ACTION));
    }

    public DesktopHttpResult downloadPackage(String packageCode, boolean dryRun) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildPackageRoute(packageCode) + DOWNLOAD_ACTION) + buildDryRunQuery(dryRun));
    }

    public DesktopHttpResult installPackage(String packageCode, boolean dryRun) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildPackageRoute(packageCode) + INSTALL_ACTION) + buildDryRunQuery(dryRun));
    }

    private String buildPackageRoute(String packageCode) {
        return DesktopApiConfig.PACKAGE_DOWNLOADS_ROUTE + PATH_SEPARATOR + encode(packageCode);
    }

    private String buildDryRunQuery(boolean dryRun) {
        return dryRun ? QUERY_DRY_RUN_TRUE : QUERY_DRY_RUN_FALSE;
    }

    private String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value.trim(), StandardCharsets.UTF_8);
    }
}
