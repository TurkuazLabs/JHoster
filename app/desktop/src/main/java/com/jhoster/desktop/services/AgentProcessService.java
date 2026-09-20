// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\AgentProcessService.java
// # 📌 Amac: Python agent process yasam dongusu is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.24.5
// # Aciklama: Agent start, stop, restart ve calisma durumu operasyonlarini saglar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.repositories.ProjectPathRepository;
import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class AgentProcessService {
    private static final String PYTHON_COMMAND = "python";
    private static final String AGENT_MAIN_FILE = "main.py";
    private static final int STOP_TIMEOUT_SECONDS = 5;

    private final ProjectPathRepository projectPathRepository;
    private Process process;

    public AgentProcessService() {
        this.projectPathRepository = new ProjectPathRepository();
    }

    public String startAgent() {
        if (isManagedAgentRunning()) {
            return "Agent already running";
        }

        File agentDirectory = projectPathRepository.resolveAgentDirectory();
        ProcessBuilder builder = new ProcessBuilder(PYTHON_COMMAND, AGENT_MAIN_FILE);
        builder.directory(agentDirectory);
        builder.redirectErrorStream(true);

        try {
            process = builder.start();
            return "Agent start requested: " + agentDirectory.getAbsolutePath();
        } catch (IOException exception) {
            return "Agent start failed: " + exception.getMessage();
        }
    }

    public String stopAgent() {
        if (!isManagedAgentRunning()) {
            process = null;
            return "Agent stop skipped: no managed agent process is running";
        }

        process.destroy();

        try {
            boolean stopped = process.waitFor(STOP_TIMEOUT_SECONDS, TimeUnit.SECONDS);

            if (!stopped) {
                process.destroyForcibly();
                process.waitFor(STOP_TIMEOUT_SECONDS, TimeUnit.SECONDS);
                process = null;
                return "Agent stop forced after timeout";
            }

            process = null;
            return "Agent stopped";
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            return "Agent stop interrupted: " + exception.getMessage();
        }
    }

    public String restartAgent() {
        String stopMessage = stopAgent();
        String startMessage = startAgent();
        return stopMessage + "\n" + startMessage;
    }

    public boolean isManagedAgentRunning() {
        return process != null && process.isAlive();
    }
}
