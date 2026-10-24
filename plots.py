import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ALGORITHMS = ("cubic", "reno", "bbr")
COLORS = {"cubic": "#24476b", "reno": "#a34c32", "bbr": "#487454"}
METRICS = (
    ("snd_cwnd_segments", "Congestion window (segments)"),
    ("rtt_us", "RTT (ms)"),
    ("retransmits_interval", "Retransmissions / interval"),
    ("goodput_bps", "Goodput (Mbit/s)"),
)
SCATTER = (
    ("snd_cwnd_segments", "Congestion window (segments)"),
    ("rtt_us", "RTT (ms)"),
    ("retransmits_interval", "Retransmissions / interval"),
)


def value(sample, key):
    number = sample[key]
    if key == "rtt_us":
        return number / 1000
    if key == "goodput_bps":
        return number / 1_000_000
    return number


def runs_for(destination, algorithm):
    return [run for run in destination["runs"] if run["algorithm"] == algorithm]


def save_figure(fig, path):
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_throughput(complete, folder):
    files = []
    for first in range(0, len(complete), 5):
        group = complete[first:first + 5]
        fig, axes = plt.subplots(len(group), 1, figsize=(9, 2.15 * len(group)), squeeze=False)
        for axis, destination in zip(axes[:, 0], group):
            candidate = destination["candidate"]
            for algorithm in ALGORITHMS:
                for repetition, run in enumerate(runs_for(destination, algorithm)):
                    axis.plot(
                        [sample["time_seconds"] for sample in run["samples"]],
                        [value(sample, "goodput_bps") for sample in run["samples"]],
                        color=COLORS[algorithm], linewidth=1.1, alpha=0.8,
                        linestyle="-" if repetition == 0 else "--",
                        label=algorithm.upper() if repetition == 0 else None,
                    )
            axis.set_title(f"{candidate['host']}:{candidate['port']}", fontsize=9)
            axis.set_ylabel("Mbit/s")
            axis.grid(alpha=0.2)
        axes[0, 0].legend(ncol=3, fontsize=8)
        axes[-1, 0].set_xlabel("Time since transfer began (s)")
        filename = f"throughput-{first // 5 + 1}.pdf"
        save_figure(fig, folder / filename)
        files.append(filename)
    return files


def plot_time_series(destination, algorithms, folder, filename):
    if len(algorithms) == 1:
        algorithm = algorithms[0]
        fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
        for axis, (key, label) in zip(axes.flat, METRICS):
            for repetition, run in enumerate(runs_for(destination, algorithm)):
                axis.plot(
                    [sample["time_seconds"] for sample in run["samples"]],
                    [value(sample, key) for sample in run["samples"]],
                    color=COLORS[algorithm], linewidth=1.1,
                    linestyle="-" if repetition == 0 else "--",
                    label=f"Run {repetition + 1}",
                )
            axis.set_ylabel(label)
            axis.grid(alpha=0.2)
        axes[0, 0].legend(fontsize=8)
        axes[1, 0].set_xlabel("Time (s)")
        axes[1, 1].set_xlabel("Time (s)")
        save_figure(fig, folder / filename)
        return

    fig, axes = plt.subplots(4, len(algorithms), figsize=(4.2 * len(algorithms), 10),
                             squeeze=False, sharex="col", sharey="row")
    for column, algorithm in enumerate(algorithms):
        runs = runs_for(destination, algorithm)
        axes[0, column].set_title(algorithm.upper())
        for row, (key, label) in enumerate(METRICS):
            axis = axes[row, column]
            for repetition, run in enumerate(runs):
                axis.plot(
                    [sample["time_seconds"] for sample in run["samples"]],
                    [value(sample, key) for sample in run["samples"]],
                    color=COLORS[algorithm], linewidth=1.1,
                    linestyle="-" if repetition == 0 else "--",
                    label=f"Run {repetition + 1}",
                )
            if column == 0:
                axis.set_ylabel(label)
            axis.grid(alpha=0.2)
        axes[-1, column].set_xlabel("Time (s)")
        axes[0, column].legend(fontsize=7)
    save_figure(fig, folder / filename)


def plot_scatter(destination, algorithms, folder, filename):
    if len(algorithms) == 1:
        algorithm = algorithms[0]
        fig, axes = plt.subplots(3, 1, figsize=(9, 9))
        for axis, (key, label) in zip(axes, SCATTER):
            for repetition, run in enumerate(runs_for(destination, algorithm)):
                axis.scatter(
                    [value(sample, key) for sample in run["samples"]],
                    [value(sample, "goodput_bps") for sample in run["samples"]],
                    color=COLORS[algorithm], s=13, alpha=0.6,
                    marker="o" if repetition == 0 else "x",
                    label=f"Run {repetition + 1}",
                )
            axis.set_xlabel(label)
            axis.set_ylabel("Goodput (Mbit/s)")
            axis.grid(alpha=0.2)
        axes[0].legend(fontsize=8)
        save_figure(fig, folder / filename)
        return

    fig, axes = plt.subplots(3, len(algorithms), figsize=(4.2 * len(algorithms), 8),
                             squeeze=False, sharex="row", sharey="row")
    for column, algorithm in enumerate(algorithms):
        axes[0, column].set_title(algorithm.upper())
        for row, (key, label) in enumerate(SCATTER):
            axis = axes[row, column]
            for repetition, run in enumerate(runs_for(destination, algorithm)):
                axis.scatter(
                    [value(sample, key) for sample in run["samples"]],
                    [value(sample, "goodput_bps") for sample in run["samples"]],
                    color=COLORS[algorithm], s=13, alpha=0.6,
                    marker="o" if repetition == 0 else "x",
                    label=f"Run {repetition + 1}",
                )
            if column == 0:
                axis.set_ylabel("Goodput (Mbit/s)")
            axis.set_xlabel(label)
            axis.grid(alpha=0.2)
        axes[0, column].legend(fontsize=7)
    save_figure(fig, folder / filename)


def make_plots(complete, representative, folder):
    throughput = plot_throughput(complete, folder)
    plot_time_series(representative, ("cubic",), folder, "cubic-time-series.pdf")
    plot_scatter(representative, ("cubic",), folder, "cubic-scatter.pdf")
    plot_time_series(representative, ALGORITHMS, folder, "comparison-time-series.pdf")
    plot_scatter(representative, ALGORITHMS, folder, "comparison-scatter.pdf")
    return {
        "throughput": throughput,
        "cubic_time_series": "cubic-time-series.pdf",
        "cubic_scatter": "cubic-scatter.pdf",
        "comparison_time_series": "comparison-time-series.pdf",
        "comparison_scatter": "comparison-scatter.pdf",
    }
