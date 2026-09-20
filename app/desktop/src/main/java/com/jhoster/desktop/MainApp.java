// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\MainApp.java
// # 📌 Amac: JHoster launcher bootstrap uygulamasini NetBeans ve Maven exec ile baslatir
// # 📌 Modul - Java
// # Version: 3.61.1
// # Aciklama: Ana giris noktasi olarak splash, GitHub Release check ve desktop acilis akisini baslatir
// # Bagimli Oldugu Katman: Controller

package com.jhoster.desktop;

import com.jhoster.desktop.launcher.LauncherBootstrapApplication;
import javafx.application.Application;

public final class MainApp {
    private MainApp() {
    }

    public static void main(String[] args) {
        Application.launch(LauncherBootstrapApplication.class, args);
    }
}
