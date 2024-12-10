import asyncio
import hashlib
import json
import os
import random
import sys
import threading
import time

import googlecloudprofiler


# プロファイル結果はランダムに1分間隔で書かれるので、1分ちょうどだと書かれないことがあるため2分ぐらい回しておく
DURATION_SECS = 120

# JSON化に使うダミーデータ
JSON_SAMPLE = {
    'foo': 'bar',
    'a': 123,
    'b': 456.789,
}

# sha256 に使うダミーデータ
HASH_SAMPLE = random.randbytes(1 * 1024 * 1024)


def run_sleep():
    """単にスリープする処理"""
    time.sleep(1)

def run_python():
    """pythonでCPUを使う処理"""
    l = [0]
    for i in range(1000000):
        l[0] = i

def run_native():
    """ネイティブコードでCPUを使う処理"""
    for _ in range(100000):
        b = json.dumps(JSON_SAMPLE)

def run_thread():
    """スレッドでCPUを使う処理"""

    def thread_task():
        start = time.monotonic()
        while time.monotonic() < start + 1:  # 1秒間実行
            l = [0]
            for i in range(1000000):
                l[0] = i

    t = threading.Thread(target=thread_task)
    t.start()
    t.join()
    
def run_async():
    """asyncでCPUを使う処理"""

    async def async_task():
        start = time.monotonic()
        while time.monotonic() < start + 1:  # 1秒間実行
            l = [0]
            for i in range(1000000):
                l[0] = i

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_task())

def run_gc():
    """大量にメモリ確保する処理。GC時間が反映されるか確認したい"""
    for i in range(1000):
        l = [None] * 100000
        l[0] = l # 循環参照を作ることでリファレンスカウントによる解放を防ぐ

def run_digest():
    """複数スレッドでCPUを使う処理、GILが解放されるケース"""

    def digest_task():
        start = time.monotonic()
        while time.monotonic() < start + 1:  # 1秒間実行
            hashlib.sha256(HASH_SAMPLE).hexdigest()

    ts = [None] * 8
    for i, _ in enumerate(ts):
        ts[i] = threading.Thread(target=digest_task)
        ts[i].start()
    for i, _ in enumerate(ts):
        ts[i].join()


TASKS = {
    'sleep': run_sleep,
    'python': run_python,
    'native': run_native,
    'thread': run_thread,
    'async': run_async,
    'gc': run_gc,
    'digest': run_digest,
}


def main():
    mode = sys.argv[1]

    # Profiler initialization. It starts a daemon thread which continuously
    # collects and uploads profiles. Best done as early as possible.
    try:
        googlecloudprofiler.start(
            service='cloud-profiler-python-example-' + mode,
            service_version='0.0.1',
            # verbose is the logging level. 0-error, 1-warning, 2-info,
            # 3-debug. It defaults to 0 (error) if not set.
            verbose=3,
            # project_id must be set if not running on GCP.
            project_id=os.environ['GOOGLE_CLOUD_PROJECT'],
        )
    except (ValueError, NotImplementedError) as exc:
        print(exc)  # Handle errors here
        return

    import gc
    gc.set_debug(gc.DEBUG_STATS)

    start = time.monotonic()

    task = TASKS[mode]

    while time.monotonic() < start + DURATION_SECS:
        task()


if __name__ == "__main__":
    main()
