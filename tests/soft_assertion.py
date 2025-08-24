class SoftAssert:
    def __init__(self):
        self.errors = []

    def check(self, condition, msg=""):
        try:
            assert condition, msg
        except AssertionError as e:
            error_number = len(self.errors) + 1
            self.errors.append(str(f"{error_number}) {e}"))

    def assert_all(self):
        if self.errors:
            raise AssertionError(f"Assertion errors ({len(self.errors)}):\n" + "\n".join(self.errors))