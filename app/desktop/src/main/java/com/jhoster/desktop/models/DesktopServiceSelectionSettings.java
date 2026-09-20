// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\DesktopServiceSelectionSettings.java
// # 📌 Amac: Desktop servis secim ayarlarini tasir
// # 📌 Modul - Java
// # Version: 3.55.1
// # Aciklama: Apache/Nginx aktif web server modu ve Start All kapsamindaki servis secimlerini merkezi model olarak tutar
// # Bagimli Oldugu Katman: Model

package com.jhoster.desktop.models;

import com.jhoster.desktop.config.DesktopApiConfig;

public class DesktopServiceSelectionSettings {
    private String activeWebServer;
    private boolean apacheEnabled;
    private boolean nginxEnabled;
    private boolean mysqlEnabled;
    private boolean phpEnabled;
    private boolean mailpitEnabled;

    public DesktopServiceSelectionSettings(
        String activeWebServer,
        boolean apacheEnabled,
        boolean nginxEnabled,
        boolean mysqlEnabled,
        boolean phpEnabled,
        boolean mailpitEnabled
    ) {
        this.activeWebServer = normalizeWebServer(activeWebServer);
        this.apacheEnabled = apacheEnabled;
        this.nginxEnabled = nginxEnabled;
        this.mysqlEnabled = mysqlEnabled;
        this.phpEnabled = phpEnabled;
        this.mailpitEnabled = mailpitEnabled;
    }

    public static DesktopServiceSelectionSettings defaults() {
        return new DesktopServiceSelectionSettings(
            DesktopApiConfig.WEB_SERVER_PROFILE_APACHE,
            true,
            false,
            true,
            true,
            true
        );
    }

    public String getActiveWebServer() {
        return normalizeWebServer(activeWebServer);
    }

    public void setActiveWebServer(String activeWebServer) {
        this.activeWebServer = normalizeWebServer(activeWebServer);
    }

    public boolean isApacheEnabled() {
        return apacheEnabled;
    }

    public void setApacheEnabled(boolean apacheEnabled) {
        this.apacheEnabled = apacheEnabled;
    }

    public boolean isNginxEnabled() {
        return nginxEnabled;
    }

    public void setNginxEnabled(boolean nginxEnabled) {
        this.nginxEnabled = nginxEnabled;
    }

    public boolean isMysqlEnabled() {
        return mysqlEnabled;
    }

    public void setMysqlEnabled(boolean mysqlEnabled) {
        this.mysqlEnabled = mysqlEnabled;
    }

    public boolean isPhpEnabled() {
        return phpEnabled;
    }

    public void setPhpEnabled(boolean phpEnabled) {
        this.phpEnabled = phpEnabled;
    }

    public boolean isMailpitEnabled() {
        return mailpitEnabled;
    }

    public void setMailpitEnabled(boolean mailpitEnabled) {
        this.mailpitEnabled = mailpitEnabled;
    }

    public boolean isServiceEnabled(String serviceCode) {
        if (DesktopApiConfig.SERVICE_CODE_APACHE.equals(serviceCode)) {
            return apacheEnabled && DesktopApiConfig.WEB_SERVER_PROFILE_APACHE.equals(getActiveWebServer());
        }

        if (DesktopApiConfig.SERVICE_CODE_NGINX.equals(serviceCode)) {
            return nginxEnabled && DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(getActiveWebServer());
        }

        if (DesktopApiConfig.SERVICE_CODE_MYSQL.equals(serviceCode)) {
            return mysqlEnabled;
        }

        if (DesktopApiConfig.SERVICE_CODE_PHP.equals(serviceCode)) {
            return phpEnabled;
        }

        if (DesktopApiConfig.SERVICE_CODE_MAILPIT.equals(serviceCode)) {
            return mailpitEnabled;
        }

        return false;
    }

    public String activeWebServerServiceCode() {
        if (DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(getActiveWebServer())) {
            return DesktopApiConfig.SERVICE_CODE_NGINX;
        }
        return DesktopApiConfig.SERVICE_CODE_APACHE;
    }

    public DesktopServiceSelectionSettings normalized() {
        String selected = getActiveWebServer();
        return new DesktopServiceSelectionSettings(
            selected,
            DesktopApiConfig.WEB_SERVER_PROFILE_APACHE.equals(selected) && apacheEnabled,
            DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(selected) && nginxEnabled,
            mysqlEnabled,
            phpEnabled,
            mailpitEnabled
        );
    }

    private String normalizeWebServer(String value) {
        if (DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equalsIgnoreCase(String.valueOf(value))) {
            return DesktopApiConfig.WEB_SERVER_PROFILE_NGINX;
        }
        return DesktopApiConfig.WEB_SERVER_PROFILE_APACHE;
    }
}
