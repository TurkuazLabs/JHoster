// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\BrandingResourceTool.java
// # 📌 Amac: JHoster logo ve ikon kaynaklarini JavaFX, splash ve tray katmanlarina guvenli sekilde saglar
// # 📌 Modul - Java
// # Version: 3.63.0
// # Aciklama: Resource icindeki branding dosyalarini yukler, UI logo ImageView ve pencere ikonu icin merkezi adaptor gorevi gorur
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import java.io.InputStream;
import java.util.Optional;
import javax.imageio.ImageIO;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

public class BrandingResourceTool {
    private static final String LOGO_RESOURCE = "/assets/branding/jhoster-logo-256.png";
    private static final String ICON_RESOURCE = "/assets/branding/jhoster-logo-64.png";
    
    public Optional<Image> loadFxLogo() {
        return loadFxImage(LOGO_RESOURCE);
    }

    public Optional<Image> loadFxIcon() {
        return loadFxImage(ICON_RESOURCE);
    }

    public Optional<ImageView> createFxLogoView(double size) {
        Optional<Image> image = loadFxLogo();
        if (image.isEmpty()) {
            return Optional.empty();
        }

        ImageView imageView = new ImageView(image.get());
        imageView.setFitWidth(size);
        imageView.setFitHeight(size);
        imageView.setPreserveRatio(true);
        imageView.setSmooth(true);
        return Optional.of(imageView);
    }

    public Optional<java.awt.Image> loadAwtTrayImage() {
        try (InputStream stream = BrandingResourceTool.class.getResourceAsStream(ICON_RESOURCE)) {
            if (stream == null) {
                return Optional.empty();
            }
            return Optional.ofNullable(ImageIO.read(stream));
        } catch (Exception exception) {
            return Optional.empty();
        }
    }

    private Optional<Image> loadFxImage(String resourcePath) {
        try (InputStream stream = BrandingResourceTool.class.getResourceAsStream(resourcePath)) {
            if (stream == null) {
                return Optional.empty();
            }
            return Optional.of(new Image(stream, 0, 0, true, true));
        } catch (Exception exception) {
            return Optional.empty();
        }
    }
}
