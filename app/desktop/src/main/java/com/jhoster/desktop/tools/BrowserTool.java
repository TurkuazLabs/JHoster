// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\BrowserTool.java
// # 📌 Amac: Sistem varsayilan tarayicisinda panel URL acma adaptorudur
// # 📌 Modul - Java
// # Version: 3.2.1
// # Aciklama: Desktop browser entegrasyonunu Tool katmaninda izole eder
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
            // MVP: user-visible log sonraki surumde controller'a geri dondurulecek.
        }
    }
}
