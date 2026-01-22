# n8n Setup - Chatbot Platform

## 🔐 Important Credentials

**SAVE THESE CREDENTIALS SECURELY!**

### n8n Web UI Login
- **URL:** http://localhost:5678 (or your ngrok/production URL)
- **Username:** `admin`
- **Password:** `ufmWVBQSwX9Y9l08TwWMv4yns0yqGFW8`

### PostgreSQL Database (n8n internal)
- **Host:** localhost (or `postgres` from inside Docker)
- **Port:** 5432
- **Database:** n8n
- **User:** n8n
- **Password:** `AXIgPNzZ54iJnQCvKxm9EcCKJFcb10QA`

---

## 🚀 Quick Start

### Start n8n
```bash
cd /Users/nico/Documents/pymes/n8n
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f n8n
```

### Stop n8n
```bash
docker-compose down
```

### Access n8n
```bash
open http://localhost:5678
```

---

## 📋 Next Steps

1. ✅ n8n is now running
2. ⬜ Setup ngrok for webhooks (if testing WhatsApp)
3. ⬜ Configure external services (OpenAI, Twilio, Pinecone)
4. ⬜ Import workflows from `/workflows` folder
5. ⬜ Create your first workflow

See **N8N_SETUP_GUIDE.md** in parent directory for detailed instructions.

---

## 🔧 Useful Commands

```bash
# Restart n8n
docker-compose restart n8n

# View PostgreSQL logs
docker-compose logs -f postgres

# Access PostgreSQL shell
docker-compose exec postgres psql -U n8n -d n8n

# Backup workflows
tar -czf backup-$(date +%Y%m%d).tar.gz workflows/

# Update n8n to latest version
docker-compose pull n8n
docker-compose up -d n8n
```

---

## ⚠️ Important Notes

- **NEVER commit .env file to git** (it's in .gitignore)
- Keep your passwords secure
- Change default passwords in production
- Update WEBHOOK_URL when using ngrok or production domain
