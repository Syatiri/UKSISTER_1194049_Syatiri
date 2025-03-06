import threading
import multiprocessing
import asyncio
import time
import random
from queue import Queue
from threading import Lock, Semaphore, Thread
from multiprocessing import Process, Queue, Event
from time import ctime, sleep
from mpi4py import MPI

# Global Variables
lock = Lock()
semaphore = Semaphore(3)  
queue_pendaftaran = Queue()
queue_terlambat = Queue()
mahasiswa = ["Syatiri", "Dewi", "Siti", "Rahman", "Tono"]

event_start = Event()
event_stop = Event()


def daftar_mahasiswa(nama_mahasiswa, q):
    """ Fungsi untuk pendaftaran mahasiswa dengan multiprocessing """
    with semaphore:
        with lock:
            print(f"Mahasiswa {nama_mahasiswa} sedang mendaftar... (PID: {multiprocessing.current_process().pid})")
        time.sleep(random.randint(2, 5))
        with lock:
            print(f"Mahasiswa {nama_mahasiswa} telah selesai mendaftar!")
            q.put(nama_mahasiswa)  


def main_multiprocessing():
    """ Fungsi untuk menjalankan multiprocessing pendaftaran mahasiswa """
    processes = []
    queue_pendaftaran = Queue()  

    for mhs in mahasiswa:
        p = Process(target=daftar_mahasiswa, args=(mhs, queue_pendaftaran), name=f"Process-{mhs}")
        processes.append(p)
        p.start()

    for p in processes:
        p.join()  

    
    daftar_terdaftar = []
    while not queue_pendaftaran.empty():
        daftar_terdaftar.append(queue_pendaftaran.get())

    print("\nSemua mahasiswa telah selesai mendaftar.")
    print(f"Mahasiswa yang terdaftar: {daftar_terdaftar}\n")


def runner(nama_mahasiswa):
    """ Fungsi untuk mahasiswa yang terlambat mendaftar """
    sleep(random.randint(2, 5))
    waktu_mendaftar = ctime()
    with lock:
        print(f"Mahasiswa {nama_mahasiswa} TERLAMBAT mendaftar pada: {waktu_mendaftar}")
        queue_terlambat.put((nama_mahasiswa, waktu_mendaftar))


def main_runners():
    """ Fungsi untuk menangani mahasiswa yang terlambat mendaftar """
    threads = []
    
    if not mahasiswa_terlambat:
        print("\nTidak ada mahasiswa yang terlambat mendaftar.\n")
        return

    for mhs in mahasiswa_terlambat:
        t = Thread(target=runner, args=(mhs,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nSemua mahasiswa terlambat telah selesai mendaftar.")
    daftar_terlambat = []
    while not queue_terlambat.empty():
        daftar_terlambat.append(queue_terlambat.get())

    print(f"\nMahasiswa terlambat yang terdaftar: {daftar_terlambat}\n")


async def async_daftar_mahasiswa(nama_mahasiswa):
    """ Fungsi Async untuk mendaftar mahasiswa """
    print(f"Mahasiswa {nama_mahasiswa} sedang mendaftar (AsyncIO)")
    await asyncio.sleep(random.randint(2, 5))
    print(f"Mahasiswa {nama_mahasiswa} telah selesai mendaftar (AsyncIO)")


async def async_main():
    """ Main Async Function """
    tasks = [asyncio.create_task(async_daftar_mahasiswa(mhs)) for mhs in mahasiswa_terlambat]
    await asyncio.gather(*tasks)
    print("\nSeluruh Pendaftaran AsyncIO Selesai!\n")


def mpi_task():
    """ Fungsi untuk menjalankan proses dengan MPI4PY """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"Proses MPI Rank {rank} dari {size} sedang berjalan")
    time.sleep(random.randint(1, 4))
    print(f"Proses MPI Rank {rank} selesai")


def spawn_process():
    """ Fungsi untuk spawning dan menghentikan proses """
    print("\n[SPAWNING] Memulai proses baru...")
    new_process = Process(target=daftar_mahasiswa, args=("Budi", queue_pendaftaran))
    new_process.start()
    time.sleep(3)  
    print(f"[KILLING] Menghentikan proses {new_process.pid}...")
    new_process.terminate()
    new_process.join()
    print(f"[INFO] Proses {new_process.pid} dihentikan!\n")


def test_threads():
    """ Fungsi untuk menguji jalannya threads """
    print("\n[TEST] Memulai Uji Coba Threads...\n")
    thread1 = Thread(target=daftar_mahasiswa, args=("Syatiri", queue_pendaftaran))
    thread2 = Thread(target=daftar_mahasiswa, args=("Dewi", queue_pendaftaran))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("\n[TEST] Uji Coba Threads Selesai!\n")


def tentukan_mahasiswa_terlambat():
    """ Simulasi pemilihan mahasiswa yang terlambat """
    global mahasiswa_terlambat
    mahasiswa_terlambat = random.sample(mahasiswa, random.randint(1, len(mahasiswa)))
    print(f"\nMahasiswa yang TERLAMBAT mendaftar: {mahasiswa_terlambat}\n")


# Main Execution Loop
if __name__ == "__main__":
    while True:
        start_time = time.time()

        print("\n=== SIMULASI PENDAFTARAN MAHASISWA ===")

        tentukan_mahasiswa_terlambat()

        main_multiprocessing() 
        main_runners()  
        asyncio.run(async_main())  
        mpi_task()  
        spawn_process() 
        test_threads()  

        end_time = time.time()
        print(f"\nWaktu eksekusi: {end_time - start_time:.2f} detik\n")
        print("\n=== Semua Proses Selesai ===\n")

        # Looping dengan konfirmasi user
        ulang = input("Ingin mengulang simulasi? (y/n): ").strip().lower()
        if ulang != 'y':
            print("\n=== Program Berhenti ===")
            break
