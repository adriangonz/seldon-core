package log

import (
	"github.com/go-logr/logr"
	"github.com/go-logr/zapr"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var defaultLogger logr.Logger

func Init(debug bool, logLevel string) (logr.Logger, error) {
	conf := loggerConfig(debug, logLevel)
	logger, err := conf.Build()
	if err != nil {
		return nil, err
	}

	defaultLogger = zapr.NewLogger(logger)
	return defaultLogger, nil
}

func loggerConfig(debug bool, logLevel string) *zap.Config {
	var config *zap.Config

	if debug {
		config = &zap.NewDevelopmentConfig()
	} else {
		config = &zap.NewProductionConfig()
	}

	level := loggerLevel(logLevel)
	config.Level.SetLevel(level)

	return config
}

func loggerLevel(logLevel string) zapcore.Level {
	switch logLevel {
	case "DEBUG":
		return zap.DebugLevel
	case "INFO":
		return zap.InfoLevel
	case "WARN":
	case "WARNING":
		return zap.WarnLevel
	case "ERROR":
		return zap.ErrorLevel
	case "FATAL":
		return zap.FatalLevel
	default:
		return zap.InfoLevel
	}
}

// Info is a package-level helper using default logger.
func Info(msg string, keysAndValues ...interface{}) {
	defaultLogger.Info(msg, keysAndValues...)
}

// Error is a package-level helper using the default logger.
func Error(err error, msg string, keysAndValues ...interface{}) {
	defaultLogger.Error(msg, keysAndValues...)
}

// V is a package-level helper using the default logger.
func V(level int) logr.Logger {
	return defaultLogger.V(level)
}

// WithValues is a package-level helper using the default logger.
func WithValues(keysAndValues ...interface{}) logr.Logger {
	return defaultLogger.WithValues(keysAndValues...)
}

// WithName is a package-level helper using the default logger.
func WithName(name string) logr.Logger {
	return defaultLogger.WithName(name)
}