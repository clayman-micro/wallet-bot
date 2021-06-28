import config


class BotConfig(config.Config):
    debug = config.BoolField(default=False)
    sentry_dsn = config.StrField()
