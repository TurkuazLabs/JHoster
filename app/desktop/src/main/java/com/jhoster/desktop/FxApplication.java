// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\FxApplication.java
// # 📌 Amac: JHoster JavaFX desktop launcher sahnesini modern tema ile olusturur
// # 📌 Modul - Java
// # Version: 3.79.0
// # Aciklama: Direkt desktop gelistirme acilisi icin JavaFX Application yasam dongusunu yonetir; ana giris artik LauncherBootstrapApplication uzerindedir
// # Bagimli Oldugu Katman: Controller

package com.jhoster.desktop;

import com.jhoster.desktop.controllers.LauncherController;
import com.jhoster.desktop.services.TrayMenuDesktopService;
import com.jhoster.desktop.tools.DevModeTool;
import com.jhoster.desktop.tools.DesktopVersionTool;
import com.jhoster.desktop.tools.BrandingResourceTool;
import java.net.URL;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public final class FxApplication extends Application {
    private static final String APP_TITLE = "JHoster Desktop";
    private static final String APP_EDITION = "Community";
    private static final String THEME_RESOURCE = "/styles/jhoster-modern.css";
    private static final double WINDOW_WIDTH = 1600;
    private static final double WINDOW_HEIGHT = 940;
    private static final double MIN_WINDOW_WIDTH = 1280;
    private static final double MIN_WINDOW_HEIGHT = 760;

    @Override
    public void start(Stage stage) {
        boolean devModeEnabled = new DevModeTool().isDevMode(getParameters().getRaw());
        LauncherController controller = new LauncherController(devModeEnabled);
        double windowWidth = devModeEnabled ? WINDOW_WIDTH : 1280;
        double windowHeight = devModeEnabled ? WINDOW_HEIGHT : 820;
        double minWindowWidth = devModeEnabled ? MIN_WINDOW_WIDTH : 1120;
        double minWindowHeight = devModeEnabled ? MIN_WINDOW_HEIGHT : 720;
        Scene scene = new Scene(controller.createView(), windowWidth, windowHeight);
        applyTheme(scene);

        stage.setTitle(APP_TITLE + " 3.79.0 " + APP_EDITION);
        new BrandingResourceTool().loadFxIcon().ifPresent(icon -> stage.getIcons().add(icon));
        stage.setMinWidth(minWindowWidth);
        stage.setMinHeight(minWindowHeight);
        stage.setScene(scene);
        stage.setMaximized(true);
        stage.show();
        new TrayMenuDesktopService().install(stage);
    }

    private void applyTheme(Scene scene) {
        URL themeUrl = FxApplication.class.getResource(THEME_RESOURCE);
        if (themeUrl != null) {
            scene.getStylesheets().add(themeUrl.toExternalForm());
        }
    }
}
