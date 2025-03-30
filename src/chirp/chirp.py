import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--N", type=int, default=1000, help="sampling_frequency")
    parser.add_argument("--T", type=float, default=0.01, help="sampling_cycle")

    parser.add_argument("--f0", type=float, default=-30, help="start_frequency")
    parser.add_argument("--f1", type=float, default=30, help="end_frequency")

    return parser.parse_args()


def make_chirp(args):
    t = np.arange(args.N) * args.T  # timestamps
    y = chirp(t, f0=args.f0, f1=args.f1, t1=args.N * args.T, method="linear")
    f = args.f0 + (args.f1 - args.f0) / (args.N * args.T) * t
    return t, y, f


def plot_graph(t, y, f):
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(t, y)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(t, f)
    plt.show()


def main():
    args = parse_arguments()
    t, y, f = make_chirp(args)
    plot_graph(t, y, f)


if __name__ == "__main__":
    main()
