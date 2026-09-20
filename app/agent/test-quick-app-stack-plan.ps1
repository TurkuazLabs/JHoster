# 📄 Dosya Yolu: E:/JHoster/app/agent/test-quick-app-stack-plan.ps1
# 📌 Amac: Quick App stack secimli plan endpointini test eder
# 📌 Modul - PowerShell
# Version: 3.72.0
# Aciklama: Apache/Nginx ve MySQL/PHP/Mailpit query parametrelerinin API cevabina yansidigini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
python - <<'PY'
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
response = client.get('/api/v1/quick-apps/demo-stack/plan?template_code=php-empty&project_name=Demo%20Stack&domain=demo-stack.test&port=80&web_server=nginx&include_mysql=true&include_php=true&include_mailpit=true')
assert response.status_code == 200, response.text
body = response.json()
data = body.get('data', body)
assert data.get('success') is True, data
assert data.get('stack_plan', {}).get('web_server') == 'nginx', data
assert data.get('stack_plan', {}).get('include_mailpit') is True, data
assert data.get('stack_label') == 'Nginx + MySQL + PHP + Mailpit', data
print('quick app stack plan ok')
PY
