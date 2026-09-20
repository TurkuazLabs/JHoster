// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\launcher\LauncherBootstrapApplication.java
// # 📌 Amac: JHoster launcher splash akisini ve desktop acilisini yonetir
// # 📌 Modul - Java
// # Version: 3.77.0
// # Aciklama: Splash ekrani gosterir, GitHub latest release kontrolu yapar ve asil Desktop sahnesini fullscreen maximized olarak acar
// # Bagimli Oldugu Katman: Controller

package com.jhoster.desktop.launcher;

import com.jhoster.desktop.controllers.LauncherController;
import com.jhoster.desktop.models.UpdateCheckResult;
import com.jhoster.desktop.services.GitHubReleaseUpdateService;
import com.jhoster.desktop.services.TrayMenuDesktopService;
import com.jhoster.desktop.tools.BrowserTool;
import com.jhoster.desktop.tools.BrandingResourceTool;
import com.jhoster.desktop.tools.DesktopVersionTool;
import com.jhoster.desktop.tools.DevModeTool;
import java.net.URL;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonBar;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressIndicator;
import javafx.scene.image.ImageView;
import javafx.animation.PauseTransition;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import javafx.util.Duration;

public final class LauncherBootstrapApplication extends Application {
    private static final String APP_TITLE = "JHoster Desktop";
    private static final String APP_EDITION = "Community";
    private static final String LAUNCHER_TITLE = "JHoster Launcher";
    private static final String THEME_RESOURCE = "/styles/jhoster-modern.css";
    private static final String SPLASH_TITLE = "JHoster";
    private static final String SPLASH_SUBTITLE = "Community local development studio";
    private static final String STATUS_LOADING = "Loading JHoster...";
    private static final String STATUS_CHECKING_UPDATE = "Checking GitHub releases...";
    private static final String STATUS_STARTING_DESKTOP = "Starting desktop...";
    private static final String UPDATE_TITLE = "JHoster Update Available";
    private static final String UPDATE_LATER = "Later";
    private static final String UPDATE_OPEN_RELEASE = "Open Release Page";
    private static final double SPLASH_WIDTH = 560;
    private static final double SPLASH_HEIGHT = 320;
    private static final double DESKTOP_WIDTH = 1600;
    private static final double DESKTOP_HEIGHT = 940;
    private static final double DESKTOP_MIN_WIDTH = 1280;
    private static final double DESKTOP_MIN_HEIGHT = 760;
    private static final double DECK_WIDTH = 1600;
    private static final double DECK_HEIGHT = 940;
    private static final double DECK_MIN_WIDTH = 1280;
    private static final double DECK_MIN_HEIGHT = 760;
    private static final long MIN_SPLASH_MILLIS = 1800L;

    private final DesktopVersionTool desktopVersionTool = new DesktopVersionTool();
    private final GitHubReleaseUpdateService gitHubReleaseUpdateService = new GitHubReleaseUpdateService();
    private final BrandingResourceTool brandingResourceTool = new BrandingResourceTool();
    private Label splashStatusLabel;
    private long splashStartedAtMillis;

    @Override
    public void start(Stage splashStage) {
        splashStage.initStyle(StageStyle.UNDECORATED);
        splashStage.setTitle(LAUNCHER_TITLE);
        applyStageIcon(splashStage);
        Scene splashScene = new Scene(buildSplashView(), SPLASH_WIDTH, SPLASH_HEIGHT);
        applyTheme(splashScene);
        splashStage.setScene(splashScene);
        splashStage.centerOnScreen();
        splashStage.show();
        splashStartedAtMillis = System.currentTimeMillis();
        runBootstrapFlow(splashStage);
    }

    private VBox buildSplashView() {
        VBox root = new VBox(20);
        root.setAlignment(Pos.CENTER);
        root.getStyleClass().add("jhoster-splash-root");

        Node mark = buildSplashLogo();

        Label title = new Label(SPLASH_TITLE);
        title.getStyleClass().add("jhoster-splash-title");

        Label subtitle = new Label(SPLASH_SUBTITLE);
        subtitle.getStyleClass().add("jhoster-splash-subtitle");

        ProgressIndicator progressIndicator = new ProgressIndicator();
        progressIndicator.getStyleClass().add("jhoster-splash-progress");
        progressIndicator.setPrefSize(34, 34);

        splashStatusLabel = new Label(STATUS_LOADING);
        splashStatusLabel.getStyleClass().add("jhoster-splash-status");

        HBox progressRow = new HBox(10);
        progressRow.setAlignment(Pos.CENTER);
        progressRow.getChildren().addAll(progressIndicator, splashStatusLabel);

        root.getChildren().addAll(mark, title, subtitle, progressRow);
        return root;
    }

    private Node buildSplashLogo() {
        Optional<ImageView> logoView = brandingResourceTool.createFxLogoView(92);
        if (logoView.isPresent()) {
            ImageView view = logoView.get();
            view.getStyleClass().add("jhoster-splash-logo-image");
            return view;
        }

        Label fallback = new Label("J");
        fallback.getStyleClass().add("jhoster-splash-logo");
        return fallback;
    }

    private void runBootstrapFlow(Stage splashStage) {
        String currentVersion = desktopVersionTool.currentVersion();
        updateSplashStatus(STATUS_CHECKING_UPDATE);

        CompletableFuture<UpdateCheckResult> updateFuture = gitHubReleaseUpdateService.checkLatestRelease(currentVersion);
        updateFuture.thenAccept(result -> Platform.runLater(() -> finishBootstrapAfterMinimumDelay(splashStage, result)));
    }

    private void finishBootstrapAfterMinimumDelay(Stage splashStage, UpdateCheckResult result) {
        long elapsedMillis = System.currentTimeMillis() - splashStartedAtMillis;
        long remainingMillis = Math.max(0L, MIN_SPLASH_MILLIS - elapsedMillis);
        updateSplashStatus(STATUS_STARTING_DESKTOP);

        if (remainingMillis == 0L) {
            finishBootstrap(splashStage, result);
            return;
        }

        PauseTransition pauseTransition = new PauseTransition(Duration.millis(remainingMillis));
        pauseTransition.setOnFinished(event -> finishBootstrap(splashStage, result));
        pauseTransition.play();
    }

    private void finishBootstrap(Stage splashStage, UpdateCheckResult result) {
        if (result.isUpdateAvailable()) {
            showUpdateDialog(splashStage, result);
        }

        openDesktopStage();
        splashStage.close();
    }

    private void showUpdateDialog(Stage owner, UpdateCheckResult result) {
        ButtonType laterButton = new ButtonType(UPDATE_LATER, ButtonBar.ButtonData.CANCEL_CLOSE);
        ButtonType openReleaseButton = new ButtonType(UPDATE_OPEN_RELEASE, ButtonBar.ButtonData.OK_DONE);
        Alert alert = new Alert(Alert.AlertType.INFORMATION, buildUpdateMessage(result), laterButton, openReleaseButton);
        alert.setTitle(UPDATE_TITLE);
        alert.setHeaderText("New version: " + result.getLatestVersion());
        alert.initOwner(owner);
        alert.showAndWait().ifPresent(button -> {
            if (button == openReleaseButton && !result.getReleaseUrl().isBlank()) {
                new BrowserTool().open(result.getReleaseUrl());
            }
        });
    }

    private String buildUpdateMessage(UpdateCheckResult result) {
        return "Current version: " + result.getCurrentVersion()
            + System.lineSeparator()
            + "Latest version: " + result.getLatestVersion()
            + System.lineSeparator()
            + System.lineSeparator()
            + "The safe updater will be added in the next stage. You can open the GitHub release page now.";
    }

    private void openDesktopStage() {
        boolean devModeEnabled = new DevModeTool().isDevMode(getParameters().getRaw());
        LauncherController controller = new LauncherController(devModeEnabled);
        double windowWidth = devModeEnabled ? DESKTOP_WIDTH : DECK_WIDTH;
        double windowHeight = devModeEnabled ? DESKTOP_HEIGHT : DECK_HEIGHT;
        double minWindowWidth = devModeEnabled ? DESKTOP_MIN_WIDTH : DECK_MIN_WIDTH;
        double minWindowHeight = devModeEnabled ? DESKTOP_MIN_HEIGHT : DECK_MIN_HEIGHT;

        Stage desktopStage = new Stage();
        Scene desktopScene = new Scene(controller.createView(), windowWidth, windowHeight);
        applyTheme(desktopScene);

        desktopStage.setTitle(APP_TITLE + " " + desktopVersionTool.currentVersion() + " " + APP_EDITION);
        applyStageIcon(desktopStage);
        desktopStage.setMinWidth(minWindowWidth);
        desktopStage.setMinHeight(minWindowHeight);
        desktopStage.setScene(desktopScene);
        desktopStage.setMaximized(true);
        desktopStage.show();
        new TrayMenuDesktopService().install(desktopStage);
    }

    private void updateSplashStatus(String text) {
        if (splashStatusLabel != null) {
            splashStatusLabel.setText(text);
        }
    }

    private void applyStageIcon(Stage stage) {
        brandingResourceTool.loadFxIcon().ifPresent(icon -> stage.getIcons().add(icon));
    }

    private void applyTheme(Scene scene) {
        URL themeUrl = LauncherBootstrapApplication.class.getResource(THEME_RESOURCE);
        if (themeUrl != null) {
            scene.getStylesheets().add(themeUrl.toExternalForm());
        }
    }
}
