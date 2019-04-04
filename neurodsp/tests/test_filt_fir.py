"""Tests fir FIR filters."""

from pytest import raises

from neurodsp.filt.fir import *
from neurodsp.filt.fir import _fir_checks

###################################################################################################
###################################################################################################

def test_filter_signal_fir(tsig):

    sig = filter_signal_fir(tsig, 500, 'bandpass', (8, 12))
    assert True

def test_design_fir_filter():

    sig_length, fs = 1000, 100
    test_filts = {'bandpass' : (8, 12), 'bandstop' : (58, 60),
                  'lowpass' : (None, 10), 'highpass' : (10, None)}

#    for pass_type, f_range in test_filts.items():
#        filter_coefs = design_fir_filter()

def test_fir_checks():

    # Settings for checks
    fs = 500
    sig_length = 2000
    f_lo, f_hi = 4, 8

    # Check filt_len, if defined using n_seconds
    n_seconds = 1.75 # Number chosen to create odd expected filt_len (not needing rounding up)
    expected_filt_len = n_seconds * fs
    filt_len = _fir_checks('bandpass', f_lo, f_hi, n_cycles=None, n_seconds=n_seconds,
                           fs=fs, sig_length=sig_length)
    assert filt_len == expected_filt_len

    # Check filt_len, if defined using n_cycles
    n_cycles = 5
    expected_filt_len = int(np.ceil(fs * n_cycles / f_lo))
    filt_len = _fir_checks('bandpass', f_lo, f_hi, n_cycles=n_cycles, n_seconds=None,
                           fs=fs, sig_length=sig_length)
    assert filt_len == expected_filt_len

    # Check filt_len, if expected to be rounded up to be odd
    n_cycles = 4
    expected_filt_len = int(np.ceil(fs * n_cycles / f_lo)) + 1
    filt_len = _fir_checks('bandpass', f_lo, f_hi, n_cycles=n_cycles, n_seconds=None,
                           fs=fs, sig_length=sig_length)
    assert filt_len == expected_filt_len

    # Check error is raised if the filter designed is longer than the signal
    with raises(ValueError):
        _fir_checks('bandpass', f_lo, f_hi, None, 3, fs, sig_length=1000)
