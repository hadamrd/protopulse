class ICancelableMessage:
    @property
    def cancel(self) -> bool:
        raise NotImplementedError()
