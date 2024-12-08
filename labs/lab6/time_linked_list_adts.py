"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module runs timing experiments to determine how the time taken
to enqueue and push take for LinkedList implementations of the ADTs
"""
from timeit import timeit
from typing import List, Tuple
from linked_list_adts import LinkedListStack, LinkedListQueue

###############################################################################
# Running timing experiments
#
# In this part of the lab, you will be conducting timing experiments on Stack
# and Queue methods when they're implemented with Linked Lists.
###############################################################################
# Experiment Parameters
# Below are our experiment settings: you may want to change these values.
#
# QUEUE_SIZES: This represents the queue sizes we'll be experimenting with.
#              i.e. enqueueing and dequeueing from Queues with size 10000,
#              20000, etc.
# NUM_TRIALS:  This represents the number of times we will repeat an
#              experiment: when we run our timing experiments, we want to get
#              use the average time over a number of trials in order to
#              minimize the effect of any outliers.
###############################################################################
SIZES = [100, 200, 400, 800, 1600]
NUM_TRIALS = 20


def _setup_queues(size: int, n: int) -> List[LinkedListQueue]:
    """Return a list of <n> queues, each with <size> elements.
    """
    queue_list = []
    for _ in range(n):
        q = LinkedListQueue()
        for _ in range(size):
            q.enqueue(1)
        queue_list.append(q)

    return queue_list


def _setup_stacks(size: int, n: int) -> List[LinkedListStack]:
    """Return a list of <n> stacks, each with <size> elements.
    """
    stack_list = []
    for _ in range(n):
        s = LinkedListStack()
        for _ in range(size):
            s.push(1)
        stack_list.append(s)

    return stack_list


def time_methods() -> Tuple[List[float], List[float]]:
    """Run timing experiments for enqueue on LinkedListQueue and
    push for LinkedListStack, returning lists with the average time it took to
    enqueue a single element to queues with sizes QUEUE_SIZES over
    NUM_TRIALS trials."""
    # These two lists will hold our timing results.
    queue_times = []
    stack_times = []

    # This loop runs the timing experiment for enqueueing one item to
    # LinkedListQueue.
    print("Running LinkedListQueue.enqueue experiments...")
    for size in SIZES:
        # 1. Initialize the sample queues
        queues = _setup_queues(size, NUM_TRIALS)

        # 2. For each queue created, call the function timeit.
        #    timeit takes three arguments:
        #        - a *string* representation of a piece of code to run
        #        - the number of times to run it (just 1 for us)
        #        - globals is a technical argument that you DON'T need to
        #          care about
        time = 0
        for queue in queues:
            time += timeit('queue.enqueue(1)', number=1, globals=locals())

        # 3. Get the average time in microseconds (μs)
        average_time = time / NUM_TRIALS * 1e6

        # 4. Report the average time taken and add that to our list of
        #    results.
        queue_times.append(average_time)
        print(f'enqueue: Queue size {size:>7}, time: {average_time}')

    print("Running LinkedListStack.push experiments...")
    # TODO: Using the above code as an example, run the same experiment
    #       but on LinkedListStack.push
    #       (You can just copy the above code and make minor modifications!)
    #       Add the results to stack_times instead of queue_times



    # Do not change the return statement below.
    return queue_times, stack_times


def plot_experiment() -> None:
    """Run the timing experiment on LinkedListQueue and LinkedListStack
     and plot a graph."""
    import matplotlib.pyplot as plt

    # Run the experiments and store the results
    queue_times, stack_times = time_methods()

    # Plot the results of our experiments and assign labels to each plot.
    # Our call to plt.plot takes 3 arguments:
    #     - The x-coordinates of the values to plot
    #     - The y-coordinates of the values to plot
    #     - The format we want to plot with.
    #       'ro' is 'red circle'
    #       'bo' is 'blue circle'
    #       Other formats include 'rx' (red X), 'bx' (blue X) and many more!
    start_plt, = plt.plot(SIZES, queue_times, 'ro')
    start_plt.set_label("LinkedListQueue.enqueue")

    end_plt, = plt.plot(SIZES, stack_times, 'bo')
    end_plt.set_label("LinkedListStack.push")

    # After we finish plotting everything, we can create the legend of
    # our graph and label the axes
    plt.legend()
    plt.xlabel("Size")
    plt.ylabel("Average Time (μs)")

    # Show our plotted results. This line must be called after
    # all of the other setup.
    plt.show()


if __name__ == '__main__':
    time_methods()

    # # Uncomment the line below to see the plotted graph once you have
    # # time_enqueue() working.
    # plot_experiment()
