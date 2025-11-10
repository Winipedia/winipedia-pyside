"""PySide6 QIODevice wrapper."""

import os
from collections.abc import Generator
from functools import partial
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import QFile, QIODevice


class PyQIODevice(QIODevice):
    """PySide6 QIODevice wrapper with enhanced functionality.

    A wrapper class that provides a Python-friendly interface to PySide6's QIODevice,
    allowing for easier integration with Python code while maintaining all the
    original functionality.

    Args:
        QIODevice: The base QIODevice class from PySide6.
    """

    def __init__(self, q_device: QIODevice, *args: Any, **kwargs: Any) -> None:
        """Initialize the PyQIODevice wrapper.

        Args:
            q_device: The QIODevice instance to wrap.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.q_device = q_device

    def atEnd(self) -> bool:  # noqa: N802
        """Check if the device is at the end of data.

        Returns:
            True if the device is at the end, False otherwise.
        """
        return self.q_device.atEnd()

    def bytesAvailable(self) -> int:  # noqa: N802
        """Get the number of bytes available for reading.

        Returns:
            The number of bytes available for reading.
        """
        return self.q_device.bytesAvailable()

    def bytesToWrite(self) -> int:  # noqa: N802
        """Get the number of bytes waiting to be written.

        Returns:
            The number of bytes waiting to be written.
        """
        return self.q_device.bytesToWrite()

    def canReadLine(self) -> bool:  # noqa: N802
        """Check if a complete line can be read from the device.

        Returns:
            True if a complete line can be read, False otherwise.
        """
        return self.q_device.canReadLine()

    def close(self) -> None:
        """Close the device and release resources.

        Closes the underlying QIODevice and calls the parent close method.
        """
        self.q_device.close()
        return super().close()

    def isSequential(self) -> bool:  # noqa: N802
        """Check if the device is sequential.

        Returns:
            True if the device is sequential, False if it supports random access.
        """
        return self.q_device.isSequential()

    def open(self, mode: QIODevice.OpenModeFlag) -> bool:
        """Open the device with the specified mode.

        Args:
            mode: The open mode flag specifying how to open the device.

        Returns:
            True if the device was opened successfully, False otherwise.
        """
        self.q_device.open(mode)
        return super().open(mode)

    def pos(self) -> int:
        """Get the current position in the device.

        Returns:
            The current position in the device.
        """
        return self.q_device.pos()

    def readData(self, maxlen: int) -> bytes:  # noqa: N802
        """Read data from the device.

        Args:
            maxlen: The maximum number of bytes to read.

        Returns:
            The data read from the device as bytes.
        """
        return bytes(self.q_device.read(maxlen).data())

    def readLineData(self, maxlen: int) -> object:  # noqa: N802
        """Read a line from the device.

        Args:
            maxlen: The maximum number of bytes to read.

        Returns:
            The line data read from the device.
        """
        return self.q_device.readLine(maxlen)

    def reset(self) -> bool:
        """Reset the device to its initial state.

        Returns:
            True if the device was reset successfully, False otherwise.
        """
        return self.q_device.reset()

    def seek(self, pos: int) -> bool:
        """Seek to a specific position in the device.

        Args:
            pos: The position to seek to.

        Returns:
            True if the seek operation was successful, False otherwise.
        """
        return self.q_device.seek(pos)

    def size(self) -> int:
        """Get the size of the device.

        Returns:
            The size of the device in bytes.
        """
        return self.q_device.size()

    def skipData(self, maxSize: int) -> int:  # noqa: N802, N803
        """Skip data in the device.

        Args:
            maxSize: The maximum number of bytes to skip.

        Returns:
            The actual number of bytes skipped.
        """
        return self.q_device.skip(maxSize)

    def waitForBytesWritten(self, msecs: int) -> bool:  # noqa: N802
        """Wait for bytes to be written to the device.

        Args:
            msecs: The maximum time to wait in milliseconds.

        Returns:
            True if bytes were written within the timeout, False otherwise.
        """
        return self.q_device.waitForBytesWritten(msecs)

    def waitForReadyRead(self, msecs: int) -> bool:  # noqa: N802
        """Wait for the device to be ready for reading.

        Args:
            msecs: The maximum time to wait in milliseconds.

        Returns:
            True if the device became ready within the timeout, False otherwise.
        """
        return self.q_device.waitForReadyRead(msecs)

    def writeData(self, data: bytes | bytearray | memoryview, len: int) -> int:  # noqa: A002, ARG002, N802
        """Write data to the device.

        Args:
            data: The data to write to the device.
            len: The length parameter (unused in this implementation).

        Returns:
            The number of bytes actually written.
        """
        return self.q_device.write(data)


class PyQFile(PyQIODevice):
    """QFile wrapper with enhanced Python integration.

    A specialized PyQIODevice wrapper for file operations, providing a more
    Python-friendly interface to PySide6's QFile functionality.
    """

    def __init__(self, path: Path, *args: Any, **kwargs: Any) -> None:
        """Initialize the PyQFile with a file path.

        Args:
            path: The file path to open.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(QFile(path), *args, **kwargs)
        self.q_device: QFile


class EncryptedPyQFile(PyQFile):
    """Encrypted file wrapper using AES-GCM encryption.

    Provides transparent encryption/decryption for file operations using
    AES-GCM (Galois/Counter Mode) encryption. Data is encrypted in chunks
    for efficient streaming operations.
    """

    NONCE_SIZE = 12
    CIPHER_SIZE = 64 * 1024
    TAG_SIZE = 16
    CHUNK_SIZE = CIPHER_SIZE + NONCE_SIZE + TAG_SIZE
    CHUNK_OVERHEAD = NONCE_SIZE + TAG_SIZE

    def __init__(self, path: Path, aes_gcm: AESGCM, *args: Any, **kwargs: Any) -> None:
        """Initialize the encrypted file wrapper.

        Args:
            path: The file path to open.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(path, *args, **kwargs)
        self.q_device: QFile
        self.aes_gcm = aes_gcm
        self.dec_size = self.size()

    def readData(self, maxlen: int) -> bytes:  # noqa: N802
        """Read and decrypt data from the encrypted file.

        Reads encrypted chunks from the file, decrypts them, and returns
        the requested portion of decrypted data.

        Args:
            maxlen: The maximum number of decrypted bytes to read.

        Returns:
            The decrypted data as bytes.
        """
        # where we are in the encrypted data
        dec_pos = self.pos()
        # where we are in the decrypted data
        enc_pos = self.get_encrypted_pos(dec_pos)

        # get the chunk start and end
        chunk_start = self.get_chunk_start(enc_pos)
        chunk_end = self.get_chunk_end(enc_pos, maxlen)
        new_maxlen = chunk_end - chunk_start

        # read the chunk
        self.seek(chunk_start)
        enc_data = super().readData(new_maxlen)
        # decrypt the chunk
        dec_data = self.decrypt_data(enc_data)

        # get the start and end of the requested data in the decrypted data
        dec_chunk_start = self.get_decrypted_pos(chunk_start + self.NONCE_SIZE)

        req_data_start = dec_pos - dec_chunk_start
        req_data_end = req_data_start + maxlen

        dec_pos += maxlen
        self.seek(dec_pos)

        return dec_data[req_data_start:req_data_end]

    def writeData(self, data: bytes | bytearray | memoryview, len: int) -> int:  # noqa: A002, ARG002, N802
        """Encrypt and write data to the file.

        Args:
            data: The data to encrypt and write.
            len: The length parameter (unused in this implementation).

        Returns:
            The number of bytes actually written.
        """
        encrypted_data = self.encrypt_data(bytes(data))
        encrypted_len = encrypted_data.__len__()
        return super().writeData(encrypted_data, encrypted_len)

    def size(self) -> int:
        """Get the decrypted size of the file.

        Calculates the decrypted size based on the encrypted file size
        and chunk structure.

        Returns:
            The decrypted size of the file in bytes.
        """
        self.enc_size = super().size()
        self.num_chunks = self.enc_size // self.CHUNK_SIZE + 1
        self.dec_size = self.num_chunks * self.CIPHER_SIZE
        return self.dec_size

    def get_decrypted_pos(self, enc_pos: int) -> int:
        """Convert encrypted file position to decrypted position.

        Args:
            enc_pos: The position in the encrypted file.

        Returns:
            The corresponding position in the decrypted data.
        """
        if enc_pos >= self.enc_size:
            return self.dec_size

        num_chunks_before = enc_pos // self.CHUNK_SIZE
        last_enc_chunk_start = num_chunks_before * self.CHUNK_SIZE
        last_dec_chunk_start = num_chunks_before * self.CIPHER_SIZE

        enc_bytes_to_move = enc_pos - last_enc_chunk_start

        return last_dec_chunk_start + enc_bytes_to_move - self.NONCE_SIZE

    def get_encrypted_pos(self, dec_pos: int) -> int:
        """Convert decrypted position to encrypted file position.

        Args:
            dec_pos: The position in the decrypted data.

        Returns:
            The corresponding position in the encrypted file.
        """
        if dec_pos >= self.dec_size:
            return self.enc_size
        num_chunks_before = dec_pos // self.CIPHER_SIZE
        last_dec_chunk_start = num_chunks_before * self.CIPHER_SIZE
        last_enc_chunk_start = num_chunks_before * self.CHUNK_SIZE

        dec_bytes_to_move = dec_pos - last_dec_chunk_start

        return last_enc_chunk_start + self.NONCE_SIZE + dec_bytes_to_move

    def get_chunk_start(self, pos: int) -> int:
        """Get the start position of the chunk containing the given position.

        Args:
            pos: The position to find the chunk start for.

        Returns:
            The start position of the chunk.
        """
        return pos // self.CHUNK_SIZE * self.CHUNK_SIZE

    def get_chunk_end(self, pos: int, maxlen: int) -> int:
        """Get the end position of the chunk range for the given position and length.

        Args:
            pos: The starting position.
            maxlen: The maximum length to read.

        Returns:
            The end position of the chunk range.
        """
        return (pos + maxlen) // self.CHUNK_SIZE * self.CHUNK_SIZE + self.CHUNK_SIZE

    @classmethod
    def chunk_generator(
        cls, data: bytes, *, is_encrypted: bool
    ) -> Generator[bytes, None, None]:
        """Generate chunks from data.

        Args:
            data: The data to split into chunks.
            is_encrypted: Whether the data is encrypted (affects chunk size).

        Yields:
            Chunks of data of appropriate size.
        """
        size = cls.CHUNK_SIZE if is_encrypted else cls.CIPHER_SIZE
        for i in range(0, len(data), size):
            yield data[i : i + size]

    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data using AES-GCM.

        Args:
            data: The data to encrypt.

        Returns:
            The encrypted data with nonce and authentication tag.
        """
        return self.encrypt_data_static(data, self.aes_gcm)

    @classmethod
    def encrypt_data_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Encrypt data using AES-GCM (static method).

        Args:
            data: The data to encrypt.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.

        Returns:
            The encrypted data with nonce and authentication tag.
        """
        decrypted_chunks = cls.chunk_generator(data, is_encrypted=False)
        encrypted_chunks = map(
            partial(cls.encrypt_chunk_static, aes_gcm=aes_gcm), decrypted_chunks
        )
        return b"".join(encrypted_chunks)

    @classmethod
    def encrypt_chunk_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Encrypt a single chunk using AES-GCM (static method).

        Args:
            data: The chunk data to encrypt.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.

        Returns:
            The encrypted chunk with nonce and authentication tag.
        """
        nonce = os.urandom(12)
        aad = cls.__name__.encode()
        return nonce + aes_gcm.encrypt(nonce, data, aad)

    def decrypt_data(self, data: bytes) -> bytes:
        """Decrypt data using AES-GCM.

        Args:
            data: The encrypted data to decrypt.

        Returns:
            The decrypted data as bytes.
        """
        return self.decrypt_data_static(data, self.aes_gcm)

    @classmethod
    def decrypt_data_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Decrypt data using AES-GCM (static method).

        Args:
            data: The encrypted data to decrypt.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.

        Returns:
            The decrypted data as bytes.
        """
        encrypted_chunks = cls.chunk_generator(data, is_encrypted=True)
        decrypted_chunks = map(
            partial(cls.decrypt_chunk_static, aes_gcm=aes_gcm), encrypted_chunks
        )
        return b"".join(decrypted_chunks)

    @classmethod
    def decrypt_chunk_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Decrypt a single chunk using AES-GCM (static method).

        Args:
            data: The encrypted chunk data to decrypt.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.

        Returns:
            The decrypted chunk data as bytes.
        """
        nonce = data[: cls.NONCE_SIZE]
        cipher_and_tag = data[cls.NONCE_SIZE :]
        aad = cls.__name__.encode()
        return aes_gcm.decrypt(nonce, cipher_and_tag, aad)
