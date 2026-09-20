// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\TrayMenuTool.java
// # 📌 Amac: JHoster Desktop sistem tepsisi ikonunu ve popup menuyu guvenli sekilde yonetir
// # 📌 Modul - Java
// # Version: 3.62.8
// # Aciklama: Java AWT SystemTray entegrasyonunu Tool katmaninda izole eder
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import java.awt.AWTException;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.PopupMenu;
import java.awt.RenderingHints;
import java.awt.SystemTray;
import java.awt.TrayIcon;
import java.awt.image.BufferedImage;

public class TrayMenuTool {
    private static final int ICON_SIZE = 16;
    private static final int ICON_MARGIN = 2;
    private static final int ICON_ARC = 6;
    private static final int ICON_LETTER_X = 5;
    private static final int ICON_LETTER_Y = 12;
    private static final String ICON_LETTER = "J";
    private static final Color ICON_BACKGROUND = new Color(0, 148, 255);
    private static final Color ICON_FOREGROUND = Color.WHITE;
    private static final Color ICON_BORDER = new Color(0, 92, 180);

    private TrayIcon trayIcon;

    public boolean isSupported() {
        return SystemTray.isSupported();
    }

    public boolean install(String tooltip, PopupMenu popupMenu) {
        if (!isSupported() || trayIcon != null) {
            return false;
        }

        TrayIcon icon = new TrayIcon(createImage(), tooltip, popupMenu);
        icon.setImageAutoSize(true);

        try {
            SystemTray.getSystemTray().add(icon);
            trayIcon = icon;
            return true;
        } catch (AWTException exception) {
            trayIcon = null;
            return false;
        }
    }

    public void remove() {
        if (trayIcon != null && isSupported()) {
            SystemTray.getSystemTray().remove(trayIcon);
        }
        trayIcon = null;
    }

    public void notifyInfo(String title, String message) {
        if (trayIcon != null) {
            trayIcon.displayMessage(title, message, TrayIcon.MessageType.INFO);
        }
    }

    public void notifyWarning(String title, String message) {
        if (trayIcon != null) {
            trayIcon.displayMessage(title, message, TrayIcon.MessageType.WARNING);
        }
    }

    private Image createImage() {
        java.util.Optional<Image> brandedImage = new BrandingResourceTool().loadAwtTrayImage();
        if (brandedImage.isPresent()) {
            return brandedImage.get();
        }

        BufferedImage image = new BufferedImage(ICON_SIZE, ICON_SIZE, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        graphics.setColor(ICON_BACKGROUND);
        graphics.fillRoundRect(ICON_MARGIN, ICON_MARGIN, ICON_SIZE - ICON_MARGIN * 2, ICON_SIZE - ICON_MARGIN * 2, ICON_ARC, ICON_ARC);
        graphics.setColor(ICON_BORDER);
        graphics.drawRoundRect(ICON_MARGIN, ICON_MARGIN, ICON_SIZE - ICON_MARGIN * 2, ICON_SIZE - ICON_MARGIN * 2, ICON_ARC, ICON_ARC);
        graphics.setColor(ICON_FOREGROUND);
        graphics.drawString(ICON_LETTER, ICON_LETTER_X, ICON_LETTER_Y);
        graphics.dispose();
        return image;
    }
}
