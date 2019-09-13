import os
import sys
from argparse import ArgumentParser, Namespace
from typing import List, Tuple, Optional, Union

import requests
from jsonasobj import loads, JsonObj, as_json


def genargs(prog: Optional[str] = None) -> ArgumentParser:
    """
    Generate a command line parser
    :param prog: program name to use for help.  Default is whatever is being run
    :return: parser
    """
    parser = ArgumentParser(prog)
    parser.add_argument("server", help="FHIR Server base node")
    parser.add_argument("resource", help="Resource to dump")
    parser.add_argument("outdir", help="Output directory")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-m", "--max", help="Maximum number to dump", type=int)
    return parser


def save_instances(opts: Namespace, query_result: JsonObj, nwritten: int = 0) -> int:
    """
    Save the instances referenced query_result
    :param opts: parameters
    :param query_result: query result
    :param nwritten: running accumulator
    :return: number of elements saved
    """
    if 'entry' in query_result:
        for instance in query_result.entry:
            if opts.verbose:
                print(f"Writing: {os.path.join(opts.resource, instance.resource.id)}")
            with open(os.path.join(opts.outdir, opts.resource, instance.resource.id), 'w') as f:
                f.write(as_json(instance.resource))
            nwritten += 1
            if opts.max and nwritten >= opts.max:
                break
    return nwritten


def dumpit(argv: Optional[Union[str, List[str]]] = None, prog: Optional[str] = None) -> int:
    """
    Dump resources from a FHIR server
    :param argv: command line arguments
    :param prog: program name for testing help output
    :return: number of resource instances dumped
    """
    if isinstance(argv, str):
        argv = argv.split()
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])
    os.makedirs(os.path.join(opts.outdir, opts.resource), exist_ok=True)
    url = f"{opts.server}/{opts.resource}?_format=json&_summary=false"
    if opts.max:
        url += f"&_count={opts.max}"
    nwritten = 0
    while True:
        resp = requests.get(url)
        url = None
        if resp.ok:
            rslts = loads(resp.text)
            nwritten = save_instances(opts, rslts, nwritten)
            if opts.max is None or nwritten < opts.max:
                for l in rslts.link:
                    if l.relation == "next":
                        url = l.url
        else:
            print(resp.reason)
        if not url:
            break
    if opts.verbose:
        print(f"{nwritten} instances written to {opts.outdir}")
    return nwritten


if __name__ == '__main__':
    dumpit(sys.argv[1:])
