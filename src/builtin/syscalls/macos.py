# import ctypes

# libc = ctypes.CDLL("libc.dylib")

# https://github.com/opensource-apple/xnu/blob/master/bsd/kern/syscalls.master


def syscall(num: int, *args) -> int:
    # return libc.syscall(num, *args)
    return 0


def exit(rval: int) -> None:
    syscall(1, rval)


def read(fd: int, cbuf: list[int], nbyte: int) -> int:
    return syscall(3, fd, cbuf, nbyte)


def write(fd: int, cbuf: bytes, nbyte: int) -> int:
    return syscall(4, fd, cbuf, nbyte)


def open(path: str, flags: int, mode: int) -> int:
    return syscall(5, path, flags, mode)


def close(fd: int) -> int:
    return syscall(6, fd)
