// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\QuickActionTool.java
// # 📌 Amac: Desktop hizli aksiyonlarini sistem araclarina guvenli sekilde aktarir
// # 📌 Modul - Java
// # Version: 3.50.0
// # Aciklama: Sade app/bin/data/etc/www layout icin Root, www, logs, terminal ve portable bin araclarini izole eder
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import com.jhoster.desktop.config.DesktopApiConfig;
import java.awt.Desktop;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class QuickActionTool {
    private static final String STATUS_SEPARATOR = ": ";
    private static final String PATH_SEPARATOR = " | ";
    private static final String EMPTY_PATH = "";
    private static final String QUOTED_SINGLE = "'";
    private static final String ESCAPED_SINGLE = "''";

    public String openFolder(String relativePath) {
        Path target = resolveRootPath().resolve(relativePath == null ? EMPTY_PATH : relativePath).normalize();
        try {
            Files.createDirectories(target);
            if (!Desktop.isDesktopSupported()) {
                return DesktopApiConfig.QUICK_ACTION_MISSING_MESSAGE + STATUS_SEPARATOR + target;
            }
            Desktop.getDesktop().open(target.toFile());
            return DesktopApiConfig.QUICK_ACTION_FOUND_MESSAGE + STATUS_SEPARATOR + target;
        } catch (IOException exception) {
            return DesktopApiConfig.QUICK_ACTION_MISSING_MESSAGE + STATUS_SEPARATOR + target;
        }
    }

    public String openTerminal() {
        Path rootPath = resolveRootPath();
        String command = DesktopApiConfig.QUICK_ACTION_TERMINAL_SET_LOCATION_COMMAND + " " + quotePowerShellPath(rootPath);
        ProcessBuilder processBuilder = new ProcessBuilder(
            DesktopApiConfig.QUICK_ACTION_TERMINAL_EXECUTABLE,
            DesktopApiConfig.QUICK_ACTION_TERMINAL_NO_EXIT_ARG,
            DesktopApiConfig.QUICK_ACTION_TERMINAL_COMMAND_ARG,
            command
        );
        processBuilder.directory(rootPath.toFile());

        try {
            processBuilder.start();
            return DesktopApiConfig.QUICK_ACTION_FOUND_MESSAGE + STATUS_SEPARATOR + rootPath;
        } catch (IOException exception) {
            return DesktopApiConfig.QUICK_ACTION_MISSING_MESSAGE + STATUS_SEPARATOR + rootPath;
        }
    }

    public String openHeidiSqlPortable() {
        return openFirstExistingExecutable(heidiSqlCandidates());
    }

    public String openCmderPortable() {
        return openFirstExistingExecutable(cmderCandidates());
    }

    public String openGitBashPortable() {
        return openFirstExistingExecutable(gitBashCandidates());
    }

    public String openNotepadPortable() {
        return openFirstExistingExecutable(notepadCandidates());
    }

    public String openNgrokPortable() {
        return openFirstExistingExecutable(ngrokCandidates());
    }

    public String openBinFolder() {
        return openFolder(DesktopApiConfig.QUICK_ACTION_BIN_FOLDER);
    }

    public String openComposerFolder() {
        return openFolder("bin/composer");
    }

    public String openYarnFolder() {
        return openFolder("bin/yarn");
    }

    public Path resolveRootPath() {
        Path currentPath = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
        List<Path> candidates = new ArrayList<>();
        candidates.add(currentPath);
        if (currentPath.getParent() != null) {
            candidates.add(currentPath.getParent());
        }
        if (currentPath.getParent() != null && currentPath.getParent().getParent() != null) {
            candidates.add(currentPath.getParent().getParent());
        }

        for (Path candidate : candidates) {
            Path appPath = candidate.resolve(DesktopApiConfig.QUICK_ACTION_APP_DIRECTORY_NAME);
            if (Files.isDirectory(appPath.resolve(DesktopApiConfig.QUICK_ACTION_DESKTOP_DIRECTORY_NAME))
                && Files.isDirectory(appPath.resolve(DesktopApiConfig.QUICK_ACTION_AGENT_DIRECTORY_NAME))) {
                return candidate;
            }

            if (Files.isDirectory(candidate.resolve(DesktopApiConfig.QUICK_ACTION_DESKTOP_DIRECTORY_NAME))
                && Files.isDirectory(candidate.resolve(DesktopApiConfig.QUICK_ACTION_AGENT_DIRECTORY_NAME))) {
                if (DesktopApiConfig.QUICK_ACTION_APP_DIRECTORY_NAME.equalsIgnoreCase(candidate.toFile().getName())
                    && candidate.getParent() != null) {
                    return candidate.getParent();
                }
                return candidate;
            }
        }

        File file = currentPath.toFile();
        if (DesktopApiConfig.QUICK_ACTION_DESKTOP_DIRECTORY_NAME.equalsIgnoreCase(file.getName())
            && currentPath.getParent() != null
            && DesktopApiConfig.QUICK_ACTION_APP_DIRECTORY_NAME.equalsIgnoreCase(currentPath.getParent().toFile().getName())
            && currentPath.getParent().getParent() != null) {
            return currentPath.getParent().getParent();
        }

        return currentPath;
    }

    private List<Path> heidiSqlCandidates() {
        Path rootPath = resolveRootPath();
        List<Path> candidates = new ArrayList<>();
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_HEIDISQL_RELATIVE_PATH_PRIMARY).normalize());
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_HEIDISQL_RELATIVE_PATH_TOOLS).normalize());
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_HEIDISQL_RELATIVE_PATH_APPS).normalize());
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_HEIDISQL_RELATIVE_PATH_USR).normalize());
        return candidates;
    }

    private List<Path> cmderCandidates() {
        Path rootPath = resolveRootPath();
        List<Path> candidates = new ArrayList<>();
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_CMDER_RELATIVE_PATH_PRIMARY).normalize());
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_CMDER_RELATIVE_PATH_ALT).normalize());
        return candidates;
    }

    private List<Path> gitBashCandidates() {
        Path rootPath = resolveRootPath();
        List<Path> candidates = new ArrayList<>();
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_GIT_BASH_RELATIVE_PATH_PRIMARY).normalize());
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_GIT_BASH_RELATIVE_PATH_ALT).normalize());
        return candidates;
    }

    private List<Path> notepadCandidates() {
        Path rootPath = resolveRootPath();
        List<Path> candidates = new ArrayList<>();
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_NOTEPAD_RELATIVE_PATH_PRIMARY).normalize());
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_NOTEPAD_RELATIVE_PATH_ALT).normalize());
        return candidates;
    }

    private List<Path> ngrokCandidates() {
        Path rootPath = resolveRootPath();
        List<Path> candidates = new ArrayList<>();
        candidates.add(rootPath.resolve(DesktopApiConfig.QUICK_ACTION_NGROK_RELATIVE_PATH_PRIMARY).normalize());
        return candidates;
    }

    private String openFirstExistingExecutable(List<Path> candidates) {
        for (Path candidate : candidates) {
            if (Files.isRegularFile(candidate)) {
                try {
                    new ProcessBuilder(candidate.toString()).directory(candidate.getParent().toFile()).start();
                    return DesktopApiConfig.QUICK_ACTION_FOUND_MESSAGE + STATUS_SEPARATOR + candidate;
                } catch (IOException exception) {
                    return DesktopApiConfig.QUICK_ACTION_MISSING_MESSAGE + STATUS_SEPARATOR + candidate;
                }
            }
        }

        return DesktopApiConfig.QUICK_ACTION_MISSING_MESSAGE + STATUS_SEPARATOR + joinCandidates(candidates);
    }

    private String joinCandidates(List<Path> candidates) {
        StringBuilder builder = new StringBuilder();
        for (Path candidate : candidates) {
            if (builder.length() > 0) {
                builder.append(PATH_SEPARATOR);
            }
            builder.append(candidate);
        }
        return builder.toString();
    }

    private String quotePowerShellPath(Path path) {
        String escapedPath = path.toString().replace(QUOTED_SINGLE, ESCAPED_SINGLE);
        return QUOTED_SINGLE + escapedPath + QUOTED_SINGLE;
    }
}
