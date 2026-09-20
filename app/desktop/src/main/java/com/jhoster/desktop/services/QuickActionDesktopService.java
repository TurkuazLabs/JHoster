// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\QuickActionDesktopService.java
// # 📌 Amac: Desktop hizli aksiyon is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.62.1
// # Aciklama: Web, Mailpit, Veritabani, Terminal, Root, Projects, Logs, Settings ve portable bin araclarini Tool katmanina baglar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.tools.BrowserTool;
import com.jhoster.desktop.tools.QuickActionTool;

public class QuickActionDesktopService {
    private static final String LOG_PREFIX = "Quick Action";
    private static final String LOG_SEPARATOR = " -> ";
    private static final String ACTION_WEB = "Web";
    private static final String ACTION_DATABASE = "Database";
    private static final String ACTION_MAILPIT = "Mailpit";
    private static final String ACTION_TERMINAL = "Terminal";
    private static final String ACTION_ROOT = "Root";
    private static final String ACTION_PROJECTS = "Projects";
    private static final String ACTION_LOGS = "Logs";
    private static final String ACTION_LOG_FOLDER = "Log Folder";
    private static final String ACTION_SETTINGS = "Settings";
    private static final String ACTION_BIN = "Bin";
    private static final String ACTION_CMDER = "Cmder";
    private static final String ACTION_GIT_BASH = "Git Bash";
    private static final String ACTION_NOTEPAD = "Notepad++";
    private static final String ACTION_NGROK = "Ngrok";
    private static final String ACTION_COMPOSER = "Composer";
    private static final String ACTION_YARN = "Yarn";

    private final BrowserTool browserTool;
    private final QuickActionTool quickActionTool;

    public QuickActionDesktopService() {
        this.browserTool = new BrowserTool();
        this.quickActionTool = new QuickActionTool();
    }

    public String openWeb() {
        browserTool.open(DesktopApiConfig.QUICK_ACTION_WEB_URL);
        return log(ACTION_WEB, DesktopApiConfig.QUICK_ACTION_WEB_URL);
    }

    public String openDatabase() {
        return log(ACTION_DATABASE, quickActionTool.openHeidiSqlPortable());
    }

    public String openMailpit() {
        browserTool.open(DesktopApiConfig.QUICK_ACTION_MAILPIT_URL);
        return log(ACTION_MAILPIT, DesktopApiConfig.QUICK_ACTION_MAILPIT_URL);
    }

    public String openTerminal() {
        return log(ACTION_TERMINAL, quickActionTool.openTerminal());
    }

    public String openRoot() {
        return log(ACTION_ROOT, quickActionTool.openFolder(DesktopApiConfig.QUICK_ACTION_ROOT_FOLDER));
    }

    public String openProjects() {
        return log(ACTION_PROJECTS, quickActionTool.openFolder(DesktopApiConfig.QUICK_ACTION_PROJECTS_FOLDER));
    }

    public String openLogs() {
        return log(ACTION_LOGS, quickActionTool.openFolder(DesktopApiConfig.QUICK_ACTION_LOGS_FOLDER));
    }

    public String openLogFolder(String relativeFolder) {
        return log(ACTION_LOG_FOLDER, quickActionTool.openFolder(relativeFolder));
    }

    public String openSettings() {
        return log(ACTION_SETTINGS, quickActionTool.openFolder(DesktopApiConfig.QUICK_ACTION_SETTINGS_FOLDER));
    }

    public String openBin() {
        return log(ACTION_BIN, quickActionTool.openBinFolder());
    }

    public String openCmder() {
        return log(ACTION_CMDER, quickActionTool.openCmderPortable());
    }

    public String openGitBash() {
        return log(ACTION_GIT_BASH, quickActionTool.openGitBashPortable());
    }

    public String openNotepad() {
        return log(ACTION_NOTEPAD, quickActionTool.openNotepadPortable());
    }

    public String openNgrok() {
        return log(ACTION_NGROK, quickActionTool.openNgrokPortable());
    }

    public String openComposerFolder() {
        return log(ACTION_COMPOSER, quickActionTool.openComposerFolder());
    }

    public String openYarnFolder() {
        return log(ACTION_YARN, quickActionTool.openYarnFolder());
    }

    private String log(String action, String result) {
        return LOG_PREFIX + LOG_SEPARATOR + action + LOG_SEPARATOR + result;
    }
}
