// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java
// # 📌 Amac: Desktop tarafinda hafif JSON metin alanlarini dis bagimlilik olmadan okur
// # 📌 Modul - Java
// # Version: 3.35.0
// # Aciklama: Agent cevaplarindan string, int, boolean ve tekrar sayisi alanlarini guvenli regex ile cikarir
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class JsonTextExtractorTool {
    private static final String EMPTY_VALUE = "";
    private static final String QUOTE_PATTERN = "\\\"";
    private static final String KEY_VALUE_SEPARATOR_PATTERN = "\\s*:\\s*";
    private static final String STRING_VALUE_PATTERN = "\\\"([^\\\"]*)\\\"";
    private static final String INT_VALUE_PATTERN = "(-?\\d+)";
    private static final String BOOLEAN_VALUE_PATTERN = "(true|false)";
    private static final int FIRST_GROUP = 1;

    public String extractString(String source, String key) {
        Matcher matcher = buildMatcher(source, key, STRING_VALUE_PATTERN);
        return matcher.find() ? matcher.group(FIRST_GROUP) : EMPTY_VALUE;
    }

    public int extractInt(String source, String key, int fallback) {
        Matcher matcher = buildMatcher(source, key, INT_VALUE_PATTERN);
        if (!matcher.find()) {
            return fallback;
        }

        try {
            return Integer.parseInt(matcher.group(FIRST_GROUP));
        } catch (NumberFormatException exception) {
            return fallback;
        }
    }

    public boolean extractBoolean(String source, String key, boolean fallback) {
        Matcher matcher = buildMatcher(source, key, BOOLEAN_VALUE_PATTERN);
        if (!matcher.find()) {
            return fallback;
        }

        return Boolean.parseBoolean(matcher.group(FIRST_GROUP));
    }

    public int countKeyOccurrences(String source, String key) {
        Matcher matcher = Pattern.compile(buildKeyPattern(key)).matcher(normalizeSource(source));
        int count = 0;

        while (matcher.find()) {
            count++;
        }

        return count;
    }

    private Matcher buildMatcher(String source, String key, String valuePattern) {
        Pattern pattern = Pattern.compile(buildKeyPattern(key) + KEY_VALUE_SEPARATOR_PATTERN + valuePattern);
        return pattern.matcher(normalizeSource(source));
    }

    private String buildKeyPattern(String key) {
        return QUOTE_PATTERN + Pattern.quote(key == null ? EMPTY_VALUE : key) + QUOTE_PATTERN;
    }

    private String normalizeSource(String source) {
        return source == null ? EMPTY_VALUE : source;
    }
}
