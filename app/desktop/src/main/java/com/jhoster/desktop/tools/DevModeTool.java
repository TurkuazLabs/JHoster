// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\DevModeTool.java
// # 📌 Amac: JHoster Desktop dev mode baslangic kosullarini algilar
// # 📌 Modul - Java
// # Version: 3.58.1
// # Aciklama: Shift basili acilis, --dev argumani, system property ve environment flag ile gelistirici modunu acan arac katmanidir
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import com.sun.jna.Library;
import com.sun.jna.Native;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public final class DevModeTool {
    private static final String ARG_DEV_MODE = "--dev";
    private static final String PROPERTY_DEV_MODE = "jhoster.dev";
    private static final String ENV_DEV_MODE = "JHOSTER_DEV_MODE";
    private static final String TRUE_VALUE = "true";
    private static final String ENABLED_VALUE = "enabled";
    private static final String ONE_VALUE = "1";
    private static final String WINDOWS_NAME_TOKEN = "win";
    private static final String OS_NAME_PROPERTY = "os.name";
    private static final int VK_SHIFT = 0x10;
    private static final int KEY_DOWN_MASK = 0x8000;

    public boolean isDevMode(List<String> launchArguments) {
        return hasDevArgument(launchArguments)
            || hasDevSystemProperty()
            || hasDevEnvironmentFlag()
            || isShiftDownOnWindows();
    }

    private boolean hasDevArgument(List<String> launchArguments) {
        if (launchArguments == null) {
            return false;
        }

        return launchArguments.stream()
            .filter(argument -> argument != null)
            .map(String::trim)
            .anyMatch(ARG_DEV_MODE::equalsIgnoreCase);
    }

    private boolean hasDevSystemProperty() {
        return isEnabled(System.getProperty(PROPERTY_DEV_MODE));
    }

    private boolean hasDevEnvironmentFlag() {
        Map<String, String> env = System.getenv();
        return isEnabled(env.get(ENV_DEV_MODE));
    }

    private boolean isEnabled(String value) {
        if (value == null) {
            return false;
        }

        String normalized = value.trim().toLowerCase(Locale.ROOT);
        return TRUE_VALUE.equals(normalized) || ENABLED_VALUE.equals(normalized) || ONE_VALUE.equals(normalized);
    }

    private boolean isShiftDownOnWindows() {
        if (!isWindows()) {
            return false;
        }

        try {
            return (WindowsUser32.INSTANCE.GetAsyncKeyState(VK_SHIFT) & KEY_DOWN_MASK) != 0;
        } catch (Throwable ignored) {
            return false;
        }
    }

    private boolean isWindows() {
        String osName = System.getProperty(OS_NAME_PROPERTY, "").toLowerCase(Locale.ROOT);
        return osName.contains(WINDOWS_NAME_TOKEN);
    }

    private interface WindowsUser32 extends Library {
        WindowsUser32 INSTANCE = Native.load("user32", WindowsUser32.class);

        short GetAsyncKeyState(int keyCode);
    }
}
