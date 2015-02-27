Building an evaluation program that works with CodaLab

This example uses python. It assumes python is installed on the codalab worker machines.

evaluate.py - is an example that loads a single value from each of the gold files, looks for a corresponding submission, and finds the difference.
metadata - this is a file that lists the contents of the program.zip bundle for the CodaLab system.

Once these pieces are assembled they are packages as program.zip which CodaLab can then use to evaluate the submissions for a competition.