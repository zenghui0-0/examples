import os
import pytest



if __name__ == "__main__":
    pytest.main(["test_time_out.py", "test_multi_thread.py::test_threads_faild_break"])