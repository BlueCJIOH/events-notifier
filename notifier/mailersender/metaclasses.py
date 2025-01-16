class MailerSendMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            if not args and not kwargs:
                raise RuntimeError(
                    "MailerSendClient instance is not created. Please provide initialization parameters."
                )
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
