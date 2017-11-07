import tracemalloc
import main

tracemalloc.start()

# ... run your application ...
_controller = Controller()
_controller.run()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)