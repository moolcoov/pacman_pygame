import sentry_sdk


def init():
    sentry_sdk.init(
        dsn="https://e07da7aa29db4d0fb0961039fc18ed09@o4504365589659648.ingest.sentry.io/4504365594443777",

        _experiments={
            "profiles_sample_rate": 1.0,
        },

        traces_sample_rate=1.0,
        auto_session_tracking=True
    )
