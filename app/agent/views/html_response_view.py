# 📄 Dosya Yolu: E:\JHoster\app\agent\views\html_response_view.py
# 📌 Amac: JHoster agent HTML response ciktilarini standart hale getirir
# 📌 Modul - FileType
# Version: 1.2.0
# Aciklama: Root endpoint icin HTML view katmani
# Bagimli Oldugu Katman: View

from typing import Any

from fastapi.responses import HTMLResponse


class HtmlResponseView:
    def render(self, response_data: dict[str, Any]) -> HTMLResponse:
        html_content = self._build_html(response_data)
        return HTMLResponse(content=html_content, status_code=200)

    def _build_html(self, response_data: dict[str, Any]) -> str:
        app_name = response_data.get("app_name", "JHoster Agent")
        app_version = response_data.get("app_version", "0.0.0")
        status = response_data.get("status", "unknown")
        health_url = response_data.get("health_url", "#")
        components_url = response_data.get("components_url", "#")
        docs_url = response_data.get("docs_url", "#")
        history_url = "/api/v1/install/history"

        return f"""
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{app_name}</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f7f8fb;
      color: #182033;
    }}
    .page {{
      max-width: 900px;
      margin: 64px auto;
      padding: 0 20px;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e6e8ef;
      border-radius: 18px;
      padding: 32px;
      box-shadow: 0 16px 40px rgba(24, 32, 51, 0.08);
    }}
    .status {{
      display: inline-block;
      padding: 7px 12px;
      border-radius: 999px;
      background: #e8f7ef;
      color: #167344;
      font-weight: 700;
      font-size: 13px;
    }}
    h1 {{
      margin: 18px 0 8px;
      font-size: 34px;
    }}
    p {{
      line-height: 1.6;
      color: #495266;
    }}
    .links {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 22px;
    }}
    a {{
      display: inline-block;
      padding: 12px 16px;
      border-radius: 12px;
      text-decoration: none;
      background: #182033;
      color: #ffffff;
      font-weight: 700;
    }}
    a.secondary {{
      background: #edf0f7;
      color: #182033;
    }}
    code {{
      background: #edf0f7;
      padding: 3px 6px;
      border-radius: 6px;
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="card">
      <span class="status">{status}</span>
      <h1>{app_name}</h1>
      <p>Agent calisiyor. Bu surum component manifestlerini YAML dosyalarindan okuyup guvenli executor ile planlayabilir.</p>
      <p>Version: <strong>{app_version}</strong></p>
      <p>Executor varsayilan olarak <code>dry_run=true</code> modunda calisir.</p>
      <div class="links">
        <a href="{components_url}">Components</a>
        <a class="secondary" href="{history_url}">Install History</a>
        <a class="secondary" href="{health_url}">Health Check</a>
        <a class="secondary" href="{docs_url}">API Docs</a>
      </div>
    </section>
  </main>
</body>
</html>
"""
