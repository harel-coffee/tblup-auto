import os
import csv
import pickle
import numpy as np
from os.path import join, isdir, isfile


class Monitor:
    """
    Class for monitoring the population statistics.
    """

    ROUND_DECIMALS = 4

    def __init__(self, args):
        """
        Constructor.
        :param args: object, argparse.Namespace.
        """
        results = join(".", "results")
        if not isdir(results):
            os.mkdir(results)

        subdir = self.make_subdir(args)

        results = join(results, subdir)
        if not isdir(results):
            os.mkdir(results)

        results_file = join(results, str(args.seed).zfill(3) + "_results")
        archive_file = join(results, str(args.seed).zfill(3) + "_archive")

        # Be sure to not overwite a file.
        i = 1
        temp_res = results_file
        temp_arch = archive_file
        while isfile(temp_res + ".csv") or isfile(temp_arch + ".json"):
            temp_res = results_file + "_" + str(i)
            temp_arch = archive_file + "_" + str(i)

            i += 1

        self.results_file = temp_res + ".csv"
        self.archive_file = temp_arch + ".pkl"

        header = ["generation", "max_fitness", "min_fitness", "median_fitness", "mean_fitness", "stdev_fitness", "len"]
        with open(self.results_file, "w") as f:
            csv.writer(f).writerow(header)

    def make_subdir(self, args):
        """
        Make the name of the directory that is going to hold all the results for a particular experiment.
        :param args: object, argparse.Namespace.
        :return: string
        """
        option_list = [str(args.regressor)]

        if args.de_strategy != "de_rand_1":
            option_list.append(str(args.de_strategy))

        if args.feature_scheduling is not None:
            option_list.append(str(args.feature_scheduling))
            option_list.append("i" + str(args.initial_features))

        option_list.append("f" + str(args.features))
        option_list.append("n" + str(args.population_size))
        option_list.append("g" + str(args.generations))
        option_list.append("cr" + str(args.crossover_rate).replace(".", ""))
        option_list.append("mi" + str(args.mutation_intensity).replace(".", ""))

        return "_".join(option_list)

    def write(self, row):
        """
        Writes a row to the csv file.
        :param row: list, list of values to write.
        :return: list, the list that was written.
        """
        with open(self.results_file, "a") as f:
            csv.writer(f).writerow(row)

        return row

    def report(self, population):
        """
        Write statistics out to file.
        :param population: tblup.Population.
        :return: list, the stats of the population.
        """
        return self.write(self.gather_stats(population))

    def save_archive(self, population):
        """
        Save the archive out to a JSON file.
        :param population: tblup.Population, the current population.
        """
        with open(self.archive_file, "wb") as f:
            pickle.dump(population.evaluator.archive, f)

    def gather_stats(self, population):
        """
        Gather statistics.
        :param population: tblup.Population.
        :return list: a row in the results file.
        """
        fits = [x.fitness for x in population]
        current_length = len(population[0])

        return [population.generation] + self.get_row_summary(fits) + [current_length]

    def get_row_summary(self, fitnesses):
        """
        Gets the summary statistics of a list of fitnesses.
        :param fitnesses: list, list of floats.
        :return: list, list of summary stats.
        """
        fitnesses.sort()

        median_idx = len(fitnesses) / 2.0
        if int(median_idx) == median_idx:
            # Population length was even, use middle index.
            median_fitness = fitnesses[int(median_idx)]

        else:
            # Population length was odd, use average of two middle values.
            median_fitness = (fitnesses[int(median_idx)] + fitnesses[int(median_idx) + 1]) / 2

        max_fitness = fitnesses[-1]
        min_fitness = fitnesses[0]
        mean_fitness = np.asscalar(np.mean(fitnesses))
        stdev_fitness = np.asscalar(np.std(fitnesses, ddof=1))

        return [
            round(max_fitness, self.ROUND_DECIMALS),
            round(min_fitness, self.ROUND_DECIMALS),
            round(median_fitness, self.ROUND_DECIMALS),
            round(mean_fitness, self.ROUND_DECIMALS),
            round(stdev_fitness, self.ROUND_DECIMALS),
        ]