import argparse, hashlib, csv, time
import apache_beam as beam
from apache_beam.metrics import Metrics
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions

class ToKeySafe(beam.DoFn):
    
    def __init__(self, key_col=0):
        self.key_col = key_col
        self.rows_in = Metrics.counter(self.__class__, "rows_in")
        self.rows_bad = Metrics.counter(self.__class__, "rows_bad")
        self.rows_empty_key = Metrics.counter(self.__class__, "rows_empty_key")

    def process(self, cols):
        self.rows_in.inc()
        try:
            key = cols[self.key_col] if len(cols) > self.key_col else ""
            if not key:
                self.rows_empty_key.inc()
                return
            yield (key, 1)
        except Exception:
            self.rows_bad.inc()

class FakeIterations(beam.DoFn):

    def __init__(self, iterations=500):
        self.iterations = int(iterations)
        self.rows_out = Metrics.counter(self.__class__, "rows_out")

    def process(self, kv):
        key, count = kv
        data = f"{key}:{count}".encode("utf-8")
        for _ in range(self.iterations):
            data = hashlib.sha256(data).digest()
        self.rows_out.inc()
        yield f"{key},{count}"

def parse_csv(line, delimiter=",", quotechar='"'):
    return next(csv.reader([line], delimiter=delimiter, quotechar=quotechar))

def run(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--has_header", action="store_true")
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--delimiter", default=",")
    parser.add_argument("--quotechar", default='"')
    parser.add_argument("--key_col", type=int, default=0)
    parser.add_argument("--out_shards", type=int, default=8)
    parser.add_argument("--job_name", default=None)

    args, beam_args = parser.parse_known_args(argv)

    options = PipelineOptions(beam_args)

    gco = options.view_as(GoogleCloudOptions)
    gco.job_name = args.job_name or f"mba-pipeline-{int(time.time())}"
    options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=options) as p:
        lines = p | "ReadCSV" >> beam.io.ReadFromText(
            args.input, skip_header_lines=1 if args.has_header else 0
        )
        rows  = lines | "ParseCSV" >> beam.Map(lambda l: parse_csv(l, args.delimiter, args.quotechar))
        keyed = rows | "ToKeySafe"    >> beam.ParDo(ToKeySafe(args.key_col))
        agg   = keyed| "CountPerKey"  >> beam.CombinePerKey(sum)
        out = agg | "FakeIterations" >> beam.ParDo(FakeIterations(args.iterations))
        _ = out | "WriteCSV" >> beam.io.WriteToText(
            file_path_prefix=args.output,
            file_name_suffix=".csv",
            num_shards=args.out_shards
        )

if __name__ == "__main__":
    run()
