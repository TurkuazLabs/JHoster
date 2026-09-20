# 📄 Dosya Yolu: E:/JHoster/app/agent/test-hosts-auto-ui-response.ps1
# 📌 Amac: Hosts auto UI icin gereken inspect count alanlarini test eder
# 📌 Modul - PowerShell
# Version: 3.69.0
# Aciklama: Agent hosts auto inspect cevabinda UI count alanlarinin dondugunu dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "../..")
Push-Location $RootPath
try {
    python - <<'PY'
import sys
sys.path.insert(0, 'app/agent')
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
response = client.get('/api/v1/hosts-auto/inspect?real_write=false')
payload = response.json()
assert response.status_code == 200, response.status_code
assert payload.get('success') is True, payload
inspect = payload.get('inspect', {})
for key in ['expected_count', 'managed_count', 'missing_count', 'stale_count', 'wrong_ip_count', 'duplicate_count', 'external_conflict_count', 'repair_required']:
    assert key in inspect, key
print('Hosts auto UI response OK')
PY
}
finally {
    Pop-Location
}
