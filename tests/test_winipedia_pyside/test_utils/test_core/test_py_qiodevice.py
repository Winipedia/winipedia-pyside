"""Tests for winipedia_pyside.core.py_qiodevice module."""

from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import QIODevice
from pytest_mock import MockerFixture
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg

from winipedia_pyside.utils.core import py_qiodevice
from winipedia_pyside.utils.core.py_qiodevice import (
    EncryptedPyQFile,
    PyQFile,
    PyQIODevice,
)


class TestPyQIODevice:
    """Test class for PyQIODevice."""

    def test___init__(self, mocker: MockerFixture) -> None:
        """Test method for __init__."""
        # Test basic initialization
        mock_device = mocker.MagicMock(spec=QIODevice)
        py_device = PyQIODevice(mock_device)
        assert_with_msg(
            py_device.q_device is mock_device,
            "q_device should be set to the provided device",
        )

    def test_atEnd(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for atEnd."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.atEnd.return_value = True
        py_device = PyQIODevice(mock_device)

        result = py_device.atEnd()
        assert_with_msg(
            result is True,
            "atEnd should return True when underlying device returns True",
        )
        mock_device.atEnd.assert_called_once()

        # Test False case
        mock_device.atEnd.return_value = False
        result = py_device.atEnd()
        assert_with_msg(
            result is False,
            "atEnd should return False when underlying device returns False",
        )

    def test_bytesAvailable(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for bytesAvailable."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_bytes = 1024
        mock_device.bytesAvailable.return_value = expected_bytes
        py_device = PyQIODevice(mock_device)

        result = py_device.bytesAvailable()
        assert_with_msg(
            result == expected_bytes, f"bytesAvailable should return {expected_bytes}"
        )
        mock_device.bytesAvailable.assert_called_once()

    def test_bytesToWrite(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for bytesToWrite."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_bytes = 512
        mock_device.bytesToWrite.return_value = expected_bytes
        py_device = PyQIODevice(mock_device)

        result = py_device.bytesToWrite()
        assert_with_msg(
            result == expected_bytes, f"bytesToWrite should return {expected_bytes}"
        )
        mock_device.bytesToWrite.assert_called_once()

    def test_canReadLine(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for canReadLine."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.canReadLine.return_value = True
        py_device = PyQIODevice(mock_device)

        result = py_device.canReadLine()
        assert_with_msg(
            result is True,
            "canReadLine should return True when underlying device returns True",
        )
        mock_device.canReadLine.assert_called_once()

    def test_close(self, mocker: MockerFixture) -> None:
        """Test method for close."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        py_device = PyQIODevice(mock_device)

        py_device.close()
        mock_device.close.assert_called_once()

    def test_isSequential(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for isSequential."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.isSequential.return_value = False
        py_device = PyQIODevice(mock_device)

        result = py_device.isSequential()
        assert_with_msg(
            result is False,
            "isSequential should return False when underlying device returns False",
        )
        mock_device.isSequential.assert_called_once()

    def test_open(self, mocker: MockerFixture) -> None:
        """Test method for open."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.open.return_value = True
        py_device = PyQIODevice(mock_device)

        mode = QIODevice.OpenModeFlag.ReadOnly
        result = py_device.open(mode)
        assert_with_msg(result is True, "open should return True when successful")
        mock_device.open.assert_called_once_with(mode)

    def test_pos(self, mocker: MockerFixture) -> None:
        """Test method for pos."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_pos = 100
        mock_device.pos.return_value = expected_pos
        py_device = PyQIODevice(mock_device)

        result = py_device.pos()
        assert_with_msg(result == expected_pos, f"pos should return {expected_pos}")
        mock_device.pos.assert_called_once()

    def test_readData(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for readData."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        test_data = b"test data"
        mock_byte_array = mocker.MagicMock()
        mock_byte_array.data.return_value = test_data
        mock_device.read.return_value = mock_byte_array
        py_device = PyQIODevice(mock_device)

        maxlen = 100
        result = py_device.readData(maxlen)
        assert_with_msg(result == test_data, f"readData should return {test_data!r}")
        mock_device.read.assert_called_once_with(maxlen)

    def test_readLineData(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for readLineData."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_line = "test line"
        mock_device.readLine.return_value = expected_line
        py_device = PyQIODevice(mock_device)

        maxlen = 100
        result = py_device.readLineData(maxlen)
        assert_with_msg(
            result == expected_line, f"readLineData should return {expected_line}"
        )
        mock_device.readLine.assert_called_once_with(maxlen)

    def test_reset(self, mocker: MockerFixture) -> None:
        """Test method for reset."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.reset.return_value = True
        py_device = PyQIODevice(mock_device)

        result = py_device.reset()
        assert_with_msg(result is True, "reset should return True when successful")
        mock_device.reset.assert_called_once()

    def test_seek(self, mocker: MockerFixture) -> None:
        """Test method for seek."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.seek.return_value = True
        py_device = PyQIODevice(mock_device)

        pos = 50
        result = py_device.seek(pos)
        assert_with_msg(result is True, "seek should return True when successful")
        mock_device.seek.assert_called_once_with(pos)

    def test_size(self, mocker: MockerFixture) -> None:
        """Test method for size."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_size = 2048
        mock_device.size.return_value = expected_size
        py_device = PyQIODevice(mock_device)

        result = py_device.size()
        assert_with_msg(result == expected_size, f"size should return {expected_size}")
        mock_device.size.assert_called_once()

    def test_skipData(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for skipData."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_skipped = 64
        mock_device.skip.return_value = expected_skipped
        py_device = PyQIODevice(mock_device)

        max_size = 100
        result = py_device.skipData(max_size)
        assert_with_msg(
            result == expected_skipped, f"skipData should return {expected_skipped}"
        )
        mock_device.skip.assert_called_once_with(max_size)

    def test_waitForBytesWritten(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for waitForBytesWritten."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.waitForBytesWritten.return_value = True
        py_device = PyQIODevice(mock_device)

        msecs = 1000
        result = py_device.waitForBytesWritten(msecs)
        assert_with_msg(
            result is True, "waitForBytesWritten should return True when successful"
        )
        mock_device.waitForBytesWritten.assert_called_once_with(msecs)

    def test_waitForReadyRead(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for waitForReadyRead."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        mock_device.waitForReadyRead.return_value = True
        py_device = PyQIODevice(mock_device)

        msecs = 1000
        result = py_device.waitForReadyRead(msecs)
        assert_with_msg(
            result is True, "waitForReadyRead should return True when successful"
        )
        mock_device.waitForReadyRead.assert_called_once_with(msecs)

    def test_writeData(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for writeData."""
        mock_device = mocker.MagicMock(spec=QIODevice)
        expected_written = 10
        mock_device.write.return_value = expected_written
        py_device = PyQIODevice(mock_device)

        test_data = b"test data"
        result = py_device.writeData(test_data, len(test_data))
        assert_with_msg(
            result == expected_written, f"writeData should return {expected_written}"
        )
        mock_device.write.assert_called_once_with(test_data)


class TestPyQFile:
    """Test class for PyQFile."""

    def test___init__(self, mocker: MockerFixture) -> None:
        """Test method for __init__."""
        # Test basic initialization
        test_path = Path("test_file.txt")
        mock_qfile_class = mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mock_qfile = mocker.MagicMock()
        mock_qfile_class.return_value = mock_qfile

        py_file = PyQFile(test_path)

        assert_with_msg(
            py_file.q_device is mock_qfile,
            "q_device should be set to QFile instance",
        )
        mock_qfile_class.assert_called_once_with(test_path)

        # Test that the QFile was created with the correct path
        mock_qfile_class.assert_called_once_with(test_path)


class TestEncryptedPyQFile:
    """Test class for EncryptedPyQFile."""

    def test___init__(self, mocker: MockerFixture) -> None:
        """Test method for __init__."""
        # Test basic initialization
        test_path = Path("encrypted_file.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mock_qfile_class = mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mock_qfile = mocker.MagicMock()
        mock_qfile_class.return_value = mock_qfile

        # Mock the size method to avoid calling it during initialization
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        assert_with_msg(
            encrypted_file.q_device is mock_qfile,
            "q_device should be set to QFile instance",
        )
        assert_with_msg(
            encrypted_file.aes_gcm is aes_gcm,
            "aes_gcm should be set to provided cipher",
        )
        expected_dec_size = 1024
        assert_with_msg(
            encrypted_file.dec_size == expected_dec_size,
            "dec_size should be set from size() call",
        )
        mock_qfile_class.assert_called_once_with(test_path)

    def test_readData(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for readData."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Mock all the methods used in readData
        mocker.patch.object(encrypted_file, "pos", return_value=0)
        mocker.patch.object(encrypted_file, "get_encrypted_pos", return_value=12)
        mocker.patch.object(encrypted_file, "get_chunk_start", return_value=0)
        mocker.patch.object(encrypted_file, "get_chunk_end", return_value=65564)
        mocker.patch.object(encrypted_file, "seek")
        mocker.patch.object(encrypted_file, "get_decrypted_pos", return_value=0)
        mocker.patch.object(
            encrypted_file, "decrypt_data", return_value=b"decrypted test data"
        )

        # Mock the parent readData method
        mocker.patch.object(PyQFile, "readData", return_value=b"encrypted data")
        result = encrypted_file.readData(10)

        assert_with_msg(
            result == b"decrypted ",
            "readData should return decrypted data slice",
        )

    def test_writeData(self, mocker: MockerFixture) -> None:  # noqa: N802
        """Test method for writeData."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Mock encrypt_data and parent writeData
        test_data = b"test data"
        encrypted_data = b"encrypted test data"
        mocker.patch.object(encrypted_file, "encrypt_data", return_value=encrypted_data)

        mock_parent_write = mocker.patch.object(
            PyQFile, "writeData", return_value=len(encrypted_data)
        )
        result = encrypted_file.writeData(test_data, len(test_data))

        assert_with_msg(
            result == len(encrypted_data),
            f"writeData should return {len(encrypted_data)}",
        )
        mock_parent_write.assert_called_once_with(encrypted_data, len(encrypted_data))

    def test_size(self, mocker: MockerFixture) -> None:
        """Test method for size."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        # Don't mock size during initialization for this test
        mocker.patch.object(PyQFile, "size", return_value=131100)  # Mock parent size
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Test the size calculation
        result = encrypted_file.size()

        # Expected calculation: enc_size=131100, num_chunks=131100//65564+1=2
        # dec_size=2*65536=131072
        expected_enc_size = 131100
        expected_num_chunks = (
            expected_enc_size // EncryptedPyQFile.CHUNK_SIZE + 1
        )  # 131100//65564+1=2
        expected_dec_size = (
            expected_num_chunks * EncryptedPyQFile.CIPHER_SIZE
        )  # 2*65536=131072

        assert_with_msg(
            result == expected_dec_size,
            f"size should return calculated decrypted size {expected_dec_size}",
        )
        assert_with_msg(
            encrypted_file.enc_size == expected_enc_size,
            "enc_size should be set from parent size",
        )
        assert_with_msg(
            encrypted_file.num_chunks == expected_num_chunks,
            "num_chunks should be calculated correctly",
        )

    def test_get_decrypted_pos(self, mocker: MockerFixture) -> None:
        """Test method for get_decrypted_pos."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)
        encrypted_file.enc_size = 131100
        encrypted_file.dec_size = 196608

        # Test position at start of first chunk (after nonce)
        result = encrypted_file.get_decrypted_pos(12)
        assert_with_msg(
            result == 0,
            "Position 12 (after first nonce) should map to decrypted position 0",
        )

        # Test position in middle of first chunk
        result = encrypted_file.get_decrypted_pos(1000)
        expected = 1000 - 12  # 988
        assert_with_msg(
            result == expected,
            f"Position 1000 should map to decrypted position {expected}",
        )

        # Test position beyond encrypted size
        result = encrypted_file.get_decrypted_pos(200000)
        assert_with_msg(
            result == encrypted_file.dec_size,
            "Position beyond enc_size should return dec_size",
        )

    def test_get_encrypted_pos(self, mocker: MockerFixture) -> None:
        """Test method for get_encrypted_pos."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)
        encrypted_file.enc_size = 131100
        encrypted_file.dec_size = 196608

        # Test position at start of decrypted data
        result = encrypted_file.get_encrypted_pos(0)
        expected_nonce_offset = EncryptedPyQFile.NONCE_SIZE
        expected_msg = (
            f"Decrypted position 0 should map to encrypted position "
            f"{expected_nonce_offset} (after nonce)"
        )
        assert_with_msg(result == expected_nonce_offset, expected_msg)

        # Test position in middle of first chunk
        result = encrypted_file.get_encrypted_pos(1000)
        expected = 12 + 1000  # 1012
        assert_with_msg(
            result == expected,
            f"Decrypted position 1000 should map to encrypted position {expected}",
        )

        # Test position beyond decrypted size
        result = encrypted_file.get_encrypted_pos(300000)
        assert_with_msg(
            result == encrypted_file.enc_size,
            "Position beyond dec_size should return enc_size",
        )

    def test_get_chunk_start(self, mocker: MockerFixture) -> None:
        """Test method for get_chunk_start."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Test position at start of chunk
        result = encrypted_file.get_chunk_start(0)
        assert_with_msg(result == 0, "Position 0 should return chunk start 0")

        # Test position in middle of first chunk
        result = encrypted_file.get_chunk_start(1000)
        assert_with_msg(result == 0, "Position 1000 should return chunk start 0")

        # Test position at start of second chunk
        chunk_size = EncryptedPyQFile.CHUNK_SIZE
        result = encrypted_file.get_chunk_start(chunk_size)
        assert_with_msg(
            result == chunk_size,
            f"Position {chunk_size} should return chunk start {chunk_size}",
        )

        # Test position in middle of second chunk
        result = encrypted_file.get_chunk_start(chunk_size + 1000)
        assert_with_msg(
            result == chunk_size,
            f"Position {chunk_size + 1000} should return chunk start {chunk_size}",
        )

    def test_get_chunk_end(self, mocker: MockerFixture) -> None:
        """Test method for get_chunk_end."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Test small read from start
        result = encrypted_file.get_chunk_end(0, 100)
        chunk_size = EncryptedPyQFile.CHUNK_SIZE
        assert_with_msg(
            result == chunk_size,
            f"Small read should return one chunk end {chunk_size}",
        )

        # Test read spanning multiple chunks
        result = encrypted_file.get_chunk_end(0, chunk_size + 1000)
        expected = 2 * chunk_size
        assert_with_msg(
            result == expected, f"Read spanning chunks should return {expected}"
        )

    def test_chunk_generator(self) -> None:
        """Test method for chunk_generator."""
        # Test with unencrypted data
        test_data = b"a" * 200000  # 200KB of data
        chunks = list(EncryptedPyQFile.chunk_generator(test_data, is_encrypted=False))

        expected_chunk_count = (
            len(test_data) + EncryptedPyQFile.CIPHER_SIZE - 1
        ) // EncryptedPyQFile.CIPHER_SIZE
        assert_with_msg(
            len(chunks) == expected_chunk_count,
            f"Should generate {expected_chunk_count} chunks for unencrypted data",
        )

        # Check first chunk size
        assert_with_msg(
            len(chunks[0]) == EncryptedPyQFile.CIPHER_SIZE,
            f"First chunk should be {EncryptedPyQFile.CIPHER_SIZE} bytes",
        )

        # Test with encrypted data
        encrypted_data = b"b" * 200000
        encrypted_chunks = list(
            EncryptedPyQFile.chunk_generator(encrypted_data, is_encrypted=True)
        )

        expected_count = (
            len(encrypted_data) + EncryptedPyQFile.CHUNK_SIZE - 1
        ) // EncryptedPyQFile.CHUNK_SIZE
        encrypted_msg = f"Should generate {expected_count} chunks for encrypted data"
        assert_with_msg(len(encrypted_chunks) == expected_count, encrypted_msg)

    def test_encrypt_data(self, mocker: MockerFixture) -> None:
        """Test method for encrypt_data."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Mock the static method
        test_data = b"test data"
        expected_encrypted = b"encrypted data"
        mock_static = mocker.patch.object(
            EncryptedPyQFile,
            "encrypt_data_static",
            return_value=expected_encrypted,
        )
        result = encrypted_file.encrypt_data(test_data)

        assert_with_msg(
            result == expected_encrypted,
            "encrypt_data should return result from static method",
        )
        mock_static.assert_called_once_with(test_data, aes_gcm)

    def test_encrypt_data_static(self, mocker: MockerFixture) -> None:
        """Test method for encrypt_data_static."""
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)
        test_data = b"test data for encryption"

        # Mock chunk_generator and encrypt_chunk_static
        mock_chunks = [b"chunk1", b"chunk2"]
        encrypted_chunks = [b"enc_chunk1", b"enc_chunk2"]

        mock_generator = mocker.patch.object(
            EncryptedPyQFile, "chunk_generator", return_value=mock_chunks
        )
        mock_encrypt_chunk = mocker.patch.object(
            EncryptedPyQFile, "encrypt_chunk_static", side_effect=encrypted_chunks
        )
        result = EncryptedPyQFile.encrypt_data_static(test_data, aes_gcm)

        expected = b"enc_chunk1enc_chunk2"
        assert_with_msg(
            result == expected,
            f"encrypt_data_static should return joined encrypted chunks {expected!r}",
        )
        mock_generator.assert_called_once_with(test_data, is_encrypted=False)
        expected_chunk_count = len(mock_chunks)
        assert_with_msg(
            mock_encrypt_chunk.call_count == expected_chunk_count,
            "encrypt_chunk_static should be called for each chunk",
        )

    def test_encrypt_chunk_static(self, mocker: MockerFixture) -> None:
        """Test method for encrypt_chunk_static."""
        test_data = b"test chunk data"
        nonce_size = EncryptedPyQFile.NONCE_SIZE

        # Mock os.urandom to get predictable nonce
        mock_urandom = mocker.patch("os.urandom", return_value=b"test_nonce12")

        # Create a mock AES-GCM object
        mock_aes_gcm = mocker.MagicMock()
        encrypted_content = b"encrypted_content"
        mock_aes_gcm.encrypt.return_value = encrypted_content

        result = EncryptedPyQFile.encrypt_chunk_static(test_data, mock_aes_gcm)

        expected = b"test_nonce12" + encrypted_content
        expected_msg = (
            f"encrypt_chunk_static should return nonce + encrypted content {expected!r}"
        )
        assert_with_msg(result == expected, expected_msg)
        mock_urandom.assert_called_once_with(nonce_size)
        mock_aes_gcm.encrypt.assert_called_once_with(
            b"test_nonce12", test_data, b"EncryptedPyQFile"
        )

    def test_decrypt_data(self, mocker: MockerFixture) -> None:
        """Test method for decrypt_data."""
        test_path = Path("test.txt")
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)

        mocker.patch(make_obj_importpath(py_qiodevice) + ".QFile")
        mocker.patch.object(EncryptedPyQFile, "size", return_value=1024)
        encrypted_file = EncryptedPyQFile(test_path, aes_gcm)

        # Mock the static method
        encrypted_data = b"encrypted data"
        expected_decrypted = b"decrypted data"
        mock_static = mocker.patch.object(
            EncryptedPyQFile,
            "decrypt_data_static",
            return_value=expected_decrypted,
        )
        result = encrypted_file.decrypt_data(encrypted_data)

        assert_with_msg(
            result == expected_decrypted,
            "decrypt_data should return result from static method",
        )
        mock_static.assert_called_once_with(encrypted_data, aes_gcm)

    def test_decrypt_data_static(self, mocker: MockerFixture) -> None:
        """Test method for decrypt_data_static."""
        test_key = AESGCM.generate_key(bit_length=256)
        aes_gcm = AESGCM(test_key)
        encrypted_data = b"encrypted data for decryption"

        # Mock chunk_generator and decrypt_chunk_static
        mock_chunks = [b"enc_chunk1", b"enc_chunk2"]
        decrypted_chunks = [b"dec_chunk1", b"dec_chunk2"]
        expected_chunk_count = len(mock_chunks)

        mock_generator = mocker.patch.object(
            EncryptedPyQFile, "chunk_generator", return_value=mock_chunks
        )
        mock_decrypt_chunk = mocker.patch.object(
            EncryptedPyQFile, "decrypt_chunk_static", side_effect=decrypted_chunks
        )
        result = EncryptedPyQFile.decrypt_data_static(encrypted_data, aes_gcm)

        expected = b"dec_chunk1dec_chunk2"
        assert_with_msg(
            result == expected,
            f"decrypt_data_static should return joined decrypted chunks {expected!r}",
        )
        mock_generator.assert_called_once_with(encrypted_data, is_encrypted=True)
        assert_with_msg(
            mock_decrypt_chunk.call_count == expected_chunk_count,
            "decrypt_chunk_static should be called for each chunk",
        )

    def test_decrypt_chunk_static(self, mocker: MockerFixture) -> None:
        """Test method for decrypt_chunk_static."""
        # Create test encrypted chunk (nonce + cipher_and_tag)
        nonce = b"test_nonce12"
        cipher_and_tag = b"encrypted_content_with_tag"
        encrypted_chunk = nonce + cipher_and_tag

        # Create a mock AES-GCM object
        mock_aes_gcm = mocker.MagicMock()
        decrypted_content = b"decrypted content"
        mock_aes_gcm.decrypt.return_value = decrypted_content

        result = EncryptedPyQFile.decrypt_chunk_static(encrypted_chunk, mock_aes_gcm)

        expected_msg = (
            f"decrypt_chunk_static should return content {decrypted_content!r}"
        )
        assert_with_msg(result == decrypted_content, expected_msg)
        mock_aes_gcm.decrypt.assert_called_once_with(
            nonce, cipher_and_tag, b"EncryptedPyQFile"
        )
