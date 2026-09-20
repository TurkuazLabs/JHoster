// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\PanelStatusService.java
// # 📌 Amac: Python panel saglik durumunu kontrol eder
// # 📌 Modul - Java
// # Version: 3.2.1
// # Aciklama: HTTP health endpoint uzerinden panelin calisip calismadigini belirler
//
// Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;

public class PanelStatusService {
    private static final int CONNECT_TIMEOUT_MS = 1200;
    private static final int READ_TIMEOUT_MS = 1200;
    private static final int HTTP_OK = 200;

    public boolean isPanelRunning(String healthUrl) {
        try {
            URL url = URI.create(healthUrl).toURL();
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(CONNECT_TIMEOUT_MS);
            connection.setReadTimeout(READ_TIMEOUT_MS);
            connection.setRequestMethod("GET");
            return connection.getResponseCode() == HTTP_OK;
        } catch (IOException exception) {
            return false;
        }
    }
}
