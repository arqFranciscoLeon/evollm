cd /root/evollm
export PYTHONPATH=/root/evollm/src
export MPLBACKEND=Agg
# Force single-threaded BLAS. Two reasons:
# 1) Avoids the fork+OpenBLAS deadlock (forked workers inherit a locked
#    OpenBLAS threadpool lock -> hang at 0% CPU; observed in the 8-proc test).
# 2) Correct for CPU-bound multiprocessing anyway: 8 workers x N BLAS threads
#    would oversubscribe the 8 cores. One BLAS thread per worker is optimal.
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
/root/venv/bin/python run_hetzner.py --iterations 500 --processes 8 --shard s1 >> run_s1.log 2>&1
