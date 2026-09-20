// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\repositories\ProjectPathRepository.java
// # 📌 Amac: Desktop uygulamanin proje dizinlerini cozmesini saglar
// # 📌 Modul - Java
// # Version: 3.2.1
// # Aciklama: Agent klasor yolunu merkezi storage mantigi ile hesaplar
//
// Bagimli Oldugu Katman: Repo

package com.jhoster.desktop.repositories;

import java.io.File;
import java.nio.file.Path;

public class ProjectPathRepository {
    private static final String AGENT_DIRECTORY_NAME = "agent";

    public File resolveAgentDirectory() {
        Path desktopDirectory = Path.of(System.getProperty("user.dir"));
        Path rootDirectory = desktopDirectory.getParent();
        if (rootDirectory == null) {
            rootDirectory = desktopDirectory;
        }
        return rootDirectory.resolve(AGENT_DIRECTORY_NAME).toFile();
    }
}
