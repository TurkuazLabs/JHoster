// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\SemanticVersionCompareTool.java
// # 📌 Amac: GitHub tag ile yerel surumu karsilastirir
// # 📌 Modul - Java
// # Version: 3.61.0
// # Aciklama: v3.61.0 gibi tag degerlerini sayisal bolumlere ayirip update karari icin karsilastirma yapar
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

public final class SemanticVersionCompareTool {
    private static final int VERSION_PART_COUNT = 4;

    public boolean isNewer(String latestVersion, String currentVersion) {
        int[] latestParts = parse(latestVersion);
        int[] currentParts = parse(currentVersion);
        for (int index = 0; index < VERSION_PART_COUNT; index++) {
            if (latestParts[index] > currentParts[index]) {
                return true;
            }
            if (latestParts[index] < currentParts[index]) {
                return false;
            }
        }
        return false;
    }

    private int[] parse(String version) {
        int[] parts = new int[VERSION_PART_COUNT];
        String normalized = version == null ? "" : version.trim().toLowerCase();
        normalized = normalized.startsWith("v") ? normalized.substring(1) : normalized;
        normalized = normalized.replaceAll("[^0-9.]", "");
        String[] tokens = normalized.split("\\.");
        for (int index = 0; index < tokens.length && index < VERSION_PART_COUNT; index++) {
            parts[index] = parsePart(tokens[index]);
        }
        return parts;
    }

    private int parsePart(String token) {
        if (token == null || token.isBlank()) {
            return 0;
        }
        try {
            return Integer.parseInt(token);
        } catch (NumberFormatException exception) {
            return 0;
        }
    }
}
