# Quick Setup Commands

```bash
# 1
curl -sL https://cli.dev.camber.cloud/install-v2.sh | bash
# 2
camber update
# 3
export CAMBER_API_KEY= # <- Insert your API-key!
# 4
camber me
# 5
git clone https://github.com/CamberCloud-Inc/prod_apps.git
# 6
cd ./prod_apps/nextflow/mag
# 7
camber app create --file app.json # Ensure app.json -> "name": "appname" is unique!
```