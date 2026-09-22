// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\BrowserTool.java
// # 📌 Amac: Sistem varsayilan tarayicisinda panel URL acma adaptorudur
// # 📌 Modul - Java
// # Version: 3.80.0
// # Aciklama: Desktop website ve mailto entegrasyonunu Tool katmaninda izole eder
//
// Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import java.awt.Desktop;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

public class BrowserTool {
    public void open(String url) {
        if (!Desktop.isDesktopSupported()) {
            return;
        }

        try {
            Desktop.getDesktop().browse(new URI(url));
        } catch (IOException | URISyntaxException exception) {
            // Browser acilamiyorsa UI akisi kesilmez.
        }
    }

    public void openMail(String emailAddress) {
        if (!Desktop.isDesktopSupported()) {
            return;
        }

        try {
            Desktop.getDesktop().mail(new URI("mailto:" + emailAddress));
        } catch (IOException | URISyntaxException exception) {
            // Mail client acilamiyorsa UI akisi kesilmez.
        }
    }
}
