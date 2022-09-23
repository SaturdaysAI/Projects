# -*- coding: utf-8 -*-
import lightkurve as lk
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np

from src.preprocess.EXO_Config import Config


class Generator:
    def __init__(
        self, binsize_global=2049, binsize_local=257, mission="Kepler"
    ):
        self.config = Config()
        source_file = "cumulative_2022.05.10_03.34.24.csv"
        self.source_data = pd.read_csv(source_file)
        self.lc_mission = mission
        self.binsize_global = binsize_global
        self.binsize_local = binsize_local
        print(self.source_data)

    def TargetGenerator(self):
        target = pd.DataFrame(
            columns=["id", "target", "disposition", "period", "t0", "duration"]
        )
        print("")
        for index, koi in self.source_data.iterrows():
            if koi["koi_disposition"] == "CONFIRMED":
                target_value = 1
            else:
                target_value = 0
            target = target.append(
                {
                    "id": koi["kepoi_name"],
                    "target": target_value,
                    "disposition": koi["koi_disposition"],
                    "period": koi["koi_period"],
                    "t0": koi["koi_time0bk"],
                    "duration": koi["koi_duration"],
                },
                ignore_index=True,
            )
            if index % 100 == 0:
                print(".", end="")
        print("\n\nTARGET FILE:\n-------------\n", target)
        target.to_csv(self.config.target_file)

    def DataGenerator(
        self, start, end, local_size=2, limit_download=16, plot=False
    ):

        tstart = time.time()
        self.source_data = self.source_data.loc[start:end]
        print(self.source_data)
        for index, koi in self.source_data.iterrows():
            koi_start = time.time()

            # SEARCH DATA
            print(
                koi["rowid"],
                "-",
                koi["kepoi_name"],
                "",
                koi["koi_disposition"],
                end=".",
            )
            if koi["kepler_name"] is not np.NaN:
                lc_target = koi["kepler_name"]
            else:
                lc_target = "".join(["KIC ", str(koi["kepid"])])
            print(" ", lc_target, end="")
            lc_search = lk.search_lightcurve(
                lc_target, mission=self.lc_mission, limit=16
            )

            if len(lc_search) > 0:
                try:
                    # DOWNLOAD DATA
                    print(". Curves =", len(lc_search), end=".")
                    lc_collection = lc_search.download_all(
                        quality_bitmask="hard",
                        download_dir="./fits",
                        flux_column="pdcsap_flux",
                    )
                    download = True
                except:
                    download = False
                    print("Error Downloading Lightcurve")
            else:
                download = False
                print("ERROR: Empty Search Result")

            if download:
                # DATA PROCESSING
                print("", end=".")
                lc_raw = lc_collection.stitch()
                print("", end=".")
                lc_flat = lc_raw.flatten(niters=3, sigma=1)
                print("", end=".")
                lc_clean = lc_flat.remove_outliers(sigma=20, sigma_upper=4)
                print("", end=".")
                lc_fold = lc_clean.fold(koi["koi_period"], koi["koi_time0bk"])
                print("", end=".")

                # GLOBAL BIN
                flux_global, nang = self.bin_lc(
                    lc_fold,
                    self.binsize_global,
                    width_to_dist_ratio=1.1,
                    limits=(-koi["koi_period"] / 2, koi["koi_period"] / 2),
                )

                # LOCAL BIN
                local_limit = (local_size * (koi["koi_duration"] / 24)) / koi[
                    "koi_period"
                ]
                if local_limit < koi["koi_period"] / 50:
                    local_limit = koi["koi_period"] / 50
                lc_fold_local = lc_fold[
                    (lc_fold.phase > -local_limit)
                    & (lc_fold.phase < local_limit)
                ]
                flux_local, nanl = self.bin_lc(
                    lc_fold_local,
                    self.binsize_local,
                    width_to_dist_ratio=1.1,
                    limits=(-local_limit, local_limit),
                )
                print("NaN = (", nang, ",", nanl, end=").")

                # SAVE DATA
                np.save(
                    "".join(
                        [
                            self.config.train_folder,
                            "/global/",
                            koi["kepoi_name"],
                            "_global.npy",
                        ]
                    ),
                    np.array(flux_global),
                )
                np.save(
                    "".join(
                        [
                            self.config.train_folder,
                            "/local/",
                            koi["kepoi_name"],
                            "_local.npy",
                        ]
                    ),
                    np.array(flux_local),
                )
                print("  {:.2f}".format(time.time() - koi_start), "seg.")
                if plot:
                    plt.plot(flux_global)
                    plt.show()
                    plt.plot(flux_local)
                    plt.show()

        print("Total Time = ", "{:.2f}".format(time.time() - tstart), "seg.\n")
        return 0

    def bin_lc(
        self,
        lc,
        num_bins,
        width_to_dist_ratio=1.0,
        limits=(-0.5, 0.5),
        method="median",
    ):

        domain_width = float(limits[1] - limits[0])
        bin_dist = domain_width / num_bins
        bin_width = width_to_dist_ratio * bin_dist
        bin_centers = np.linspace(limits[0], limits[1], num_bins)
        bin_values = []

        if method == "median":
            agg = np.nanmedian
        elif method == "mean":
            agg = np.nanmean

        for bin_center in bin_centers:
            bin_lower = bin_center - bin_width / 2.0
            bin_upper = bin_center + bin_width / 2.0
            flux_bin = lc[(bin_lower < lc.phase) & (lc.phase < bin_upper)].flux
            if len(flux_bin) > 0:
                bin_values.append(agg(flux_bin, overwrite_input=True))
            else:
                bin_values.append(np.nan)
        bin_values = np.array(bin_values)
        nan = np.isnan(bin_values).sum()
        return bin_values, nan


############################################################•

MISSION = "Kepler"
BINSIZE_GLOBAL = 2049
BINSIZE_LOCAL = 257
START = 151
END = 500
LOCAL_SIZE = 2
LIMIT_DOWNLOAD = 16
generator = Generator(
    mission=MISSION, binsize_global=BINSIZE_GLOBAL, binsize_local=BINSIZE_LOCAL
)

# generator.TargetGenerator()
generator.DataGenerator(
    START, END, local_size=LOCAL_SIZE, limit_download=LIMIT_DOWNLOAD, plot=True
)
