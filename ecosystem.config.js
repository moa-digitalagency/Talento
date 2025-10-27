module.exports = {
  apps: [{
    name: 'talento',
    script: 'app.py',
    interpreter: 'python3',
    cwd: '/root/Talento',  // Changez selon votre chemin
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production',
      PORT: '5004',
      FLASK_ENV: 'production'
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: '5004',
      FLASK_ENV: 'production'
    },
    error_file: './logs/pm2-error.log',
    out_file: './logs/pm2-out.log',
    log_file: './logs/pm2-combined.log',
    time: true,
    merge_logs: true
  }]
};
