// lib/logger.js
// Centralized logging configuration for Sim Studio

const isDevelopment = process.env.NODE_ENV === 'development'
const logLevel = process.env.LOG_LEVEL || (isDevelopment ? 'debug' : 'info')

class Logger {
  constructor() {
    this.levels = {
      error: 0,
      warn: 1, 
      info: 2,
      debug: 3
    }
    this.currentLevel = this.levels[logLevel] || this.levels.info
  }

  formatMessage(level, message, meta = {}) {
    const timestamp = new Date().toISOString()
    const logEntry = {
      timestamp,
      level,
      message,
      ...meta
    }

    if (isDevelopment) {
      return `[${timestamp}] ${level.toUpperCase()}: ${message}`
    }

    return JSON.stringify(logEntry)
  }

  log(level, message, meta = {}) {
    if (this.levels[level] <= this.currentLevel) {
      console.log(this.formatMessage(level, message, meta))
    }
  }

  error(message, meta = {}) {
    this.log('error', message, meta)
  }

  warn(message, meta = {}) {
    this.log('warn', message, meta)
  }

  info(message, meta = {}) {
    this.log('info', message, meta)
  }

  debug(message, meta = {}) {
    this.log('debug', message, meta)
  }
}

export const logger = new Logger()
export default logger
