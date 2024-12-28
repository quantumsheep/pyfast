from builtin.syscalls import macos as syscalls


class TextIO:
    def __init__(self, fd: int):
        self.fd = fd

    def read(self, n: int = -1) -> str:
        if n == 0:
            return ""

        to_read = n if n > 0 else 1024
        result = bytes()

        while True:
            cbuf = [0 for _ in range(to_read)]
            received = syscalls.read(self.fd, cbuf, to_read)
            result += bytes(cbuf)

            if received <= 0 or (n > 0 and len(result) >= n):
                if received == -1:
                    raise OSError("Error reading from file descriptor")
                break

        return result.decode()

    def readline(self) -> str:
        result = bytearray()

        while True:
            cbuf = [0]
            received = syscalls.read(self.fd, cbuf, 1)

            if received <= 0:
                if received == -1:
                    raise OSError("Error reading from file descriptor")
                break

            if cbuf[0] == b"\n":
                break

            result.extend(cbuf)

        return result.decode()

    def write(self, s: str) -> int:
        return syscalls.write(self.fd, s.encode(), len(s))

    def flush(self) -> None:
        pass


stderr = TextIO(0)
stdout = TextIO(1)
stdin = TextIO(2)
