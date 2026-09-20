// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\DesktopServiceSelectionService.java
// # 📌 Amac: Desktop servis secim ayarlari icin is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.55.1
// # Aciklama: Ayarlar menusu, Start All ve web server secimi icin merkezi servis secim kararlarini saglar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopServiceSelectionSettings;
import com.jhoster.desktop.repositories.DesktopServiceSelectionRepository;

public class DesktopServiceSelectionService {
    private static final String DISABLED_BY_SETTINGS_PREFIX = "Service disabled by settings: ";
    private static final String SETTINGS_SAVED_PREFIX = "Service settings saved: ";

    private final DesktopServiceSelectionRepository repository;

    public DesktopServiceSelectionService() {
        this.repository = new DesktopServiceSelectionRepository();
    }

    public DesktopServiceSelectionSettings loadSettings() {
        return repository.load();
    }

    public String saveSettings(DesktopServiceSelectionSettings settings) {
        DesktopServiceSelectionSettings safeSettings = settings == null ? DesktopServiceSelectionSettings.defaults() : settings.normalized();
        repository.save(safeSettings);
        return SETTINGS_SAVED_PREFIX + safeSettings.getActiveWebServer();
    }

    public boolean canStart(String serviceCode) {
        return loadSettings().isServiceEnabled(serviceCode);
    }

    public String disabledMessage(String serviceCode) {
        return DISABLED_BY_SETTINGS_PREFIX + serviceCode;
    }

    public boolean isWebServer(String serviceCode) {
        return DesktopApiConfig.SERVICE_CODE_APACHE.equals(serviceCode) || DesktopApiConfig.SERVICE_CODE_NGINX.equals(serviceCode);
    }
}
