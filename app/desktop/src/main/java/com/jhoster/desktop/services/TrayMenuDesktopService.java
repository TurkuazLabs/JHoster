// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\TrayMenuDesktopService.java
// # 📌 Amac: JHoster Desktop sistem tepsisi menusu is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.51.0
// # Aciklama: Laragon benzeri tray menude web, www, servisler, portable bin araclari, runtime, profil, ayarlar ve cikis aksiyonlarini saglar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.ServiceManagerSummary;
import com.jhoster.desktop.tools.BrowserTool;
import com.jhoster.desktop.tools.TrayMenuTool;
import java.awt.CheckboxMenuItem;
import java.awt.Menu;
import java.awt.MenuItem;
import java.awt.PopupMenu;
import java.awt.event.ActionListener;
import javafx.application.Platform;
import javafx.stage.Stage;

public class TrayMenuDesktopService {
    private static final String APP_NAME = "JHoster";
    private static final String NOTIFY_TITLE = "JHoster";
    private static final String NOTIFY_TRAY_READY = "Tray menu hazir";
    private static final String NOTIFY_TRAY_UNSUPPORTED = "System tray desteklenmiyor";
    private static final String NOTIFY_WINDOW_HIDDEN = "JHoster arka planda calismaya devam ediyor";
    private static final String NOTIFY_SEPARATOR = " | ";
    private static final String LABEL_SHOW = "JHoster Goster";
    private static final String LABEL_HIDE = "Gizle";
    private static final String LABEL_OPEN_PANEL = "Panel";
    private static final String LABEL_ROOT_MENU = "JHoster";
    private static final String LABEL_WWW = "www";
    private static final String LABEL_QUICK_APP = "Hizli uygulama";
    private static final String LABEL_TOOLS = "Araclar";
    private static final String LABEL_NGINX = "Nginx";
    private static final String LABEL_MYSQL = "MySQL";
    private static final String LABEL_MAILPIT = "Mailpit";
    private static final String LABEL_NODE = "Node.js";
    private static final String LABEL_PHP = "PHP";
    private static final String LABEL_PYTHON = "Python";
    private static final String LABEL_STOP_ALL = "Durdur";
    private static final String LABEL_PROFILE = "Profil";
    private static final String LABEL_OPTIONS = "Secenekler...";
    private static final String LABEL_EXIT = "Cikis";
    private static final String LABEL_WEB = "Web";
    private static final String LABEL_DATABASE = "Veritabani";
    private static final String LABEL_TERMINAL = "Terminal";
    private static final String LABEL_ROOT = "Root";
    private static final String LABEL_PROJECTS = "Projects";
    private static final String LABEL_LOGS = "Logs";
    private static final String LABEL_BIN = "Bin";
    private static final String LABEL_CMDER = "Cmder";
    private static final String LABEL_GIT_BASH = "Git Bash";
    private static final String LABEL_NOTEPAD = "Notepad++";
    private static final String LABEL_NGROK = "Ngrok";
    private static final String LABEL_COMPOSER = "Composer";
    private static final String LABEL_YARN = "Yarn";
    private static final String LABEL_REDIS = "Redis";
    private static final String LABEL_MEMCACHED = "Memcached";
    private static final String LABEL_SENDMAIL = "Sendmail";
    private static final String LABEL_OPEN = "Ac";
    private static final String LABEL_STATUS = "Status";
    private static final String LABEL_START = "Start";
    private static final String LABEL_STOP = "Stop";
    private static final String LABEL_RESTART = "Restart";
    private static final String LABEL_ACTIVE_PROFILE = "Active Profile";
    private static final String LABEL_WEB_PROFILES = "Web Server Profiles";
    private static final String LABEL_PROCESS = "Process";
    private static final String LABEL_RUNTIMES = "Runtime Versions";
    private static final String LABEL_QUICK_APPS = "Quick Apps";

    private final TrayMenuTool trayMenuTool;
    private final QuickActionDesktopService quickActionDesktopService;
    private final ServiceManagerDesktopService serviceManagerDesktopService;
    private final BrowserTool browserTool;

    public TrayMenuDesktopService() {
        this.trayMenuTool = new TrayMenuTool();
        this.quickActionDesktopService = new QuickActionDesktopService();
        this.serviceManagerDesktopService = new ServiceManagerDesktopService();
        this.browserTool = new BrowserTool();
    }

    public void install(Stage stage) {
        Platform.setImplicitExit(false);
        stage.setOnCloseRequest(event -> {
            event.consume();
            stage.hide();
            trayMenuTool.notifyInfo(NOTIFY_TITLE, NOTIFY_WINDOW_HIDDEN);
        });

        PopupMenu popupMenu = createMenu(stage);
        boolean installed = trayMenuTool.install(APP_NAME, popupMenu);
        if (installed) {
            trayMenuTool.notifyInfo(NOTIFY_TITLE, NOTIFY_TRAY_READY);
        } else {
            trayMenuTool.notifyWarning(NOTIFY_TITLE, NOTIFY_TRAY_UNSUPPORTED);
        }
    }

    private PopupMenu createMenu(Stage stage) {
        PopupMenu popupMenu = new PopupMenu();
        popupMenu.add(menuItem(LABEL_SHOW, event -> showStage(stage)));
        popupMenu.add(menuItem(LABEL_HIDE, event -> hideStage(stage)));
        popupMenu.addSeparator();
        popupMenu.add(menuItem(LABEL_OPEN_PANEL, event -> openRoute(DesktopApiConfig.ROOT_ROUTE)));
        popupMenu.add(rootMenu());
        popupMenu.add(menuItem(LABEL_WWW, event -> notifyResult(LABEL_WWW, quickActionDesktopService.openRoot())));
        popupMenu.add(quickAppMenu());
        popupMenu.add(toolsMenu());
        popupMenu.addSeparator();
        popupMenu.add(serviceMenu(LABEL_NGINX, DesktopApiConfig.SERVICE_CODE_NGINX, false));
        popupMenu.add(serviceMenu(LABEL_MYSQL, DesktopApiConfig.SERVICE_CODE_MYSQL, true));
        popupMenu.add(serviceMenu(LABEL_MAILPIT, DesktopApiConfig.SERVICE_CODE_MAILPIT, false));
        popupMenu.add(serviceMenu(LABEL_REDIS, DesktopApiConfig.SERVICE_CODE_REDIS, false));
        popupMenu.add(serviceMenu(LABEL_MEMCACHED, DesktopApiConfig.SERVICE_CODE_MEMCACHED, false));
        popupMenu.add(serviceMenu(LABEL_SENDMAIL, DesktopApiConfig.SERVICE_CODE_SENDMAIL, false));
        popupMenu.add(runtimeMenu(LABEL_NODE, DesktopApiConfig.RUNTIME_FAMILY_NODE));
        popupMenu.add(runtimeMenu(LABEL_PHP, DesktopApiConfig.RUNTIME_FAMILY_PHP));
        popupMenu.add(runtimeMenu(LABEL_PYTHON, DesktopApiConfig.RUNTIME_FAMILY_PYTHON));
        popupMenu.addSeparator();
        popupMenu.add(menuItem(LABEL_STOP_ALL, event -> stopAllServices()));
        popupMenu.add(profileMenu());
        popupMenu.add(optionsMenu());
        popupMenu.addSeparator();
        popupMenu.add(menuItem(LABEL_EXIT, event -> exitApp(stage)));
        return popupMenu;
    }

    private Menu rootMenu() {
        Menu menu = new Menu(LABEL_ROOT_MENU);
        menu.add(menuItem(LABEL_WEB, event -> notifyResult(LABEL_WEB, quickActionDesktopService.openWeb())));
        menu.add(menuItem(LABEL_ROOT, event -> notifyResult(LABEL_ROOT, quickActionDesktopService.openRoot())));
        menu.add(menuItem(LABEL_PROJECTS, event -> notifyResult(LABEL_PROJECTS, quickActionDesktopService.openProjects())));
        menu.add(menuItem(LABEL_LOGS, event -> notifyResult(LABEL_LOGS, quickActionDesktopService.openLogs())));
        return menu;
    }

    private Menu quickAppMenu() {
        Menu menu = new Menu(LABEL_QUICK_APP);
        menu.add(menuItem(LABEL_OPEN, event -> openRoute(DesktopApiConfig.QUICK_APPS_ROUTE)));
        menu.add(menuItem(LABEL_PROJECTS, event -> notifyResult(LABEL_PROJECTS, quickActionDesktopService.openProjects())));
        return menu;
    }

    private Menu toolsMenu() {
        Menu menu = new Menu(LABEL_TOOLS);
        menu.add(menuItem(LABEL_TERMINAL, event -> notifyResult(LABEL_TERMINAL, quickActionDesktopService.openTerminal())));
        menu.add(menuItem(LABEL_DATABASE, event -> notifyResult(LABEL_DATABASE, quickActionDesktopService.openDatabase())));
        menu.add(menuItem(LABEL_MAILPIT, event -> notifyResult(LABEL_MAILPIT, quickActionDesktopService.openMailpit())));
        menu.add(menuItem(LABEL_LOGS, event -> notifyResult(LABEL_LOGS, quickActionDesktopService.openLogs())));
        menu.addSeparator();
        menu.add(menuItem(LABEL_BIN, event -> notifyResult(LABEL_BIN, quickActionDesktopService.openBin())));
        menu.add(menuItem(LABEL_CMDER, event -> notifyResult(LABEL_CMDER, quickActionDesktopService.openCmder())));
        menu.add(menuItem(LABEL_GIT_BASH, event -> notifyResult(LABEL_GIT_BASH, quickActionDesktopService.openGitBash())));
        menu.add(menuItem(LABEL_NOTEPAD, event -> notifyResult(LABEL_NOTEPAD, quickActionDesktopService.openNotepad())));
        menu.add(menuItem(LABEL_NGROK, event -> notifyResult(LABEL_NGROK, quickActionDesktopService.openNgrok())));
        menu.add(menuItem(LABEL_COMPOSER, event -> notifyResult(LABEL_COMPOSER, quickActionDesktopService.openComposerFolder())));
        menu.add(menuItem(LABEL_YARN, event -> notifyResult(LABEL_YARN, quickActionDesktopService.openYarnFolder())));
        return menu;
    }

    private Menu serviceMenu(String label, String serviceCode, boolean includeDatabase) {
        Menu menu = new Menu(label);
        CheckboxMenuItem enabledItem = new CheckboxMenuItem(label);
        enabledItem.setState(false);
        enabledItem.setEnabled(false);
        menu.add(enabledItem);
        menu.add(menuItem(LABEL_STATUS, event -> notifyService(serviceManagerDesktopService.statusSummary(serviceCode))));
        menu.add(menuItem(LABEL_START, event -> notifyService(serviceManagerDesktopService.startSummary(serviceCode))));
        menu.add(menuItem(LABEL_STOP, event -> notifyService(serviceManagerDesktopService.stopSummary(serviceCode))));
        menu.add(menuItem(LABEL_RESTART, event -> notifyService(serviceManagerDesktopService.restartSummary(serviceCode))));
        if (includeDatabase) {
            menu.addSeparator();
            menu.add(menuItem(LABEL_DATABASE, event -> notifyResult(LABEL_DATABASE, quickActionDesktopService.openDatabase())));
        }
        if (DesktopApiConfig.SERVICE_CODE_MAILPIT.equals(serviceCode)) {
            menu.addSeparator();
            menu.add(menuItem(LABEL_OPEN, event -> notifyResult(LABEL_MAILPIT, quickActionDesktopService.openMailpit())));
        }
        return menu;
    }

    private Menu runtimeMenu(String label, String family) {
        Menu menu = new Menu(label);
        menu.add(menuItem(LABEL_OPEN, event -> openRoute(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE + "/" + family)));
        menu.add(menuItem(LABEL_RUNTIMES, event -> openRoute(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE)));
        return menu;
    }

    private Menu profileMenu() {
        Menu menu = new Menu(LABEL_PROFILE);
        menu.add(menuItem(LABEL_ACTIVE_PROFILE, event -> openRoute(DesktopApiConfig.WEB_SERVER_CURRENT_PROFILE_ROUTE)));
        menu.add(menuItem(LABEL_WEB_PROFILES, event -> openRoute(DesktopApiConfig.WEB_SERVER_PROFILES_ROUTE)));
        return menu;
    }

    private Menu optionsMenu() {
        Menu menu = new Menu(LABEL_OPTIONS);
        menu.add(menuItem(LABEL_PROCESS, event -> openRoute(DesktopApiConfig.PROCESS_ROUTE)));
        menu.add(menuItem(LABEL_RUNTIMES, event -> openRoute(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE)));
        menu.add(menuItem(LABEL_QUICK_APPS, event -> openRoute(DesktopApiConfig.QUICK_APPS_ROUTE)));
        return menu;
    }

    private MenuItem menuItem(String label, ActionListener listener) {
        MenuItem item = new MenuItem(label);
        item.addActionListener(listener);
        return item;
    }

    private void showStage(Stage stage) {
        Platform.runLater(() -> {
            if (!stage.isShowing()) {
                stage.show();
            }
            stage.toFront();
            stage.requestFocus();
        });
    }

    private void hideStage(Stage stage) {
        Platform.runLater(stage::hide);
    }

    private void exitApp(Stage stage) {
        trayMenuTool.remove();
        Platform.runLater(() -> {
            Platform.setImplicitExit(true);
            stage.close();
            Platform.exit();
        });
    }

    private void openRoute(String route) {
        browserTool.open(DesktopApiConfig.resolveUrl(route));
        trayMenuTool.notifyInfo(NOTIFY_TITLE, DesktopApiConfig.resolveUrl(route));
    }

    private void stopAllServices() {
        StringBuilder builder = new StringBuilder();
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_PHP));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_REDIS));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MEMCACHED));
        appendServiceResult(builder, serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_SENDMAIL));
        trayMenuTool.notifyInfo(LABEL_STOP_ALL, builder.toString());
    }

    private void notifyService(ServiceManagerSummary summary) {
        trayMenuTool.notifyInfo(summary.getServiceCode(), summary.getOperation() + NOTIFY_SEPARATOR + summary.getStatus());
    }

    private void notifyResult(String title, String result) {
        trayMenuTool.notifyInfo(title, result);
    }

    private void appendServiceResult(StringBuilder builder, ServiceManagerSummary summary) {
        if (builder.length() > 0) {
            builder.append(NOTIFY_SEPARATOR);
        }
        builder.append(summary.getServiceCode()).append(":").append(summary.getStatus());
    }
}
